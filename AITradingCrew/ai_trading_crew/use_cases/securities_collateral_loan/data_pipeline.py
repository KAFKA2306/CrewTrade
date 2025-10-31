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

        settings = self.config.optimization
        lookback = settings.lookback if settings else self.config.period
        history_window = settings.history_window if settings and settings.history_window else lookback
        start = None
        if as_of is not None and history_window:
            start = self._calculate_start(as_of, history_window)
        frames = self.client.get_frames(tickers, period=None, start=start, end=as_of)
        prices_full = self._combine_close(frames, start=start, as_of=as_of)

        training_start = None
        if as_of is not None and lookback:
            training_start = self._calculate_start(as_of, lookback)
        if training_start is not None:
            coverage_start = prices_full.apply(lambda series: series.first_valid_index())
            coverage_start = pd.to_datetime(coverage_start, errors="coerce")
            eligible = coverage_start[coverage_start.notna() & (coverage_start <= training_start)].index.tolist()
            if not eligible:
                coverage_order = coverage_start.dropna().sort_values()
                eligible = coverage_order.head(min(len(coverage_order), 40)).index.tolist()
            prices_full = prices_full[eligible]

        prices = prices_full
        if training_start is not None:
            prices = prices_full.loc[training_start:]

        valid_tickers = prices.columns.tolist()
        etf_master_filtered = etf_master[etf_master["ticker"].isin(valid_tickers)].copy()

        expense_ratios = self.expense_client.get_expense_ratios()
        if not expense_ratios.empty:
            etf_master_filtered = etf_master_filtered.merge(expense_ratios, on="ticker", how="left")
        else:
            etf_master_filtered["expense_ratio"] = None

        etf_master_filtered = etf_master_filtered[
            (etf_master_filtered["expense_ratio"].isna()) |
            (etf_master_filtered["expense_ratio"] < 0.004)
        ]

        valid_tickers_filtered = etf_master_filtered["ticker"].tolist()
        prices = prices[valid_tickers_filtered]

        prices_forward = None
        if as_of is not None and self.config.optimization and self.config.optimization.forward_test_period:
            forward_start = as_of + pd.Timedelta(days=1)
            forward_end = self._calculate_end(as_of, self.config.optimization.forward_test_period)
            frames_forward = self.client.get_frames(valid_tickers_filtered, period=None, start=forward_start, end=forward_end)
            prices_forward = self._combine_close(frames_forward, start=forward_start, as_of=forward_end)

        result = {
            "mode": "optimization",
            "etf_master": etf_master_filtered,
            "prices": prices,
        }
        if prices_forward is not None and not prices_forward.empty:
            result["prices_forward"] = prices_forward
        return result

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
            series = series.dropna()
            if series.empty:
                continue
            series_list[ticker] = series.rename(ticker)
        if not series_list:
            return pd.DataFrame()
        combined = pd.concat(series_list.values(), axis=1).sort_index()
        combined = combined.ffill()

        if self.config.optimization and self.config.optimization.enabled:
            if not combined.empty:
                coverage = combined.notna().sum()
                required_rows = max(int(len(combined.index) * 0.5), 60)
                valid_cols = coverage[coverage >= required_rows].index.tolist()
                if not valid_cols:
                    valid_cols = coverage.sort_values(ascending=False).head(40).index.tolist()
                combined = combined[valid_cols]
                min_valid = max(int(len(valid_cols) * 0.7), 1)
                combined = combined.dropna(thresh=min_valid)
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

    def _calculate_end(self, as_of: pd.Timestamp, forward_period: str) -> pd.Timestamp:
        forward_period = forward_period.strip().lower()
        if not forward_period:
            return as_of
        value = float(forward_period[:-1]) if forward_period[:-1] else 1.0
        unit = forward_period[-1]
        if unit == "y":
            offset = pd.DateOffset(years=int(value))
        elif unit == "m":
            offset = pd.DateOffset(months=int(value))
        elif unit == "d":
            offset = pd.DateOffset(days=int(value))
        else:
            offset = pd.DateOffset(days=365 * value)
        return (as_of + offset).normalize()
