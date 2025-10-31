from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import pandas as pd

from ai_trading_crew.use_cases.data_clients import (
    IndexETFMappingClient,
    YFinanceEquityDataClient,
    JPXETFExpenseRatioClient,
    ToushinKyokaiDataClient,
    get_price_series,
)
from ai_trading_crew.use_cases.index_etf_comparison.config import IndexETFComparisonConfig, INDEX_KEYWORDS


class IndexETFComparisonDataPipeline:
    def __init__(self, config: IndexETFComparisonConfig, raw_data_dir: Path) -> None:
        self.config = config
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.mapping_client = IndexETFMappingClient(raw_data_dir, INDEX_KEYWORDS)
        self.price_client = YFinanceEquityDataClient(raw_data_dir)
        self.expense_client = JPXETFExpenseRatioClient(raw_data_dir)
        self.etf_master_client = ToushinKyokaiDataClient(raw_data_dir)

    def collect(self) -> Dict[str, Any]:
        mapping_df = self.mapping_client.get_mapping()
        etf_master = self.etf_master_client.get_etf_master()
        expense_ratios = self.expense_client.get_expense_ratios()

        all_tickers = mapping_df["ticker"].unique().tolist()
        price_frames = self.price_client.get_frames(all_tickers, period=self.config.lookback)

        prices_dict = {}
        for ticker, frame in price_frames.items():
            series = get_price_series(frame)
            if len(series.dropna()) >= self.config.min_data_points:
                prices_dict[ticker] = series

        prices_df = pd.DataFrame(prices_dict).sort_index()

        etf_metadata = etf_master.merge(expense_ratios, on="ticker", how="left")

        return {
            "mapping": mapping_df,
            "prices": prices_df,
            "etf_metadata": etf_metadata,
            "price_frames": price_frames,
        }
