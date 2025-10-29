from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
import yfinance as yf


class YFinanceEquityDataClient:
    """Cache-aware yfinance downloader for equity/ETF price series."""

    def __init__(self, raw_data_dir: Path) -> None:
        self.raw_data_dir = raw_data_dir
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def get_frames(self, tickers: Iterable[str], period: str) -> Dict[str, pd.DataFrame]:
        requested: List[str] = list(dict.fromkeys(ticker for ticker in tickers if ticker))
        cached_frames, missing = self._load_cached(requested)
        if missing:
            downloaded = self._download_price_frames(missing, period)
            self._store_frames(downloaded)
            cached_frames.update(downloaded)
        return cached_frames

    def _path(self, ticker: str) -> Path:
        safe = ticker.replace("/", "-")
        return self.raw_data_dir / f"{safe}.parquet"

    def _load_cached(self, tickers: List[str]) -> tuple[Dict[str, pd.DataFrame], List[str]]:
        frames: Dict[str, pd.DataFrame] = {}
        missing: List[str] = []
        for ticker in tickers:
            path = self._path(ticker)
            if path.exists():
                frames[ticker] = pd.read_parquet(path)
            else:
                missing.append(ticker)
        return frames, missing

    def _download_price_frames(self, tickers: List[str], period: str) -> Dict[str, pd.DataFrame]:
        if not tickers:
            return {}
        frame = yf.download(tickers, period=period, auto_adjust=False, progress=False)
        frame = frame.dropna(how="all")
        if isinstance(frame.columns, pd.MultiIndex):
            downloaded: Dict[str, pd.DataFrame] = {}
            for ticker in tickers:
                try:
                    ticker_frame = frame.xs(ticker, axis=1, level=1)
                except KeyError:
                    continue
                downloaded[ticker] = ticker_frame
            return downloaded
        downloaded = {}
        for ticker in tickers:
            downloaded[ticker] = frame.copy()
        return downloaded

    def _store_frames(self, frames: Dict[str, pd.DataFrame]) -> None:
        for ticker, frame in frames.items():
            path = self._path(ticker)
            frame.to_parquet(path)
