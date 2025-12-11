from __future__ import annotations

from crew.registry import register_use_case
from crew.yields.config import DEFAULT_CONFIG, YieldSpreadConfig
from crew.yields.use_case import YieldSpreadUseCase

register_use_case(DEFAULT_CONFIG.name, YieldSpreadUseCase, YieldSpreadConfig)


__all__ = [
    "YieldSpreadConfig",
    "YieldSpreadUseCase",
    "DEFAULT_CONFIG",
]
