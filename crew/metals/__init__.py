from crew.metals.config import (
    DEFAULT_CONFIG,
    PreciousMetalsSpreadConfig,
)
from crew.metals.use_case import PreciousMetalsSpreadUseCase
from crew.registry import register_use_case

register_use_case(
    DEFAULT_CONFIG.name, PreciousMetalsSpreadUseCase, PreciousMetalsSpreadConfig
)


__all__ = [
    "PreciousMetalsSpreadConfig",
    "PreciousMetalsSpreadUseCase",
    "DEFAULT_CONFIG",
]
