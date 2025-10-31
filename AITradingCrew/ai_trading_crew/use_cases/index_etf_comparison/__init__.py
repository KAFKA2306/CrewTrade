from __future__ import annotations

from ai_trading_crew.use_cases.registry import register_use_case
from ai_trading_crew.use_cases.index_etf_comparison.config import DEFAULT_CONFIG, IndexETFComparisonConfig
from ai_trading_crew.use_cases.index_etf_comparison.use_case import IndexETFComparisonUseCase


register_use_case(DEFAULT_CONFIG.name, IndexETFComparisonUseCase, IndexETFComparisonConfig)


__all__ = [
    "IndexETFComparisonConfig",
    "IndexETFComparisonUseCase",
    "DEFAULT_CONFIG",
]
