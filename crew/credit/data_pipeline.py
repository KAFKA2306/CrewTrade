from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import FixedIncomeDataClient, get_price_series
from crew.credit.config import CreditSpreadConfig


class CreditSpreadDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: CreditSpreadConfig) -> None:
        super().__init__(raw_data_dir, config)
        self.client = FixedIncomeDataClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        frames = self.client.get_frames(self.config.tickers, self.config.period)
        prices = self._combine_close(frames)

        saved_files = {}
        # Save logic
        name = "prices"
        df = prices.reset_index()
        self._save(name, df)
        saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")
        return saved_files

    def _combine_close(self, frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        series_list = []
        for ticker, frame in frames.items():
            price_series = get_price_series(frame)
            series_list.append(price_series.rename(ticker))
        combined = pd.concat(series_list, axis=1)
        combined = combined.sort_index()
        return combined.ffill()


# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = (
    PROJECT_ROOT / "config" / "use_cases" / "credit.yaml"
)  # Assuming credit.yaml exists


def main() -> None:
    from crew.app import GenericUseCase
    from crew.credit.analysis import CreditSpreadAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=CreditSpreadDataPipeline,
        analyzer_class=CreditSpreadAnalyzer,  # Assuming this exists
        config_class=CreditSpreadConfig,
    )

    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
