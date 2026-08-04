from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict
from zoneinfo import ZoneInfo

import pandas as pd
import yaml

from crew.oracle.config import OracleEarningsConfig


class OracleEarningsAnalyzer:
    """Audit Oracle filings and XBRL facts without treating model scenarios as actuals."""

    def __init__(self, config: OracleEarningsConfig) -> None:
        self.config = config
        self.raw_data_dir: Path | None = None

    def evaluate(self, data_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        payload = data_payload or {}
        filings = self._load_frame(payload.get("filings"), "filings.parquet")
        facts = self._load_frame(payload.get("facts"), "facts.parquet")

        for column in ("filing_date", "report_date", "acceptance_datetime", "_retrieved_at"):
            if column in filings.columns:
                filings[column] = pd.to_datetime(filings[column])
        for column in ("start_date", "end_date", "filed_date", "_retrieved_at"):
            if column in facts.columns:
                facts[column] = pd.to_datetime(facts[column])
        facts["value"] = pd.to_numeric(facts["value"], errors="coerce")
        facts = facts.dropna(subset=["value"])

        filing_snapshot = (
            filings.sort_values(
                ["form", "filing_date", "acceptance_datetime"],
                ascending=[True, False, False],
            )
            .groupby("form", as_index=False)
            .head(1)
            .reset_index(drop=True)
        )
        fact_snapshot = self._latest_facts(facts)
        derived_fcf = self._derive_free_cash_flow(facts)
        configured_metrics = set(self.config.concepts)
        available_metrics = set(fact_snapshot.get("metric", pd.Series(dtype=str)))
        coverage = pd.DataFrame(
            [
                {
                    "configured_metrics": len(configured_metrics),
                    "available_metrics": len(configured_metrics.intersection(available_metrics)),
                    "coverage_ratio": (
                        len(configured_metrics.intersection(available_metrics))
                        / len(configured_metrics)
                        if configured_metrics
                        else 1.0
                    ),
                    "model_projection_enabled": self.config.allow_model_projection,
                }
            ]
        )
        return {
            "filings": filings,
            "facts": facts,
            "filing_snapshot": filing_snapshot,
            "fact_snapshot": fact_snapshot,
            "derived_fcf": derived_fcf,
            "coverage": coverage,
            "projections": {},
        }

    def _load_frame(self, value: object, filename: str) -> pd.DataFrame:
        if isinstance(value, pd.DataFrame):
            return value.copy()
        if isinstance(value, (str, Path)) and Path(value).is_file():
            return pd.read_parquet(value)
        if self.raw_data_dir is not None:
            path = self.raw_data_dir / filename
            if path.is_file():
                return pd.read_parquet(path)
        raise FileNotFoundError(
            f"Canonical Oracle export {filename} is missing. Run `task fetch:oracle`."
        )

    @staticmethod
    def _latest_facts(facts: pd.DataFrame) -> pd.DataFrame:
        if facts.empty:
            return facts
        ordering = ["metric", "end_date", "filed_date", "_retrieved_at"]
        available_ordering = [column for column in ordering if column in facts.columns]
        sorted_facts = facts.sort_values(
            available_ordering,
            ascending=[True] + [False] * (len(available_ordering) - 1),
            na_position="last",
        )
        group_columns = ["metric", "unit"] if "unit" in facts.columns else ["metric"]
        return (
            sorted_facts.groupby(group_columns, as_index=False, dropna=False)
            .head(1)
            .reset_index(drop=True)
        )

    @staticmethod
    def _derive_free_cash_flow(facts: pd.DataFrame) -> pd.DataFrame:
        required = {"operating_cash_flow", "capital_expenditure"}
        if "metric" not in facts.columns or not required.issubset(set(facts["metric"])):
            return pd.DataFrame(
                columns=[
                    "start_date",
                    "end_date",
                    "filed_date",
                    "unit",
                    "operating_cash_flow",
                    "capital_expenditure",
                    "derived_free_cash_flow",
                ]
            )
        subset = facts[facts["metric"].isin(required)].copy()
        keys = ["start_date", "end_date", "filed_date", "unit"]
        pivot = subset.pivot_table(
            index=keys,
            columns="metric",
            values="value",
            aggfunc="last",
        ).reset_index()
        pivot = pivot.dropna(subset=list(required))
        pivot["derived_free_cash_flow"] = (
            pivot["operating_cash_flow"] - pivot["capital_expenditure"].abs()
        )
        return pivot.sort_values(["end_date", "filed_date"], ascending=False)


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "oracle.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "oracle"


def main() -> None:
    from crew.oracle.reporting import OracleEarningsReporter

    config = OracleEarningsConfig(
        **yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    )
    analyzer = OracleEarningsAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR
    result = analyzer.evaluate({})
    report_date = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d")
    reporter = OracleEarningsReporter(
        PROJECT_ROOT / "output" / "use_cases" / "oracle" / report_date
    )
    stored = reporter.produce_report(result)
    print(f"Canonical Oracle report: {stored['report_file']}")


if __name__ == "__main__":
    main()
