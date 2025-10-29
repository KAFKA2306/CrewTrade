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

    available_returns: pd.DataFrame | None = None
    available_tickers: Iterable[str] = []
    if asset_prices is not None and not asset_prices.empty:
        available_tickers = [ticker for ticker in normalized_weights if ticker in asset_prices.columns]
        if len(available_tickers) > 0:
            available_returns = asset_prices[list(available_tickers)].pct_change().dropna()

    opt_cfg = allocation_config.optimization

    if available_returns is not None and not available_returns.empty:
        base_weights = _filter_and_normalize_weights(normalized_weights, available_returns.columns)
        if base_weights:
            base_metrics = _compute_performance_metrics(available_returns, base_weights, opt_cfg.risk_free_rate)
            if base_metrics is not None:
                payload["base_metrics"] = base_metrics

    if opt_cfg.enabled and available_returns is not None and not available_returns.empty:
        optimized = _optimize_weights(available_returns, opt_cfg)
        if optimized is not None:
            payload["base_weights"] = normalized_weights
            payload["weights"] = _merge_weights(normalized_weights, optimized["weights"])
            payload["method"] = "optimized"
            payload["sharpe"] = optimized["metrics"].get("sharpe")
            payload["metrics"] = optimized["metrics"]
            payload["optimization_meta"] = optimized["meta"]
            sensitivity = optimized.get("sensitivity")
            if sensitivity:
                payload["sensitivity"] = sensitivity

    return payload


def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return weights
    return {asset: round(weight / total, 4) for asset, weight in weights.items()}


def _filter_and_normalize_weights(weights: Dict[str, float], columns: Iterable[str]) -> Dict[str, float]:
    filtered = {ticker: weight for ticker, weight in weights.items() if ticker in columns and weight > 0}
    total = sum(filtered.values())
    if total <= 0:
        return {}
    return {ticker: round(weight / total, 4) for ticker, weight in filtered.items()}


def _merge_weights(base_weights: Dict[str, float], optimized_weights: Dict[str, float]) -> Dict[str, float]:
    merged = {}
    for ticker in base_weights.keys():
        merged[ticker] = round(optimized_weights.get(ticker, 0.0), 4)
    total = sum(merged.values())
    if total > 0:
        merged = {ticker: round(weight / total, 4) for ticker, weight in merged.items()}
    return merged


def _optimize_weights(
    returns: pd.DataFrame,
    opt_cfg: OptimizationConfig,
) -> Dict[str, object] | None:
    tickers = list(returns.columns)
    if len(tickers) == 0:
        return None

    primary_result = _run_random_search(returns, tickers, opt_cfg.sample_size, opt_cfg, seed=42)
    if primary_result is None:
        return None

    metrics = _compute_performance_metrics(returns, primary_result["weights"], opt_cfg.risk_free_rate)
    if metrics is None:
        return None

    sensitivity_results = []
    for sample_size in opt_cfg.sensitivity_sample_sizes:
        if sample_size == opt_cfg.sample_size:
            continue
        sensitivity = _run_random_search(returns, tickers, sample_size, opt_cfg, seed=42 + sample_size)
        if sensitivity is None:
            continue
        sensitivity_metrics = _compute_performance_metrics(returns, sensitivity["weights"], opt_cfg.risk_free_rate)
        if sensitivity_metrics is None:
            continue
        sensitivity_results.append(
            {
                "sample_size": sample_size,
                "sharpe": sensitivity_metrics.get("sharpe"),
                "annual_return": sensitivity_metrics.get("annual_return"),
                "annual_volatility": sensitivity_metrics.get("annual_volatility"),
            }
        )

    return {
        "weights": primary_result["weights"],
        "metrics": metrics,
        "meta": {
            "lookback": opt_cfg.lookback,
            "sample_size": opt_cfg.sample_size,
            "risk_free_rate": opt_cfg.risk_free_rate,
        },
        "sensitivity": sensitivity_results,
    }


def _run_random_search(
    returns: pd.DataFrame,
    tickers: list[str],
    sample_size: int,
    opt_cfg: OptimizationConfig,
    seed: int,
) -> Dict[str, object] | None:
    if sample_size <= 0:
        return None
    cov = returns.cov() * 252.0
    mu = returns.mean() * 252.0
    if (cov.values == 0).all():
        return None

    rng = np.random.default_rng(seed)
    best_sharpe = -np.inf
    best_weights: Optional[np.ndarray] = None
    cov_matrix = cov.to_numpy()
    mu_vector = mu.to_numpy()
    min_w = opt_cfg.min_weight
    max_w = opt_cfg.max_weight

    for _ in range(sample_size):
        weights = rng.dirichlet(np.ones(len(tickers)))
        if np.any(weights < min_w) or np.any(weights > max_w):
            continue
        volatility = float(np.sqrt(weights @ cov_matrix @ weights))
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

    weights_dict = {ticker: float(weight) for ticker, weight in zip(tickers, best_weights)}
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
    weights: Dict[str, float],
    risk_free_rate: float,
) -> Dict[str, float] | None:
    tickers = [ticker for ticker, weight in weights.items() if weight > 0 and ticker in returns.columns]
    if not tickers:
        return None
    filtered_returns = returns[tickers]
    if filtered_returns.empty:
        return None
    weight_vector = np.array([weights[t] for t in tickers])
    weight_vector = weight_vector / weight_vector.sum()
    portfolio_returns = filtered_returns.to_numpy() @ weight_vector
    series = pd.Series(portfolio_returns, index=filtered_returns.index)
    if series.empty:
        return None
    cumulative = (1 + series).cumprod()
    total_return = float(cumulative.iloc[-1] - 1)
    periods = len(series)
    if periods == 0:
        return None
    annual_return = float((1 + total_return) ** (252 / periods) - 1)
    annual_volatility = float(series.std() * np.sqrt(252))
    sharpe = None
    if annual_volatility > 0:
        sharpe = float((annual_return - risk_free_rate) / annual_volatility)
    drawdown = cumulative / cumulative.cummax() - 1
    max_drawdown = float(drawdown.min())
    return {
        "total_return": round(total_return, 4),
        "annual_return": round(annual_return, 4),
        "annual_volatility": round(annual_volatility, 4),
        "sharpe": round(sharpe, 4) if sharpe is not None and np.isfinite(sharpe) else None,
        "max_drawdown": round(max_drawdown, 4),
    }
