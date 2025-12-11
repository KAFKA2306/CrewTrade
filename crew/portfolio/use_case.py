from pathlib import Path
from typing import Any, Dict

import pandas as pd

from crew.base import BaseUseCase, UseCasePaths
from crew.portfolio.analysis import Index7PortfolioAnalyzer
from crew.portfolio.config import Index7PortfolioConfig
from crew.portfolio.data_pipeline import (
    Index7PortfolioDataPipeline,
)
from crew.portfolio.reporting import Index7PortfolioReporter


class Index7PortfolioUseCase(BaseUseCase):
    def __init__(self, config: Index7PortfolioConfig, paths: UseCasePaths):
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, Any]:
        print("Step 1/3: Collecting index data...")
        pipeline = Index7PortfolioDataPipeline(self.config)
        data_payload = pipeline.collect(as_of=None)
        print(f"  ✓ Loaded {len(data_payload['prices'].columns)} indices")
        print(
            f"  ✓ Date range: {data_payload['prices'].index.min()} to {data_payload['prices'].index.max()}"
        )
        return data_payload

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        print("\nStep 2/3: Analyzing and optimizing portfolio...")
        analyzer = Index7PortfolioAnalyzer(self.config)
        analysis_payload = analyzer.evaluate(data_payload)
        print(f"  ✓ Portfolio value: ¥{analysis_payload['portfolio_value']:,.0f}")
        print(f"  ✓ Current LTV: {analysis_payload['current_ltv'] * 100:.2f}%")
        return analysis_payload

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        print("\nStep 3/3: Generating reports...")
        reporter = Index7PortfolioReporter(self.paths.report_dir, self.config)
        report_payload = reporter.persist(analysis_payload)
        print(f"  ✓ Portfolio saved: {report_payload['portfolio_path']}")
        print(f"  ✓ Report saved: {report_payload['report_path']}")
        if "chart_paths" in report_payload:
            print(
                f"  ✓ Charts saved: {len(report_payload['chart_paths'])} visualizations"
            )
        return report_payload

    def execute(self, config_path: Path | None = None) -> dict:
        timestamp = pd.Timestamp.now().strftime("%Y%m%d")
        output_dir = Path("output/use_cases/index_7_portfolio") / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'=' * 60}")
        print("Index 7-Portfolio Use Case")
        print(f"{'=' * 60}\n")

        print("Step 1/3: Collecting index data...")
        pipeline = Index7PortfolioDataPipeline(self.config)
        data_payload = pipeline.collect(as_of=None)
        print(f"  ✓ Loaded {len(data_payload['prices'].columns)} indices")
        print(
            f"  ✓ Date range: {data_payload['prices'].index.min()} to {data_payload['prices'].index.max()}"
        )

        print("\nStep 2/3: Analyzing and optimizing portfolio...")
        analyzer = Index7PortfolioAnalyzer(self.config)
        analysis_payload = analyzer.evaluate(data_payload)
        print(f"  ✓ Portfolio value: ¥{analysis_payload['portfolio_value']:,.0f}")
        print(f"  ✓ Current LTV: {analysis_payload['current_ltv'] * 100:.2f}%")

        print("\nStep 3/3: Generating reports...")
        reporter = Index7PortfolioReporter(output_dir, self.config)
        report_payload = reporter.persist(analysis_payload)
        print(f"  ✓ Portfolio saved: {report_payload['portfolio_path']}")
        print(f"  ✓ Report saved: {report_payload['report_path']}")
        if "chart_paths" in report_payload:
            print(
                f"  ✓ Charts saved: {len(report_payload['chart_paths'])} visualizations"
            )

        print(f"\n{'=' * 60}")
        print("✅ Index 7-Portfolio analysis complete!")
        print(f"{'=' * 60}\n")

        return {
            "status": "success",
            "output_dir": str(output_dir),
            **report_payload,
        }
