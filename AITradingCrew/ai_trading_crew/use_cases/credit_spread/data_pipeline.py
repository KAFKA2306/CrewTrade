from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.credit_spread.config import CreditSpreadConfig
from ai_trading_crew.use_cases.data_clients import FixedIncomeDataClient


class CreditSpreadDataPipeline:
    def __init__(self, config: CreditSpreadConfig, raw_data_dir: Path) -> None:
        self.config = config
        self.client = FixedIncomeDataClient(raw_data_dir)

    def collect(self) -> Dict[str, pd.DataFrame]:
        frames = self.client.get_frames(self.config.tickers, self.config.period)
        prices = self._combine_close(frames)
        return {"prices": prices}

    def _combine_close(self, frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        series_list = []
        for ticker, frame in frames.items():
            close_series = frame["Close"].copy()
            tz_info = getattr(close_series.index, "tz", None)
            if tz_info is not None:
                close_series = close_series.tz_convert(None)
            series_list.append(close_series.rename(ticker))
        combined = pd.concat(series_list, axis=1)
        combined = combined.sort_index()
        return combined.ffill()
