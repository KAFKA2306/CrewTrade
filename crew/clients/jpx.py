from __future__ import annotations

import re
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import List

import pandas as pd
import requests

from .ticker_utils import normalize_jpx_ticker


class JPXETFExpenseRatioClient:
    """Downloader for JPX ETF expense ratio tables with simple caching."""

    BASE_URL = "https://www.jpx.co.jp/equities/products/etfs/issues"
    TABLE_PATHS: List[str] = [
        "01-01.html",
        "01-02.html",
        "01-03.html",
        "01-04.html",
        "01-05.html",
        "01-07.html",
        "01-08.html",
        "01-09.html",
    ]
    CACHE_DURATION_DAYS = 30
    RAW_COLUMN_CODE = "コード"
    RAW_COLUMN_EXPENSE = "信託 報酬"
    PERCENT_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]+)?)")

    def __init__(self, raw_data_dir: Path) -> None:
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path = self.raw_data_dir / "jpx_etf_expense_ratios.parquet"

    def get_expense_ratios(self) -> pd.DataFrame:
        if self._is_cache_valid():
            return pd.read_parquet(self.cache_path)

        df = self._download_and_parse()
        df.to_parquet(self.cache_path)
        return df

    def _is_cache_valid(self) -> bool:
        if not self.cache_path.exists():
            return False
        cache_age = datetime.now() - datetime.fromtimestamp(
            self.cache_path.stat().st_mtime
        )
        return cache_age < timedelta(days=self.CACHE_DURATION_DAYS)

    def _download_and_parse(self) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for path_suffix in self.TABLE_PATHS:
            url = f"{self.BASE_URL}/{path_suffix}"
            frame = self._fetch_table(url)
            if frame is None or frame.empty:
                continue
            frame["source_url"] = url
            frames.append(frame)

        if not frames:
            return pd.DataFrame(columns=["ticker", "expense_ratio"])

        combined = pd.concat(frames, ignore_index=True)
        combined = combined.dropna(subset=[self.RAW_COLUMN_CODE])

        combined["ticker"] = combined[self.RAW_COLUMN_CODE].apply(normalize_jpx_ticker)
        combined["expense_ratio"] = combined[self.RAW_COLUMN_EXPENSE].map(
            self._parse_expense_ratio
        )

        result = (
            combined[["ticker", "expense_ratio"]]
            .dropna(subset=["ticker"])
            .drop_duplicates("ticker", keep="first")
        )
        result = result.reset_index(drop=True)
        return result

    def _fetch_table(self, url: str) -> pd.DataFrame | None:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException:
            return None

        response.encoding = response.apparent_encoding
        html_buffer = StringIO(response.text)
        try:
            tables = pd.read_html(html_buffer)
        except ValueError:
            return None
        if not tables:
            return None

        table = tables[0]
        expected_columns = {self.RAW_COLUMN_CODE, self.RAW_COLUMN_EXPENSE}
        if not expected_columns.issubset(set(table.columns)):
            return None
        return table

    def _parse_expense_ratio(self, value) -> float | None:
        if value is None or pd.isna(value):
            return None
        text = str(value).strip()
        if not text or text in {"-", "－", "―"}:
            return None

        text = text.replace("％", "%").replace(" ", "")
        match = self.PERCENT_PATTERN.search(text)
        if not match:
            return None

        try:
            ratio = float(match.group(1))
        except ValueError:
            return None

        if "%" in text:
            ratio /= 100.0
        return ratio if ratio >= 0 else None
