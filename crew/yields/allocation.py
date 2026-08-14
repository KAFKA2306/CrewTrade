from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from crew.yields.config import AllocationConfig, OptimizationConfig


def build_allocation_recommendation(
    allocation_config: AllocationConfig | None,
    snapshot: pd.DataFrame,
    asset_prices: pd.DataFrame | None = None,
) -> dict[str, object] | None:
    if allocation_config is None or snapshot.empty:
        return None
    latest = snapshot.iloc[-1]
    z_score = float(latest.get("z_score", 0.0))
    profile = allocation_config.neutral
    regime = "neutral"
    if z_score >= allocation_config.z_score_threshold:
        profile = allocation_config.steepener
        regime = "steepener"
    elif z_score <= -allocation_config.z_score_threshold:
        profile = allocation_config.flattener
        regime = "flattener"
    else:
        regime = profile.label
    normalized_weights = _normalize_weights(profile.weights)
    payload: dict[str, object] = {
        "regime": regime,
        "z_score": z_score,
        "weights": normalized_weights,
    }
    if asset_prices is None or asset_prices.empty:
        return payload

    returns = asset_prices.pct_change().dropna(how="all")
    if returns.empty:
        return payload
    filtered_weights = _filter_and_normalize_weights(normalized_weights, returns.columns)
    if not filtered_weights:
        return payload
    performance = _compute_performance_metrics(
        returns, filtered_weights, allocation_config.optimization.risk_free_rate
    )
    if performance is not None:
        payload["performance"] = performance

    optimization = _optimize_weights(returns, allocation_config.optimization)
    if optimization is not None:
        optimized_weights = optimization["weights"]
        if isinstance(optimized_weights, dict):
            payload["optimized_weights"] = optimized_weights
            payload["blended_weights"] = _merge_weights(normalized_weights, optimized_weights)
        payload["optimization"] = optimization
    return payload


def _normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return {}
    return {ticker: round(weight / total, 4) for ticker, weight in weights.items()}


def _filter_and_normalize_weights(
    weights: dict[str, float], columns: Iterable[str]
) -> dict[str, float]:
    filtered = {
        ticker: weight for ticker, weight in weights.items() if ticker in columns and weight > 0
    }
    return _normalize_weights(filtered)


def _merge_weights(
    base_weights: dict[str, float], optimized_weights: dict[str, float]
) -> dict[str, float]:
    merged = {}
    for ticker in base_weights.keys():
        base = base_weights.get(ticker, 0.0)
        optimized = optimized_weights.get(ticker, base)
        merged[ticker] = 0.5 * base + 0.5 * optimized
    return _normalize_weights(merged)


def _optimize_weights(
    returns: pd.DataFrame,
    opt_cfg: OptimizationConfig,
) -> dict[str, object] | None:
    tickers = list(returns.columns)
    if len(tickers) == 0:
        return None
    covariance = returns.cov() * 252.0
    expected_returns = returns.mean() * 252.0
    optimization = _random_search(
        tickers,
        covariance,
        expected_returns,
        opt_cfg,
        opt_cfg.samples,
        opt_cfg.seed,
    )
    if optimization is None:
        return None
    return {
        **optimization,
        "method": "random_search",
        "samples": opt_cfg.samples,
        "seed": opt_cfg.seed,
    }


def _random_search(
    tickers: list[str],
    cov: pd.DataFrame,
    mu: pd.Series,
    opt_cfg: OptimizationConfig,
    sample_size: int,
    seed: int,
) -> dict[str, object] | None:
    if sample_size <= 0:
        return None
    if len(tickers) != len(mu) or cov.shape != (len(tickers), len(tickers)):
        return None
    rng = np.random.default_rng(seed)
    best_sharpe = -np.inf
    best_weights: np.ndarray | None = None
    cov_matrix = cov.to_numpy()
    mu_vector = mu.to_numpy()
    for _ in range(sample_size):
        weights = rng.dirichlet(np.ones(len(tickers)))
        volatility = float(np.sqrt(weights.T @ cov_matrix @ weights))
        if volatility == 0:
            continue
        expected_return = float(weights @ mu_vector)
        sharpe = (expected_return - opt_cfg.risk_free_rate) / volatility
        if not np.isfinite(sharpe):
            continue
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = weights
    if best_weights is None or best_sharpe == -np.inf:
        return None
    weights_dict = {
        ticker: float(weight) for ticker, weight in zip(tickers, best_weights, strict=True)
    }
    total = sum(weights_dict.values())
    if total <= 0:
        return None
    weights_dict = {ticker: round(weight / total, 4) for ticker, weight in weights_dict.items()}
    return {
        "weights": weights_dict,
        "sharpe": float(round(best_sharpe, 4)),
    }


def _compute_performance_metrics(
    returns: pd.DataFrame,
    weights: dict[str, float],
    risk_free_rate: float,
) -> dict[str, float] | None:
    tickers = [
        ticker for ticker, weight in weights.items() if weight > 0 and ticker in returns.columns
    ]
    if not tickers:
        return None
    weight_vector = np.array([weights[ticker] for ticker in tickers])
    frame = returns[tickers].dropna(how="any")
    if frame.empty:
        return None
    portfolio_returns = frame.to_numpy() @ weight_vector
    annual_return = float(np.mean(portfolio_returns) * 252.0)
    annual_volatility = float(np.std(portfolio_returns, ddof=1) * np.sqrt(252.0))
    sharpe = (annual_return - risk_free_rate) / annual_volatility if annual_volatility > 0 else 0.0
    return {
        "annual_return": round(annual_return, 4),
        "annual_volatility": round(annual_volatility, 4),
        "sharpe": round(float(sharpe), 4),
    }
