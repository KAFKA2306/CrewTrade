from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from crew.base import BaseUseCase, UseCasePaths
from crew.loan.analysis import SecuritiesCollateralLoanAnalyzer
from crew.loan.config import SecuritiesCollateralLoanConfig
from crew.loan.data_pipeline import (
    SecuritiesCollateralLoanDataPipeline,
)
from crew.loan.reporting import SecuritiesCollateralLoanReporter


class SecuritiesCollateralLoanUseCase(BaseUseCase):
    config: SecuritiesCollateralLoanConfig

    def __init__(
        self, config: SecuritiesCollateralLoanConfig, paths: UseCasePaths
    ) -> None:
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, pd.DataFrame]:
        pipeline = SecuritiesCollateralLoanDataPipeline(
            self.config, self.paths.raw_data_dir
        )
        return pipeline.collect()

    def analyze(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        analyzer = SecuritiesCollateralLoanAnalyzer(self.config)
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = SecuritiesCollateralLoanReporter(
            self.config, self.paths.processed_data_dir, self.paths.report_dir
        )
        return reporter.persist(analysis_payload)
