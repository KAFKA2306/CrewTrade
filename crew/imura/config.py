from typing import Dict
from crew.base import UseCaseConfig
class ImuraFundConfig(UseCaseConfig):
    days: int
    targets: Dict[str, str]
