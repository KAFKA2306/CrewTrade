from typing import List, Dict

from crew.base import UseCaseConfig


class LegendaryInvestorsConfig(UseCaseConfig):
    """Configuration for legendary investors portfolio tracking."""

    soros_holdings: List[str] = [
        "AMZN",
        "SW",
        "GOOGL",
        "RSP",
        "TKO",
    ]
    druckenmiller_holdings: List[str] = [
        "NTRA",
        "INSM",
        "TEVA",
        "TSM",
        "WWD",
        "CPNG",
        "MELI",
        "DOCU",
    ]
    period: str = "1y"
    benchmark: str = "SPY"
