from pathlib import Path

import pandas as pd
import yaml

from ai_trading_crew.use_cases.index_7_portfolio.config import Index7PortfolioConfig
from ai_trading_crew.use_cases.index_7_portfolio.validation import Index7PortfolioValidator


def main():
    config_path = Path("config/use_cases/index_7_portfolio.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)
    config = Index7PortfolioConfig(**payload)

    timestamp = pd.Timestamp.now().strftime("%Y%m%d")
    output_dir = Path("output/use_cases/index_7_portfolio") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("Index 7-Portfolio Validation")
    print(f"{'='*60}\n")

    validator = Index7PortfolioValidator(config)

    print("Generating validation report...")
    report_path = validator.generate_validation_report(output_dir)

    print(f"\n✅ Validation complete!")
    print(f"Report: {report_path}\n")


if __name__ == "__main__":
    main()
