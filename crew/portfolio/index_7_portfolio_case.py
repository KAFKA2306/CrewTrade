from typing import Any, Dict

from crew.base import BaseUseCase, UseCaseConfig, UseCasePaths

from .analysis import Index7PortfolioAnalyzer
from .config import Index7PortfolioConfig
from .data_pipeline import Index7PortfolioDataPipeline
from .reporting import Index7PortfolioReporter


class Index7PortfolioUseCase(BaseUseCase):
    def __init__(self, config: Index7PortfolioConfig, paths: UseCasePaths):
        super().__init__(config, paths)
        # Type helper
        self.config: Index7PortfolioConfig = config

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = Index7PortfolioDataPipeline(self.paths.raw_data_dir, self.config)
        # config has period, but pipeline signature is fetch_data(targets, days) in BaseDataPipeline ??
        # Wait, BaseDataPipeline.fetch_data calls fetch_data_internal
        # Index7PortfolioDataPipeline inherits BaseDataPipeline.
        # But Index7 uses config.period, not passed `days` param in fetch_data_internal (it ignores it mostly).
        return pipeline.fetch_data({}, 365)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = Index7PortfolioAnalyzer(self.config)
        # Inject raw_data_dir to analyzer just in case (like Imura did)
        analyzer.raw_data_dir = self.paths.raw_data_dir
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = Index7PortfolioReporter(
            self.paths.report_dir, self.config, self.paths.raw_data_dir
        )
        return reporter.persist(analysis_payload)
