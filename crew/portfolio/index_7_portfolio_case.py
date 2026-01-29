from typing import Any, Dict
import pandas as pd

from crew.base import BaseUseCase, UseCasePaths

from .analysis import Index7PortfolioAnalyzer
from .config import Index7PortfolioConfig
from .data_pipeline import Index7PortfolioDataPipeline
from .reporting import Index7PortfolioReporter


class Index7PortfolioUseCase(BaseUseCase):
    def __init__(self, config: Index7PortfolioConfig, paths: UseCasePaths):
        super().__init__(config, paths)
        # Type helper
        self.config: Index7PortfolioConfig = config

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = Index7PortfolioDataPipeline(self.paths.raw_data_dir, self.config)
        return pipeline.fetch_data({}, 365)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = Index7PortfolioAnalyzer(self.config)
        analyzer.raw_data_dir = self.paths.raw_data_dir
        results = analyzer.evaluate(data_payload)

        # Kronos Integration
        portfolio = results.get("portfolio")
        forecasts = {}
        if isinstance(portfolio, pd.DataFrame) and not portfolio.empty:
            tickers = portfolio["ticker"].tolist()
            for ticker in tickers:
                # Load frame from disk (cached by client)
                p_path = self.paths.raw_data_dir / f"{ticker}.parquet"
                c_path = self.paths.raw_data_dir / f"{ticker}.csv"
                df = None
                if p_path.exists():
                    df = pd.read_parquet(p_path)
                elif c_path.exists():
                    df = pd.read_csv(c_path, index_col=0, parse_dates=True)

                if df is not None:
                    try:
                        # Normalize columns
                        df.columns = [str(c).lower() for c in df.columns]
                        if "close" in df.columns and "open" not in df.columns:
                            df["open"] = df["close"]
                            df["high"] = df["close"]
                            df["low"] = df["close"]
                            df["volume"] = 0.0

                        # Ensure Date
                        if "date" in df.columns:
                            df["Date"] = pd.to_datetime(df["date"])
                        elif df.index.name and df.index.name.lower() == "date":
                            df = df.reset_index()
                            df["Date"] = pd.to_datetime(df["Date"])
                        else:
                            df = df.reset_index()
                            df.columns.values[0] = "Date"
                            df["Date"] = pd.to_datetime(df.iloc[:, 0])

                        if "Date" in df.columns:
                            df = df.sort_values("Date").reset_index(drop=True)
                            if len(df) > 30:
                                x_timestamp = df["Date"]
                                pred_len = 30
                                last_date = df["Date"].iloc[-1]
                                future_dates = [
                                    last_date + pd.Timedelta(days=i + 1)
                                    for i in range(pred_len)
                                ]
                                y_timestamp = pd.Series(future_dates)

                                pred_df = self.get_kronos_forecast(
                                    df=df,
                                    x_timestamp=x_timestamp,
                                    y_timestamp=y_timestamp,
                                    pred_len=pred_len,
                                )
                                forecasts[ticker] = pred_df.to_dict(orient="records")
                    except Exception:
                        pass

        if forecasts:
            results["forecasts"] = forecasts

        return results

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = Index7PortfolioReporter(
            self.paths.report_dir, self.config, self.paths.raw_data_dir
        )
        return reporter.persist(analysis_payload)
