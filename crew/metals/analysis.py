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
        self, data_payload: Dict[str, pd.DataFrame]
    ) -> Dict[str, pd.DataFrame]:
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
        return edges_frame
