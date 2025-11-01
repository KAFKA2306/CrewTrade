from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.securities_collateral_loan.hrp_optimizer import HierarchicalRiskParity


def _weighted_metric_score(metrics: Dict[str, float], objective_weights: Dict[str, float]) -> float:
    active: List[Tuple[float, float]] = []
    for key, weight in objective_weights.items():
        if key in metrics:
            active.append((weight, metrics[key]))
    if not active:
        return 0.0
    weights = np.array([item[0] for item in active], dtype=float)
    total = weights.sum()
    if total == 0:
        weights = np.full_like(weights, 1 / len(weights), dtype=float)
    else:
        weights = weights / total
    values = np.array([item[1] for item in active], dtype=float)
    return float(values @ weights)


def _portfolio_expense(
    weights: np.ndarray,
    tickers: List[str],
    expense_lookup: Dict[str, float],
    default_expense: float,
) -> Optional[float]:
    if not expense_lookup:
        return None
    expense_values: List[float] = []
    for ticker, weight in zip(tickers, weights):
        if weight <= 0:
            continue
        expense = expense_lookup.get(ticker, default_expense)
        if np.isnan(expense):
            expense = default_expense
        expense_values.append(weight * float(expense))
    if not expense_values:
        return None
    return float(sum(expense_values))


def _priority_score_bonus(
    weights: np.ndarray,
    tickers: List[str],
    priority_indices: Optional[Dict[str, List[str]]],
) -> float:
    if not priority_indices:
        return 0.0

    tier1 = set(priority_indices.get("tier1", []))
    tier2 = set(priority_indices.get("tier2", []))
    tier3 = set(priority_indices.get("tier3", []))

    bonus = 0.0
    tier1_weight = 0.0

    for ticker, weight in zip(tickers, weights):
        if weight <= 1e-4:
            continue
        if ticker in tier1:
            tier1_weight += weight
            bonus += weight * 2.0
        elif ticker in tier2:
            bonus += weight * 1.0
        elif ticker in tier3:
            bonus += weight * 0.3

    if tier1 and tier1_weight < 0.15:
        bonus -= 5.0

    return bonus


