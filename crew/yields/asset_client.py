from __future__ import annotations
from pathlib import Path
from typing import Dict, Iterable
import pandas as pd
import yfinance as yf
class AllocationAssetClient:
    """Cache-aware price downloader for allocation assets via yfinance."""
    def __init__(self, raw_data_dir: Path) -> None:
        self.base_dir = raw_data_dir / "allocation_assets"
        self.base_dir.mkdir(parents=True, exist_ok=True)
    def get_prices(self, tickers: Iterable[str], period: str) -> pd.DataFrame:
        tickers = list(dict.fromkeys(tickers))
        frames: Dict[str, pd.Series] = {}
        missing: list[str] = []
        for ticker in tickers:
            path = self._path(ticker)
            if path.exists():
                frame = pd.read_parquet(path)
                series = self._extract_close(frame)
                frames[ticker] = series
            else:
                missing.append(ticker)
        if missing:
            downloaded = yf.download(
                missing, period=period, auto_adjust=False, progress=False
            )
            downloaded = downloaded.dropna(how="all")
            if isinstance(downloaded.columns, pd.MultiIndex):
                for ticker in missing:
                    frame = downloaded.xs(ticker, axis=1, level=1)
                    series = self._extract_close(frame)
                    frames[ticker] = series
                    self._store(ticker, frame)
            else:
                series = self._extract_close(downloaded)
                for ticker in missing:
                    frames[ticker] = series.copy()
                    self._store(ticker, downloaded)
        combined = pd.concat(frames.values(), axis=1, keys=frames.keys())
        combined = combined.sort_index().ffill()
        combined.columns = list(frames.keys())
        return combined
    def _path(self, ticker: str) -> Path:
        safe = ticker.replace("/", "-")
        return self.base_dir / f"{safe}.parquet"
    def _store(self, ticker: str, frame: pd.DataFrame) -> None:
        path = self._path(ticker)
        frame.to_parquet(path)
    def _extract_close(self, frame: pd.DataFrame) -> pd.Series:
        if isinstance(frame, pd.Series):
            series = frame.sort_index()
            tz_info = getattr(series.index, "tz", None)
            if tz_info is not None:
                series = series.tz_convert(None)
            return series
        if "Close" in frame.columns:
            series = frame["Close"].copy()
        else:
            series = frame.iloc[:, 0].copy()
        tz_info = getattr(series.index, "tz", None)
        if tz_info is not None:
            series = series.tz_convert(None)
        return series.sort_index()
