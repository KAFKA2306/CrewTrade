from typing import Any, Dict
import pandas as pd
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
        analyzer = SemiconductorsAnalyzer(config, self.paths.raw_data_dir)
        results = analyzer.analyze(data_payload)
        price_frames = data_payload.get("price_frames", {})
        if not price_frames and analyzer.raw_data_dir:
            from pathlib import Path
            raw_path = Path(analyzer.raw_data_dir)
            for symbol in config.tickers + [config.benchmark]:
                p = raw_path / f"{symbol}.parquet"
                if p.exists():
                    price_frames[symbol] = pd.read_parquet(p)
        forecasts = self.run_kronos_forecasts(price_frames, pred_len=91)
        if forecasts:
            results["forecasts"] = forecasts
        return results
    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = SemiconductorsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
