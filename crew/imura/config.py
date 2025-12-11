from typing import Dict

from crew.base import UseCaseConfig


class ImuraFundConfig(UseCaseConfig):
    days: int = 365
    targets: Dict[str, str] = {
        "Fundnote_Kaihou": "BK311251",
        "Nikkei225_Proxy": "998407.O",
        "JPX400_ETF": "1591.T",
        "TSE_Growth250_ETF": "2516.T",
        "NASDAQ100_ETF": "1545.T",
    }
