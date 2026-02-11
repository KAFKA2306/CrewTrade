from typing import Any, Dict
from crew.base import BaseUseCase
from .config import OracleEarningsConfig
from .reporting import OracleEarningsReporter
class OracleEarningsUseCase(BaseUseCase):
    def fetch_data(self) -> Dict[str, Any]:
        from crew.clients.equities import YFinanceEquityDataClient
        client = YFinanceEquityDataClient(self.paths.raw_data_dir)
        frames = client.get_frames(
            ["ORCL"], period="2y"
        )
        return {"price_frames": frames}
    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        if isinstance(self.config, OracleEarningsConfig):
            from .analysis import OracleEarningsAnalyzer
            analyzer = OracleEarningsAnalyzer(self.config)
            results = analyzer.evaluate(data_payload)
        else:
            results = {"error": "Invalid configuration type"}
        price_frames = data_payload.get("price_frames", {})
        if price_frames:
            forecasts = self.run_kronos_forecasts(price_frames, pred_len=91)
            results["forecasts"] = forecasts
        return results
    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = OracleEarningsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
