from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline, GenericUseCase
from crew.data_platform.consumer import sec_company_facts, sec_filings
from crew.oracle.config import OracleEarningsConfig


class OracleDataPipeline(BaseDataPipeline):
    """Export Oracle filings and selected XBRL facts from canonical SEC storage."""

    def __init__(self, raw_data_dir: Path, config: OracleEarningsConfig) -> None:
        super().__init__(raw_data_dir, config)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        filings = sec_filings(
            entity_names=[self.config.entity_name], forms=self.config.forms
        )
        all_facts = sec_company_facts(entity_name=self.config.entity_name)
        selected: list[pd.DataFrame] = []
        for metric, candidates in self.config.concepts.items():
            matched = all_facts[all_facts["concept"].isin(candidates)].copy()
            if matched.empty:
                continue
            matched["metric"] = metric
            selected.append(matched)
        if selected:
            facts = pd.concat(selected, ignore_index=True)
        else:
            pattern = (
                "Revenue|OperatingIncome|CashProvided|PropertyPlant|"
                "ProductiveAssets|PerformanceObligation"
            )
            facts = all_facts[
                all_facts["concept"].str.contains(pattern, case=False, na=False)
            ].copy()
            facts["metric"] = "unmapped"
        if facts.empty:
            raise ValueError("No decision-relevant Oracle SEC facts were found")

        self._save("filings", filings)
        self._save("facts", facts)
        return {
            "filings": str(self.raw_data_dir / "filings.parquet"),
            "facts": str(self.raw_data_dir / "facts.parquet"),
        }


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "oracle.yaml"


def main() -> None:
    from crew.oracle.analysis import OracleEarningsAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=OracleDataPipeline,
        analyzer_class=OracleEarningsAnalyzer,
        config_class=OracleEarningsConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved canonical Oracle {name}: {path}")


if __name__ == "__main__":
    main()
