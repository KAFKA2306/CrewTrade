from typing import Any, Dict

from crew.base import BaseUseCase
from crew.clients.equities import YFinanceEquityDataClient

from .analysis import LegendaryInvestorsAnalyzer
from .config import LegendaryInvestorsConfig
from .reporting import LegendaryInvestorsReporter


class LegendaryInvestorsUseCase(BaseUseCase):
    """Use case for tracking legendary investors' top holdings."""

    def fetch_data(self) -> Dict[str, Any]:
        config: LegendaryInvestorsConfig = self.config
        client = YFinanceEquityDataClient(self.paths.raw_data_dir)
        
        all_tickers = list(set(
            config.soros_holdings + 
            config.druckenmiller_holdings + 
            [config.benchmark]
        ))
        
        frames = client.get_frames(all_tickers, period=config.period)
        return {"price_frames": frames}

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        config: LegendaryInvestorsConfig = self.config
        analyzer = LegendaryInvestorsAnalyzer(config)
        return analyzer.analyze(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = LegendaryInvestorsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
