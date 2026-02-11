from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Tuple
import pandas as pd
from .ticker_utils import normalize_text
from .toushin_kyokai import ToushinKyokaiDataClient
class IndexETFMappingClient:
    def __init__(
        self, raw_data_dir: Path, index_keywords: Dict[str, Dict[str, Any]]
    ) -> None:
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path = self.raw_data_dir / "etf_index_mapping.parquet"
        self.index_keywords = index_keywords
        self.toushin_client = ToushinKyokaiDataClient(raw_data_dir)
    def get_mapping(self, force_refresh: bool = False) -> pd.DataFrame:
        if not force_refresh and self.cache_path.exists():
            return pd.read_parquet(self.cache_path)
        etf_master = self.toushin_client.get_etf_master()
        best_matches: Dict[str, Tuple[Tuple[int, int], str]] = {}
        for index_name, index_config in self.index_keywords.items():
            keywords = index_config.get("keywords", [])
            expected_categories = index_config.get("expected_categories", [])
            exclude_keywords = index_config.get("exclude_keywords", [])
            matched_etfs = self._match_etfs(
                etf_master, keywords, expected_categories, exclude_keywords
            )
            for ticker, score in matched_etfs.items():
                current = best_matches.get(ticker)
                candidate = (score, index_name)
                if current is None or candidate > current:
                    best_matches[ticker] = candidate
        mapping_records = [
            {"index_name": index, "ticker": ticker}
            for ticker, (_, index) in best_matches.items()
        ]
        mapping_df = pd.DataFrame(mapping_records)
        mapping_df = mapping_df.drop_duplicates()
        if not mapping_df.empty:
            mapping_df = mapping_df.sort_values(["index_name", "ticker"]).reset_index(
                drop=True
            )
        mapping_df.to_parquet(self.cache_path, index=False)
        return mapping_df
    def _match_etfs(
        self,
        etf_master: pd.DataFrame,
        keywords: List[str],
        expected_categories: List[str],
        exclude_keywords: List[str],
    ) -> Dict[str, Tuple[int, int]]:
        normalized_keywords: List[str] = []
        for keyword in keywords:
            token = normalize_text(keyword)
            if token:
                normalized_keywords.append(token)
        normalized_excludes: List[str] = []
        for keyword in exclude_keywords:
            token = normalize_text(keyword)
            if token:
                normalized_excludes.append(token)
        allowed_categories = {category for category in expected_categories if category}
        matched: Dict[str, Tuple[int, int]] = {}
        for _, row in etf_master.iterrows():
            name = row.get("name", "")
            category = row.get("category", "")
            ticker = row.get("ticker")
            normalized_name = normalize_text(name)
            if not normalized_name or not ticker:
                continue
            if allowed_categories and category not in allowed_categories:
                continue
            if normalized_excludes and self._contains_any(
                normalized_name, normalized_excludes
            ):
                continue
            score = self._match_score(normalized_name, normalized_keywords)
            if score == (0, 0):
                continue
            current = matched.get(ticker)
            if current is None or score > current:
                matched[ticker] = score
        return matched
    def _contains_any(self, normalized_name: str, keywords: List[str]) -> bool:
        return any(keyword in normalized_name for keyword in keywords)
    def _match_score(
        self, normalized_name: str, keywords: List[str]
    ) -> Tuple[int, int]:
        matched = [keyword for keyword in keywords if keyword in normalized_name]
        if not matched:
            return (0, 0)
        length = sum(len(keyword.replace(" ", "")) for keyword in matched)
        return (len(matched), length)
    def get_etfs_for_index(self, index_name: str) -> List[str]:
        mapping = self.get_mapping()
        filtered = mapping[mapping["index_name"] == index_name]
        return filtered["ticker"].tolist()
