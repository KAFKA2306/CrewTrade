from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from ai_trading_crew.use_cases.base import BaseUseCase, UseCasePaths
from ai_trading_crew.use_cases.yield_spread.analysis import YieldSpreadAnalyzer
from ai_trading_crew.use_cases.yield_spread.config import YieldSpreadConfig
from ai_trading_crew.use_cases.yield_spread.data_pipeline import YieldSpreadDataPipeline
from ai_trading_crew.use_cases.yield_spread.reporting import YieldSpreadReporter


class YieldSpreadUseCase(BaseUseCase):
    config: YieldSpreadConfig

    def __init__(self, config: YieldSpreadConfig, paths: UseCasePaths) -> None:
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, pd.DataFrame]:
        pipeline = YieldSpreadDataPipeline(self.config, self.paths.raw_data_dir)
        return pipeline.collect()

    def analyze(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        analyzer = YieldSpreadAnalyzer(self.config)
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = YieldSpreadReporter(self.config, self.paths.processed_data_dir, self.paths.report_dir)
        return reporter.persist(analysis_payload)
