from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from ai_trading_crew.use_cases.base import BaseUseCase, UseCasePaths
from ai_trading_crew.use_cases.credit_spread.analysis import CreditSpreadAnalyzer
from ai_trading_crew.use_cases.credit_spread.config import CreditSpreadConfig
from ai_trading_crew.use_cases.credit_spread.data_pipeline import CreditSpreadDataPipeline
from ai_trading_crew.use_cases.credit_spread.reporting import CreditSpreadReporter


class CreditSpreadUseCase(BaseUseCase):
    config: CreditSpreadConfig

    def __init__(self, config: CreditSpreadConfig, paths: UseCasePaths) -> None:
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, pd.DataFrame]:
        pipeline = CreditSpreadDataPipeline(self.config, self.paths.raw_data_dir)
        return pipeline.collect()

    def analyze(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        analyzer = CreditSpreadAnalyzer(self.config)
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = CreditSpreadReporter(self.config, self.paths.processed_data_dir, self.paths.report_dir)
        return reporter.persist(analysis_payload)
