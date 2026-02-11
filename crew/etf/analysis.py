from __future__ import annotations
from typing import Any, Dict
import numpy as np
import pandas as pd
from crew.etf.config import (
    IndexETFComparisonConfig,
)
class IndexETFComparisonAnalyzer:
    def __init__(self, config: IndexETFComparisonConfig) -> None:
        self.config = config
    def evaluate(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        mapping = data_payload.get("mapping")
        prices = data_payload.get("prices")
        etf_metadata = data_payload.get("etf_metadata")
        price_frames = data_payload.get("price_frames", {})
        if isinstance(mapping, str) or mapping is None:
            p = self.raw_data_dir / "mapping.parquet"
            if p.exists():
                mapping = pd.read_parquet(p)
            else:
                mapping = pd.read_csv(self.raw_data_dir / "mapping.csv")
        if isinstance(prices, str) or prices is None:
            p = self.raw_data_dir / "prices.parquet"
            if p.exists():
                prices = pd.read_parquet(p)
            else:
                prices = pd.read_csv(
                    self.raw_data_dir / "prices.csv", index_col=0, parse_dates=True
                )
        if isinstance(etf_metadata, str) or etf_metadata is None:
            p = self.raw_data_dir / "etf_metadata.parquet"
            if p.exists():
                etf_metadata = pd.read_parquet(p)
            else:
                etf_metadata = pd.read_csv(self.raw_data_dir / "etf_metadata.csv")
        if not price_frames and (self.raw_data_dir / "frames").exists():
            price_frames = {}
            for f in (self.raw_data_dir / "frames").glob("*.parquet"):
                price_frames[f.stem] = pd.read_parquet(f)
            if not price_frames:
                for f in (self.raw_data_dir / "frames").glob("*.csv"):
                    price_frames[f.stem] = pd.read_csv(f, index_col=0, parse_dates=True)
        index_results = {}
        for index_name in self.config.indices:
            tickers = mapping[mapping["index_name"] == index_name]["ticker"].tolist()
            if not tickers:
                continue
            available_tickers = [t for t in tickers if t in prices.columns]
            if not available_tickers:
                continue
            index_prices = prices[available_tickers].dropna(how="all")
            if index_prices.empty:
                continue
            metrics = []
            for ticker in available_tickers:
                if ticker not in index_prices.columns:
                    continue
                series = index_prices[ticker].dropna()
                if len(series) < self.config.min_data_points:
                    continue
                returns = series.pct_change().dropna()
                annual_return = (1 + returns.mean()) ** 252 - 1
                annual_volatility = returns.std() * np.sqrt(252)
                sharpe_ratio = (
                    annual_return / annual_volatility if annual_volatility > 0 else 0
                )
                if abs(annual_return) > 10 or abs(annual_volatility) > 10:
                    continue
                frame = price_frames.get(ticker)
                avg_volume = 0
                if frame is not None:
                    cols = {c.lower(): c for c in frame.columns}
                    if "volume" in cols:
                        avg_volume = frame[cols["volume"]].mean()
                metadata = etf_metadata[etf_metadata["ticker"] == ticker]
                name = (
                    metadata["name"].iloc[0]
                    if len(metadata) > 0 and "name" in metadata.columns
                    else ""
                )
                provider = (
                    metadata["provider"].iloc[0]
                    if len(metadata) > 0 and "provider" in metadata.columns
                    else ""
                )
                expense_ratio = (
                    metadata["expense_ratio"].iloc[0]
                    if len(metadata) > 0 and "expense_ratio" in metadata.columns
                    else None
                )
                metrics.append(
                    {
                        "ticker": ticker,
                        "name": name,
                        "provider": provider,
                        "expense_ratio": expense_ratio,
                        "annual_return": annual_return,
                        "annual_volatility": annual_volatility,
                        "sharpe_ratio": sharpe_ratio,
                        "avg_volume": avg_volume,
                        "data_points": len(series),
                    }
                )
            metrics_df = pd.DataFrame(metrics)
            if not metrics_df.empty:
                metrics_df = metrics_df.sort_values("sharpe_ratio", ascending=False)
            index_results[index_name] = {
                "metrics": metrics_df,
                "prices": index_prices,
            }
        return {
            "index_results": index_results,
            "mapping": mapping,
            "etf_metadata": etf_metadata,
        }
if __name__ == "__main__":
    import yaml
    from pathlib import Path
    from crew.etf.config import IndexETFComparisonConfig
    from crew.etf.reporting import IndexETFComparisonReporter
    from crew.utils.kronos_utils import get_kronos_forecast
    import datetime
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "etf.yaml"
    DATA_DIR = PROJECT_ROOT / "data" / "etf"
    today = datetime.date.today().strftime("%Y%m%d")
    REPORT_DIR = PROJECT_ROOT / "output" / "use_cases" / "etf" / today
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    if not config_data:
        config = IndexETFComparisonConfig(name="etf", indices=[], lookback="1y")
    else:
        config = IndexETFComparisonConfig(**config_data)
    analyzer = IndexETFComparisonAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR
    analysis_payload = {}
    results = analyzer.evaluate(analysis_payload)
    index_results = results["index_results"]
    for index_name, result in index_results.items():
        metrics = result["metrics"]
        if metrics.empty:
            continue
        top_tickers = metrics.head(3)["ticker"].tolist()
        forecasts = {}
        frames_dir = DATA_DIR / "frames"
        for ticker in top_tickers:
            p_path = frames_dir / f"{ticker}.parquet"
            c_path = frames_dir / f"{ticker}.csv"
            df = None
            if p_path.exists():
                df = pd.read_parquet(p_path)
            elif c_path.exists():
                df = pd.read_csv(c_path, index_col=0, parse_dates=True)
            if df is not None:
                try:
                    df.columns = [str(c).lower() for c in df.columns]
                    if "close" in df.columns and "open" not in df.columns:
                        df["open"] = df["close"]
                        df["high"] = df["close"]
                        df["low"] = df["close"]
                        df["volume"] = 0.0
                    if "date" not in df.columns:
                        df = df.reset_index()
                        if "index" in df.columns:
                            df["Date"] = df["index"]
                        elif "Date" in df.columns:
                            pass
                        else:
                            df["Date"] = df.iloc[:, 0]
                    else:
                        df["Date"] = df["date"]
                    df["Date"] = pd.to_datetime(df["Date"])
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
                        pred_df = get_kronos_forecast(
                            df=df,
                            x_timestamp=x_timestamp,
                            y_timestamp=y_timestamp,
                            pred_len=pred_len,
                        )
                        forecasts[ticker] = pred_df.to_dict(orient="records")
                except Exception as e:
                    print(f"Kronos forecast failed for {ticker}: {e}")
                    forecasts[ticker] = {"error": str(e)}
        if forecasts:
            result["forecasts"] = forecasts
    reporter = IndexETFComparisonReporter(config, DATA_DIR / "processed", REPORT_DIR)
    reporter.persist(results)
    print(f"Report produced in {REPORT_DIR}")
