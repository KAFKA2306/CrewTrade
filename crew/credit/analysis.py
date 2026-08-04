from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo
import datetime

import numpy as np
import pandas as pd
import yaml

from crew.credit.config import CreditSpreadConfig


class CreditSpreadAnalyzer:
    """Measure official ICE BofA option-adjusted spreads, not ETF price ratios."""

    def __init__(self, config: CreditSpreadConfig) -> None:
        self.config = config
        self.raw_data_dir: Path | None = None

    def evaluate(self, data_payload: Dict[str, object]) -> Dict[str, pd.DataFrame]:
        oas = self._load_frame(data_payload.get("oas"), "oas.parquet")
        provenance = self._load_frame(
            data_payload.get("provenance"), "provenance.parquet", required=False
        )
        if "Date" in oas.columns:
            oas["Date"] = pd.to_datetime(oas["Date"])
            oas = oas.set_index("Date")
        oas.index = pd.to_datetime(oas.index)
        oas = oas.sort_index()

        missing = sorted(set(self.config.series_labels).difference(oas.columns))
        if missing:
            raise ValueError(f"Canonical credit series are missing: {missing}")
        oas = oas[self.config.series_labels].apply(pd.to_numeric, errors="coerce")

        metrics = self._compute_metrics(oas)
        signals = self._detect_signals(metrics)
        snapshot = self._build_snapshot(metrics)
        return {
            "oas": oas,
            "metrics": metrics,
            "signals": signals,
            "snapshot": snapshot,
            "provenance": provenance,
        }

    def _load_frame(
        self, value: object, filename: str, *, required: bool = True
    ) -> pd.DataFrame:
        if isinstance(value, pd.DataFrame):
            return value.copy()
        if isinstance(value, (str, Path)) and Path(value).is_file():
            return pd.read_parquet(value)
        if self.raw_data_dir is not None:
            path = self.raw_data_dir / filename
            if path.is_file():
                return pd.read_parquet(path)
        if required:
            raise FileNotFoundError(
                f"Canonical export {filename} is missing. Run `task fetch:credit`."
            )
        return pd.DataFrame()

    def _compute_metrics(self, oas: pd.DataFrame) -> pd.DataFrame:
        store: Dict[str, pd.DataFrame] = {}
        for label in self.config.series_labels:
            level = oas[label].dropna()
            mean = level.rolling(
                self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).mean()
            std = level.rolling(
                self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).std().replace(0, np.nan)
            store[label] = pd.DataFrame(
                {
                    "level_pct": level,
                    "change_1d_bp": level.diff() * 100.0,
                    "change_20d_bp": level.diff(20) * 100.0,
                    "rolling_mean_pct": mean,
                    "rolling_std_pct": std,
                    "z_score": (level - mean) / std,
                }
            )
        return pd.concat(store, axis=1).sort_index()

    def _detect_signals(self, metrics: pd.DataFrame) -> pd.DataFrame:
        records: List[dict[str, object]] = []
        for label in self.config.series_labels:
            frame = metrics[label].dropna(subset=["z_score"])
            mask = frame["z_score"].abs() >= self.config.z_score_threshold
            if self.config.bp_alert_threshold > 0:
                mask &= frame["change_20d_bp"].abs() >= self.config.bp_alert_threshold
            for timestamp, row in frame.loc[mask].iterrows():
                records.append(
                    {
                        "date": timestamp,
                        "series": label,
                        "level_pct": float(row["level_pct"]),
                        "change_20d_bp": float(row["change_20d_bp"]),
                        "z_score": float(row["z_score"]),
                        "direction": "widening" if row["z_score"] > 0 else "tightening",
                    }
                )
        columns = [
            "date",
            "series",
            "level_pct",
            "change_20d_bp",
            "z_score",
            "direction",
        ]
        return pd.DataFrame.from_records(records, columns=columns).sort_values(
            "date", ignore_index=True
        ) if records else pd.DataFrame(columns=columns)

    def _build_snapshot(self, metrics: pd.DataFrame) -> pd.DataFrame:
        rows: List[dict[str, object]] = []
        for label in self.config.series_labels:
            frame = metrics[label].dropna(subset=["level_pct"])
            if frame.empty:
                continue
            latest = frame.iloc[-1]
            rows.append(
                {
                    "series": label,
                    "latest_date": frame.index[-1],
                    "level_pct": float(latest["level_pct"]),
                    "change_1d_bp": _optional_float(latest["change_1d_bp"]),
                    "change_20d_bp": _optional_float(latest["change_20d_bp"]),
                    "z_score": _optional_float(latest["z_score"]),
                }
            )
        return pd.DataFrame(rows)


def _optional_float(value: object) -> float | None:
    return None if pd.isna(value) else float(value)


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "credit.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "credit_spread"


def main() -> None:
    from crew.credit.reporting import CreditSpreadReporter

    config = CreditSpreadConfig(
        **yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    )
    analyzer = CreditSpreadAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR
    results = analyzer.evaluate({})
    report_date = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d")
    report_dir = PROJECT_ROOT / "output" / "use_cases" / "credit" / report_date
    reporter = CreditSpreadReporter(config, DATA_DIR / "processed", report_dir)
    stored = reporter.persist(results)
    print(f"Canonical credit report: {stored['report']}")


if __name__ == "__main__":
    main()
