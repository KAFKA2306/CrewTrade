from typing import Any, Dict

from crew.base import BaseUseCase, UseCaseConfig, UseCasePaths

from .analysis import ImuraFundAnalyzer
from .data import ImuraFundDataPipeline
from .reporting import ImuraFundReporter


class ImuraFundUseCase(BaseUseCase):
    def __init__(self, config: UseCaseConfig, paths: UseCasePaths):
        super().__init__(config, paths)

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = ImuraFundDataPipeline(self.paths.raw_data_dir)
        return pipeline.fetch_data(self.config.targets, self.config.days)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = ImuraFundAnalyzer(self.paths.raw_data_dir)
        return analyzer.analyze(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = ImuraFundReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
