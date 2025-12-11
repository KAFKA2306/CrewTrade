from __future__ import annotations

from crew.etf.config import (
    DEFAULT_CONFIG,
    IndexETFComparisonConfig,
)
from crew.etf.use_case import (
    IndexETFComparisonUseCase,
)
from crew.registry import register_use_case

register_use_case(
    DEFAULT_CONFIG.name, IndexETFComparisonUseCase, IndexETFComparisonConfig
)


__all__ = [
    "IndexETFComparisonConfig",
    "IndexETFComparisonUseCase",
    "DEFAULT_CONFIG",
]
