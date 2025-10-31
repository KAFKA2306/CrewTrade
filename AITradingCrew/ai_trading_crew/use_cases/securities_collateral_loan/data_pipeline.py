from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.data_clients import (
    JPXETFExpenseRatioClient,
    ToushinKyokaiDataClient,
    YFinanceEquityDataClient,
)
from ai_trading_crew.use_cases.securities_collateral_loan.config import SecuritiesCollateralLoanConfig


class SecuritiesCollateralLoanDataPipeline:
    def __init__(self, config: SecuritiesCollateralLoanConfig, raw_data_dir: Path) -> None:
        self.config = config
        self.client = YFinanceEquityDataClient(raw_data_dir)
        self.toushin_client = ToushinKyokaiDataClient(raw_data_dir)
        self.expense_client = JPXETFExpenseRatioClient(raw_data_dir)

    def collect(self, as_of: pd.Timestamp | None = None) -> Dict[str, pd.DataFrame]:
        if self.config.optimization and self.config.optimization.enabled:
            return self._collect_optimization_mode(as_of=as_of)
        else:
            return self._collect_manual_mode(as_of=as_of)

    def _collect_manual_mode(self, as_of: pd.Timestamp | None = None) -> Dict[str, pd.DataFrame]:
        tickers = [asset.ticker for asset in self.config.collateral_assets]
        frames = self.client.get_frames(tickers, period=None, start=None, end=as_of)
        prices = self._combine_close(frames, start=None, as_of=as_of)
        return {"mode": "manual", "prices": prices}

    def _collect_optimization_mode(self, as_of: pd.Timestamp | None = None) -> Dict[str, pd.DataFrame]:
        etf_master = self.toushin_client.get_etf_master()
        tickers = etf_master["ticker"].tolist()

        lookback = self.config.optimization.lookback if self.config.optimization else self.config.period
        start = None
        if as_of is not None and lookback:
            start = self._calculate_start(as_of, lookback)
        frames = self.client.get_frames(tickers, period=None, start=start, end=as_of)
        prices = self._combine_close(frames, start=start, as_of=as_of)

        valid_tickers = prices.columns.tolist()
        etf_master_filtered = etf_master[etf_master["ticker"].isin(valid_tickers)].copy()

        expense_ratios = self.expense_client.get_expense_ratios()
        if not expense_ratios.empty:
            etf_master_filtered = etf_master_filtered.merge(expense_ratios, on="ticker", how="left")
        else:
            etf_master_filtered["expense_ratio"] = None

        return {
            "mode": "optimization",
            "etf_master": etf_master_filtered,
            "prices": prices,
        }

    def _combine_close(self, frames: Dict[str, pd.DataFrame], start: pd.Timestamp | None = None, as_of: pd.Timestamp | None = None) -> pd.DataFrame:
        series_list: Dict[str, pd.Series] = {}
        for ticker, frame in frames.items():
            if "Close" in frame.columns:
                series = frame["Close"].copy()
            else:
                series = frame.iloc[:, 0].copy()
            tz_info = getattr(series.index, "tz", None)
            if tz_info is not None:
                series = series.tz_convert(None)
            if start is not None:
                series = series.loc[start:]
            if as_of is not None:
                series = series.loc[:as_of]
            series_list[ticker] = series.rename(ticker)
        if not series_list:
            return pd.DataFrame()
        combined = pd.concat(series_list.values(), axis=1).sort_index()
        combined = combined.ffill()

        if self.config.optimization and self.config.optimization.enabled:
            min_valid = int(len(combined.columns) * 0.7)
            combined = combined.dropna(thresh=min_valid)
            valid_cols = combined.columns[combined.notna().sum() >= len(combined) * 0.9]
            combined = combined[valid_cols]
        else:
            combined = combined.dropna(how="any")
        return combined

    def _calculate_start(self, as_of: pd.Timestamp, lookback: str) -> pd.Timestamp:
        lookback = lookback.strip().lower()
        if not lookback:
            return as_of
        value = float(lookback[:-1]) if lookback[:-1] else 1.0
        unit = lookback[-1]
        if unit == "y":
            offset = pd.DateOffset(years=int(value))
        elif unit == "m":
            offset = pd.DateOffset(months=int(value))
        elif unit == "d":
            offset = pd.DateOffset(days=int(value))
        else:
            offset = pd.DateOffset(days=365 * value)
        return (as_of - offset).normalize()
