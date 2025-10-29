from __future__ import annotations

from typing import Dict, Optional, Iterable

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.yield_spread.config import AllocationConfig, OptimizationConfig


def compute_allocation(
    allocation_config: AllocationConfig,
    snapshot: pd.DataFrame,
    asset_prices: pd.DataFrame | None = None,
) -> Dict[str, object] | None:
    if allocation_config is None or snapshot.empty:
        return None

    latest = snapshot.iloc[-1]
    z_score = float(latest.get("z_score", 0.0))
    spread_bp = float(latest.get("spread_bp", 0.0))

    if z_score >= allocation_config.upper_z:
        profile = allocation_config.widening
        regime = profile.label
    elif z_score <= allocation_config.lower_z:
        profile = allocation_config.tightening
        regime = profile.label
    else:
        profile = allocation_config.neutral
        regime = profile.label

    normalized_weights = _normalize_weights(profile.weights)
    payload: Dict[str, object] = {
        "regime": regime,
        "z_score": z_score,
        "spread_bp": spread_bp,
        "weights": normalized_weights,
        "method": "static",
    }

    opt_cfg = allocation_config.optimization
    if opt_cfg.enabled and asset_prices is not None:
        optimized = _optimize_weights(asset_prices, profile.weights.keys(), opt_cfg)
        if optimized is not None:
            payload["base_weights"] = normalized_weights
            payload["weights"] = optimized["weights"]
            payload["sharpe"] = optimized["sharpe"]
            payload["method"] = "optimized"
            payload["optimization_meta"] = {
                "lookback": opt_cfg.lookback,
                "sample_size": opt_cfg.sample_size,
                "risk_free_rate": opt_cfg.risk_free_rate,
            }

    return payload


def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return weights
    return {asset: round(weight / total, 4) for asset, weight in weights.items()}


def _optimize_weights(
    asset_prices: pd.DataFrame,
    tickers: Iterable[str],
    opt_cfg: OptimizationConfig,
) -> Dict[str, object] | None:
    tickers = [ticker for ticker in tickers if ticker in asset_prices.columns]
    if len(tickers) == 0:
        return None
    returns = asset_prices[tickers].pct_change().dropna()
    if returns.empty:
        return None
    cov = returns.cov() * 252.0
    mu = returns.mean() * 252.0
    if (cov.values == 0).all():
        return None

    rng = np.random.default_rng(42)
    best_sharpe = -np.inf
    best_weights: Optional[np.ndarray] = None
    cov_matrix = cov.to_numpy()
    mu_vector = mu.to_numpy()
    min_w = opt_cfg.min_weight
    max_w = opt_cfg.max_weight

    for _ in range(max(opt_cfg.sample_size, 1)):
        weights = rng.dirichlet(np.ones(len(tickers)))
        if np.any(weights < min_w) or np.any(weights > max_w):
            continue
        volatility = float(np.sqrt(weights @ cov_matrix @ weights))
        if volatility == 0:
            continue
        expected_return = float(weights @ mu_vector)
        sharpe = (expected_return - opt_cfg.risk_free_rate) / volatility
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = weights

    if best_weights is None or not np.isfinite(best_sharpe):
        return None

    weights_dict = {ticker: float(round(weight, 4)) for ticker, weight in zip(tickers, best_weights)}
    total = sum(weights_dict.values())
    if total != 0:
        weights_dict = {ticker: round(value / total, 4) for ticker, value in weights_dict.items()}
    return {
        "weights": weights_dict,
        "sharpe": float(round(best_sharpe, 4)),
    }
