from __future__ import annotations

from crew.loan.config import (
    DEFAULT_CONFIG,
    SecuritiesCollateralLoanConfig,
)
from crew.loan.use_case import SecuritiesCollateralLoanUseCase
from crew.registry import register_use_case

register_use_case(
    DEFAULT_CONFIG.name, SecuritiesCollateralLoanUseCase, SecuritiesCollateralLoanConfig
)


__all__ = [
    "SecuritiesCollateralLoanConfig",
    "SecuritiesCollateralLoanUseCase",
    "DEFAULT_CONFIG",
]
