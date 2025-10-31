from __future__ import annotations

from typing import Dict, List

from pydantic import Field

from ai_trading_crew.use_cases.base import UseCaseConfig


INDEX_KEYWORDS: Dict[str, List[str]] = {
    "JPX/S&P 設備・人材投資指数": ["設備", "人材投資", "capex"],
    "iSTOXX MUTB 積極投資企業200": ["積極投資", "istoxx", "mutb"],
    "FTSE世界国債": ["ftse", "世界国債", "除く日本"],
    "S&P500": ["s&p500", "s&p 500", "spx"],
    "東証REIT Core": ["reit", "core", "東証reit core"],
    "MSCI ジャパン高配当": ["msci", "高配当", "japan", "dividend"],
    "MSCI日本株最小分散": ["msci", "最小分散", "minimum variance"],
    "MSCIエマージング": ["msci", "エマージング", "emerging"],
    "JPX日経400": ["jpx", "日経400", "nikkei 400"],
    "野村企業価値分配": ["野村", "企業価値分配", "neva"],
    "野村高利回りJリート": ["野村", "高利回り", "jリート", "j-reit"],
    "情報通信サービス": ["情報通信", "サービス", "it", "通信"],
    "LBMA金": ["金", "ゴールド", "gold", "lbma"],
    "NASDAQ100": ["nasdaq", "ナスダック"],
    "TOPIX-17 小売": ["topix", "小売", "retail"],
    "東証配当フォーカス100": ["配当フォーカス", "dividend focus"],
    "東証REIT配当込": ["reit", "配当込", "東証reit指数"],
    "ブルームバーグ米国国債": ["bloomberg", "米国国債", "us treasury", "ブルームバーグ"],
    "ブルームバーグ・フランス国債": ["bloomberg", "フランス国債", "france", "ブルームバーグ"],
}


class IndexETFComparisonConfig(UseCaseConfig):
    indices: List[str] = Field(default_factory=lambda: list(INDEX_KEYWORDS.keys()))
    lookback: str = Field(default="max")
    min_data_points: int = Field(default=252, gt=0)


DEFAULT_CONFIG = IndexETFComparisonConfig(
    name="index_etf_comparison",
)
