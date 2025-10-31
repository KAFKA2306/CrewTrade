from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.securities_collateral_loan.config import (
    CollateralAsset,
    LoanScenario,
    OptimizationProfile,
    SecuritiesCollateralLoanConfig,
)
from ai_trading_crew.use_cases.securities_collateral_loan import etf_screening, optimizer


@dataclass
class ThresholdStats:
    ratio: float
    label: str


class SecuritiesCollateralLoanAnalyzer:
    def __init__(self, config: SecuritiesCollateralLoanConfig) -> None:
        self.config = config

    def evaluate(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, object]:
        mode = data_payload.get("mode", "manual")

        if mode == "optimization":
            return self._evaluate_optimization_mode(data_payload)
        else:
            return self._evaluate_manual_mode(data_payload)

    def _evaluate_optimization_mode(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, object]:
        prices = data_payload["prices"]
        etf_master = data_payload["etf_master"]

        if prices.empty:
            raise ValueError("Price data is empty")

        risk_metrics = etf_screening.compute_risk_metrics(prices, etf_master)
        correlation_matrix = etf_screening.compute_correlation_matrix(prices)

        def _is_hedged_label(value: str) -> bool:
            text = (value or "").strip()
            if not text:
                return False
            text_lower = text.lower()
            if "hedged" in text_lower and "unhedged" not in text_lower and "hedge-free" not in text_lower:
                return True
            if "ヘッジ" in text:
                if any(keyword in text for keyword in ("ヘッジなし", "ヘッジ無し", "ヘッジ無", "ノーヘッジ")):
                    return False
                return True
            return False

        hedged_mask = pd.Series(False, index=etf_master.index)
        for column in ("name", "description"):
            if column in etf_master.columns:
                hedged_mask = hedged_mask | etf_master[column].fillna("").apply(_is_hedged_label)
        hedged_tickers = set(etf_master.loc[hedged_mask, "ticker"].tolist())

        hedged_assets: List[Dict[str, str]] = []
        if hedged_tickers:
            risk_metrics = risk_metrics[~risk_metrics["ticker"].isin(hedged_tickers)]
            correlation_matrix = correlation_matrix.drop(index=list(hedged_tickers), columns=list(hedged_tickers), errors="ignore")
            hedged_assets = (
                etf_master.loc[etf_master["ticker"].isin(hedged_tickers), ["ticker", "name"]]
                .drop_duplicates(subset=["ticker"])
                .to_dict("records")
            )

        if risk_metrics.empty:
            raise ValueError("No ETFs remain after removing hedged products. Adjust filters or allow hedged ETFs.")

        objective_weights = self.config.optimization.objective_weights
        constraints = self.config.optimization.constraints
        sample_size = self.config.optimization.sample_size
        base_correlation_threshold = self.config.optimization.correlation_threshold
        base_universe_cap = self.config.optimization.max_universe_size
        base_portfolio_cap = self.config.optimization.max_portfolio_size
        base_min_assets = min(self.config.optimization.min_assets, len(prices.columns))
        base_min_assets = max(base_min_assets, 3)

        volatility_excluded: List[Dict[str, str]] = []
        drawdown_excluded: List[Dict[str, str]] = []

        max_asset_volatility = constraints.get("max_asset_volatility")
        max_asset_drawdown = constraints.get("max_asset_drawdown")

        if max_asset_volatility is not None and "annual_volatility" in risk_metrics.columns:
            mask_volatility = (risk_metrics["annual_volatility"] <= max_asset_volatility).fillna(False)
            excluded_vol_df = risk_metrics.loc[~mask_volatility, ["ticker", "name"]].drop_duplicates(subset=["ticker"])
            if not excluded_vol_df.empty:
                volatility_excluded = excluded_vol_df.to_dict("records")
                drop_tickers = excluded_vol_df["ticker"].tolist()
                correlation_matrix = correlation_matrix.drop(index=drop_tickers, columns=drop_tickers, errors="ignore")
            risk_metrics = risk_metrics.loc[mask_volatility]

        if max_asset_drawdown is not None and "max_drawdown" in risk_metrics.columns:
            mask_drawdown = (risk_metrics["max_drawdown"].abs() <= max_asset_drawdown).fillna(False)
            excluded_drawdown_df = risk_metrics.loc[~mask_drawdown, ["ticker", "name"]].drop_duplicates(subset=["ticker"])
            if not excluded_drawdown_df.empty:
                drawdown_excluded = excluded_drawdown_df.to_dict("records")
                drop_tickers = excluded_drawdown_df["ticker"].tolist()
                correlation_matrix = correlation_matrix.drop(index=drop_tickers, columns=drop_tickers, errors="ignore")
            risk_metrics = risk_metrics.loc[mask_drawdown]

        if risk_metrics.empty:
            raise ValueError("No ETFs remain after applying volatility/drawdown filters. Adjust thresholds or review data.")

        ranked_etfs = etf_screening.rank_etfs(risk_metrics, objective_weights)

        profile_configs: List[OptimizationProfile]
        if self.config.optimization.profiles:
            profile_configs = self.config.optimization.profiles
        else:
            profile_configs = [
                OptimizationProfile(name="max_sharpe", objective_weights={"sharpe": 1.0, "volatility": 0.0}),
                OptimizationProfile(name="balanced", objective_weights=objective_weights),
                OptimizationProfile(name="min_volatility", objective_weights={"sharpe": 0.0, "volatility": 1.0}),
            ]

        profile_results: Dict[str, Dict[str, object]] = {}
        target_value = self.config.loan_amount / self.config.ltv_limit

        for profile in profile_configs:
            profile_corr_threshold = profile.correlation_threshold or base_correlation_threshold
            profile_universe_cap = profile.max_universe_size or base_universe_cap

            candidate_universe = etf_screening.select_candidate_universe(
                ranked_etfs,
                correlation_matrix,
                profile_corr_threshold,
                max_assets=profile_universe_cap,
            )

            if candidate_universe.empty:
                profile_results[profile.name] = {"error": "No ETFs after correlation filtering."}
                continue

            candidate_tickers = candidate_universe["ticker"].tolist()
            prices_subset = prices[candidate_tickers]
            metadata_subset = etf_master[etf_master["ticker"].isin(candidate_tickers)].copy()

            try:
                profile_constraints = constraints.copy()
                if profile.constraints_override:
                    profile_constraints.update(profile.constraints_override)

                profile_portfolio_cap = profile.max_portfolio_size or base_portfolio_cap
                profile_min_assets = profile.min_assets or base_min_assets
                profile_min_assets = min(profile_min_assets, len(candidate_tickers))
                profile_min_assets = max(profile_min_assets, 3)

                result = optimizer.optimize_collateral_portfolio(
                    prices_subset,
                    metadata_subset,
                    profile.objective_weights,
                    profile_constraints,
                    profile.sample_size or sample_size,
                    target_value=target_value,
                    max_assets=profile_portfolio_cap,
                    min_assets=profile_min_assets,
                )
                result["candidate_universe"] = candidate_universe
                result["metadata_subset"] = metadata_subset
                result["correlation_threshold"] = profile_corr_threshold
                result["max_universe_size"] = profile_universe_cap
                profile_results[profile.name] = result
            except Exception as exc:
                profile_results[profile.name] = {
                    "error": str(exc),
                    "candidate_universe": candidate_universe,
                    "metadata_subset": metadata_subset,
                }

        primary_profile_name = None
        for profile in profile_configs:
            result = profile_results.get(profile.name)
            if result and "portfolio" in result:
                primary_profile_name = profile.name
                break
        if primary_profile_name is None:
            raise RuntimeError("Optimization failed for all configured profiles.")

        optimized = profile_results[primary_profile_name]
        optimized_portfolio = optimized["portfolio"]
        self.config.collateral_assets = [
            CollateralAsset(
                ticker=row["ticker"],
                quantity=row["quantity"],
                description=row.get("name") or row.get("description") or "",
            )
            for _, row in optimized_portfolio.iterrows()
        ]

        selected_prices = prices[optimized_portfolio["ticker"].tolist()]
        manual_result = self._evaluate_manual_mode({"prices": selected_prices})

        asset_breakdown = manual_result["asset_breakdown"]
        metadata_subset_primary = optimized.get("metadata_subset", etf_master)
        merge_cols = [col for col in ["ticker", "category", "expense_ratio", "name", "provider"] if col in metadata_subset_primary.columns]
        if merge_cols:
            enriched = metadata_subset_primary[merge_cols].drop_duplicates(subset=["ticker"])
            asset_breakdown = asset_breakdown.merge(enriched, on="ticker", how="left")
            asset_breakdown["description"] = asset_breakdown["name"].fillna(asset_breakdown["description"])
        portfolio_merge_cols = [col for col in ["ticker", "weight", "weight_realized"] if col in optimized_portfolio.columns]
        if portfolio_merge_cols:
            asset_breakdown = asset_breakdown.merge(optimized_portfolio[portfolio_merge_cols], on="ticker", how="left")
        asset_breakdown["category"] = asset_breakdown["category"].fillna("その他")

        risk_merge_cols = [col for col in ["ticker", "annual_return", "annual_volatility", "sharpe_ratio"] if col in risk_metrics.columns]
        if risk_merge_cols:
            risk_enriched = (
                risk_metrics[risk_metrics["ticker"].isin(asset_breakdown["ticker"])]
                [risk_merge_cols]
                .drop_duplicates(subset=["ticker"])
            )
            asset_breakdown = asset_breakdown.merge(risk_enriched, on="ticker", how="left")

        manual_result["asset_breakdown"] = asset_breakdown

        manual_result.update({
            "mode": "optimization",
            "etf_master": etf_master,
            "risk_metrics": risk_metrics,
            "ranked_etfs": ranked_etfs,
            "correlation_matrix": correlation_matrix,
            "optimized_portfolio": optimized_portfolio,
            "optimization_metrics": optimized["metrics"],
            "optimization_profiles": {
                name: result.get("metrics")
                for name, result in profile_results.items()
                if "metrics" in result
            },
            "optimization_profile_results": profile_results,
            "primary_profile": primary_profile_name,
            "candidate_universe": optimized.get("candidate_universe"),
            "annual_asset_returns": self._compute_annual_asset_returns(selected_prices, asset_breakdown),
            "annual_portfolio_returns": self._compute_annual_portfolio_returns(manual_result["portfolio_value"]),
            "hedged_excluded": hedged_assets,
            "volatility_excluded": volatility_excluded,
            "drawdown_excluded": drawdown_excluded,
            "asset_filter_thresholds": {
                "max_asset_volatility": max_asset_volatility,
                "max_asset_drawdown": max_asset_drawdown,
            },
        })

        return manual_result

    def _evaluate_manual_mode(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, object]:
        prices = data_payload["prices"]
        if prices.empty:
            raise ValueError("Price data is empty. Please check collateral tickers.")
        positions = self._build_position_value(prices)
        portfolio_value = positions.sum(axis=1)
        loan_ratio_series = self.config.loan_amount / portfolio_value
        interest_projection = self._compute_interest_projection()
        drawdown_series, max_drawdown = self._compute_drawdown(portfolio_value)
        warning_events = self._extract_events(loan_ratio_series, self.config.warning_ratio, "warning")
        liquidation_events = self._extract_events(loan_ratio_series, self.config.liquidation_ratio, "liquidation")
        scenarios = self._run_scenarios(portfolio_value.iloc[-1])

        summary = {
            "current_collateral_value": float(portfolio_value.iloc[-1]),
            "current_loan_ratio": float(loan_ratio_series.iloc[-1]),
            "loan_amount": self.config.loan_amount,
            "ltv_limit": self.config.ltv_limit,
            "warning_ratio": self.config.warning_ratio,
            "liquidation_ratio": self.config.liquidation_ratio,
            "buffer_to_warning_pct": self._buffer_to_ratio(
                portfolio_value.iloc[-1],
                self.config.loan_amount,
                self.config.warning_ratio,
            ),
            "buffer_to_liquidation_pct": self._buffer_to_ratio(
                portfolio_value.iloc[-1],
                self.config.loan_amount,
                self.config.liquidation_ratio,
            ),
            "max_drawdown": max_drawdown,
            "drawdown_series": drawdown_series,
            "interest_projection": interest_projection,
        }

        asset_breakdown = pd.DataFrame(
            {
                "ticker": [asset.ticker for asset in self.config.collateral_assets],
                "quantity": [asset.quantity for asset in self.config.collateral_assets],
                "description": [asset.description or "" for asset in self.config.collateral_assets],
                "latest_price": [float(prices[asset.ticker].iloc[-1]) for asset in self.config.collateral_assets],
            }
        )
        asset_breakdown["market_value"] = asset_breakdown["latest_price"] * asset_breakdown["quantity"]

        return {
            "prices": prices,
            "positions": positions,
            "portfolio_value": portfolio_value,
            "loan_ratio_series": loan_ratio_series,
            "summary": summary,
            "warning_events": warning_events,
            "liquidation_events": liquidation_events,
            "scenarios": scenarios,
            "asset_breakdown": asset_breakdown,
        }

    def _build_position_value(self, prices: pd.DataFrame) -> pd.DataFrame:
        holdings: Dict[str, pd.Series] = {}
        for asset in self.config.collateral_assets:
            if asset.ticker not in prices.columns:
                continue
            holdings[asset.ticker] = prices[asset.ticker] * asset.quantity
        if not holdings:
            raise ValueError("No matching price columns for collateral assets.")
        return pd.DataFrame(holdings)

    def _compute_interest_projection(self) -> List[Dict[str, float]]:
        rate = self.config.annual_interest_rate
        projections: List[Dict[str, float]] = []
        for days in self.config.interest_horizons_days:
            interest = self.config.loan_amount * rate * (days / 365)
            projections.append(
                {
                    "days": days,
                    "interest": round(interest, 2),
                }
            )
        return projections

    def _compute_drawdown(self, portfolio_value: pd.Series) -> tuple[pd.Series, float]:
        rolling_peak = portfolio_value.cummax()
        drawdown = portfolio_value / rolling_peak - 1.0
        max_drawdown = float(drawdown.min())
        return drawdown, max_drawdown

    def _extract_events(self, ratio_series: pd.Series, threshold: float, label: str) -> pd.DataFrame:
        mask = ratio_series >= threshold
        if not mask.any():
            return pd.DataFrame(columns=["date", "loan_ratio", "label"])
        events = pd.DataFrame(
            {
                "date": ratio_series.index[mask],
                "loan_ratio": ratio_series[mask].values,
                "label": label,
            }
        )
        return events

    def _run_scenarios(self, latest_value: float) -> List[Dict[str, float]]:
        scenarios: List[Dict[str, float]] = []
        for scenario in self.config.scenarios:
            effective_value = latest_value * (1 - scenario.drop_pct)
            ratio = self.config.loan_amount / effective_value if effective_value > 0 else np.inf
            scenarios.append(
                {
                    "label": scenario.label or f"-{int(scenario.drop_pct * 100)}%",
                    "drop_pct": scenario.drop_pct,
                    "post_value": round(effective_value, 2),
                    "loan_ratio": round(float(ratio), 4),
                    "breach_warning": ratio >= self.config.warning_ratio,
                    "breach_liquidation": ratio >= self.config.liquidation_ratio,
                }
            )
        return scenarios

    def _buffer_to_ratio(self, value: float, loan: float, threshold: float) -> float | None:
        if value <= 0:
            return None
        target_collateral = loan / threshold
        if target_collateral <= 0:
            return None
        cushion = 1 - target_collateral / value
        return round(float(cushion), 4)

    def _compute_annual_asset_returns(self, prices: pd.DataFrame, asset_breakdown: pd.DataFrame) -> List[Dict[str, float]]:
        if prices.empty:
            return []
        tickers = asset_breakdown["ticker"].tolist()
        returns = prices[tickers].pct_change().dropna(how="all")
        if returns.empty:
            return []
        returns["__year__"] = returns.index.year
        annual_rows: List[Dict[str, float]] = []
        grouped = returns.groupby("__year__")
        name_map = {}
        if "description" in asset_breakdown.columns:
            name_map = asset_breakdown.set_index("ticker")["description"].fillna("").to_dict()
        if not name_map and "name" in asset_breakdown.columns:
            name_map = asset_breakdown.set_index("ticker")["name"].fillna("").to_dict()
        for year, df_year in grouped:
            for ticker in tickers:
                if ticker not in df_year.columns:
                    continue
                series = df_year[ticker].dropna()
                if series.empty:
                    continue
                ann_return = (1 + series).prod() - 1
                ann_vol = float(series.std() * np.sqrt(252))
                sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan
                annual_rows.append(
                    {
                        "year": int(year),
                        "ticker": ticker,
                        "name": name_map.get(ticker) or "",
                        "annual_return": float(ann_return),
                        "annual_volatility": ann_vol,
                        "sharpe_ratio": float(sharpe) if not np.isnan(sharpe) else None,
                    }
                )
        return sorted(annual_rows, key=lambda row: (row["year"], row["ticker"]))

    def _compute_annual_portfolio_returns(self, portfolio_value: pd.Series) -> List[Dict[str, float]]:
        if portfolio_value.empty:
            return []
        returns = portfolio_value.pct_change().dropna()
        if returns.empty:
            return []
        returns_by_year = returns.groupby(returns.index.year)
        annual_rows: List[Dict[str, float]] = []
        for year, series in returns_by_year:
            if series.empty:
                continue
            ann_return = (1 + series).prod() - 1
            ann_vol = float(series.std() * np.sqrt(252))
            sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan
            annual_rows.append(
                {
                    "year": int(year),
                    "annual_return": float(ann_return),
                    "annual_volatility": ann_vol,
                    "sharpe_ratio": float(sharpe) if not np.isnan(sharpe) else None,
                }
            )
        return sorted(annual_rows, key=lambda row: row["year"])
