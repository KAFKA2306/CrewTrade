from __future__ import annotations

from pathlib import Path

import pandas as pd

from crew.app import BaseDataPipeline
from crew.data_platform.consumer import (
    latest_vintage_series,
    pivot_latest_vintage,
    treasury_curve,
)
from crew.yields.config import YieldSpreadConfig


class YieldSpreadDataPipeline(BaseDataPipeline):
    """Export official rate series and the Treasury curve from canonical storage."""

    def __init__(self, raw_data_dir: Path, config: YieldSpreadConfig) -> None:
        super().__init__(raw_data_dir, config)

    def fetch_data_internal(self, targets: dict[str, str], days: int) -> dict[str, str]:
        rates = pivot_latest_vintage(self.config.rates_dataset)
        rates = self._slice_period(rates, self.config.period)
        required_labels = {
            label
            for spread in self.config.curve_spreads.values()
            for label in (spread.short_label, spread.long_label)
        }
        required_labels.update({"us_10y_real", "us_10y_breakeven"})
        missing = sorted(required_labels.difference(rates.columns))
        if missing:
            raise ValueError(f"Canonical rate series are missing: {missing}")

        provenance = latest_vintage_series(self.config.rates_dataset)
        provenance = provenance[provenance["label"].isin(required_labels)].copy()
        if not rates.empty:
            provenance = provenance[provenance["observation_date"] >= rates.index.min()]

        curve = treasury_curve(latest_only=False)
        self._save("rates", rates.reset_index())
        self._save("rates_provenance", provenance)
        self._save("treasury_curve", curve)
        return {
            "rates": str(self.raw_data_dir / "rates.parquet"),
            "rates_provenance": str(self.raw_data_dir / "rates_provenance.parquet"),
            "treasury_curve": str(self.raw_data_dir / "treasury_curve.parquet"),
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
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "yields.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.yields.analysis import YieldSpreadAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=YieldSpreadDataPipeline,
        analyzer_class=YieldSpreadAnalyzer,
        config_class=YieldSpreadConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved canonical {name}: {path}")


if __name__ == "__main__":
    main()
