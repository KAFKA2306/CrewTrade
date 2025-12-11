from pathlib import Path

from crew.imura.config import ImuraFundConfig
from crew.imura.data import ImuraFundDataPipeline

RAW_DATA_DIR = Path(__file__).parent / "data"


def main() -> None:
    config = ImuraFundConfig(name="imura")
    pipeline = ImuraFundDataPipeline(RAW_DATA_DIR)
    saved_files = pipeline.fetch_data(config.targets, config.days)
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
