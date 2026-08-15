from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from datetime import date
from html.parser import HTMLParser
from typing import Any

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient

_DEFAULT_URL = "https://www.jpx.co.jp/equities/products/etfs/issues/01.html"
_TICKER_PATTERN = re.compile(r"^[0-9]{3}[A-Z0-9]$")
_MANAGER_PATTERN = re.compile(r"^(?P<name>.*?)(?:\((?P<code>[0-9A-Z]+)\))?$")


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table_depth = 0
        self._rows: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._rows = []
        elif self._table_depth == 1 and tag == "tr":
            self._row = []
        elif self._table_depth == 1 and tag in {"th", "td"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._table_depth == 1 and tag in {"th", "td"} and self._cell is not None:
            assert self._row is not None
            self._row.append(_normalize_text("".join(self._cell)))
            self._cell = None
        elif self._table_depth == 1 and tag == "tr" and self._row is not None:
            if any(self._row):
                assert self._rows is not None
                self._rows.append(self._row)
            self._row = None
        elif tag == "table" and self._table_depth:
            if self._table_depth == 1 and self._rows:
                self.tables.append(self._rows)
                self._rows = None
            self._table_depth -= 1


class JpxEtfMasterSource:
    name = "jpx_etf_master"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = dict(config)
        self.dataset = str(self.config.get("dataset", "jpx_etf_master"))
        self.url = str(self.config.get("url", _DEFAULT_URL))
        self.client = HttpClient(
            user_agent=str(self.config.get("user_agent", "CrewTrade data-platform")),
            min_interval_seconds=float(self.config.get("min_interval_seconds", 0.5)),
            timeout_seconds=float(self.config.get("timeout_seconds", 60)),
            max_attempts=int(self.config.get("max_attempts", 3)),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        payload = self.client.get(self.url, headers={"Accept": "text/html,*/*"})
        as_of_date = payload.retrieved_at.date()
        rows = parse_jpx_etf_master(payload.body, as_of_date=as_of_date)
        if not rows:
            raise ValueError("JPX ETF master page contained no recognized ETF rows")
        frame = pd.DataFrame(rows)
        return [
            DatasetBatch(
                dataset=self.dataset,
                source="jpx",
                frame=frame,
                primary_key=("as_of_date", "ticker"),
                source_url=payload.url,
                raw_payload=payload.body,
                content_type=payload.content_type,
                retrieved_at=payload.retrieved_at,
                metadata={
                    "retrieval_mode": "official_html",
                    "source_page": "JPX ETF issues all",
                    "parsed_rows": len(frame),
                },
            )
        ]


def parse_jpx_etf_master(payload: bytes, *, as_of_date: date) -> list[dict[str, object]]:
    parser = _TableParser()
    parser.feed(payload.decode("utf-8", errors="replace"))
    rows = _find_etf_table(parser.tables)
    parsed: list[dict[str, object]] = []
    seen: set[str] = set()
    for row in rows:
        if len(row) < 7:
            continue
        ticker = _normalize_text(row[1]).upper()
        if not _TICKER_PATTERN.fullmatch(ticker) or ticker in seen:
            continue
        seen.add(ticker)
        manager, manager_search_code = _parse_manager(row[3])
        index_name = _nullable_text(row[0])
        official_name = re.sub(r"\s+iNAV$", "", row[2], flags=re.IGNORECASE).strip()
        trust_fee_text = _nullable_text(row[4])
        market_marker = row[6]
        parsed.append(
            {
                "as_of_date": as_of_date,
                "ticker": ticker,
                "index_name": index_name,
                "official_name": official_name,
                "manager": manager,
                "manager_search_code": manager_search_code,
                "trust_fee_text": trust_fee_text,
                "long_term_flag": "●" in row[5],
                "market_maker_status": (
                    "star" if "★" in market_marker else "circle" if "●" in market_marker else "none"
                ),
            }
        )
    return parsed


def _find_etf_table(tables: Sequence[Sequence[Sequence[str]]]) -> Sequence[Sequence[str]]:
    for table in tables:
        for index, row in enumerate(table):
            normalized = {_normalize_text(value) for value in row}
            if {"連動対象指標", "コード", "名称"}.issubset(normalized) and any(
                value.startswith("管理会社") for value in normalized
            ):
                return table[index + 1 :]
    return []


def _parse_manager(value: str) -> tuple[str, str | None]:
    normalized = _normalize_text(value)
    match = _MANAGER_PATTERN.fullmatch(normalized)
    if not match:
        return normalized, None
    name = _normalize_text(match.group("name"))
    code = match.group("code")
    return name, code


def _nullable_text(value: str) -> str | None:
    normalized = _normalize_text(value)
    return None if normalized in {"", "-", "―", "－"} else normalized


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u3000", " ")).strip()
