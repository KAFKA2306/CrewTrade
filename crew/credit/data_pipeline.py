from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.credit.config import CreditSpreadConfig
from crew.data_platform.consumer import latest_vintage_series, pivot_latest_vintage


class CreditSpreadDataPipeline(BaseDataPipeline):
    """Export point-in-time FRED OAS data from the canonical DuckDB catalogue."""

    def __init__(self, raw_data_dir: Path, config: CreditSpreadConfig) -> None:
        super().__init__(raw_data_dir, config)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        history = pivot_latest_vintage(self.config.dataset)
        history = self._slice_period(history, self.config.period)
        missing = sorted(set(self.config.series_labels).difference(history.columns))
        if missing:
            raise ValueError(f"Canonical credit series are missing: {missing}")
        history = history[self.config.series_labels]

        provenance = latest_vintage_series(self.config.dataset)
        provenance = provenance[
            provenance["label"].isin(self.config.series_labels)
        ].copy()
        if not history.empty:
            provenance = provenance[
                provenance["observation_date"] >= history.index.min()
            ]

        self._save("oas", history.reset_index())
        self._save("provenance", provenance)
        return {
            "oas": str(self.raw_data_dir / "oas.parquet"),
            "provenance": str(self.raw_data_dir / "provenance.parquet"),
        }

    @staticmethod
    def _slice_period(frame: pd.DataFrame, period: str) -> pd.DataFrame:
        if frame.empty:
            return frame
        value = int(period[:-1])
        unit = period[-1]
        end = frame.index.max()
        if unit == "y":
            start = end - pd.DateOffset(years=value)
        elif unit == "m":
            start = end - pd.DateOffset(months=value)
        else:
            start = end - pd.Timedelta(days=value)
        return frame.loc[start:end]


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "credit.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.credit.analysis import CreditSpreadAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=CreditSpreadDataPipeline,
        analyzer_class=CreditSpreadAnalyzer,
        config_class=CreditSpreadConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved canonical {name}: {path}")


if __name__ == "__main__":
    main()
