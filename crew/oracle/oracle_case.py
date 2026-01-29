from typing import Any, Dict

from crew.base import BaseUseCase

from .config import OracleEarningsConfig
from .reporting import OracleEarningsReporter


class OracleEarningsUseCase(BaseUseCase):
    def fetch_data(self) -> Dict[str, Any]:
        from crew.clients.equities import YFinanceEquityDataClient

        client = YFinanceEquityDataClient(self.paths.raw_data_dir)
        # Fetch ORCL data for Kronos forecasting as a "bonus" feature for this use case
        frames = client.get_frames(
            ["ORCL"], period="2y"
        )  # 2y is sufficient for model context
        return {"price_frames": frames}

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        # Config is already loaded in self.config by the runner
        results = {}
        if isinstance(self.config, OracleEarningsConfig):
            from .analysis import OracleEarningsAnalyzer

            analyzer = OracleEarningsAnalyzer(self.config)
            results = analyzer.evaluate(data_payload)
        else:
            results = {"error": "Invalid configuration type"}

        # Add Kronos Forecasts
        price_frames = data_payload.get("price_frames", {})
        if price_frames:
            forecasts = self.run_kronos_forecasts(price_frames, pred_len=30)
            results["forecasts"] = forecasts

        return results

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = OracleEarningsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
