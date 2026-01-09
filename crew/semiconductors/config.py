from typing import List

from crew.base import UseCaseConfig


class SemiconductorsConfig(UseCaseConfig):
    """Configuration for semiconductor stock analysis."""

    tickers: List[str] = [
        "NVDA",
        "TSM",
        "AVGO",
        "ASML",
        "QCOM",
        "AMD",
        "INTC",
        "LRCX",
        "ADI",
        "MU",
    ]
    period: str = "1y"
    benchmark: str = "SOXX"
