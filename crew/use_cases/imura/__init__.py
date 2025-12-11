from crew.use_cases.registry import register_use_case
from .imura_fund_case import ImuraFundUseCase
from .config import ImuraFundConfig

register_use_case("imura", ImuraFundUseCase, ImuraFundConfig)
