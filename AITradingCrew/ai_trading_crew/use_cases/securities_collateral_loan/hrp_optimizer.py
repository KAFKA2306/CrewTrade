from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform


class HierarchicalRiskParity:
    def __init__(self, prices: pd.DataFrame, constraints: Dict[str, float]):
        self.prices = prices
        self.constraints = constraints
        self.returns = prices.pct_change().dropna()

    def optimize(self) -> pd.DataFrame:
        if len(self.prices.columns) < 3:
            return self._equal_weight_fallback()

        corr_matrix = self.returns.corr()
        dist_matrix = self._correlation_to_distance(corr_matrix)

        linkage = hierarchy.linkage(squareform(dist_matrix), method='single')

        sorted_idx = self._quasi_diag(linkage)
        sorted_tickers = [self.prices.columns[i] for i in sorted_idx]

        weights = self._recursive_bisection(sorted_tickers)

        weights_series = pd.Series(weights, index=sorted_tickers)

        weights_series = self._apply_constraints(weights_series)

        result_df = pd.DataFrame({
            'ticker': weights_series.index,
            'weight': weights_series.values,
        })

        return result_df

    def _correlation_to_distance(self, corr: pd.DataFrame) -> np.ndarray:
        dist = np.sqrt((1 - corr) / 2)
        np.fill_diagonal(dist.values, 0)
        return dist.values

    def _quasi_diag(self, linkage: np.ndarray) -> list:
        sorted_idx = hierarchy.leaves_list(linkage)
        return sorted_idx.tolist()

    def _recursive_bisection(self, tickers: list) -> Dict[str, float]:
        weights = pd.Series(1.0, index=tickers)
        clusters = [tickers]

        while len(clusters) > 0:
            clusters = [
                cluster[start:end]
                for cluster in clusters
                for start, end in [(0, len(cluster) // 2), (len(cluster) // 2, len(cluster))]
                if len(cluster) > 1
            ]

            for i in range(0, len(clusters), 2):
                if i + 1 < len(clusters):
                    cluster1 = clusters[i]
                    cluster2 = clusters[i + 1]

                    var1 = self._cluster_variance(cluster1)
                    var2 = self._cluster_variance(cluster2)

                    alpha = 1 - var1 / (var1 + var2)

                    weights[cluster1] *= alpha
                    weights[cluster2] *= (1 - alpha)

        return weights.to_dict()

    def _cluster_variance(self, tickers: list) -> float:
        if len(tickers) == 0:
            return 0.0

        cluster_returns = self.returns[tickers]
        cov_matrix = cluster_returns.cov()

        if len(tickers) == 1:
            return float(cov_matrix.iloc[0, 0])

        equal_weights = np.ones(len(tickers)) / len(tickers)
        portfolio_variance = equal_weights @ cov_matrix @ equal_weights

        return float(portfolio_variance)

    def _apply_constraints(self, weights: pd.Series) -> pd.Series:
        min_weight = self.constraints.get('min_weight', 0.0)
        max_weight = self.constraints.get('max_weight', 1.0)

        weights = weights.clip(lower=min_weight, upper=max_weight)

        weights = weights / weights.sum()

        return weights

    def _equal_weight_fallback(self) -> pd.DataFrame:
        n = len(self.prices.columns)
        equal_w = 1.0 / n

        result_df = pd.DataFrame({
            'ticker': self.prices.columns.tolist(),
            'weight': [equal_w] * n,
        })

        return result_df
