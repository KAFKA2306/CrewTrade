from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.data_clients import YFinanceEquityDataClient, ToushinKyokaiDataClient
from ai_trading_crew.use_cases.securities_collateral_loan.config import SecuritiesCollateralLoanConfig


class SecuritiesCollateralLoanDataPipeline:
    def __init__(self, config: SecuritiesCollateralLoanConfig, raw_data_dir: Path) -> None:
        self.config = config
        self.client = YFinanceEquityDataClient(raw_data_dir)
        self.toushin_client = ToushinKyokaiDataClient(raw_data_dir)

    def collect(self) -> Dict[str, pd.DataFrame]:
        if self.config.optimization and self.config.optimization.enabled:
            return self._collect_optimization_mode()
        else:
            return self._collect_manual_mode()

    def _collect_manual_mode(self) -> Dict[str, pd.DataFrame]:
        tickers = [asset.ticker for asset in self.config.collateral_assets]
        frames = self.client.get_frames(tickers, self.config.period)
        prices = self._combine_close(frames)
        return {"mode": "manual", "prices": prices}

    def _collect_optimization_mode(self) -> Dict[str, pd.DataFrame]:
        etf_master = self.toushin_client.get_etf_master()
        tickers = etf_master["ticker"].tolist()

        lookback = self.config.optimization.lookback if self.config.optimization else self.config.period
        frames = self.client.get_frames(tickers, lookback)
        prices = self._combine_close(frames)

        valid_tickers = prices.columns.tolist()
        etf_master_filtered = etf_master[etf_master["ticker"].isin(valid_tickers)]

        return {
            "mode": "optimization",
            "etf_master": etf_master_filtered,
            "prices": prices,
        }

    def _combine_close(self, frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        series_list: Dict[str, pd.Series] = {}
        for ticker, frame in frames.items():
            if "Close" in frame.columns:
                series = frame["Close"].copy()
            else:
                series = frame.iloc[:, 0].copy()
            tz_info = getattr(series.index, "tz", None)
            if tz_info is not None:
                series = series.tz_convert(None)
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
