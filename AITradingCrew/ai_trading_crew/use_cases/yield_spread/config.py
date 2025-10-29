from __future__ import annotations

from typing import Dict, Literal

from pydantic import BaseModel, Field, validator

from ai_trading_crew.use_cases.base import UseCaseConfig


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


class YieldSpreadConfig(UseCaseConfig):
    period: str = Field(default="5y")
    rolling_window: int = Field(default=60)
    minimum_periods: int = Field(default=20)
    z_score_threshold: float = Field(default=1.5)
    bp_alert_threshold: float = Field(default=0.0)
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
            raise ValueError("period must end with 'y', 'm', or 'd' (e.g., '5y', '18m')")
        int(value[:-1])  # raises if not numeric
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
