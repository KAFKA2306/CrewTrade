from typing import Any, Dict
import pandas as pd
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
        all_tickers = list(
            set(
                config.soros_holdings
                + config.druckenmiller_holdings
                + [config.benchmark]
            )
        )
        frames = client.get_frames(all_tickers, period=config.period)
        return {"price_frames": frames}
    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        config: LegendaryInvestorsConfig = self.config
        analyzer = LegendaryInvestorsAnalyzer(config, self.paths.raw_data_dir)
        results = analyzer.analyze(data_payload)
        price_frames = data_payload.get("price_frames", {})
        if not price_frames and analyzer.raw_data_dir:
            from pathlib import Path
            raw = Path(analyzer.raw_data_dir)
            tickers = list(
                set(
                    config.soros_holdings
                    + config.druckenmiller_holdings
                    + [config.benchmark]
                )
            )
            for t in tickers:
                p = raw / f"{t}.parquet"
                if p.exists():
                    price_frames[t] = pd.read_parquet(p)
        forecasts = {}
        for ticker, df in price_frames.items():
            if df is None or df.empty:
                continue
            try:
                df = df.copy()
                df.columns = [str(c).lower() for c in df.columns]
                if "close" in df.columns and "open" not in df.columns:
                    df["open"] = df["close"]
                    df["high"] = df["close"]
                    df["low"] = df["close"]
                    df["volume"] = 0.0
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
        reporter = LegendaryInvestorsReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
