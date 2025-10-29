from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Literal, Optional, Tuple

import pandas as pd
import pandas_datareader.data as fred_data
import yfinance as yf

SourceType = Literal["fred", "yfinance"]


@dataclass(frozen=True)
class YieldSeriesRequest:
    source: SourceType
    identifier: str
    scaling: float = 1.0
    field: str = "Close"


class YieldSpreadDataClient:
    """Fetch and cache yield time series from FRED (via pandas_datareader) and yfinance."""

    def __init__(self, raw_data_dir: Path) -> None:
        self.raw_data_dir = raw_data_dir
        self.fred_dir = raw_data_dir / "fred"
        self.yf_dir = raw_data_dir / "yfinance"
        self.fred_dir.mkdir(parents=True, exist_ok=True)
        self.yf_dir.mkdir(parents=True, exist_ok=True)

    def fetch_series(
        self,
        requests: Iterable[YieldSeriesRequest],
        start_date: datetime,
        period: str,
    ) -> Dict[str, pd.Series]:
        frames: Dict[str, pd.Series] = {}
        for request in requests:
            if request.source == "fred":
                frames[request.identifier] = self._get_fred_series(request, start_date)
            else:
                frames[request.identifier] = self._get_yfinance_series(request, period)
        return frames

    def _get_fred_series(self, request: YieldSeriesRequest, start_date: datetime) -> pd.Series:
        path = self._fred_path(request.identifier)
        if path.exists():
            series = pd.read_parquet(path)["value"]
        else:
            data = fred_data.DataReader(request.identifier, "fred", start_date)
            series = data[request.identifier] if request.identifier in data.columns else data.squeeze("columns")
            series = series.dropna()
            series.to_frame(name="value").to_parquet(path)
        series = series.sort_index()
        return series * request.scaling

    def _get_yfinance_series(self, request: YieldSeriesRequest, period: str) -> pd.Series:
        path = self._yfinance_path(request.identifier)
        if path.exists():
            frame = pd.read_parquet(path)
        else:
            frame = yf.download(request.identifier, period=period, auto_adjust=False, progress=False)
            frame = frame.dropna(how="all")
            frame.to_parquet(path)
        series = frame[request.field].copy()
        tz_info = getattr(series.index, "tz", None)
        if tz_info is not None:
            series = series.tz_convert(None)
        series = series.sort_index()
        return series * request.scaling

    def _fred_path(self, identifier: str) -> Path:
        return self.fred_dir / f"{identifier}.parquet"

    def _yfinance_path(self, identifier: str) -> Path:
        return self.yf_dir / f"{identifier}.parquet"
