from typing import Dict, List
from pydantic import Field
from ai_trading_crew.use_cases.base import UseCaseConfig
from pydantic import BaseModel


class ETFInstrument(BaseModel):
    ticker: str
    metal_symbol: str
    grams_per_unit: float


class PreciousMetalsSpreadConfig(UseCaseConfig):
    period: str = Field(default="2y")
    fx_symbol: str = Field(default="USDJPY=X")
    rolling_window: int = Field(default=20)
    z_score_threshold: float = Field(default=2.0)
    etf_instruments: Dict[str, ETFInstrument] = Field(default_factory=lambda: {
        "1540": ETFInstrument(ticker="1540.T", metal_symbol="XAUUSD=X", grams_per_unit=1.0),
        "1541": ETFInstrument(ticker="1541.T", metal_symbol="XPTUSD=X", grams_per_unit=1.0),
        "1542": ETFInstrument(ticker="1542.T", metal_symbol="XAGUSD=X", grams_per_unit=100.0),
        "1543": ETFInstrument(ticker="1543.T", metal_symbol="XPDUSD=X", grams_per_unit=10.0),
    })

    @property
    def etf_tickers(self) -> List[str]:
        return [instrument.ticker for instrument in self.etf_instruments.values()]

    @property
    def metal_tickers(self) -> List[str]:
        return [instrument.metal_symbol for instrument in self.etf_instruments.values()]


DEFAULT_CONFIG = PreciousMetalsSpreadConfig(name="precious_metals_spread")
