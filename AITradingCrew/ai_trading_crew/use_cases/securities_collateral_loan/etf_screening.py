import numpy as np
import pandas as pd
from typing import Dict, List, Set


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


def select_candidate_universe(
    ranked_metrics: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
    correlation_threshold: float,
    max_assets: int | None = None,
) -> pd.DataFrame:
    if ranked_metrics.empty:
        return ranked_metrics

    tickers: List[str] = ranked_metrics["ticker"].tolist()
    corr = correlation_matrix.reindex(index=tickers, columns=tickers).abs().fillna(0)

    visited: Set[str] = set()
    selected: List[str] = []

    for ticker in tickers:
        if ticker in visited:
            continue

        component = _collect_component(ticker, corr, correlation_threshold)
        visited.update(component)

        component_df = ranked_metrics[ranked_metrics["ticker"].isin(component)].copy()
        component_df["expense_ratio_filled"] = component_df["expense_ratio"].fillna(float("inf"))
        component_df = component_df.sort_values(
            by=["expense_ratio_filled", "composite_score", "sharpe_ratio"],
            ascending=[True, False, False],
        )
        selected.append(component_df.iloc[0]["ticker"])

    selected_df = ranked_metrics[ranked_metrics["ticker"].isin(selected)].drop_duplicates(subset=["ticker"], keep="first")

    if max_assets is not None and len(selected_df) > max_assets:
        selected_df = selected_df.sort_values(by=["composite_score", "sharpe_ratio"], ascending=[False, False]).head(max_assets)

    selected_order = [ticker for ticker in tickers if ticker in selected_df["ticker"].values]
    selected_df = selected_df.set_index("ticker").loc[selected_order].reset_index()
    selected_df = selected_df.drop(columns=["expense_ratio_filled"], errors="ignore")
    return selected_df


def _collect_component(seed: str, corr: pd.DataFrame, threshold: float) -> Set[str]:
    component: Set[str] = {seed}
    to_visit: List[str] = [seed]

    while to_visit:
        current = to_visit.pop()
        row = corr.loc[current]
        neighbors = [col for col, value in row.items() if value >= threshold and col != current]
        for neighbor in neighbors:
            if neighbor in component:
                continue
            component.add(neighbor)
            to_visit.append(neighbor)
    return component
