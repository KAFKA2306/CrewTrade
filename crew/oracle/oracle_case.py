from typing import Any, Dict

from crew.base import BaseUseCase

from .analysis import OracleEarningsAnalyzer
from .config import OracleEarningsConfig
from .reporting import OracleEarningsReporter


class OracleEarningsUseCase(BaseUseCase):
    def fetch_data(self) -> Dict[str, Any]:
        # Simulation only, no external data fetch
        return {}

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        # Config is already loaded in self.config by the runner
        if isinstance(self.config, OracleEarningsConfig):
            analyzer = OracleEarningsAnalyzer()
            return analyzer.analyze(self.config)
        return {"error": "Invalid configuration type"}

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = OracleEarningsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
