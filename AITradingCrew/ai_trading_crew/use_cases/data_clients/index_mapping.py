from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from .toushin_kyokai import ToushinKyokaiDataClient


class IndexETFMappingClient:
    def __init__(self, raw_data_dir: Path, index_keywords: Dict[str, Dict[str, Any]]) -> None:
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path = self.raw_data_dir / "etf_index_mapping.parquet"
        self.index_keywords = index_keywords
        self.toushin_client = ToushinKyokaiDataClient(raw_data_dir)

    def get_mapping(self, force_refresh: bool = False) -> pd.DataFrame:
        if not force_refresh and self.cache_path.exists():
            return pd.read_parquet(self.cache_path)

        etf_master = self.toushin_client.get_etf_master()
        mapping_records = []

        for index_name, index_config in self.index_keywords.items():
            keywords = index_config.get("keywords", [])
            expected_categories = index_config.get("expected_categories", [])
            exclude_keywords = index_config.get("exclude_keywords", [])

            matched_etfs = self._match_etfs(
                etf_master,
                keywords,
                expected_categories,
                exclude_keywords
            )
            for ticker in matched_etfs:
                mapping_records.append({"index_name": index_name, "ticker": ticker})

        mapping_df = pd.DataFrame(mapping_records)
        mapping_df = mapping_df.drop_duplicates()
        mapping_df.to_parquet(self.cache_path, index=False)
        return mapping_df

    def _match_etfs(
        self,
        etf_master: pd.DataFrame,
        keywords: List[str],
        expected_categories: List[str],
        exclude_keywords: List[str]
    ) -> List[str]:
        matched = set()
        for _, row in etf_master.iterrows():
            name = row.get("name", "")
            category = row.get("category", "")
            if not isinstance(name, str):
                continue

            if self._is_hedged(name):
                continue

            if expected_categories and category not in expected_categories:
                continue

            if self._has_exclude_keyword(name, exclude_keywords):
                continue

            name_lower = name.lower()
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in name_lower:
                    matched.add(row["ticker"])
                    break
        return list(matched)

    def _is_hedged(self, name: str) -> bool:
        hedged_keywords = [
            "為替ヘッジあり",
            "為替ヘッジ有",
            "ヘッジあり",
            "ヘッジ有",
            "為替ヘッジ)",
            "(為替ヘッジ",
            "hedged",
            "hedge)",
            "(hedge",
        ]
        name_lower = name.lower()
        for keyword in hedged_keywords:
            if keyword.lower() in name_lower:
                return True
        return False

    def _has_exclude_keyword(self, name: str, exclude_keywords: List[str]) -> bool:
        if not exclude_keywords:
            return False
        name_lower = name.lower()
        for keyword in exclude_keywords:
            if keyword.lower() in name_lower:
                return True
        return False

    def get_etfs_for_index(self, index_name: str) -> List[str]:
        mapping = self.get_mapping()
        filtered = mapping[mapping["index_name"] == index_name]
        return filtered["ticker"].tolist()
