from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import yfinance as yf


class FixedIncomeDataClient:
    """Cache-aware price downloader for bond ETFs via yfinance."""

    def __init__(self, raw_data_dir: Path) -> None:
        self.raw_data_dir = raw_data_dir
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def get_frames(self, tickers: List[str], period: str) -> Dict[str, pd.DataFrame]:
        cached_frames, missing = self._load_cached_frames(tickers)
        if missing:
            downloaded = self._download_price_frames(missing, period)
            self._store_frames(downloaded)
            cached_frames.update(downloaded)
        return cached_frames

    def _build_path(self, ticker: str) -> Path:
        return self.raw_data_dir / f"{ticker}.parquet"

    def _load_cached_frames(self, tickers: List[str]) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
        frames: Dict[str, pd.DataFrame] = {}
        missing: List[str] = []
        for ticker in tickers:
            path = self._build_path(ticker)
            if path.exists():
                frames[ticker] = pd.read_parquet(path)
            else:
                missing.append(ticker)
        return frames, missing

    def _download_price_frames(self, tickers: List[str], period: str) -> Dict[str, pd.DataFrame]:
        if not tickers:
            return {}
        target = tickers[0] if len(tickers) == 1 else tickers
        frame = yf.download(target, period=period, auto_adjust=False, progress=False)
        if isinstance(frame.columns, pd.MultiIndex):
            downloaded = {}
            for ticker in tickers:
                downloaded[ticker] = frame.xs(ticker, axis=1, level=1)
            return downloaded
        if len(tickers) == 1:
            return {tickers[0]: frame.copy()}
        return {ticker: frame.copy() for ticker in tickers}

    def _store_frames(self, frames: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        stored_paths: Dict[str, Path] = {}
        for ticker, frame in frames.items():
            path = self._build_path(ticker)
            frame.to_parquet(path)
            stored_paths[ticker] = path
        return stored_paths
