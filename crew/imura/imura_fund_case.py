from typing import Any, Dict

from crew.base import BaseUseCase, UseCaseConfig, UseCasePaths

from .analysis import ImuraFundAnalyzer
from .data import ImuraFundDataPipeline
from .reporting import ImuraFundReporter


class ImuraFundUseCase(BaseUseCase):
    def __init__(self, config: UseCaseConfig, paths: UseCasePaths):
        super().__init__(config, paths)

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = ImuraFundDataPipeline(self.paths.raw_data_dir)
        return pipeline.fetch_data(self.config.targets, self.config.days)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = ImuraFundAnalyzer(self.paths.raw_data_dir)
        analysis_result = analyzer.analyze(data_payload)

        # Add Kronos Forecasts
        # Add Kronos Forecasts
        import pandas as pd

        price_frames = {}

        for name, path in data_payload.items():
            try:
                if str(path).endswith(".parquet"):
                    df = pd.read_parquet(path)
                else:
                    df = pd.read_csv(path, parse_dates=["Date"])
                price_frames[name] = df
            except Exception:
                continue

        forecasts = self.run_kronos_forecasts(price_frames, pred_len=30)
        analysis_result["forecasts"] = forecasts

        return analysis_result

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = ImuraFundReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
