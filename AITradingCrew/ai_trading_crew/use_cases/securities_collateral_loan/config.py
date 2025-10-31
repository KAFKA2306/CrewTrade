from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator

from ai_trading_crew.use_cases.base import UseCaseConfig


class CollateralAsset(BaseModel):
    ticker: str
    quantity: float = Field(gt=0)
    description: str | None = None


class LoanScenario(BaseModel):
    drop_pct: float = Field(gt=0, lt=1, description="Price drop ratio (e.g., 0.2 for -20%).")
    label: str | None = None


class OptimizationProfile(BaseModel):
    name: str = Field(description="Identifier for the optimization profile.")
    objective_weights: Dict[str, float]
    constraints_override: Dict[str, float] | None = None
    correlation_threshold: float | None = Field(default=None, gt=0, lt=1)
    max_universe_size: int | None = Field(default=None, ge=3)
    max_portfolio_size: int | None = Field(default=None, ge=1)
    min_assets: int | None = Field(default=None, ge=1)
    sample_size: int | None = Field(default=None, gt=0)


class OptimizationSettings(BaseModel):
    enabled: bool = Field(default=False)
    objective_weights: Dict[str, float] = Field(
        default_factory=lambda: {"sharpe": 0.6, "volatility": 0.4}
    )
    constraints: Dict[str, float] = Field(
        default_factory=lambda: {
            "min_weight": 0.05,
            "max_weight": 0.35,
            "max_category_weight": 0.50,
            "max_volatility": 0.12,
            "max_asset_volatility": 0.25,
            "max_asset_drawdown": 0.30,
        }
    )
    sample_size: int = Field(default=20000, gt=0)
    lookback: str = Field(default="3y")
    correlation_threshold: float = Field(default=0.9, gt=0, lt=1)
    max_universe_size: int = Field(default=40, ge=3)
    max_portfolio_size: int = Field(default=12, ge=3)
    min_assets: int = Field(default=5, ge=1)
    profiles: Optional[List[OptimizationProfile]] = None


class SecuritiesCollateralLoanConfig(UseCaseConfig):
    period: str = Field(default="3y")
    loan_amount: float = Field(default=10_000_000, gt=0)
    annual_interest_rate: float = Field(default=0.01875, gt=0, description="Annual simple interest rate.")
    ltv_limit: float = Field(default=0.60, gt=0, lt=1, description="Maximum borrowing ratio vs collateral market value.")
    warning_ratio: float = Field(default=0.70, gt=0, lt=1)
    liquidation_ratio: float = Field(default=0.85, gt=0, lt=1)
    collateral_assets: List[CollateralAsset] = Field(default_factory=list)
    scenarios: List[LoanScenario] = Field(
        default_factory=lambda: [
            LoanScenario(drop_pct=0.10, label="-10%"),
            LoanScenario(drop_pct=0.20, label="-20%"),
            LoanScenario(drop_pct=0.30, label="-30%"),
            LoanScenario(drop_pct=0.40, label="-40%"),
        ]
    )
    interest_horizons_days: List[int] = Field(default_factory=lambda: [30, 90, 180])
    optimization: OptimizationSettings | None = None

    @validator("period")
    def _validate_period(cls, value: str) -> str:
        value = value.strip().lower()
        if len(value) < 2 or value[-1] not in {"y", "m", "d"}:
            raise ValueError("period must end with 'y', 'm', or 'd' (e.g., '3y').")
        int(value[:-1])
        return value


DEFAULT_CONFIG = SecuritiesCollateralLoanConfig(
    name="securities_collateral_loan",
    collateral_assets=[
        CollateralAsset(ticker="1306.T", quantity=73, description="NEXT FUNDS TOPIX ETF"),
        CollateralAsset(ticker="2568.T", quantity=118, description="NASDAQ100 ETF (No Hedge)"),
        CollateralAsset(ticker="2510.T", quantity=19302, description="NEXT FUNDS Domestic Bond NOMURA-BPI"),
        CollateralAsset(ticker="2622.T", quantity=159, description="iShares USD Emerging Markets Bond Hedged"),
        CollateralAsset(ticker="348A.T", quantity=1004, description="MAXIS Yomiuri 333 ETF"),
    ],
)
