from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import (
    IndexETFMappingClient,
    JPXETFExpenseRatioClient,
    YFinanceEquityDataClient,
    get_price_series,
)
from crew.clients.ticker_utils import normalize_jpx_ticker
from crew.data_platform.jpx_consumer import jpx_etf_master
from crew.etf.config import INDEX_KEYWORDS, IndexETFComparisonConfig


class IndexETFComparisonDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: IndexETFComparisonConfig) -> None:
        super().__init__(raw_data_dir, config)
        self.mapping_client = IndexETFMappingClient(INDEX_KEYWORDS)
        self.price_client = YFinanceEquityDataClient(raw_data_dir)
        self.expense_client = JPXETFExpenseRatioClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        del targets, days
        official_master = jpx_etf_master()
        mapping_df = self.mapping_client.get_mapping(official_master)
        expense_ratios = self.expense_client.get_expense_ratios()

        all_tickers = mapping_df["ticker"].unique().tolist()
        price_frames = self.price_client.get_frames(
            all_tickers, period=self.config.lookback
        )
        prices_dict = {}
        for ticker, frame in price_frames.items():
            series = get_price_series(frame)
            if len(series.dropna()) >= self.config.min_data_points:
                prices_dict[ticker] = series
        prices_df = pd.DataFrame(prices_dict).sort_index()

        etf_metadata = official_master.copy()
        etf_metadata["official_ticker"] = etf_metadata["ticker"]
        etf_metadata["ticker"] = etf_metadata["official_ticker"].map(normalize_jpx_ticker)
        etf_metadata = etf_metadata.dropna(subset=["ticker"]).copy()
        etf_metadata["name"] = etf_metadata["official_name"]
        etf_metadata["provider"] = etf_metadata["manager"]
        etf_metadata["category"] = etf_metadata["index_name"]
        etf_metadata = etf_metadata.merge(expense_ratios, on="ticker", how="left")

        saved_files = {}
        for name, df in [
            ("mapping", mapping_df),
            ("prices", prices_df),
            ("etf_metadata", etf_metadata),
        ]:
            self._save(name, df)
            saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")

        frames_dir = self.raw_data_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        for ticker, frame in price_frames.items():
            frame_path = frames_dir / f"{ticker}.parquet"
            frame.to_parquet(frame_path)
        saved_files["frames_dir"] = str(frames_dir)
        return saved_files


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "etf.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.etf.analysis import IndexETFComparisonAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=IndexETFComparisonDataPipeline,
        analyzer_class=IndexETFComparisonAnalyzer,
        config_class=IndexETFComparisonConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
