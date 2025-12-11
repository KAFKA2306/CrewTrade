from pathlib import Path
from typing import Dict

from crew.app import BaseDataPipeline, GenericUseCase
from crew.oracle.analysis import OracleEarningsAnalyzer
from crew.oracle.config import OracleEarningsConfig


class OracleDataPipeline(BaseDataPipeline):
    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        # Simulation only, no data to fetch
        return {}


# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "oracle.yaml"


def main() -> None:
    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=OracleDataPipeline,
        analyzer_class=OracleEarningsAnalyzer,
        config_class=OracleEarningsConfig,
    )

    use_case.fetch_data()
    # No saved files expected


if __name__ == "__main__":
    main()
