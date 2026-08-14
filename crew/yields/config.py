from __future__ import annotations

from pydantic import BaseModel, Field, validator

from crew.base import UseCaseConfig


class CurveSpreadConfig(BaseModel):
    short_label: str
    long_label: str
    description: str | None = None


class YieldSpreadConfig(UseCaseConfig):
    rates_dataset: str = Field(default="rates_macro")
    curve_dataset: str = Field(default="treasury_par_yield_curve")
    period: str = Field(default="5y")
    rolling_window: int = Field(default=60, ge=2)
    minimum_periods: int = Field(default=20, ge=2)
    z_score_threshold: float = Field(default=1.5, gt=0)
    bp_alert_threshold: float = Field(default=25.0, ge=0)
    curve_spreads: dict[str, CurveSpreadConfig] = Field(
        default_factory=lambda: {
            "us_2s10s": CurveSpreadConfig(
                short_label="us_2y",
                long_label="us_10y",
                description="US 10Y minus 2Y constant maturity rate",
            ),
            "us_10s30s": CurveSpreadConfig(
                short_label="us_10y",
                long_label="us_30y",
                description="US 30Y minus 10Y constant maturity rate",
            ),
        }
    )

    @validator("period")
    def _validate_period(cls, value: str) -> str:
        normalized = value.strip().lower()
        if len(normalized) < 2 or normalized[-1] not in {"y", "m", "d"}:
            raise ValueError("period must end with y, m, or d")
        int(normalized[:-1])
        return normalized

    @validator("minimum_periods")
    def _validate_minimum_periods(cls, value: int, values: dict) -> int:
        rolling_window = values.get("rolling_window")
        if rolling_window is not None and value > rolling_window:
            raise ValueError("minimum_periods must not exceed rolling_window")
        return value


DEFAULT_CONFIG = YieldSpreadConfig(name="yield_spread")
