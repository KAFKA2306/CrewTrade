from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict
from zoneinfo import ZoneInfo

import pandas as pd
import yaml

from crew.legendary_investors.config import LegendaryInvestorsConfig


class LegendaryInvestorsAnalyzer:
    """Analyze point-in-time 13F information tables instead of fixed ticker lists."""

    def __init__(
        self, config: LegendaryInvestorsConfig, raw_data_dir: Any = None
    ) -> None:
        self.config = config
        self.raw_data_dir = Path(raw_data_dir) if raw_data_dir else None

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        filings = self._load_frame(data_payload.get("filings"), "filings.parquet")
        holdings = self._load_frame(data_payload.get("holdings"), "holdings.parquet")
        for column in ("filing_date", "report_date", "acceptance_datetime", "_retrieved_at"):
            if column in filings.columns:
                filings[column] = pd.to_datetime(filings[column])
        for column in ("report_date", "filing_date", "_retrieved_at"):
            if column in holdings.columns:
                holdings[column] = pd.to_datetime(holdings[column])
        holdings["reported_value"] = pd.to_numeric(
            holdings["reported_value"], errors="coerce"
        )
        holdings["shares_or_principal"] = pd.to_numeric(
            holdings["shares_or_principal"], errors="coerce"
        )
        holdings = (
            holdings.sort_values("_retrieved_at", ascending=False)
            .drop_duplicates("holding_id", keep="first")
            .reset_index(drop=True)
        )

        manager_summaries: list[dict[str, object]] = []
        latest_tables: list[pd.DataFrame] = []
        change_tables: list[pd.DataFrame] = []
        for manager_name, manager_config in self.config.managers.items():
            manager_holdings = holdings[
                holdings["entity_name"] == manager_name
            ].copy()
            report_dates = sorted(
                manager_holdings["report_date"].dropna().unique(), reverse=True
            )
            if not report_dates:
                continue
            latest_date = pd.Timestamp(report_dates[0])
            previous_date = (
                pd.Timestamp(report_dates[1]) if len(report_dates) > 1 else None
            )
            latest = manager_holdings[
                manager_holdings["report_date"] == latest_date
            ].copy()
            latest = self._aggregate_positions(latest)
            total_value = latest["reported_value"].sum(min_count=1)
            latest["portfolio_weight"] = (
                latest["reported_value"] / total_value
                if pd.notna(total_value) and total_value != 0
                else pd.NA
            )
            latest["manager"] = manager_name
            latest["manager_display_name"] = manager_config.display_name
            latest_tables.append(
                latest.sort_values("reported_value", ascending=False).head(
                    self.config.top_holdings_limit
                )
            )

            changes = pd.DataFrame()
            if previous_date is not None:
                previous = self._aggregate_positions(
                    manager_holdings[
                        manager_holdings["report_date"] == previous_date
                    ].copy()
                )
                changes = self._compare_positions(latest, previous)
                changes["manager"] = manager_name
                changes["manager_display_name"] = manager_config.display_name
                change_tables.append(changes)

            latest_filing = filings[
                (filings["entity_name"] == manager_name)
                & (filings["report_date"] == latest_date)
            ].sort_values("filing_date", ascending=False)
            filing_date = (
                pd.Timestamp(latest_filing.iloc[0]["filing_date"])
                if not latest_filing.empty
                else pd.Timestamp(latest["filing_date"].max())
            )
            manager_summaries.append(
                {
                    "manager": manager_name,
                    "manager_display_name": manager_config.display_name,
                    "latest_report_date": latest_date,
                    "previous_report_date": previous_date,
                    "filing_date": filing_date,
                    "filing_lag_days": (filing_date - latest_date).days,
                    "position_count": len(latest),
                    "reported_value_total": total_value,
                    "history_quarters": len(report_dates),
                    "comparison_ready": len(report_dates)
                    >= self.config.minimum_history_quarters,
                }
            )

        summary = pd.DataFrame(manager_summaries)
        latest_holdings = (
            pd.concat(latest_tables, ignore_index=True)
            if latest_tables
            else pd.DataFrame()
        )
        changes = (
            pd.concat(change_tables, ignore_index=True)
            if change_tables
            else pd.DataFrame()
        )
        return {
            "filings": filings,
            "holdings": holdings,
            "manager_summary": summary,
            "latest_holdings": latest_holdings,
            "quarter_changes": changes,
            "analysis_date": pd.Timestamp.now(tz="UTC"),
        }

    evaluate = analyze

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
            f"Canonical investor export {filename} is missing. "
            "Run `task fetch:legendary_investors`."
        )

    @staticmethod
    def _aggregate_positions(frame: pd.DataFrame) -> pd.DataFrame:
        keys = ["cusip", "issuer", "title_of_class", "put_call"]
        aggregations = {
            "reported_value": "sum",
            "shares_or_principal": "sum",
            "shares_or_principal_type": "first",
            "accession_number": "first",
            "report_date": "first",
            "filing_date": "max",
            "source_document_url": "first",
            "_source_url": "first",
            "_raw_sha256": "first",
        }
        available = {
            key: value
            for key, value in aggregations.items()
            if key in frame.columns
        }
        return frame.groupby(keys, dropna=False, as_index=False).agg(available)

    @staticmethod
    def _compare_positions(latest: pd.DataFrame, previous: pd.DataFrame) -> pd.DataFrame:
        keys = ["cusip", "issuer", "title_of_class", "put_call"]
        left = latest[keys + ["reported_value", "shares_or_principal"]].rename(
            columns={
                "reported_value": "latest_value",
                "shares_or_principal": "latest_shares",
            }
        )
        right = previous[keys + ["reported_value", "shares_or_principal"]].rename(
            columns={
                "reported_value": "previous_value",
                "shares_or_principal": "previous_shares",
            }
        )
        compared = left.merge(right, on=keys, how="outer")
        compared["value_change"] = (
            compared["latest_value"].fillna(0)
            - compared["previous_value"].fillna(0)
        )
        compared["share_change"] = (
            compared["latest_shares"].fillna(0)
            - compared["previous_shares"].fillna(0)
        )

        def classify(row: pd.Series) -> str:
            if pd.isna(row["previous_shares"]):
                return "new"
            if pd.isna(row["latest_shares"]):
                return "exited"
            if row["share_change"] > 0:
                return "increased"
            if row["share_change"] < 0:
                return "decreased"
            return "unchanged"

        compared["change_type"] = compared.apply(classify, axis=1)
        return compared.sort_values("value_change", key=lambda values: values.abs(), ascending=False)


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "legendary_investors.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "legendary_investors"


def main() -> None:
    from crew.legendary_investors.reporting import LegendaryInvestorsReporter

    config = LegendaryInvestorsConfig(
        **yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    )
    analyzer = LegendaryInvestorsAnalyzer(config, DATA_DIR)
    result = analyzer.analyze({})
    report_date = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d")
    reporter = LegendaryInvestorsReporter(
        PROJECT_ROOT
        / "output"
        / "use_cases"
        / "legendary_investors"
        / report_date
    )
    stored = reporter.produce_report(result)
    print(f"Canonical investor report: {stored['report_file']}")


if __name__ == "__main__":
    main()
