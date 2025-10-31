from __future__ import annotations

from typing import Dict, List, Any

from pydantic import Field

from ai_trading_crew.use_cases.base import UseCaseConfig


INDEX_KEYWORDS: Dict[str, Dict[str, Any]] = {
    "JPX/S&P 設備・人材投資指数": {
        "keywords": ["設備", "人材投資", "capex"],
        "expected_categories": ["国内株式", "国内セクター"],
        "exclude_keywords": [],
    },
    "iSTOXX MUTB 積極投資企業200": {
        "keywords": ["積極投資", "istoxx", "mutb"],
        "expected_categories": ["国内株式", "国内セクター"],
        "exclude_keywords": [],
    },
    "FTSE世界国債": {
        "keywords": ["ftse", "世界国債", "除く日本"],
        "expected_categories": ["債券"],
        "exclude_keywords": ["株式", "株", "equity", "reit"],
    },
    "S&P500": {
        "keywords": ["s&p500", "s&p 500", "spx"],
        "expected_categories": ["海外株式"],
        "exclude_keywords": ["債券", "bond", "reit", "配当", "貴族", "半導体", "キャッシュ", "トップ", "均等", "イコール", "equal", "aristocrat", "cash", "semiconductor", "top"],
    },
    "東証REIT Core": {
        "keywords": ["reit", "core", "東証reit core"],
        "expected_categories": ["REIT"],
        "exclude_keywords": ["株式", "債券"],
    },
    "MSCI ジャパン高配当": {
        "keywords": ["msci", "高配当", "japan", "dividend"],
        "expected_categories": ["国内株式", "国内セクター"],
        "exclude_keywords": ["reit", "債券", "bond"],
    },
    "MSCI日本株最小分散": {
        "keywords": ["msci", "最小分散", "minimum variance"],
        "expected_categories": ["国内株式"],
        "exclude_keywords": [],
    },
    "MSCIエマージング": {
        "keywords": ["エマージング", "新興国株式", "emerging"],
        "expected_categories": ["海外株式"],
        "exclude_keywords": ["債券", "bond", "固定", "kokusai", "先進国"],
    },
    "新興国債券": {
        "keywords": ["新興国", "債券", "emerging", "bond"],
        "expected_categories": ["債券"],
        "exclude_keywords": ["株式", "株", "equity", "reit"],
    },
    "JPX日経400": {
        "keywords": ["jpx", "日経400", "nikkei 400"],
        "expected_categories": ["国内株式"],
        "exclude_keywords": [],
    },
    "野村企業価値分配": {
        "keywords": ["野村", "企業価値分配", "neva"],
        "expected_categories": ["国内株式"],
        "exclude_keywords": [],
    },
    "野村高利回りJリート": {
        "keywords": ["野村", "高利回り", "jリート", "j-reit"],
        "expected_categories": ["REIT"],
        "exclude_keywords": ["株式", "債券"],
    },
    "情報通信サービス": {
        "keywords": ["情報通信・サービス", "情報通信サービス"],
        "expected_categories": ["国内株式", "国内セクター"],
        "exclude_keywords": [],
    },
    "LBMA金": {
        "keywords": ["金", "ゴールド", "gold", "lbma"],
        "expected_categories": ["コモディティ"],
        "exclude_keywords": ["株式", "債券", "reit"],
    },
    "NASDAQ100": {
        "keywords": ["nasdaq", "ナスダック"],
        "expected_categories": ["海外株式"],
        "exclude_keywords": ["債券", "bond", "reit", "トップ", "top"],
    },
    "TOPIX-17 小売": {
        "keywords": ["小売", "retail"],
        "expected_categories": ["国内株式", "国内セクター"],
        "exclude_keywords": [],
    },
    "東証配当フォーカス100": {
        "keywords": ["配当フォーカス", "dividend focus"],
        "expected_categories": ["国内株式"],
        "exclude_keywords": ["reit"],
    },
    "東証REIT配当込": {
        "keywords": ["reit", "配当込", "東証reit指数"],
        "expected_categories": ["REIT"],
        "exclude_keywords": ["株式", "債券"],
    },
    "ブルームバーグ米国国債": {
        "keywords": ["bloomberg", "米国国債", "us treasury", "ブルームバーグ"],
        "expected_categories": ["債券"],
        "exclude_keywords": ["株式", "株", "equity", "reit"],
    },
    "ブルームバーグ・フランス国債": {
        "keywords": ["bloomberg", "フランス国債", "france", "ブルームバーグ"],
        "expected_categories": ["債券"],
        "exclude_keywords": ["株式", "株", "equity", "reit"],
    },
}


class IndexETFComparisonConfig(UseCaseConfig):
    indices: List[str] = Field(default_factory=lambda: list(INDEX_KEYWORDS.keys()))
    lookback: str = Field(default="max")
    min_data_points: int = Field(default=252, gt=0)


DEFAULT_CONFIG = IndexETFComparisonConfig(
    name="index_etf_comparison",
)
