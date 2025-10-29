from __future__ import annotations

from ai_trading_crew.use_cases.registry import register_use_case
from ai_trading_crew.use_cases.securities_collateral_loan.config import DEFAULT_CONFIG, SecuritiesCollateralLoanConfig
from ai_trading_crew.use_cases.securities_collateral_loan.use_case import SecuritiesCollateralLoanUseCase


register_use_case(DEFAULT_CONFIG.name, SecuritiesCollateralLoanUseCase, SecuritiesCollateralLoanConfig)


__all__ = [
    "SecuritiesCollateralLoanConfig",
    "SecuritiesCollateralLoanUseCase",
    "DEFAULT_CONFIG",
]
