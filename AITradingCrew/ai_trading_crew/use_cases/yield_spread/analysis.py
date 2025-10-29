from __future__ import annotations

from typing import Dict, List

import pandas as pd

from ai_trading_crew.use_cases.yield_spread.config import YieldSpreadConfig
from ai_trading_crew.use_cases.yield_spread.allocation import compute_allocation


class YieldSpreadAnalyzer:
    def __init__(self, config: YieldSpreadConfig) -> None:
        self.config = config

    def evaluate(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        series_frame = data_payload["series"]
        metrics = self._compute_pair_metrics(series_frame)
        edges = self._detect_edges(metrics)
        snapshot = self._build_snapshot(metrics)
        payload = {
            "series": series_frame,
            "metrics": metrics,
            "edges": edges,
            "snapshot": snapshot,
        }
        allocation = None
        if self.config.allocation is not None:
            allocation = compute_allocation(self.config.allocation, snapshot)
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
                bp_mask = pair_frame["spread_bp"].abs() >= self.config.bp_alert_threshold
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
