from __future__ import annotations

from typing import Dict, List

import pandas as pd

from crew.yields.allocation import compute_allocation
from crew.yields.config import YieldSpreadConfig


class YieldSpreadAnalyzer:
    def __init__(self, config: YieldSpreadConfig) -> None:
        self.config = config

    def evaluate(
        self, data_payload: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
        # Load from disk if needed
        if "series" not in data_payload or isinstance(data_payload.get("series"), str):
            p = self.raw_data_dir / "series.parquet"
            if p.exists():
                data_payload["series"] = pd.read_parquet(p)
            else:
                series_path = self.raw_data_dir / "series.csv"
                if series_path.exists():
                    data_payload["series"] = pd.read_csv(
                        series_path, index_col=0, parse_dates=True
                    )
                else:
                    data_payload["series"] = pd.DataFrame()

        if "asset_prices" not in data_payload or isinstance(
            data_payload.get("asset_prices"), str
        ):
            p = self.raw_data_dir / "asset_prices.parquet"
            if p.exists():
                data_payload["asset_prices"] = pd.read_parquet(p)
            else:
                prices_path = self.raw_data_dir / "asset_prices.csv"
                if prices_path.exists():
                    data_payload["asset_prices"] = pd.read_csv(
                        prices_path, index_col=0, parse_dates=True
                    )

        series_frame = data_payload["series"]
        asset_prices = data_payload.get("asset_prices")
        metrics = self._compute_pair_metrics(series_frame)
        edges = self._detect_edges(metrics)
        snapshot = self._build_snapshot(metrics)
        payload = {
            "series": series_frame,
            "metrics": metrics,
            "edges": edges,
            "snapshot": snapshot,
        }
        if asset_prices is not None:
            payload["asset_prices"] = asset_prices
        allocation = None
        if self.config.allocation is not None:
            allocation = compute_allocation(
                self.config.allocation, snapshot, asset_prices
            )
        if allocation is not None:
            payload["allocation"] = allocation
        return payload

    def _compute_pair_metrics(self, series_frame: pd.DataFrame) -> pd.DataFrame:
        metrics_store: Dict[str, pd.DataFrame] = {}
        for label, pair in self.config.pairs.items():
            junk_series = series_frame[pair.junk.identifier]
            treasury_series = series_frame[pair.treasury.identifier]
            spread = junk_series - treasury_series
            spread_bp = spread * 100
            rolling_mean = spread.rolling(
                window=self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).mean()
            rolling_std = spread.rolling(
                window=self.config.rolling_window,
                min_periods=self.config.minimum_periods,
            ).std()
            rolling_std = rolling_std.replace(0, pd.NA)
            z_score = (spread - rolling_mean) / rolling_std
            metrics_store[label] = pd.DataFrame(
                {
                    "junk_yield": junk_series,
                    "treasury_yield": treasury_series,
                    "spread": spread,
                    "spread_bp": spread_bp,
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
            z_mask = pair_frame["z_score"].abs() >= self.config.z_score_threshold
            if self.config.bp_alert_threshold > 0:
                bp_mask = (
                    pair_frame["spread_bp"].abs() >= self.config.bp_alert_threshold
                )
                mask = z_mask & bp_mask
            else:
                mask = z_mask
            filtered = pair_frame.loc[mask]
            for timestamp, row in filtered.iterrows():
                direction = "widening" if row["z_score"] >= 0 else "tightening"
                records.append(
                    {
                        "date": timestamp,
                        "pair": label,
                        "junk_identifier": pair.junk.identifier,
                        "treasury_identifier": pair.treasury.identifier,
                        "spread_bp": row["spread_bp"],
                        "spread": row["spread"],
                        "z_score": row["z_score"],
                        "junk_yield": row["junk_yield"],
                        "treasury_yield": row["treasury_yield"],
                        "direction": direction,
                        "description": pair.description or "",
                    }
                )
        if not records:
            return pd.DataFrame(
                columns=[
                    "date",
                    "pair",
                    "junk_identifier",
                    "treasury_identifier",
                    "spread_bp",
                    "spread",
                    "z_score",
                    "junk_yield",
                    "treasury_yield",
                    "direction",
                    "description",
                ]
            )
        edges_frame = pd.DataFrame.from_records(records)
        edges_frame = edges_frame.sort_values("date")
        return edges_frame

    def _build_snapshot(self, metrics_frame: pd.DataFrame) -> pd.DataFrame:
        rows: List[Dict[str, object]] = []
        for label, pair in self.config.pairs.items():
            pair_frame = metrics_frame[label].dropna(subset=["spread"])
            if pair_frame.empty:
                continue
            last_row = pair_frame.iloc[-1]
            rows.append(
                {
                    "pair": label,
                    "latest_date": pair_frame.index[-1],
                    "spread_bp": last_row["spread_bp"],
                    "spread": last_row["spread"],
                    "z_score": last_row["z_score"],
                    "junk_yield": last_row["junk_yield"],
                    "treasury_yield": last_row["treasury_yield"],
                }
            )
        if not rows:
            return pd.DataFrame(
                columns=[
                    "pair",
                    "latest_date",
                    "spread_bp",
                    "spread",
                    "z_score",
                    "junk_yield",
                    "treasury_yield",
                ]
            )
        return pd.DataFrame(rows)


if __name__ == "__main__":
    import yaml
    from pathlib import Path
    import datetime
    from crew.yields.config import YieldSpreadConfig
    from crew.yields.reporting import YieldSpreadReporter
    from crew.utils.kronos_utils import get_kronos_forecast

    # Setup paths
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "yields.yaml"
    DATA_DIR = PROJECT_ROOT / "data" / "yields"

    today = datetime.date.today().strftime("%Y%m%d")
    REPORT_DIR = PROJECT_ROOT / "output" / "use_cases" / "yields" / today

    # Load config
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    config = YieldSpreadConfig(**config_data)

    # Analyze
    analyzer = YieldSpreadAnalyzer(config)
    analyzer.raw_data_dir = DATA_DIR

    # Empty payload -> load from disk
    analysis_payload = {}
    results = analyzer.evaluate(analysis_payload)

    # Kronos Integration
    # Forecast spreads
    forecasts = {}
    metrics = results.get("metrics")
    if isinstance(metrics, pd.DataFrame):
        # MultiIndex columns: (pair, metric)
        pairs = metrics.columns.levels[0]
        for pair in pairs:
            # Get spread series
            spread_series = metrics[pair]["spread"].dropna()

            if len(spread_series) > 30:
                # Create DF for Kronos
                df = spread_series.to_frame(name="close")
                df["open"] = df["close"]
                df["high"] = df["close"]
                df["low"] = df["close"]
                df["volume"] = 0.0
                df = df.reset_index()
                # Index handling
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
                    forecasts[pair] = pred_df.to_dict(orient="records")
                except Exception as e:
                    print(f"Kronos forecast failed for {pair}: {e}")
                    forecasts[pair] = {"error": str(e)}

    results["forecasts"] = forecasts

    # Report
    reporter = YieldSpreadReporter(config, DATA_DIR / "processed", REPORT_DIR)
    reporter.persist(results)
    print(f"Report produced in {REPORT_DIR}")
