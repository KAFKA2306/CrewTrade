from ai_trading_crew.use_cases.registry import register_use_case
from ai_trading_crew.use_cases.precious_metals_spread.config import PreciousMetalsSpreadConfig, DEFAULT_CONFIG
from ai_trading_crew.use_cases.precious_metals_spread.use_case import PreciousMetalsSpreadUseCase


register_use_case(DEFAULT_CONFIG.name, PreciousMetalsSpreadUseCase, PreciousMetalsSpreadConfig)


__all__ = [
    "PreciousMetalsSpreadConfig",
    "PreciousMetalsSpreadUseCase",
    "DEFAULT_CONFIG",
]
