from typing import Any, Dict

import pandas as pd

from crew.base import BaseUseCase, UseCasePaths
from crew.metals.analysis import PreciousMetalsSpreadAnalyzer
from crew.metals.config import PreciousMetalsSpreadConfig
from crew.metals.data_pipeline import (
    PreciousMetalsSpreadDataPipeline,
)
from crew.metals.reporting import PreciousMetalsSpreadReporter


class PreciousMetalsSpreadUseCase(BaseUseCase):
    config: PreciousMetalsSpreadConfig

    def __init__(self, config: PreciousMetalsSpreadConfig, paths: UseCasePaths) -> None:
        super().__init__(config, paths)
        self.config = config

    def fetch_data(self) -> Dict[str, pd.DataFrame]:
        pipeline = PreciousMetalsSpreadDataPipeline(
            self.config, self.paths.raw_data_dir
        )
        return pipeline.collect()

    def analyze(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        analyzer = PreciousMetalsSpreadAnalyzer(self.config)
        return analyzer.evaluate(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = PreciousMetalsSpreadReporter(
            self.config, self.paths.processed_data_dir, self.paths.report_dir
        )
        return reporter.persist(analysis_payload)
