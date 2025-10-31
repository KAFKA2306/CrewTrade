from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd

_ADJUSTED_ALIASES: Sequence[str] = (
    "adj close",
    "adj_close",
    "adjusted close",
    "adjusted_close",
    "adjclose",
    "adjusted",
)

_UNADJUSTED_ALIASES: Sequence[str] = (
    "close",
    "last",
    "price",
)


def get_price_series(
    frame: pd.DataFrame,
    *,
    prefer_adjusted: bool = True,
    adjusted_aliases: Iterable[str] = _ADJUSTED_ALIASES,
    unadjusted_aliases: Iterable[str] = _UNADJUSTED_ALIASES,
) -> pd.Series:
    """
    Return a single-column price series from a vendor frame, preferring adjusted closes
    so that splits/dividends do not introduce artificial gaps.
    Falls back to unadjusted closes when adjusted data is unavailable.
    """

    if frame is None or frame.empty:
        raise ValueError("Frame is empty; cannot select price series.")

    search_order = []
    if prefer_adjusted:
        search_order.extend(adjusted_aliases)
    search_order.extend(unadjusted_aliases)

    normalized = frame
    if isinstance(frame.columns, pd.MultiIndex):
        normalized = frame.copy()
        normalized.columns = ["|".join(str(level) for level in col if level is not None) for col in frame.columns]

    columns = {str(col).lower(): col for col in normalized.columns}

    for alias in search_order:
        key = alias.lower()
        if key in columns:
            series = normalized[columns[key]].copy()
            if isinstance(series, pd.DataFrame):
                continue
            tz_info = getattr(series.index, "tz", None)
            if tz_info is not None:
                series = series.tz_convert(None)
            return series.astype(float)

    raise KeyError("No recognized price column found; expected adjusted or close prices.")
