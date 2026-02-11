from pathlib import Path
from crew.app import GenericUseCase
from crew.imura.config import ImuraFundConfig
from crew.imura.data import ImuraFundDataPipeline
from crew.imura.analysis import ImuraFundAnalyzer
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "imura.yaml"
def main() -> None:
    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=ImuraFundDataPipeline,
        analyzer_class=ImuraFundAnalyzer,
        config_class=ImuraFundConfig,
    )
    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")
if __name__ == "__main__":
    main()
