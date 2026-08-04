from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from crew.credit.analysis import CreditSpreadAnalyzer
from crew.credit.config import CreditSpreadConfig
from crew.data_platform.consumer import sec_13f_holdings
from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.gold import refresh_gold_views
from crew.data_platform.sources.fred import parse_fred_public_csv
from crew.data_platform.sources.sec import parse_13f_information_table
from crew.data_platform.sources.treasury import build_rates_macro
from crew.data_platform.storage import DataPlatformStorage
from crew.yields.analysis import YieldSpreadAnalyzer
from crew.yields.config import YieldSpreadConfig


def test_parse_fred_public_csv() -> None:
    rows = parse_fred_public_csv(
        label="us_10y",
        series_id="DGS10",
        payload=b"DATE,DGS10\n2026-08-01,4.70\n2026-08-02,.\n",
        retrieval_date="2026-08-04",
    )
    assert len(rows) == 1
    assert rows[0]["value"] == 4.70
    assert str(rows[0]["realtime_start"]) == "2026-08-04"


def test_build_rates_macro_from_treasury_curves() -> None:
    nominal = pd.DataFrame(
        [
            {"observation_date": pd.Timestamp("2026-08-03").date(), "tenor": "2Y", "value": 4.25},
            {"observation_date": pd.Timestamp("2026-08-03").date(), "tenor": "10Y", "value": 4.70},
            {"observation_date": pd.Timestamp("2026-08-03").date(), "tenor": "30Y", "value": 5.23},
        ]
    )
    real = pd.DataFrame(
        [
            {"observation_date": pd.Timestamp("2026-08-03").date(), "tenor": "10Y", "value": 2.15},
        ]
    )
    result = build_rates_macro(
        nominal,
        real,
        retrieval_date="2026-08-04",
    ).set_index("label")
    assert result.loc["us_2y", "value"] == 4.25
    assert result.loc["us_10y_real", "value"] == 2.15
    assert result.loc["us_10y_breakeven", "value"] == pytest.approx(2.55)
    assert set(result.index) == {
        "us_2y",
        "us_10y",
        "us_30y",
        "us_10y_real",
        "us_10y_breakeven",
    }


def test_parse_sec_13f_information_table() -> None:
    payload = b"""<?xml version='1.0' encoding='UTF-8'?>
    <informationTable xmlns='http://www.sec.gov/edgar/document/thirteenf/informationtable'>
      <infoTable>
        <nameOfIssuer>EXAMPLE INC</nameOfIssuer>
        <titleOfClass>COM</titleOfClass>
        <cusip>123456789</cusip>
        <value>250000</value>
        <shrsOrPrnAmt><sshPrnamt>1000</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
        <investmentDiscretion>SOLE</investmentDiscretion>
        <votingAuthority><Sole>1000</Sole><Shared>0</Shared><None>0</None></votingAuthority>
      </infoTable>
    </informationTable>"""
    rows = parse_13f_information_table(
        entity_name="manager",
        cik="0000000001",
        accession_number="0000000001-26-000001",
        report_date="2026-06-30",
        filing_date="2026-08-14",
        source_url="https://www.sec.gov/example.xml",
        payload=payload,
    )
    assert len(rows) == 1
    assert rows[0]["cusip"] == "123456789"
    assert rows[0]["shares_or_principal"] == 1000.0
    assert len(rows[0]["holding_id"]) == 64


def test_latest_13f_gold_view(tmp_path: Path) -> None:
    root = tmp_path / "platform"
    storage = DataPlatformStorage(root)
    run_id = "20260804T000000Z-13f"
    storage.start_run(run_id, ["sec_edgar"])
    frame = pd.DataFrame(
        [
            _holding("old", "2026-03-31", "2026-05-15", 100.0),
            _holding("new", "2026-06-30", "2026-08-14", 200.0),
        ]
    )
    batch = DatasetBatch(
        dataset="sec_13f_holdings",
        source="sec_edgar",
        frame=frame,
        primary_key=("holding_id",),
        source_url="https://www.sec.gov/example.xml",
        raw_payload=b"fixture",
    )
    storage.persist(run_id, batch)
    storage.finish_run(run_id, status="success")
    refresh_gold_views(storage.catalog_path)

    latest = sec_13f_holdings(
        entity_names=["manager"], latest_only=True, root=root
    )
    assert list(latest["holding_id"]) == ["new"]
    assert latest.iloc[0]["reported_value"] == 200.0


def test_credit_analyzer_uses_oas_levels() -> None:
    dates = pd.date_range("2026-01-01", periods=80, freq="D")
    frame = pd.DataFrame(
        {
            "us_corporate_oas": range(80),
            "us_bbb_oas": range(10, 90),
            "us_high_yield_oas": range(20, 100),
        },
        index=dates,
        dtype=float,
    ) / 100
    analyzer = CreditSpreadAnalyzer(
        CreditSpreadConfig(name="credit", minimum_periods=20, rolling_window=30)
    )
    result = analyzer.evaluate({"oas": frame, "provenance": pd.DataFrame()})
    assert set(result["snapshot"]["series"]) == {
        "us_corporate_oas",
        "us_bbb_oas",
        "us_high_yield_oas",
    }
    assert "ratio" not in result["metrics"].columns.get_level_values(1)


def test_yield_analyzer_separates_curve_spreads() -> None:
    dates = pd.date_range("2026-01-01", periods=80, freq="D")
    rates = pd.DataFrame(
        {
            "us_2y": 4.0,
            "us_10y": 4.5,
            "us_30y": 5.0,
            "us_10y_real": 2.0,
            "us_10y_breakeven": 2.5,
        },
        index=dates,
    )
    curve = pd.DataFrame(
        [
            {"observation_date": dates[-1], "tenor": "2Y", "value": 4.0},
            {"observation_date": dates[-1], "tenor": "10Y", "value": 4.5},
            {"observation_date": dates[-1], "tenor": "30Y", "value": 5.0},
        ]
    )
    analyzer = YieldSpreadAnalyzer(
        YieldSpreadConfig(name="yields", minimum_periods=20, rolling_window=30)
    )
    result = analyzer.evaluate(
        {
            "rates": rates,
            "treasury_curve": curve,
            "rates_provenance": pd.DataFrame(),
        }
    )
    snapshot = result["spread_snapshot"].set_index("spread")
    assert snapshot.loc["us_2s10s", "spread_bp"] == 50.0
    assert snapshot.loc["us_10s30s", "spread_bp"] == 50.0


def _holding(
    holding_id: str, report_date: str, filing_date: str, value: float
) -> dict[str, object]:
    return {
        "holding_id": holding_id,
        "entity_name": "manager",
        "entity_cik": "0000000001",
        "accession_number": f"accession-{holding_id}",
        "report_date": pd.Timestamp(report_date).date(),
        "filing_date": pd.Timestamp(filing_date).date(),
        "issuer": "EXAMPLE INC",
        "title_of_class": "COM",
        "cusip": "123456789",
        "figi": None,
        "reported_value": value,
        "reported_value_unit": "SEC_13F_as_filed",
        "shares_or_principal": value,
        "shares_or_principal_type": "SH",
        "put_call": None,
        "investment_discretion": "SOLE",
        "other_manager": None,
        "voting_sole": value,
        "voting_shared": 0.0,
        "voting_none": 0.0,
        "source_document_url": "https://www.sec.gov/example.xml",
    }
