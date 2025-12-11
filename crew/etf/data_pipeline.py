from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import (
    IndexETFMappingClient,
    JPXETFExpenseRatioClient,
    ToushinKyokaiDataClient,
    YFinanceEquityDataClient,
    get_price_series,
)
from crew.etf.config import (
    INDEX_KEYWORDS,
    IndexETFComparisonConfig,
)


class IndexETFComparisonDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: IndexETFComparisonConfig) -> None:
        super().__init__(raw_data_dir, config)
        self.mapping_client = IndexETFMappingClient(raw_data_dir, INDEX_KEYWORDS)
        self.price_client = YFinanceEquityDataClient(raw_data_dir)
        self.expense_client = JPXETFExpenseRatioClient(raw_data_dir)
        self.etf_master_client = ToushinKyokaiDataClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        mapping_df = self.mapping_client.get_mapping()
        etf_master = self.etf_master_client.get_etf_master()
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

        etf_metadata = etf_master.merge(expense_ratios, on="ticker", how="left")

        saved_files = {}
        # Save main DataFrames
        for name, df in [
            ("mapping", mapping_df),
            ("prices", prices_df),
            ("etf_metadata", etf_metadata),
        ]:
            self._save(name, df)
            saved_files[name] = str(self.raw_data_dir / f"{name}.csv")

        # Save price_frames
        frames_dir = self.raw_data_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        for ticker, frame in price_frames.items():
            frame_path = frames_dir / f"{ticker}.csv"
            frame.to_csv(frame_path)
            # We don't necessarily need to return every single frame path in saved_files,
            # or we can return the dir.
        saved_files["frames_dir"] = str(frames_dir)

        return saved_files


# Assume project root is 3 levels up
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
