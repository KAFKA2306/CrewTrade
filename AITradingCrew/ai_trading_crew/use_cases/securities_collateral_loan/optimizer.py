from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import pandas as pd


def optimize_collateral_portfolio(
    prices: pd.DataFrame,
    etf_master: pd.DataFrame,
    objective_weights: Dict[str, float],
    constraints: Dict[str, float],
    sample_size: int,
    target_value: float = 10_000_000,
    max_assets: Optional[int] = None,
    min_assets: int = 3,
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

        score = sharpe / portfolio_volatility if portfolio_volatility > 0 else 0

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
    if expense_lookup:
        expense_values = []
        for ticker, weight in zip(tickers, best_portfolio):
            if weight <= 0:
                continue
            expense = expense_lookup.get(ticker)
            if expense is None or np.isnan(expense):
                expense = default_expense
            expense_values.append(weight * float(expense))
        if expense_values:
            weighted_expense_ratio = float(sum(expense_values))
    else:
        weighted_expense_ratio = 0.0

    return {
        "portfolio": portfolio_df,
        "weights": best_portfolio,
        "metrics": {
            "annual_return": portfolio_return,
            "annual_volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "composite_score": best_score,
            "expense_ratio": weighted_expense_ratio,
        },
    }
