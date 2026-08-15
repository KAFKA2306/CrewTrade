from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.quality import assert_quality, validate_batch
from crew.data_platform.sources.fred import parse_fred_series
from crew.data_platform.sources.sec import (
    parse_sec_companyfacts,
    parse_sec_submissions,
)
from crew.data_platform.sources.treasury import parse_treasury_yield_xml
from crew.data_platform.storage import DataPlatformStorage


def test_quality_rejects_duplicate_primary_keys() -> None:
    batch = DatasetBatch(
        dataset="example",
        source="fixture",
        frame=pd.DataFrame(
            [
                {"date": "2026-01-01", "value": 1.0},
                {"date": "2026-01-01", "value": 2.0},
            ]
        ),
        primary_key=("date",),
        source_url="https://example.com/data",
        raw_payload=b"fixture",
    )
    checks = validate_batch(batch)
    assert any(check.name == "primary_key_unique" and not check.passed for check in checks)
    with pytest.raises(ValueError, match="primary_key_unique"):
        assert_quality(checks)


def test_quality_rejects_contract_schema_drift() -> None:
    batch = DatasetBatch(
        dataset="example",
        source="fixture",
        frame=pd.DataFrame([{"id": "A", "value": 200.0, "surprise": "drift"}]),
        primary_key=("id",),
        source_url="https://example.com/data",
        raw_payload=b"fixture",
        metadata={"vintage": "2026-08-15"},
        contract={
            "source": "fixture",
            "primary_key": ["id"],
            "strict_columns": True,
            "required_metadata": ["vintage"],
            "fields": {
                "id": {"type": "string", "nullable": False},
                "value": {"type": "number", "nullable": False, "maximum": 100},
            },
        },
    )

    checks = validate_batch(batch)
    assert any(
        check.name == "contract_no_unexpected_columns" and not check.passed for check in checks
    )
    assert any(check.name == "contract_value_range" and not check.passed for check in checks)
    with pytest.raises(ValueError, match="contract_no_unexpected_columns"):
        assert_quality(checks)


def test_storage_preserves_raw_lineage_and_creates_view(tmp_path: Path) -> None:
    storage = DataPlatformStorage(tmp_path / "platform")
    run_id = "20260804T000000Z-test"
    storage.start_run(run_id, ["fixture"])
    batch = DatasetBatch(
        dataset="test_observations",
        source="fixture",
        frame=pd.DataFrame(
            [
                {"series_id": "X", "date": pd.Timestamp("2026-08-01").date(), "value": 1.25},
                {"series_id": "X", "date": pd.Timestamp("2026-08-02").date(), "value": 1.50},
            ]
        ),
        primary_key=("series_id", "date"),
        source_url="https://example.com/fixture.json",
        raw_payload=b'{"fixture":true}',
        content_type="application/json",
    )
    persisted = storage.persist(run_id, batch)
    manifest = storage.write_manifest(run_id, [persisted])
    storage.finish_run(run_id, status="success")

    assert Path(persisted.raw_path).read_bytes() == b'{"fixture":true}'
    assert Path(persisted.parquet_path).is_file()
    assert manifest.is_file()
    with duckdb.connect(str(storage.catalog_path), read_only=True) as connection:
        assert (
            connection.execute("SELECT count(*) FROM bronze_test_observations").fetchone()[0] == 2
        )
        assert connection.execute("SELECT status FROM ingestion_runs").fetchone()[0] == "success"


def test_parse_fred_series() -> None:
    rows = parse_fred_series(
        label="high_yield_oas",
        series_id="BAMLH0A0HYM2",
        metadata={
            "seriess": [
                {
                    "frequency": "Daily",
                    "units": "Percent",
                    "seasonal_adjustment": "Not Seasonally Adjusted",
                    "last_updated": "2026-08-03 09:00:00-05",
                    "title": "ICE BofA US High Yield Index OAS",
                }
            ]
        },
        observations={
            "observations": [
                {
                    "date": "2026-08-01",
                    "value": "2.84",
                    "realtime_start": "2026-08-04",
                    "realtime_end": "2026-08-04",
                },
                {
                    "date": "2026-08-02",
                    "value": ".",
                    "realtime_start": "2026-08-04",
                    "realtime_end": "2026-08-04",
                },
            ]
        },
    )
    assert len(rows) == 1
    assert rows[0]["value"] == 2.84


def test_parse_treasury_yield_xml() -> None:
    payload = b"""<?xml version='1.0' encoding='utf-8'?>
    <feed xmlns:m='http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
          xmlns:d='http://schemas.microsoft.com/ado/2007/08/dataservices'>
      <entry><content><m:properties>
        <d:NEW_DATE>2026-08-03T00:00:00</d:NEW_DATE>
        <d:BC_2YEAR>4.25</d:BC_2YEAR>
        <d:BC_10YEAR>4.70</d:BC_10YEAR>
      </m:properties></content></entry>
    </feed>"""
    rows = parse_treasury_yield_xml(payload)
    assert {(row["tenor"], row["value"]) for row in rows} == {
        ("2Y", 4.25),
        ("10Y", 4.70),
    }


def test_parse_sec_payloads() -> None:
    submissions = {
        "filings": {
            "recent": {
                "accessionNumber": ["0000000000-26-000001"],
                "filingDate": ["2026-08-01"],
                "reportDate": ["2026-06-30"],
                "acceptanceDateTime": ["20260801120000"],
                "form": ["10-Q"],
                "primaryDocument": ["form10q.htm"],
                "primaryDocDescription": ["FORM 10-Q"],
                "fileNumber": ["001-00001"],
                "isXBRL": [1],
                "isInlineXBRL": [1],
            }
        }
    }
    filing_rows = parse_sec_submissions(
        entity_name="example", cik="0000000001", payload=submissions
    )
    assert filing_rows[0]["form"] == "10-Q"

    facts = {
        "facts": {
            "us-gaap": {
                "RevenueFromContractWithCustomerExcludingAssessedTax": {
                    "label": "Revenue",
                    "description": "Revenue",
                    "units": {
                        "USD": [
                            {
                                "val": 100,
                                "start": "2026-04-01",
                                "end": "2026-06-30",
                                "filed": "2026-08-01",
                                "form": "10-Q",
                                "fy": 2026,
                                "fp": "Q2",
                                "frame": "CY2026Q2",
                                "accn": "0000000000-26-000001",
                            }
                        ]
                    },
                }
            }
        }
    }
    fact_rows = parse_sec_companyfacts(entity_name="example", cik="0000000001", payload=facts)
    assert len(fact_rows) == 1
    assert len(fact_rows[0]["fact_id"]) == 64
    json.dumps(fact_rows[0], default=str)
