from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.index_etf_comparison.config import IndexETFComparisonConfig


class IndexETFComparisonAnalyzer:
    def __init__(self, config: IndexETFComparisonConfig) -> None:
        self.config = config

    def evaluate(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        mapping = data_payload["mapping"]
        prices = data_payload["prices"]
        etf_metadata = data_payload["etf_metadata"]
        price_frames = data_payload["price_frames"]

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
                sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0

                frame = price_frames.get(ticker)
                avg_volume = 0
                if frame is not None and "Volume" in frame.columns:
                    avg_volume = frame["Volume"].mean()

                metadata = etf_metadata[etf_metadata["ticker"] == ticker]
                name = metadata["name"].iloc[0] if len(metadata) > 0 and "name" in metadata.columns else ""
                provider = metadata["provider"].iloc[0] if len(metadata) > 0 and "provider" in metadata.columns else ""
                expense_ratio = metadata["expense_ratio"].iloc[0] if len(metadata) > 0 and "expense_ratio" in metadata.columns else None

                metrics.append({
                    "ticker": ticker,
                    "name": name,
                    "provider": provider,
                    "expense_ratio": expense_ratio,
                    "annual_return": annual_return,
                    "annual_volatility": annual_volatility,
                    "sharpe_ratio": sharpe_ratio,
                    "avg_volume": avg_volume,
                    "data_points": len(series),
                })

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
