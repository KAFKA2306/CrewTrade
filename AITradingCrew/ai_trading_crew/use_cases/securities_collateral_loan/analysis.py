from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.securities_collateral_loan.config import (
    CollateralAsset,
    CoreSatelliteConfig,
    LoanScenario,
    OptimizationProfile,
    PortfolioMetadata,
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

        cs_config = self.config.optimization.core_satellite if self.config.optimization else None
        prev_portfolio = data_payload.get('previous_portfolio')
        prev_metadata = data_payload.get('previous_metadata')

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
        target_value = (self.config.loan_amount / self.config.ltv_limit) * 1.10

        for profile in profile_configs:
            profile_corr_threshold = profile.correlation_threshold or base_correlation_threshold
            profile_universe_cap = profile.max_universe_size or base_universe_cap

            candidate_universe = etf_screening.select_candidate_universe(
                ranked_etfs,
                correlation_matrix,
                profile_corr_threshold,
                max_assets=profile_universe_cap,
                priority_indices=self.config.optimization.priority_indices if self.config.optimization else None,
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
                    priority_indices=self.config.optimization.priority_indices if self.config.optimization else None,
                )
                result["candidate_universe"] = candidate_universe
                result["metadata_subset"] = metadata_subset
                result["correlation_threshold"] = profile_corr_threshold
                result["max_universe_size"] = profile_universe_cap
                result["candidate_tickers"] = candidate_tickers
                result["constraints_used"] = profile_constraints.copy()
                result["sample_size_used"] = profile.sample_size or sample_size
                result["max_assets_used"] = profile_portfolio_cap
                result["min_assets_used"] = profile_min_assets
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

        variant_portfolios: Dict[str, Dict[str, object]] = {}
        candidate_tickers_primary = optimized.get("candidate_tickers")
        metadata_subset_primary = optimized.get("metadata_subset", etf_master)
        constraints_primary = optimized.get("constraints_used", constraints)
        sample_size_primary = optimized.get("sample_size_used", sample_size)
        max_assets_primary = optimized.get("max_assets_used", base_portfolio_cap)
        min_assets_primary = optimized.get("min_assets_used", base_min_assets)
        if candidate_tickers_primary:
            prices_candidate = prices[candidate_tickers_primary]
            variant_specs = [
                ("max_sharpe", "Max Sharpe Portfolio"),
                ("min_variance", "Minimum-Variance Portfolio"),
                ("max_kelly", "Max Kelly Criterion Portfolio"),
            ]
            for strategy_key, strategy_label in variant_specs:
                try:
                    variant_result = optimizer.optimize_collateral_portfolio(
                        prices_candidate,
                        metadata_subset_primary,
                        {},
                        constraints_primary,
                        sample_size_primary,
                        target_value=target_value,
                        max_assets=max_assets_primary,
                        min_assets=min_assets_primary,
                        score_strategy=strategy_key,
                        priority_indices=self.config.optimization.priority_indices if self.config.optimization else None,
                    )
                    variant_result["strategy"] = strategy_key
                    variant_result["strategy_label"] = strategy_label
                    variant_result["source_profile"] = strategy_key
                    variant_portfolios[strategy_key] = variant_result
                except Exception as exc:
                    variant_portfolios[strategy_key] = {
                        "strategy": strategy_key,
                        "strategy_label": strategy_label,
                        "error": str(exc),
                    }

        if cs_config and cs_config.enabled:
            optimized_portfolio, portfolio_metadata = self._apply_core_satellite_strategy(
                optimized_portfolio, prev_portfolio, prev_metadata, cs_config, prices
            )
        else:
            portfolio_metadata = None

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

        portfolio_returns = manual_result["portfolio_value"].pct_change().dropna()
        drawdown_validation = self._validate_portfolio_drawdown(portfolio_returns)
        allocation_validation = self._validate_asset_allocation(asset_breakdown)

        prices_forward = data_payload.get("prices_forward")
        forward_test = None
        if isinstance(prices_forward, pd.DataFrame) and not prices_forward.empty:
            forward_test = self._compute_forward_test(prices_forward, optimized_portfolio)

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
            "variant_portfolios": variant_portfolios,
            "drawdown_validation": drawdown_validation,
            "allocation_validation": allocation_validation,
        })

        if portfolio_metadata is not None:
            manual_result["metadata"] = portfolio_metadata

        if self.config.optimization and self.config.optimization.risk_policy:
            manual_result["risk_policy"] = self.config.optimization.risk_policy.dict()

        if forward_test is not None:
            manual_result["forward_test"] = forward_test

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

    def _compute_forward_test(self, prices_forward: pd.DataFrame, optimized_portfolio: pd.DataFrame) -> Dict[str, object]:
        portfolio_tickers = optimized_portfolio["ticker"].tolist()
        available_tickers = [t for t in portfolio_tickers if t in prices_forward.columns]

        if not available_tickers:
            return {}

        prices_subset = prices_forward[available_tickers].copy()

        if prices_subset.empty:
            return {}

        weights_map = optimized_portfolio.set_index("ticker")["weight_realized"].to_dict()
        weights = np.array([weights_map.get(t, 0) for t in available_tickers])
        weights = weights / weights.sum()

        returns = prices_subset.pct_change().dropna()

        if returns.empty:
            return {}

        portfolio_returns = (returns * weights).sum(axis=1)
        portfolio_value = (1 + portfolio_returns).cumprod()

        cumulative_return = float(portfolio_value.iloc[-1] - 1) if len(portfolio_value) > 0 else 0.0

        n_days = len(portfolio_returns)
        n_years = n_days / 252.0
        annualized_return = (1 + cumulative_return) ** (1 / n_years) - 1 if n_years > 0 else 0.0

        annualized_volatility = float(portfolio_returns.std() * np.sqrt(252))

        sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility > 0 else 0.0

        running_max = portfolio_value.cummax()
        drawdown = (portfolio_value - running_max) / running_max
        max_drawdown = float(drawdown.min())

        return {
            "series": portfolio_value.to_frame(name="portfolio_value"),
            "summary": {
                "start": prices_subset.index.min(),
                "end": prices_subset.index.max(),
                "cumulative_return": cumulative_return,
                "annualized_return": annualized_return,
                "annualized_volatility": annualized_volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
            },
        }

    def _validate_portfolio_drawdown(self, portfolio_returns: pd.Series) -> Dict[str, object]:
        cumulative = (1 + portfolio_returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = float(drawdown.min())

        max_dd_constraint = self.config.optimization.constraints.get("max_portfolio_drawdown")
        if max_dd_constraint is None:
            return {"max_drawdown": max_drawdown, "constraint": None, "compliant": True}

        compliant = abs(max_drawdown) <= max_dd_constraint
        return {
            "max_drawdown": max_drawdown,
            "constraint": max_dd_constraint,
            "compliant": compliant,
            "breach_amount": abs(max_drawdown) - max_dd_constraint if not compliant else 0.0,
        }

    def _validate_asset_allocation(self, asset_breakdown: pd.DataFrame) -> Dict[str, object]:
        allocation_config = self.config.optimization.constraints.get("asset_allocation")
        if not allocation_config:
            return {"compliant": True, "allocations": {}, "constraints": {}}

        category_map = {
            "債券": "bonds",
            "金": "commodity",
            "ゴールド": "commodity",
            "コモディティ": "commodity",
            "株式": "equity",
            "国内株式": "equity",
            "海外株式": "equity",
            "国内セクター": "equity",
            "REIT": "reit",
            "その他": "other",
        }

        allocations = {}
        for allocation_key in allocation_config.keys():
            allocations[allocation_key] = 0.0

        if "category" in asset_breakdown.columns and "weight" in asset_breakdown.columns:
            for _, row in asset_breakdown.iterrows():
                category = str(row["category"]).strip() if pd.notna(row["category"]) else ""
                weight = float(row["weight"]) if pd.notna(row["weight"]) else 0.0

                allocation_key = category_map.get(category)
                if allocation_key and allocation_key in allocations:
                    allocations[allocation_key] += weight
                elif allocation_key is None and category:
                    if "other" in allocations:
                        allocations["other"] += weight

        violations = []
        for allocation_key, current_weight in allocations.items():
            constraint = allocation_config.get(allocation_key, {})
            min_weight = constraint.get("min", 0.0)
            max_weight = constraint.get("max", 1.0)

            if current_weight < min_weight:
                violations.append({
                    "type": allocation_key,
                    "current": current_weight,
                    "constraint": f">= {min_weight}",
                    "breach": min_weight - current_weight,
                })
            elif current_weight > max_weight:
                violations.append({
                    "type": allocation_key,
                    "current": current_weight,
                    "constraint": f"<= {max_weight}",
                    "breach": current_weight - max_weight,
                })

        return {
            "compliant": len(violations) == 0,
            "allocations": allocations,
            "constraints": allocation_config,
            "violations": violations,
        }

    def _apply_core_satellite_strategy(
        self,
        optimized_portfolio: pd.DataFrame,
        prev_portfolio: pd.DataFrame | None,
        prev_metadata: PortfolioMetadata | None,
        cs_config: CoreSatelliteConfig,
        prices: pd.DataFrame
    ) -> tuple[pd.DataFrame, PortfolioMetadata]:
        needs_core_rebalance = (
            prev_portfolio is None or
            prev_metadata is None or
            prev_metadata.rebalance_year >= cs_config.core_rebalance_years
        )

        anchor_date = prices.index.max()

        if needs_core_rebalance:
            sorted_by_sharpe = optimized_portfolio.copy()
            if "sharpe_ratio" in sorted_by_sharpe.columns:
                sorted_by_sharpe = sorted_by_sharpe.sort_values("sharpe_ratio", ascending=False)
            elif "weight" in sorted_by_sharpe.columns:
                sorted_by_sharpe = sorted_by_sharpe.sort_values("weight", ascending=False)

            n_total = len(optimized_portfolio)
            n_core = max(1, int(n_total * cs_config.core_weight))

            priority_indices = self.config.optimization.priority_indices if self.config.optimization else None
            tier1_tickers = set(priority_indices.get("tier1", [])) if priority_indices else set()
            tier2_tickers = set(priority_indices.get("tier2", [])) if priority_indices else set()

            priority_core = sorted_by_sharpe[sorted_by_sharpe["ticker"].isin(tier1_tickers | tier2_tickers)]
            other_core_candidates = sorted_by_sharpe[~sorted_by_sharpe["ticker"].isin(tier1_tickers | tier2_tickers)]

            core_portfolio = pd.concat([priority_core, other_core_candidates]).head(n_core).copy()
            core_portfolio["portfolio_type"] = "core"

            core_tickers_set = set(core_portfolio["ticker"])
            satellite_portfolio = sorted_by_sharpe[~sorted_by_sharpe["ticker"].isin(core_tickers_set)].copy()
            satellite_portfolio["portfolio_type"] = "satellite"

            core_total_weight = core_portfolio["weight"].sum() if len(core_portfolio) > 0 else 0
            satellite_total_weight = satellite_portfolio["weight"].sum() if len(satellite_portfolio) > 0 else 0

            if core_total_weight > 0:
                core_portfolio["weight"] = core_portfolio["weight"] / core_total_weight * cs_config.core_weight
            if satellite_total_weight > 0:
                satellite_portfolio["weight"] = satellite_portfolio["weight"] / satellite_total_weight * cs_config.satellite_weight

            combined = pd.concat([core_portfolio, satellite_portfolio], ignore_index=True)

            metadata = PortfolioMetadata(
                anchor_date=anchor_date.isoformat(),
                portfolio_type="mixed",
                core_weight=cs_config.core_weight,
                satellite_weight=cs_config.satellite_weight,
                rebalance_year=0,
                valid_until=(anchor_date + pd.DateOffset(years=cs_config.core_rebalance_years)).isoformat(),
                optimization_method="hrp"
            )

            return combined, metadata
        else:
            core_portfolio = prev_portfolio[prev_portfolio["portfolio_type"] == "core"].copy()

            available_tickers = set(prices.columns)
            core_portfolio = core_portfolio[core_portfolio["ticker"].isin(available_tickers)]

            satellite_portfolio = optimized_portfolio.copy()
            satellite_portfolio["portfolio_type"] = "satellite"

            core_tickers = set(core_portfolio["ticker"].tolist())
            satellite_portfolio = satellite_portfolio[~satellite_portfolio["ticker"].isin(core_tickers)]

            core_total_weight = core_portfolio["weight"].sum() if len(core_portfolio) > 0 else 0
            satellite_total_weight = satellite_portfolio["weight"].sum() if len(satellite_portfolio) > 0 else 0

            if core_total_weight > 0:
                core_portfolio["weight"] = core_portfolio["weight"] / core_total_weight * cs_config.core_weight
            if satellite_total_weight > 0:
                satellite_portfolio["weight"] = satellite_portfolio["weight"] / satellite_total_weight * cs_config.satellite_weight

            combined = pd.concat([core_portfolio, satellite_portfolio], ignore_index=True)

            metadata = PortfolioMetadata(
                anchor_date=anchor_date.isoformat(),
                portfolio_type="mixed",
                core_weight=cs_config.core_weight,
                satellite_weight=cs_config.satellite_weight,
                rebalance_year=prev_metadata.rebalance_year + 1,
                valid_until=prev_metadata.valid_until,
                optimization_method="hrp"
            )

            return combined, metadata
