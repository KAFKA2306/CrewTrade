from __future__ import annotations

from typing import List

from pydantic import Field, validator

from crew.base import UseCaseConfig


class CreditSpreadConfig(UseCaseConfig):
    dataset: str = Field(default="credit_oas")
    period: str = Field(default="5y")
    rolling_window: int = Field(default=60, ge=2)
    minimum_periods: int = Field(default=20, ge=2)
    z_score_threshold: float = Field(default=1.5, gt=0)
    bp_alert_threshold: float = Field(default=15.0, ge=0)
    series_labels: List[str] = Field(
        default_factory=lambda: [
            "us_corporate_oas",
            "us_bbb_oas",
            "us_high_yield_oas",
        ]
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


DEFAULT_CONFIG = CreditSpreadConfig(name="credit_spread")
