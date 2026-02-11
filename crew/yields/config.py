from __future__ import annotations
from typing import Dict, List, Literal
from pydantic import BaseModel, Field, validator
from crew.base import UseCaseConfig
class YieldSeriesConfig(BaseModel):
    source: Literal["fred", "yfinance"]
    identifier: str
    scaling: float = Field(default=1.0)
    field: str = Field(default="Close")
    description: str | None = None
class YieldSpreadPair(BaseModel):
    junk: YieldSeriesConfig
    treasury: YieldSeriesConfig
    description: str | None = None
class AllocationProfile(BaseModel):
    label: str
    weights: Dict[str, float]
    @validator("weights")
    def _ensure_positive(cls, value: Dict[str, float]) -> Dict[str, float]:
        if not value:
            raise ValueError("weights must not be empty")
        total = sum(value.values())
        if total <= 0:
            raise ValueError("weights must sum to a positive value")
        return value
class OptimizationConfig(BaseModel):
    enabled: bool = Field(default=False)
    lookback: str = Field(default="1y")
    sample_size: int = Field(default=5000)
    min_weight: float = Field(default=0.0)
    max_weight: float = Field(default=1.0)
    risk_free_rate: float = Field(default=0.0)
    sensitivity_sample_sizes: List[int] = Field(
        default_factory=lambda: [1000, 5000, 10000]
    )
    @validator("lookback")
    def _validate_lookback(cls, value: str) -> str:
        value = value.strip().lower()
        if len(value) < 2 or value[-1] not in {"y", "m", "d"}:
            raise ValueError(
                "lookback must end with 'y', 'm', or 'd' (e.g., '1y', '6m')"
            )
        int(value[:-1])
        return value
class AllocationConfig(BaseModel):
    upper_z: float = Field(
        default=1.0, description="Threshold above which the regime is defensive."
    )
    lower_z: float = Field(
        default=-1.0, description="Threshold below which the regime is risk-on."
    )
    widening: AllocationProfile = Field(
        default_factory=lambda: AllocationProfile(
            label="Defensive",
            weights={"IEF": 0.5, "TLT": 0.3, "BIL": 0.2},
        )
    )
    neutral: AllocationProfile = Field(
        default_factory=lambda: AllocationProfile(
            label="Neutral",
            weights={"SPY": 0.5, "IEF": 0.3, "HYG": 0.2},
        )
    )
    tightening: AllocationProfile = Field(
        default_factory=lambda: AllocationProfile(
            label="Risk-On",
            weights={"SPY": 0.6, "QQQ": 0.2, "HYG": 0.2},
        )
    )
    optimization: OptimizationConfig = Field(default_factory=OptimizationConfig)
    @validator("upper_z")
    def _check_upper(cls, value: float, values: Dict[str, float]) -> float:
        lower = values.get("lower_z")
        if lower is not None and value <= lower:
            raise ValueError("upper_z must be greater than lower_z")
        return value
class YieldSpreadConfig(UseCaseConfig):
    period: str = Field(default="5y")
    rolling_window: int = Field(default=60)
    minimum_periods: int = Field(default=20)
    z_score_threshold: float = Field(default=1.5)
    bp_alert_threshold: float = Field(default=0.0)
    allocation: AllocationConfig | None = Field(default_factory=AllocationConfig)
    pairs: Dict[str, YieldSpreadPair] = Field(
        default_factory=lambda: {
            "us_high_yield_vs_us10y": YieldSpreadPair(
                junk=YieldSeriesConfig(
                    source="fred",
                    identifier="BAMLH0A0HYM2EY",
                    description="ICE BofA US High Yield Index Effective Yield (%)",
                ),
                treasury=YieldSeriesConfig(
                    source="fred",
                    identifier="DGS10",
                    field="value",
                    description="US 10Y Treasury Constant Maturity Rate (%)",
                ),
                description="US High Yield minus 10Y Treasury yield spread",
            )
        }
    )
    @validator("period")
    def _validate_period(cls, value: str) -> str:
        value = value.strip().lower()
        if len(value) < 2 or value[-1] not in {"y", "m", "d"}:
            raise ValueError(
                "period must end with 'y', 'm', or 'd' (e.g., '5y', '18m')"
            )
        int(value[:-1])
        return value
    @property
    def series_configs(self) -> Dict[str, YieldSeriesConfig]:
        configs: Dict[str, YieldSeriesConfig] = {}
        for pair in self.pairs.values():
            for series in (pair.junk, pair.treasury):
                key = f"{series.source}:{series.identifier}"
                configs.setdefault(key, series)
        return configs
DEFAULT_CONFIG = YieldSpreadConfig(name="yield_spread")
