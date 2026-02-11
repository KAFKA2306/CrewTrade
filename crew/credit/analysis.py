from __future__ import annotations
from typing import Dict, List
import numpy as np
import pandas as pd
from crew.credit.config import CreditSpreadConfig
class CreditSpreadAnalyzer:
    def __init__(self, config: CreditSpreadConfig) -> None:
        self.config = config
    def evaluate(
        self, data_payload: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
        price_frame = data_payload["prices"]
        metrics = self._compute_pair_metrics(price_frame)
        edges = self._detect_edges(metrics)
        snapshot = self._build_snapshot(metrics)
        return {
            "prices": price_frame,
            "metrics": metrics,
            "edges": edges,
            "snapshot": snapshot,
        }
    def _compute_pair_metrics(self, price_frame: pd.DataFrame) -> pd.DataFrame:
        metrics_store: Dict[str, pd.DataFrame] = {}
        returns = price_frame.pct_change()
        for label, pair in self.config.pairs.items():
            junk = price_frame[pair.junk_ticker]
            treasury = price_frame[pair.treasury_ticker]
            ratio = junk / treasury
            log_ratio = np.log(ratio)
            rolling_mean = log_ratio.rolling(
                window=self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).mean()
            rolling_std = log_ratio.rolling(
                window=self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).std()
            rolling_std = rolling_std.replace(0, np.nan)
            z_score = (log_ratio - rolling_mean) / rolling_std
            return_gap = returns[pair.junk_ticker] - returns[pair.treasury_ticker]
            metrics_store[label] = pd.DataFrame(
                {
                    "ratio": ratio,
                    "log_ratio": log_ratio,
                    "return_gap": return_gap,
                    "rolling_mean": rolling_mean,
                    "rolling_std": rolling_std,
                    "z_score": z_score,
                }
            )
        metrics_frame = pd.concat(metrics_store, axis=1)
        return metrics_frame
    def _detect_edges(self, metrics_frame: pd.DataFrame) -> pd.DataFrame:
        records: List[Dict[str, object]] = []
        for label, pair in self.config.pairs.items():
            pair_frame = metrics_frame[label].dropna(subset=["z_score"])
            if pair_frame.empty:
                continue
            mask = pair_frame["z_score"].abs() >= self.config.z_score_threshold
            filtered = pair_frame.loc[mask]
            if filtered.empty:
                continue
            for timestamp, row in filtered.iterrows():
                direction = (
                    "spread_widening" if row["z_score"] > 0 else "spread_tightening"
                )
                records.append(
                    {
                        "date": timestamp,
                        "pair": label,
                        "junk": pair.junk_ticker,
                        "treasury": pair.treasury_ticker,
                        "z_score": row["z_score"],
                        "ratio": row["ratio"],
                        "return_gap": row["return_gap"],
                        "signal": direction,
                        "description": pair.description or "",
                    }
                )
        if not records:
            return pd.DataFrame(
                columns=[
                    "date",
                    "pair",
                    "junk",
                    "treasury",
                    "z_score",
                    "ratio",
                    "return_gap",
                    "signal",
                    "description",
                ]
            )
        edges_frame = pd.DataFrame.from_records(records)
        edges_frame = edges_frame.sort_values("date")
        return edges_frame
    def _build_snapshot(self, metrics_frame: pd.DataFrame) -> pd.DataFrame:
        snapshot_rows: List[Dict[str, object]] = []
        for label, pair in self.config.pairs.items():
            pair_frame = metrics_frame[label].dropna(subset=["z_score"])
            if pair_frame.empty:
                continue
            last_row = pair_frame.iloc[-1]
            snapshot_rows.append(
                {
                    "pair": label,
                    "junk": pair.junk_ticker,
                    "treasury": pair.treasury_ticker,
                    "latest_date": pair_frame.index[-1],
                    "z_score": last_row["z_score"],
                    "ratio": last_row["ratio"],
                    "return_gap": last_row["return_gap"],
                }
            )
        if not snapshot_rows:
            return pd.DataFrame(
                columns=[
                    "pair",
                    "junk",
                    "treasury",
                    "latest_date",
                    "z_score",
                    "ratio",
                    "return_gap",
                ]
            )
        return pd.DataFrame(snapshot_rows)
if __name__ == "__main__":
    import yaml
    from pathlib import Path
    from crew.credit.config import CreditSpreadConfig
    from crew.credit.reporting import CreditSpreadReporter
    from crew.utils.kronos_utils import get_kronos_forecast
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "credit.yaml"
    DATA_DIR = PROJECT_ROOT / "data" / "credit_spread"
    import datetime
    today = datetime.date.today().strftime("%Y%m%d")
    REPORT_DIR = PROJECT_ROOT / "output" / "use_cases" / "credit" / today
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    config = CreditSpreadConfig(**config_data)
    prices_path = DATA_DIR / "prices.parquet"
    if not prices_path.exists():
        print(f"Warning: {prices_path} not found. Trying CSV fallback.")
        prices_path = DATA_DIR / "prices.csv"
    if str(prices_path).endswith(".parquet") and prices_path.exists():
        prices = pd.read_parquet(prices_path)
    elif prices_path.exists():
        prices = pd.read_csv(prices_path, parse_dates=["Date"])
    else:
        print("Error: No price data found.")
        exit(1)
    data_payload = {"prices": prices.set_index("Date")}
    analyzer = CreditSpreadAnalyzer(config)
    analysis_results = analyzer.evaluate(data_payload)
    forecasts = {}
    for ticker in config.tickers:
        ticker_path = DATA_DIR / f"{ticker}.parquet"
        if ticker_path.exists():
            try:
                df = pd.read_parquet(ticker_path)
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
                    df["Date"] = pd.to_datetime(
                        df["Date"] if "Date" in df.columns else df["date"]
                    )
                if "Date" in df.columns:
                    df = df.sort_values("Date").reset_index(drop=True)
                    x_timestamp = df["Date"]
                    pred_len = 30
                    last_date = df["Date"].iloc[-1]
                    future_dates = [
                        last_date + pd.Timedelta(days=i + 1) for i in range(pred_len)
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
    analysis_results["forecasts"] = forecasts
    reporter = CreditSpreadReporter(config, DATA_DIR / "processed", REPORT_DIR)
    reporter.persist(analysis_results)
    print(f"Report produced in {REPORT_DIR}")
