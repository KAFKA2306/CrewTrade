import pandas as pd
import numpy as np
from typing import Dict, List


def optimize_collateral_portfolio(
    prices: pd.DataFrame,
    etf_master: pd.DataFrame,
    objective_weights: Dict[str, float],
    constraints: Dict[str, float],
    sample_size: int,
    target_value: float = 10_000_000
) -> Dict:
    returns = prices.pct_change().dropna()
    tickers = list(prices.columns)
    n_assets = len(tickers)

    if n_assets < 3:
        raise ValueError(f"At least 3 ETFs required for optimization, got {n_assets}")

    min_weight = constraints.get("min_weight", 0.05)
    max_weight = constraints.get("max_weight", 0.35)
    max_volatility = constraints.get("max_volatility", 0.12)

    cov_matrix = returns.cov() * 252

    best_portfolio = None
    best_score = -np.inf

    for _ in range(sample_size):
        weights = np.random.dirichlet(np.ones(n_assets))

        if np.any(weights < min_weight) or np.any(weights > max_weight):
            continue

        portfolio_return = np.sum(returns.mean() * 252 * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        if portfolio_volatility > max_volatility:
            continue

        sharpe = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0

        w_sharpe = objective_weights.get("sharpe", 0.6)
        w_volatility = objective_weights.get("volatility", 0.4)

        score = w_sharpe * sharpe - w_volatility * portfolio_volatility

        if score > best_score:
            best_score = score
            best_portfolio = weights

    if best_portfolio is None:
        weights = np.ones(n_assets) / n_assets
        best_portfolio = weights

    latest_prices = prices.iloc[-1]
    quantities = []
    for i, ticker in enumerate(tickers):
        value = target_value * best_portfolio[i]
        qty = int(value / latest_prices[ticker])
        quantities.append(max(1, qty))

    portfolio_df = pd.DataFrame({
        "ticker": tickers,
        "weight": best_portfolio,
        "quantity": quantities,
    })

    portfolio_df = portfolio_df.merge(etf_master[["ticker", "name", "provider"]], on="ticker", how="left")

    portfolio_return = np.sum(returns.mean() * 252 * best_portfolio)
    portfolio_volatility = np.sqrt(np.dot(best_portfolio.T, np.dot(cov_matrix, best_portfolio)))
    sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0

    return {
        "portfolio": portfolio_df,
        "weights": best_portfolio,
        "metrics": {
            "annual_return": portfolio_return,
            "annual_volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "composite_score": best_score,
        },
    }
