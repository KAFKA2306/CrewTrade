from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

from .ticker_utils import normalize_jpx_ticker, normalize_text

CATEGORY_KEYWORDS = [
    ("REIT", tuple(normalize_text(x) for x in ["リート", "REIT", "不動産"])),
    (
        "債券",
        tuple(
            normalize_text(x)
            for x in ["債券", "国債", "トレジャリー", "ボンド", "bond"]
        ),
    ),
    (
        "コモディティ",
        tuple(
            normalize_text(x)
            for x in [
                "金",
                "銀",
                "プラチナ",
                "パラジウム",
                "原油",
                "コモディティ",
                "商品",
            ]
        ),
    ),
    (
        "国内セクター",
        tuple(
            normalize_text(x)
            for x in [
                "食品",
                "エネルギー",
                "素材",
                "化学",
                "医薬品",
                "自動車",
                "輸送機",
                "鉄鋼",
                "非鉄",
                "機械",
                "電機",
                "情報通信",
                "サービス",
                "電力",
                "ガス",
                "運輸",
                "物流",
                "商社",
                "小売",
                "銀行",
                "証券",
                "保険",
                "金融",
            ]
        ),
    ),
    (
        "国内株式",
        tuple(
            normalize_text(x)
            for x in [
                "TOPIX",
                "日経",
                "JPX",
                "東証",
                "225",
                "グロース",
                "スタンダード",
                "ジャパン",
                "日本株",
                "日本",
            ]
        ),
    ),
    (
        "海外株式",
        tuple(
            normalize_text(x)
            for x in [
                "s&p",
                "nasdaq",
                "nyダウ",
                "ダウ",
                "米国",
                "アメリカ",
                "world",
                "先進国",
                "kokusai",
                "acwi",
                "新興国",
                "エマージング",
                "海外",
                "グローバル",
                "欧州",
                "アジア",
                "中国",
                "インド",
                "ブラジル",
                "豪州",
            ]
        ),
    ),
]


class ToushinKyokaiDataClient:
    EXCEL_URL = (
        "https://www.toushin.or.jp/files/static/486/listed_fund_for_investor.xlsx"
    )
    CACHE_DURATION_DAYS = 30

    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path = self.raw_data_dir / "toushin_etf_master.parquet"
        self.excel_path = (
            self.raw_data_dir.parent.parent.parent
            / "resources"
            / "reference"
            / "toushin_etf_list.xlsx"
        )

    def get_etf_master(self) -> pd.DataFrame:
        if self._is_cache_valid():
            return pd.read_parquet(self.cache_path)

        df = self._load_and_parse_excel()
        df.to_parquet(self.cache_path)
        return df

    def _is_cache_valid(self) -> bool:
        if not self.cache_path.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(
            self.cache_path.stat().st_mtime
        )
        return cache_age < timedelta(days=self.CACHE_DURATION_DAYS)

    def _load_and_parse_excel(self) -> pd.DataFrame:
        self.excel_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.excel_path.exists():
            response = requests.get(self.EXCEL_URL, timeout=30)
            response.raise_for_status()
            self.excel_path.write_bytes(response.content)

        df = pd.read_excel(self.excel_path, sheet_name="対象商品一覧", header=1)

        etf_only = df[df["上場投信・上場投資法人の別"] == "上場投信"].copy()

        etf_only["ticker"] = etf_only["銘柄コード"].apply(normalize_jpx_ticker)
        etf_only["name"] = etf_only["ファンド名称"]
        etf_only["provider"] = etf_only["運用会社名"]
        etf_only["category"] = etf_only["name"].apply(self._infer_category)

        result = etf_only[["ticker", "name", "provider", "category"]].copy()
        result = result.dropna(subset=["ticker"])
        result = result.drop_duplicates(subset=["ticker"], keep="first")

        return result

    @staticmethod
    def _infer_category(name: str) -> str:
        normalized = normalize_text(name)
        if not normalized:
            return "その他"
        for category, keywords in CATEGORY_KEYWORDS:
            if any(token in normalized for token in keywords):
                return category
        return "その他"
