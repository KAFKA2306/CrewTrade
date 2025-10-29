from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import yfinance as yf


class PreciousMetalsDataClient:
    def __init__(self, raw_data_dir: Path) -> None:
        self.raw_data_dir = raw_data_dir
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def get_frames(self, tickers: List[str], suffix: str, period: str) -> Dict[str, pd.DataFrame]:
        cached_frames, missing = self._load_cached_frames(tickers, suffix)
        if len(missing) > 0:
            downloaded = self._download_price_frames(missing, period)
            self._store_frames(downloaded, suffix)
            cached_frames.update(downloaded)
        return cached_frames

    def _build_path(self, ticker: str, suffix: str) -> Path:
        return self.raw_data_dir / f"{ticker}_{suffix}.parquet"

    def _load_cached_frames(self, tickers: List[str], suffix: str) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
        frames: Dict[str, pd.DataFrame] = {}
        missing: List[str] = []
        for ticker in tickers:
            path = self._build_path(ticker, suffix)
            if path.exists():
                frames[ticker] = pd.read_parquet(path)
            else:
                missing.append(ticker)
        return frames, missing

    def _download_price_frames(self, tickers: List[str], period: str) -> Dict[str, pd.DataFrame]:
        target = tickers[0] if len(tickers) == 1 else tickers
        frame = yf.download(target, period=period, auto_adjust=False, progress=False)
        if isinstance(frame.columns, pd.MultiIndex):
            frames = {}
            for ticker in tickers:
                ticker_frame = frame.xs(ticker, axis=1, level=1)
                frames[ticker] = ticker_frame
            return frames
        frames = {}
        if len(tickers) == 1:
            frames[tickers[0]] = frame.copy()
            return frames
        for ticker in tickers:
            frames[ticker] = frame.copy()
        return frames

    def _store_frames(self, frames: Dict[str, pd.DataFrame], suffix: str) -> Dict[str, Path]:
        stored_paths: Dict[str, Path] = {}
        for ticker, data_frame in frames.items():
            path = self._build_path(ticker, suffix)
            data_frame.to_parquet(path)
            stored_paths[ticker] = path
        return stored_paths
