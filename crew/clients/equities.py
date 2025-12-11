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

    def get_frames(
        self,
        tickers: Iterable[str],
        period: str | None = None,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
    ) -> Dict[str, pd.DataFrame]:
        requested: List[str] = list(
            dict.fromkeys(ticker for ticker in tickers if ticker)
        )
        cached_frames, missing = self._load_cached(requested)
        if missing:
            downloaded = self._download_price_frames(missing)
            self._store_frames(downloaded)
            cached_frames.update(downloaded)

        sliced_frames: Dict[str, pd.DataFrame] = {}
        start_ts = pd.Timestamp(start) if start is not None else None
        end_ts = pd.Timestamp(end) if end is not None else None
        for ticker, frame in cached_frames.items():
            df = frame.copy()
            if start_ts is not None or end_ts is not None:
                df = df.loc[start_ts:end_ts]
            elif period is not None:
                offset = self._period_to_offset(period)
                if offset is not None and not df.empty:
                    end_ts = df.index.max()
                    start_ts_calc = end_ts - offset
                    df = df.loc[start_ts_calc:end_ts]
            sliced_frames[ticker] = df
        return sliced_frames

    def _path(self, ticker: str) -> Path:
        safe = ticker.replace("/", "-")
        return self.raw_data_dir / f"{safe}.parquet"

    def _load_cached(
        self, tickers: List[str]
    ) -> tuple[Dict[str, pd.DataFrame], List[str]]:
        frames: Dict[str, pd.DataFrame] = {}
        missing: List[str] = []
        for ticker in tickers:
            path = self._path(ticker)
            if path.exists():
                frames[ticker] = pd.read_parquet(path)
            else:
                missing.append(ticker)
        return frames, missing

    def _download_price_frames(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        if not tickers:
            return {}
        frame = yf.download(tickers, period="max", auto_adjust=False, progress=False)
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

    def _period_to_offset(self, period: str | None) -> pd.Timedelta | None:
        if period is None:
            return None
        period = period.strip().lower()
        if not period:
            return None
        try:
            unit = period[-1]
            value = float(period[:-1]) if period[:-1] else 1.0
        except ValueError:
            return None

        if unit == "y":
            return pd.Timedelta(days=365 * value)
        if unit == "m":
            return pd.Timedelta(days=30 * value)
        if unit == "d":
            return pd.Timedelta(days=value)
        return None
