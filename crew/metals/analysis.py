from typing import Dict, List
import pandas as pd
from crew.metals.config import (
    ETFInstrument,
    PreciousMetalsSpreadConfig,
)
class PreciousMetalsSpreadAnalyzer:
    def __init__(self, config: PreciousMetalsSpreadConfig) -> None:
        self.config = config
    def evaluate(
        self, data_payload: Dict[str, pd.DataFrame] = None
    ) -> Dict[str, pd.DataFrame]:
        if not data_payload:
            data_payload = {}
            for name in ["etf", "metal", "fx"]:
                p = self.raw_data_dir / f"{name}.parquet"
                if p.exists():
                    df = pd.read_parquet(p)
                    if "Date" in df.columns:
                        df = df.set_index("Date")
                    elif "index" in df.columns:
                        df = df.set_index("index")
                    data_payload[name] = df
                else:
                    c = self.raw_data_dir / f"{name}.csv"
                    if c.exists():
                        data_payload[name] = pd.read_csv(
                            c, index_col=0, parse_dates=True
                        )
        aligned_frames = self._align_frames(data_payload)
        theoretical_prices = self._compute_theoretical_prices(
            aligned_frames, self.config.etf_instruments.values()
        )
        metrics = self._compute_metrics(aligned_frames["etf"], theoretical_prices)
        edges = self._detect_edges(metrics)
        return {
            "aligned": aligned_frames,
            "theoretical": theoretical_prices,
            "metrics": metrics,
            "edges": edges,
        }
    def _align_frames(
        self, data_payload: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
        etf_frame = data_payload["etf"]
        metal_frame = data_payload["metal"]
        fx_frame = data_payload["fx"]
        combined_index = etf_frame.index.union(metal_frame.index).union(fx_frame.index)
        etf_aligned = etf_frame.reindex(combined_index).ffill()
        metal_aligned = metal_frame.reindex(combined_index).ffill()
        fx_aligned = fx_frame.reindex(combined_index).ffill()
        return {
            "etf": etf_aligned,
            "metal": metal_aligned,
            "fx": fx_aligned,
        }
    def _compute_theoretical_prices(
        self, aligned_frames: Dict[str, pd.DataFrame], instruments: List[ETFInstrument]
    ) -> pd.DataFrame:
        fx_series = aligned_frames["fx"][self.config.fx_symbol]
        theoretical_series = {}
        for instrument in instruments:
            metal_series = aligned_frames["metal"][instrument.metal_symbol]
            price = (metal_series / 31.1034768) * instrument.grams_per_unit * fx_series
            theoretical_series[instrument.ticker] = price
        theoretical_frame = pd.DataFrame(theoretical_series)
        theoretical_frame = theoretical_frame.sort_index()
        return theoretical_frame
    def _compute_metrics(
        self, etf_frame: pd.DataFrame, theoretical_frame: pd.DataFrame
    ) -> pd.DataFrame:
        metrics_store: Dict[str, pd.DataFrame] = {}
        for ticker in theoretical_frame.columns:
            gap = etf_frame[ticker] - theoretical_frame[ticker]
            gap_pct = gap / theoretical_frame[ticker]
            rolling_mean = gap.rolling(
                window=self.config.rolling_window, min_periods=1
            ).mean()
            rolling_std = gap.rolling(
                window=self.config.rolling_window, min_periods=1
            ).std()
            z_score = (gap - rolling_mean) / rolling_std
            ticker_metrics = pd.DataFrame(
                {
                    "gap": gap,
                    "gap_pct": gap_pct,
                    "rolling_mean": rolling_mean,
                    "rolling_std": rolling_std,
                    "z_score": z_score,
                }
            )
            metrics_store[ticker] = ticker_metrics
        metrics_frame = pd.concat(metrics_store, axis=1)
        return metrics_frame
    def _detect_edges(self, metrics_frame: pd.DataFrame) -> pd.DataFrame:
        records = []
        for ticker in metrics_frame.columns.levels[0]:
            ticker_frame = metrics_frame[ticker]
            mask = ticker_frame["z_score"].abs() >= self.config.z_score_threshold
            filtered = ticker_frame.loc[mask]
            for timestamp, row in filtered.iterrows():
                direction = "positive" if row["z_score"] > 0 else "negative"
                records.append(
                    {
                        "date": timestamp,
                        "ticker": ticker,
                        "gap": row["gap"],
                        "gap_pct": row["gap_pct"],
                        "z_score": row["z_score"],
                        "direction": direction,
                    }
                )
        if len(records) == 0:
            return pd.DataFrame(
                columns=["date", "ticker", "gap", "gap_pct", "z_score", "direction"]
            )
        edges_frame = pd.DataFrame.from_records(records)
        edges_frame = edges_frame.sort_values("date")
        edges_frame = edges_frame.sort_values("date")
        return edges_frame
if __name__ == "__main__":
    import yaml
    from pathlib import Path
    import datetime
    from crew.metals.config import PreciousMetalsSpreadConfig
    from crew.metals.reporting import PreciousMetalsSpreadReporter
    from crew.utils.kronos_utils import get_kronos_forecast
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "metals.yaml"
    DATA_DIR = PROJECT_ROOT / "data" / "metals"
    today = datetime.date.today().strftime("%Y%m%d")
    REPORT_DIR = PROJECT_ROOT / "output" / "use_cases" / "metals" / today
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    config = PreciousMetalsSpreadConfig(**config_data)
    analyzer = PreciousMetalsSpreadAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR
    analysis_payload = {}
    results = analyzer.evaluate(analysis_payload)
    aligned = results["aligned"]
    etf_frame = aligned["etf"]
    forecasts = {}
    for ticker in etf_frame.columns:
        series = etf_frame[ticker].dropna()
        if len(series) > 30:
            df = series.to_frame(name="close")
            df["open"] = df["close"]
            df["high"] = df["close"]
            df["low"] = df["close"]
            df["volume"] = 0.0
            df = df.reset_index()
            df.columns = ["date", "close", "open", "high", "low", "volume"]
            df["Date"] = pd.to_datetime(df["date"])
            try:
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
    results["forecasts"] = forecasts
    reporter = PreciousMetalsSpreadReporter(config, DATA_DIR / "processed", REPORT_DIR)
    reporter.persist(results)
    print(f"Report produced in {REPORT_DIR}")
