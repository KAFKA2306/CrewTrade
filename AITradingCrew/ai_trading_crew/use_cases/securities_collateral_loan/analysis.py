from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd

from ai_trading_crew.use_cases.securities_collateral_loan.config import LoanScenario, SecuritiesCollateralLoanConfig


@dataclass
class ThresholdStats:
    ratio: float
    label: str


class SecuritiesCollateralLoanAnalyzer:
    def __init__(self, config: SecuritiesCollateralLoanConfig) -> None:
        self.config = config

    def evaluate(self, data_payload: Dict[str, pd.DataFrame]) -> Dict[str, object]:
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
