import numpy as np
import pandas as pd
from typing import Dict, List, Set, Tuple

FEATURE_CONFIG: Tuple[Tuple[str, bool, str], ...] = (
    ("annual_return", False, "return_percentile"),
    ("annual_volatility", True, "volatility_percentile"),
    ("sharpe_ratio", False, "sharpe_percentile"),
    ("max_drawdown", True, "drawdown_percentile"),
    ("expense_ratio", True, "expense_percentile"),
)


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
    percentiles = _compute_percentiles(result)
    result = result.join(percentiles)

    return result


def compute_correlation_matrix(prices: pd.DataFrame) -> pd.DataFrame:
    returns = prices.pct_change().dropna()
    return returns.corr()


def rank_etfs(
    risk_metrics: pd.DataFrame,
    objective_weights: Dict[str, float]
) -> pd.DataFrame:
    df = risk_metrics.copy()

    metric_map = {
        "return": "return_percentile",
        "volatility": "volatility_percentile",
        "sharpe": "sharpe_percentile",
        "drawdown": "drawdown_percentile",
        "expense": "expense_percentile",
    }

    active = [(metric_map[key], objective_weights[key]) for key in objective_weights if key in metric_map and metric_map[key] in df.columns]
    if active:
        columns, weights = zip(*active)
        values = df.loc[:, list(columns)].to_numpy()
        weights_array = np.array(weights, dtype=float)
        total_weight = weights_array.sum()
        if total_weight == 0:
            weights_array = np.full_like(weights_array, 1 / len(weights_array), dtype=float)
        else:
            weights_array = weights_array / total_weight
        composite = values @ weights_array
        df["composite_score"] = composite
    else:
        df["composite_score"] = df["sharpe_ratio"].rank(pct=True, ascending=False, method="average")

    df = df.sort_values("composite_score", ascending=False)

    return df


def select_candidate_universe(
    ranked_metrics: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
    correlation_threshold: float,
    max_assets: int | None = None,
    priority_indices: dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    if ranked_metrics.empty:
        return ranked_metrics

    tickers: List[str] = ranked_metrics["ticker"].tolist()
    corr = correlation_matrix.reindex(index=tickers, columns=tickers).abs().fillna(0)

    tier1_set = set(priority_indices.get("tier1", [])) if priority_indices else set()
    tier2_set = set(priority_indices.get("tier2", [])) if priority_indices else set()

    visited: Set[str] = set()
    selected: List[str] = []

    for ticker in tickers:
        if ticker in visited:
            continue

        component = _collect_component(ticker, corr, correlation_threshold)
        visited.update(component)

        component_df = ranked_metrics[ranked_metrics["ticker"].isin(component)].copy()

        priority_in_component = component_df[component_df["ticker"].isin(tier1_set | tier2_set)]
        if not priority_in_component.empty:
            tier1_match = priority_in_component[priority_in_component["ticker"].isin(tier1_set)]
            if not tier1_match.empty:
                selected.append(tier1_match.iloc[0]["ticker"])
                continue
            selected.append(priority_in_component.iloc[0]["ticker"])
            continue

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


def _compute_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame(index=df.index)
    for source, ascending, target in FEATURE_CONFIG:
        if source in df.columns:
            series = df[source]
            result[target] = series.rank(pct=True, ascending=ascending, method="average")
    return result
