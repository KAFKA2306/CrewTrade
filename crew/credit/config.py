from __future__ import annotations
from typing import Dict, List, Set
from pydantic import BaseModel, Field
from crew.base import UseCaseConfig
class CreditSpreadPair(BaseModel):
    junk_ticker: str
    treasury_ticker: str
    description: str | None = None
class CreditSpreadConfig(UseCaseConfig):
    period: str = Field(default="5y")
    rolling_window: int = Field(default=30)
    minimum_periods: int = Field(default=10)
    z_score_threshold: float = Field(default=1.5)
    pairs: Dict[str, CreditSpreadPair] = Field(
        default_factory=lambda: {
            "HYG_vs_IEF": CreditSpreadPair(
                junk_ticker="HYG",
                treasury_ticker="IEF",
                description="US high yield vs 7-10Y Treasury",
            ),
            "JNK_vs_TLT": CreditSpreadPair(
                junk_ticker="JNK",
                treasury_ticker="TLT",
                description="US high yield vs 20Y Treasury",
            ),
        }
    )
    @property
    def tickers(self) -> List[str]:
        seen: Set[str] = set()
        ordered: List[str] = []
        for pair in self.pairs.values():
            if pair.junk_ticker not in seen:
                ordered.append(pair.junk_ticker)
                seen.add(pair.junk_ticker)
            if pair.treasury_ticker not in seen:
                ordered.append(pair.treasury_ticker)
                seen.add(pair.treasury_ticker)
        return ordered
DEFAULT_CONFIG = CreditSpreadConfig(name="credit_spread")
