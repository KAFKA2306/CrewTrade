from __future__ import annotations

from crew.credit.config import DEFAULT_CONFIG, CreditSpreadConfig
from crew.credit.use_case import CreditSpreadUseCase
from crew.registry import register_use_case

register_use_case(DEFAULT_CONFIG.name, CreditSpreadUseCase, CreditSpreadConfig)


__all__ = [
    "CreditSpreadConfig",
    "CreditSpreadUseCase",
    "DEFAULT_CONFIG",
]
