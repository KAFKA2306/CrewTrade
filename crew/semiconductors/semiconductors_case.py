from typing import Any, Dict

from crew.base import BaseUseCase
from crew.clients.equities import YFinanceEquityDataClient

from .analysis import SemiconductorsAnalyzer
from .config import SemiconductorsConfig
from .reporting import SemiconductorsReporter


class SemiconductorsUseCase(BaseUseCase):
    """Use case for analyzing top semiconductor stocks."""

    def fetch_data(self) -> Dict[str, Any]:
        config: SemiconductorsConfig = self.config
        client = YFinanceEquityDataClient(self.paths.raw_data_dir)
        all_tickers = config.tickers + [config.benchmark]
        frames = client.get_frames(all_tickers, period=config.period)
        return {"price_frames": frames}

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        config: SemiconductorsConfig = self.config
        analyzer = SemiconductorsAnalyzer(config)
        return analyzer.analyze(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = SemiconductorsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
