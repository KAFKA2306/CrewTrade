import pandas as pd
import numpy as np
from typing import Dict


def compute_risk_metrics(prices: pd.DataFrame, etf_master: pd.DataFrame) -> pd.DataFrame:
    returns = prices.pct_change().dropna()

    metrics_list = []
    for ticker in prices.columns:
        ticker_returns = returns[ticker].dropna()

        if len(ticker_returns) < 20:
            continue

        annual_return = ticker_returns.mean() * 252
        annual_volatility = ticker_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0

        cumulative = (1 + ticker_returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()

        metrics_list.append({
            "ticker": ticker,
            "annual_return": annual_return,
            "annual_volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
        })

    metrics_df = pd.DataFrame(metrics_list)
    result = metrics_df.merge(etf_master, on="ticker", how="left")

    return result


def compute_correlation_matrix(prices: pd.DataFrame) -> pd.DataFrame:
    returns = prices.pct_change().dropna()
    return returns.corr()


def rank_etfs(
    risk_metrics: pd.DataFrame,
    objective_weights: Dict[str, float]
) -> pd.DataFrame:
    df = risk_metrics.copy()

    sharpe_norm = (df["sharpe_ratio"] - df["sharpe_ratio"].min()) / (df["sharpe_ratio"].max() - df["sharpe_ratio"].min() + 1e-9)
    volatility_norm = 1 - (df["annual_volatility"] - df["annual_volatility"].min()) / (df["annual_volatility"].max() - df["annual_volatility"].min() + 1e-9)

    w_sharpe = objective_weights.get("sharpe", 0.6)
    w_volatility = objective_weights.get("volatility", 0.4)

    df["composite_score"] = w_sharpe * sharpe_norm + w_volatility * volatility_norm
    df = df.sort_values("composite_score", ascending=False)

    return df
