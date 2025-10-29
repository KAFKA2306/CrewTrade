from __future__ import annotations

from ai_trading_crew.use_cases.credit_spread.config import CreditSpreadConfig, DEFAULT_CONFIG
from ai_trading_crew.use_cases.credit_spread.use_case import CreditSpreadUseCase
from ai_trading_crew.use_cases.registry import register_use_case


register_use_case(DEFAULT_CONFIG.name, CreditSpreadUseCase, CreditSpreadConfig)


__all__ = [
    "CreditSpreadConfig",
    "CreditSpreadUseCase",
    "DEFAULT_CONFIG",
]
