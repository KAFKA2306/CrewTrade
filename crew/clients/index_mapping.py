from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pandas as pd

from .ticker_utils import normalize_jpx_ticker, normalize_text

_REQUIRED_MASTER_COLUMNS = {"ticker", "official_name", "index_name", "manager"}


class IndexETFMappingClient:
    """Map comparison labels to products using only official JPX master fields."""

    def __init__(self, index_keywords: Dict[str, Dict[str, Any]]) -> None:
        self.index_keywords = index_keywords

    def get_mapping(self, etf_master: pd.DataFrame) -> pd.DataFrame:
        missing = sorted(_REQUIRED_MASTER_COLUMNS - set(etf_master.columns))
        if missing:
            raise ValueError(f"JPX ETF master missing required columns: {', '.join(missing)}")

        best_matches: Dict[str, Tuple[Tuple[int, int, int], str, str]] = {}
        for comparison_name, index_config in self.index_keywords.items():
            keywords = index_config.get("keywords", [])
            exclude_keywords = index_config.get("exclude_keywords", [])
            matched_etfs = self._match_etfs(etf_master, keywords, exclude_keywords)
            for official_ticker, score in matched_etfs.items():
                market_ticker = normalize_jpx_ticker(official_ticker)
                if not market_ticker:
                    continue
                current = best_matches.get(market_ticker)
                candidate = (score, comparison_name, official_ticker)
                if current is None or candidate > current:
                    best_matches[market_ticker] = candidate

        records = [
            {
                "index_name": comparison_name,
                "ticker": market_ticker,
                "official_ticker": official_ticker,
            }
            for market_ticker, (_, comparison_name, official_ticker) in best_matches.items()
        ]
        mapping = pd.DataFrame(records, columns=["index_name", "ticker", "official_ticker"])
        if not mapping.empty:
            mapping = mapping.drop_duplicates().sort_values(
                ["index_name", "ticker"]
            ).reset_index(drop=True)
        return mapping

    def _match_etfs(
        self,
        etf_master: pd.DataFrame,
        keywords: List[str],
        exclude_keywords: List[str],
    ) -> Dict[str, Tuple[int, int, int]]:
        normalized_keywords = [
            token for keyword in keywords if (token := normalize_text(keyword))
        ]
        normalized_excludes = [
            token for keyword in exclude_keywords if (token := normalize_text(keyword))
        ]
        matched: Dict[str, Tuple[int, int, int]] = {}

        for _, row in etf_master.iterrows():
            official_ticker = str(row.get("ticker", "")).strip().upper()
            index_text = normalize_text(row.get("index_name", ""))
            name_text = normalize_text(row.get("official_name", ""))
            searchable = f"{index_text} {name_text}".strip()
            if not official_ticker or not searchable:
                continue
            if normalized_excludes and self._contains_any(searchable, normalized_excludes):
                continue
            score = self._match_score(index_text, name_text, normalized_keywords)
            if score == (0, 0, 0):
                continue
            current = matched.get(official_ticker)
            if current is None or score > current:
                matched[official_ticker] = score
        return matched

    @staticmethod
    def _contains_any(text: str, keywords: List[str]) -> bool:
        return any(keyword in text for keyword in keywords)

    @staticmethod
    def _match_score(
        index_text: str, name_text: str, keywords: List[str]
    ) -> Tuple[int, int, int]:
        index_matches = [keyword for keyword in keywords if keyword in index_text]
        name_matches = [keyword for keyword in keywords if keyword in name_text]
        all_matches = set(index_matches + name_matches)
        if not all_matches:
            return (0, 0, 0)
        matched_length = sum(len(keyword.replace(" ", "")) for keyword in all_matches)
        return (len(index_matches), len(all_matches), matched_length)

    def get_etfs_for_index(self, index_name: str, etf_master: pd.DataFrame) -> List[str]:
        mapping = self.get_mapping(etf_master)
        return mapping[mapping["index_name"] == index_name]["ticker"].tolist()
