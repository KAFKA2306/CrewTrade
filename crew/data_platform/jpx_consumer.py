from __future__ import annotations

from pathlib import Path

import pandas as pd

from crew.data_platform.consumer import CanonicalDataUnavailable, query_frame

_REQUIRED_COLUMNS = ("ticker", "official_name", "index_name", "manager")


def jpx_etf_master(*, root: Path | None = None) -> pd.DataFrame:
    """Return the latest validated JPX ETF product-master snapshot.

    Product identity comes only from the canonical ``jpx_etf_master`` dataset.
    Price-vendor ticker suffixes, currency, hedge flags and ISIN are deliberately
    outside this consumer contract.
    """
    frame = query_frame(
        """
        WITH latest AS (
            SELECT max(as_of_date) AS as_of_date
            FROM bronze_jpx_etf_master
        )
        SELECT as_of_date, ticker, official_name, index_name, manager,
               manager_search_code, trust_fee_text, long_term_flag,
               market_maker_status, _retrieved_at, _source_url, _raw_sha256
        FROM bronze_jpx_etf_master
        WHERE as_of_date = (SELECT as_of_date FROM latest)
        ORDER BY ticker
        """,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable("Canonical JPX ETF master is empty")

    missing_columns = [
        column for column in _REQUIRED_COLUMNS if column not in frame.columns
    ]
    if missing_columns:
        raise CanonicalDataUnavailable(
            "Canonical JPX ETF master is missing required columns: "
            + ", ".join(missing_columns)
        )
    if frame[list(_REQUIRED_COLUMNS)].isna().any().any():
        raise CanonicalDataUnavailable(
            "Canonical JPX ETF master contains null product identity"
        )
    if frame["ticker"].duplicated().any():
        raise CanonicalDataUnavailable(
            "Canonical JPX ETF master contains duplicate tickers"
        )
    if frame["as_of_date"].nunique(dropna=False) != 1:
        raise CanonicalDataUnavailable(
            "Canonical JPX ETF master must expose one latest as-of date"
        )

    frame["as_of_date"] = pd.to_datetime(frame["as_of_date"])
    frame["_retrieved_at"] = pd.to_datetime(frame["_retrieved_at"])
    return frame
