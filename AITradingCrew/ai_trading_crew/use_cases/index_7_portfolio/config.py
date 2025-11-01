from typing import Dict, List

from pydantic import BaseModel, Field

from ai_trading_crew.use_cases.base import UseCaseConfig


class IndexAsset(BaseModel):
    ticker: str = Field(description="Yahoo Finance ticker symbol for the index")
    name: str = Field(description="Human-readable index name")
    category: str = Field(description="Asset category: equity, bonds, commodity, reit")


class OptimizationSettings(BaseModel):
    enabled: bool = Field(default=True)
    objective_weights: Dict[str, float] = Field(
        default_factory=lambda: {"sharpe": 0.6, "volatility": 0.4}
    )
    constraints: Dict[str, float] = Field(
        default_factory=lambda: {
            "min_weight": 0.05,
            "max_weight": 0.30,
            "max_volatility": 0.15,
        }
    )
    sample_size: int = Field(default=10000, gt=0)
    lookback: str = Field(default="10y")


class Index7PortfolioConfig(UseCaseConfig):
    period: str = Field(default="20y", description="Historical data period")
    indices: List[IndexAsset] = Field(description="List of 7 index assets")
    optimization: OptimizationSettings = Field(default_factory=OptimizationSettings)
    loan_amount: float = Field(default=10_000_000, description="Loan amount for LTV calculation")
    annual_interest_rate: float = Field(default=0.01875)
    ltv_limit: float = Field(default=0.6)
    warning_ratio: float = Field(default=0.7)
    liquidation_ratio: float = Field(default=0.85)
