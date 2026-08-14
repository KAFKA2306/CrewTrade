from __future__ import annotations

import pytest

from crew.data_platform.sources.fred import parse_fred_public_csv


@pytest.mark.parametrize("date_header", ["observation_date", "DATE", "date"])
def test_parse_fred_public_csv_date_header_variants(date_header: str) -> None:
    payload = (f"{date_header},DGS10\n2026-08-01,4.70\n2026-08-02,.\n").encode()
    rows = parse_fred_public_csv(
        label="us_10y",
        series_id="DGS10",
        payload=payload,
        retrieval_date="2026-08-04",
    )
    assert len(rows) == 1
    assert str(rows[0]["observation_date"]) == "2026-08-01"
    assert rows[0]["value"] == 4.70
