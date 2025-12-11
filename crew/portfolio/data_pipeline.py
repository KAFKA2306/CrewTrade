from pathlib import Path
from typing import Dict

import pandas as pd

from crew.clients.equities import YFinanceEquityDataClient
from crew.clients.pricing import get_price_series
from crew.portfolio.config import Index7PortfolioConfig


class Index7PortfolioDataPipeline:
    def __init__(self, config: Index7PortfolioConfig):
        self.config = config
        raw_data_dir = Path("resources/data/use_cases/index_7_portfolio/raw")
        raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.client = YFinanceEquityDataClient(raw_data_dir)

    def collect(self, as_of: pd.Timestamp | None = None) -> Dict[str, pd.DataFrame]:
        tickers = [idx.ticker for idx in self.config.indices]

        period = self.config.period
        frames = self.client.get_frames(tickers, period=period, start=None, end=as_of)

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

        return {
            "mode": "index",
            "prices": prices,
            "index_master": index_master,
        }

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
        combined = combined.dropna(how="any")
        return combined