def optimize_collateral_portfolio(
    prices: pd.DataFrame,
    etf_master: pd.DataFrame,
    objective_weights: Dict[str, float],
    constraints: Dict[str, float],
    sample_size: int,
    target_value: float = 10_000_000,
    max_assets: Optional[int] = None,
    min_assets: int = 3,
    score_strategy: Optional[str] = None,
    use_hrp: bool = False,
    priority_indices: Optional[Dict[str, List[str]]] = None,
) -> Dict:
    returns = prices.pct_change().dropna()
    tickers = list(prices.columns)
    n_assets = len(tickers)

    if n_assets < 3:
        raise ValueError(f"At least 3 ETFs required for optimization, got {n_assets}")

    min_weight = constraints.get("min_weight", 0.0)
    max_weight = constraints.get("max_weight", 1.0)
    max_volatility = constraints.get("max_volatility", float("inf"))
    max_category_weight = constraints.get("max_category_weight")

    cov_matrix = returns.cov() * 252
    annual_returns = returns.mean() * 252

    category_lookup = etf_master.set_index("ticker")["category"].to_dict() if not etf_master.empty else {}
    expense_lookup = etf_master.set_index("ticker")["expense_ratio"].to_dict() if not etf_master.empty else {}
    expense_values_all = [
        float(value)
        for value in expense_lookup.values()
        if value is not None and not np.isnan(value)
    ]
    default_expense = float(np.mean(expense_values_all)) if expense_values_all else 0.0

    subset_capacity = n_assets
    if max_assets is not None:
        subset_capacity = min(subset_capacity, max_assets)
    if min_weight > 0:
        subset_capacity = min(subset_capacity, int(1.0 / min_weight))
    subset_capacity = max(subset_capacity, min_assets)

    best_portfolio = None
    best_score = -np.inf

    if use_hrp:
        hrp = HierarchicalRiskParity(prices, constraints)
        hrp_result = hrp.optimize()

        hrp_weights = np.zeros(n_assets)
        for _, row in hrp_result.iterrows():
            ticker = row['ticker']
            weight = row['weight']
            if ticker in tickers:
                idx = tickers.index(ticker)
                hrp_weights[idx] = weight

        if max_assets is not None and np.sum(hrp_weights > 1e-4) > max_assets:
            top_indices = np.argsort(hrp_weights)[-max_assets:]
            filtered_weights = np.zeros(n_assets)
            filtered_weights[top_indices] = hrp_weights[top_indices]
            filtered_weights = filtered_weights / filtered_weights.sum()
            hrp_weights = filtered_weights

        portfolio_return = float(np.dot(annual_returns.values, hrp_weights))
        portfolio_volatility = float(np.sqrt(np.dot(hrp_weights, cov_matrix @ hrp_weights)))

        if portfolio_volatility <= max_volatility and portfolio_volatility > 0:
            sharpe = portfolio_return / portfolio_volatility
            best_portfolio = hrp_weights
            best_score = sharpe

    if best_portfolio is None:
        for _ in range(sample_size):
            if subset_capacity < n_assets:
                subset_size = np.random.randint(min_assets, subset_capacity + 1)
                subset_indices = np.random.choice(n_assets, size=subset_size, replace=False)
            else:
                subset_indices = np.arange(n_assets)
            candidate_weights = np.random.dirichlet(np.ones(len(subset_indices)))

            if min_weight > 0 and np.any(candidate_weights < min_weight):
                continue
            if np.any(candidate_weights > max_weight):
                continue

            weights = np.zeros(n_assets)
            weights[subset_indices] = candidate_weights

            if max_category_weight is not None and category_lookup:
                category_weights: Dict[str, float] = {}
                for idx, weight in zip(subset_indices, candidate_weights):
                    ticker = tickers[idx]
                    category = category_lookup.get(ticker, "その他")
                    category_weights[category] = category_weights.get(category, 0.0) + weight
                if any(weight > max_category_weight for weight in category_weights.values()):
                    continue

            portfolio_return = float(np.dot(annual_returns.values, weights))
            portfolio_volatility = float(np.sqrt(np.dot(weights, cov_matrix @ weights)))

            if portfolio_volatility > max_volatility or portfolio_volatility == 0:
                continue

            sharpe = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0

            candidate_expense = _portfolio_expense(weights, tickers, expense_lookup, default_expense)

            if score_strategy:
                strategy = score_strategy.lower()
                if strategy == "min_variance":
                    score = -portfolio_volatility
                elif strategy == "max_sharpe":
                    score = sharpe
                elif strategy == "max_kelly":
                    if portfolio_volatility > 0:
                        score = portfolio_return / (portfolio_volatility ** 2)
                    else:
                        score = -np.inf
                else:
                    score = -np.inf
            else:
                metric_inputs = {
                    "return": portfolio_return,
                    "volatility": -portfolio_volatility,
                    "sharpe": sharpe,
                }
                if candidate_expense is not None:
                    metric_inputs["expense"] = -candidate_expense
                score = _weighted_metric_score(metric_inputs, objective_weights)
                if score == 0 and portfolio_volatility > 0:
                    score = sharpe / portfolio_volatility

            priority_bonus = _priority_score_bonus(weights, tickers, priority_indices)
            score += priority_bonus

            if score > best_score:
                best_score = score
                best_portfolio = weights

    if best_portfolio is None:
        fallback_subset = min(subset_capacity, n_assets)
        weights = np.zeros(n_assets)
        if fallback_subset <= 0:
            raise ValueError("Unable to construct fallback portfolio; no assets available.")
        weights[:fallback_subset] = 1.0 / fallback_subset
        best_portfolio = weights

    significant_indices = [i for i, weight in enumerate(best_portfolio) if weight > 1e-4]
    if not significant_indices:
        significant_indices = [int(np.argmax(best_portfolio))]

    selected_weights = best_portfolio[significant_indices]
    selected_weights = selected_weights / selected_weights.sum()
    selected_tickers = [tickers[i] for i in significant_indices]

    latest_prices = prices.iloc[-1]
    quantities: List[int] = []
    for weight, ticker in zip(selected_weights, selected_tickers):
        price = float(latest_prices[ticker])
        allocation_value = target_value * weight
        qty = int(allocation_value // price)
        if qty <= 0:
            qty = 1
        quantities.append(qty)

    portfolio_df = pd.DataFrame(
        {
            "ticker": selected_tickers,
            "weight": selected_weights,
            "quantity": quantities,
            "latest_price": latest_prices[selected_tickers].values,
        }
    )

    portfolio_df["allocation_value"] = portfolio_df["quantity"] * portfolio_df["latest_price"]
    total_allocated = portfolio_df["allocation_value"].sum()
    if total_allocated > 0:
        portfolio_df["weight_realized"] = portfolio_df["allocation_value"] / total_allocated
    else:
        portfolio_df["weight_realized"] = portfolio_df["weight"]

    merge_cols = [col for col in ["ticker", "name", "provider", "category", "expense_ratio"] if col in etf_master.columns]
    if merge_cols:
        portfolio_df = portfolio_df.merge(etf_master[merge_cols], on="ticker", how="left")

    portfolio_return = float(np.dot(annual_returns.values, best_portfolio))
    portfolio_volatility = float(np.sqrt(np.dot(best_portfolio, cov_matrix @ best_portfolio)))
    sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0

    weighted_expense_ratio = None
    expense = _portfolio_expense(best_portfolio, tickers, expense_lookup, default_expense)
    if expense is not None:
        weighted_expense_ratio = expense
    elif not expense_lookup:
        weighted_expense_ratio = 0.0

    kelly_ratio = None
    if portfolio_volatility > 0:
        kelly_ratio = portfolio_return / (portfolio_volatility ** 2)

    return {
        "portfolio": portfolio_df,
        "weights": best_portfolio,
        "metrics": {
            "annual_return": portfolio_return,
            "annual_volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "composite_score": best_score,
            "expense_ratio": weighted_expense_ratio,
            "kelly_ratio": kelly_ratio,
        },
        "score_strategy": score_strategy,
    }
