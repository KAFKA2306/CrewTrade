from __future__ import annotations

import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yaml

from crew.yields.config import YieldSpreadConfig


class YieldSpreadAnalyzer:
    """Analyze official Treasury rates without mixing credit and duration proxies."""

    def __init__(self, config: YieldSpreadConfig) -> None:
        self.config = config
        self.raw_data_dir: Path | None = None

    def evaluate(self, data_payload: dict[str, object]) -> dict[str, pd.DataFrame]:
        rates = self._load_frame(data_payload.get("rates"), "rates.parquet")
        curve = self._load_frame(data_payload.get("treasury_curve"), "treasury_curve.parquet")
        provenance = self._load_frame(
            data_payload.get("rates_provenance"),
            "rates_provenance.parquet",
            required=False,
        )

        if "Date" in rates.columns:
            rates["Date"] = pd.to_datetime(rates["Date"])
            rates = rates.set_index("Date")
        rates.index = pd.to_datetime(rates.index)
        rates = rates.sort_index().apply(pd.to_numeric, errors="coerce")
        curve["observation_date"] = pd.to_datetime(curve["observation_date"])
        curve["value"] = pd.to_numeric(curve["value"], errors="coerce")

        metrics = self._compute_spreads(rates)
        signals = self._detect_signals(metrics)
        spread_snapshot = self._spread_snapshot(metrics)
        macro_snapshot = self._macro_snapshot(rates)
        curve_snapshot = self._curve_snapshot(curve)
        return {
            "rates": rates,
            "treasury_curve": curve,
            "metrics": metrics,
            "signals": signals,
            "spread_snapshot": spread_snapshot,
            "macro_snapshot": macro_snapshot,
            "curve_snapshot": curve_snapshot,
            "provenance": provenance,
        }

    def _load_frame(self, value: object, filename: str, *, required: bool = True) -> pd.DataFrame:
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
                f"Canonical export {filename} is missing. Run `task fetch:yield`."
            )
        return pd.DataFrame()

    def _compute_spreads(self, rates: pd.DataFrame) -> pd.DataFrame:
        store: dict[str, pd.DataFrame] = {}
        for label, definition in self.config.curve_spreads.items():
            missing = sorted(
                {definition.short_label, definition.long_label}.difference(rates.columns)
            )
            if missing:
                raise ValueError(f"Missing canonical rate series for {label}: {missing}")
            aligned = rates[[definition.short_label, definition.long_label]].dropna()
            spread_pct = aligned[definition.long_label] - aligned[definition.short_label]
            rolling_mean = spread_pct.rolling(
                self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).mean()
            rolling_std = (
                spread_pct.rolling(
                    self.config.rolling_window,
                    min_periods=self.config.minimum_periods,
                )
                .std()
                .replace(0, np.nan)
            )
            store[label] = pd.DataFrame(
                {
                    "short_rate_pct": aligned[definition.short_label],
                    "long_rate_pct": aligned[definition.long_label],
                    "spread_pct": spread_pct,
                    "spread_bp": spread_pct * 100.0,
                    "change_20d_bp": spread_pct.diff(20) * 100.0,
                    "rolling_mean_pct": rolling_mean,
                    "rolling_std_pct": rolling_std,
                    "z_score": (spread_pct - rolling_mean) / rolling_std,
                }
            )
        return pd.concat(store, axis=1).sort_index()

    def _detect_signals(self, metrics: pd.DataFrame) -> pd.DataFrame:
        records: list[dict[str, object]] = []
        for label in self.config.curve_spreads:
            frame = metrics[label].dropna(subset=["z_score"])
            mask = frame["z_score"].abs() >= self.config.z_score_threshold
            if self.config.bp_alert_threshold > 0:
                mask &= frame["change_20d_bp"].abs() >= self.config.bp_alert_threshold
            for timestamp, row in frame.loc[mask].iterrows():
                records.append(
                    {
                        "date": timestamp,
                        "spread": label,
                        "spread_bp": float(row["spread_bp"]),
                        "change_20d_bp": float(row["change_20d_bp"]),
                        "z_score": float(row["z_score"]),
                        "direction": "steepening" if row["change_20d_bp"] > 0 else "flattening",
                    }
                )
        columns = [
            "date",
            "spread",
            "spread_bp",
            "change_20d_bp",
            "z_score",
            "direction",
        ]
        return (
            pd.DataFrame.from_records(records, columns=columns).sort_values(
                "date", ignore_index=True
            )
            if records
            else pd.DataFrame(columns=columns)
        )

    def _spread_snapshot(self, metrics: pd.DataFrame) -> pd.DataFrame:
        rows: list[dict[str, object]] = []
        for label, definition in self.config.curve_spreads.items():
            frame = metrics[label].dropna(subset=["spread_pct"])
            if frame.empty:
                continue
            row = frame.iloc[-1]
            rows.append(
                {
                    "spread": label,
                    "description": definition.description or "",
                    "latest_date": frame.index[-1],
                    "short_rate_pct": float(row["short_rate_pct"]),
                    "long_rate_pct": float(row["long_rate_pct"]),
                    "spread_bp": float(row["spread_bp"]),
                    "change_20d_bp": _optional_float(row["change_20d_bp"]),
                    "z_score": _optional_float(row["z_score"]),
                }
            )
        return pd.DataFrame(rows)

    @staticmethod
    def _macro_snapshot(rates: pd.DataFrame) -> pd.DataFrame:
        rows: list[dict[str, object]] = []
        for label in rates.columns:
            series = rates[label].dropna()
            if series.empty:
                continue
            rows.append(
                {
                    "series": label,
                    "latest_date": series.index[-1],
                    "value_pct": float(series.iloc[-1]),
                }
            )
        return pd.DataFrame(rows)

    @staticmethod
    def _curve_snapshot(curve: pd.DataFrame) -> pd.DataFrame:
        if curve.empty:
            return curve
        latest_date = curve["observation_date"].max()
        return curve[curve["observation_date"] == latest_date].sort_values("tenor")


def _optional_float(value: object) -> float | None:
    return None if pd.isna(value) else float(value)


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "yields.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "yields"


def main() -> None:
    from crew.yields.reporting import YieldSpreadReporter

    config = YieldSpreadConfig(**yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")))
    analyzer = YieldSpreadAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR
    results = analyzer.evaluate({})
    report_date = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d")
    report_dir = PROJECT_ROOT / "output" / "use_cases" / "yield_spread" / report_date
    reporter = YieldSpreadReporter(config, DATA_DIR / "processed", report_dir)
    stored = reporter.persist(results)
    print(f"Canonical yield report: {stored['report']}")


if __name__ == "__main__":
    main()
