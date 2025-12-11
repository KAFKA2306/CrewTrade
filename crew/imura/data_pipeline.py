from pathlib import Path

from crew.app import GenericUseCase
from crew.imura.config import ImuraFundConfig
from crew.imura.data import ImuraFundDataPipeline
from crew.imura.analysis import ImuraFundAnalyzer

# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "imura.yaml"


def main() -> None:
    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=ImuraFundDataPipeline,
        analyzer_class=ImuraFundAnalyzer,
        config_class=ImuraFundConfig,
    )

    # Just run fetching for this script as it is named data_pipeline
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
