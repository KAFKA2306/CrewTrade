from __future__ import annotations

from typing import Any, Dict

from crew.base import BaseUseCase, UseCasePaths
from crew.etf.analysis import (
    IndexETFComparisonAnalyzer,
)
from crew.etf.config import (
    IndexETFComparisonConfig,
)
from crew.etf.data_pipeline import (
    IndexETFComparisonDataPipeline,
)
from crew.etf.reporting import (
    IndexETFComparisonReporter,
)


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
        reporter = IndexETFComparisonReporter(
            self.config, self.paths.processed_data_dir, self.paths.report_dir
        )
        return reporter.persist(analysis_payload)
