from __future__ import annotations

from ai_trading_crew.use_cases.registry import register_use_case
from ai_trading_crew.use_cases.yield_spread.config import DEFAULT_CONFIG, YieldSpreadConfig
from ai_trading_crew.use_cases.yield_spread.use_case import YieldSpreadUseCase


register_use_case(DEFAULT_CONFIG.name, YieldSpreadUseCase, YieldSpreadConfig)


__all__ = [
    "YieldSpreadConfig",
    "YieldSpreadUseCase",
    "DEFAULT_CONFIG",
]
