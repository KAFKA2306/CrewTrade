from __future__ import annotations

from typing import Any, Dict

from ai_trading_crew.use_cases.base import BaseUseCase, UseCasePaths
from ai_trading_crew.use_cases.index_etf_comparison.config import IndexETFComparisonConfig
from ai_trading_crew.use_cases.index_etf_comparison.data_pipeline import IndexETFComparisonDataPipeline
from ai_trading_crew.use_cases.index_etf_comparison.analysis import IndexETFComparisonAnalyzer
from ai_trading_crew.use_cases.index_etf_comparison.reporting import IndexETFComparisonReporter


class IndexETFComparisonUseCase(BaseUseCase):
    config: IndexETFComparisonConfig

    def __init__(self, config: IndexETFComparisonConfig, paths: UseCasePaths) -> None:
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = IndexETFComparisonDataPipeline(self.config, self.paths.raw_data_dir)
        return pipeline.collect()

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = IndexETFComparisonAnalyzer(self.config)
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = IndexETFComparisonReporter(self.config, self.paths.processed_data_dir, self.paths.report_dir)
        return reporter.persist(analysis_payload)
