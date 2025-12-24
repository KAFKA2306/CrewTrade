from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients.equities import YFinanceEquityDataClient
from crew.clients.pricing import get_price_series
from crew.portfolio.config import Index7PortfolioConfig


class Index7PortfolioDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: Index7PortfolioConfig):
        super().__init__(raw_data_dir, config)
        self.client = YFinanceEquityDataClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        tickers = [idx.ticker for idx in self.config.indices]

        period = self.config.period
        frames = self.client.get_frames(tickers, period=period, start=None, end=None)

        prices = self._combine_close(frames, as_of=None)

        index_master = pd.DataFrame(
            [
                {
                    "ticker": idx.ticker,
                    "name": idx.name,
                    "category": idx.category,
                    "expense_ratio": 0.0,
                }
                for idx in self.config.indices
            ]
        )

        saved_files = {}
        for name, df in [("prices", prices), ("index_master", index_master)]:
            self._save(name, df)
            saved_files[name] = str(self.raw_data_dir / f"{name}.csv")

        # mode="index" was returned before. Analyzer usually needs it?
        # Analyzer can infer or default to "index".

        return saved_files

    def collect(self, as_of: pd.Timestamp | None = None) -> Dict:
        tickers = [idx.ticker for idx in self.config.indices]
        period = self.config.period
        frames = self.client.get_frames(tickers, period=period, start=None, end=None)
        prices = self._combine_close(frames, as_of=as_of)

        index_master = pd.DataFrame(
            [
                {
                    "ticker": idx.ticker,
                    "name": idx.name,
                    "category": idx.category,
                    "expense_ratio": 0.0,
                }
                for idx in self.config.indices
            ]
        )

        return {"prices": prices, "index_master": index_master}

    def _combine_close(
        self, frames: Dict[str, pd.DataFrame], as_of: pd.Timestamp | None = None
    ) -> pd.DataFrame:
        series_list: Dict[str, pd.Series] = {}
        for ticker, frame in frames.items():
            series = get_price_series(frame)
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
        # Use how='all' to keep history even if some new assets are NaN.
        # This prevents truncating 20y history to 3mo (e.g. for 399A.T).
        combined = combined.dropna(how="all")
        return combined
