from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.credit_spread.config import CreditSpreadConfig


class CreditSpreadAnalyzer:
    def __init__(self, config: CreditSpreadConfig) -> None:
        self.config = config

    def evaluate(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
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
                direction = "spread_widening" if row["z_score"] > 0 else "spread_tightening"
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
            return pd.DataFrame(columns=["date", "pair", "junk", "treasury", "z_score", "ratio", "return_gap", "signal", "description"])
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
            return pd.DataFrame(columns=["pair", "junk", "treasury", "latest_date", "z_score", "ratio", "return_gap"])
        return pd.DataFrame(snapshot_rows)
