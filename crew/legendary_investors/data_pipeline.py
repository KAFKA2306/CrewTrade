from __future__ import annotations

from pathlib import Path
from typing import Dict

from crew.app import BaseDataPipeline, GenericUseCase
from crew.data_platform.consumer import sec_13f_holdings, sec_filings
from crew.legendary_investors.config import LegendaryInvestorsConfig


class LegendaryInvestorsDataPipeline(BaseDataPipeline):
    """Export 13F filings and information-table holdings from canonical SEC data."""

    def __init__(self, raw_data_dir: Path, config: LegendaryInvestorsConfig) -> None:
        super().__init__(raw_data_dir, config)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        manager_names = self.config.manager_names
        filings = sec_filings(
            entity_names=manager_names,
            forms=self.config.forms,
        )
        holdings = sec_13f_holdings(
            entity_names=manager_names,
            latest_only=False,
        )
        self._save("filings", filings)
        self._save("holdings", holdings)
        return {
            "filings": str(self.raw_data_dir / "filings.parquet"),
            "holdings": str(self.raw_data_dir / "holdings.parquet"),
        }


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "legendary_investors.yaml"


def main() -> None:
    from crew.legendary_investors.analysis import LegendaryInvestorsAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=LegendaryInvestorsDataPipeline,
        analyzer_class=LegendaryInvestorsAnalyzer,
        config_class=LegendaryInvestorsConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved canonical investor {name}: {path}")


if __name__ == "__main__":
    main()
