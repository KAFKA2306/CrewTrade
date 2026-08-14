from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

import duckdb
import pandas as pd


class CanonicalDataUnavailable(RuntimeError):
    """Raised when a canonical dataset has not been materialized yet."""


def resolve_root(root: Path | None = None) -> Path:
    if root is not None:
        return Path(root)
    configured = os.environ.get("CREWTRADE_DATA_ROOT", "data/platform").strip()
    return Path(configured or "data/platform")


def resolve_catalog(root: Path | None = None) -> Path:
    catalog = resolve_root(root) / "catalog.duckdb"
    if not catalog.is_file():
        raise CanonicalDataUnavailable(
            f"Canonical catalogue is missing: {catalog}. Run `crew-data sync` first."
        )
    return catalog


def query_frame(
    sql: str,
    parameters: Iterable[object] | None = None,
    *,
    root: Path | None = None,
) -> pd.DataFrame:
    catalog = resolve_catalog(root)
    try:
        with duckdb.connect(str(catalog), read_only=True) as connection:
            return connection.execute(sql, list(parameters or [])).fetchdf()
    except duckdb.CatalogException as error:
        raise CanonicalDataUnavailable(str(error)) from error


def latest_vintage_series(dataset: str, *, root: Path | None = None) -> pd.DataFrame:
    if dataset not in {"credit_oas", "rates_macro"}:
        raise ValueError(f"Unsupported series dataset: {dataset}")
    frame = query_frame(
        f"""
        WITH ranked AS (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY series_id, observation_date
                       ORDER BY realtime_start DESC, _retrieved_at DESC
                   ) AS vintage_rank
            FROM bronze_{dataset}
        )
        SELECT series_id, label, observation_date, value, realtime_start,
               realtime_end, units, title, _retrieved_at, _source_url,
               _raw_sha256
        FROM ranked
        WHERE vintage_rank = 1
        ORDER BY observation_date, label
        """,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable(f"Canonical dataset is empty: {dataset}")
    frame["observation_date"] = pd.to_datetime(frame["observation_date"])
    return frame


def pivot_latest_vintage(dataset: str, *, root: Path | None = None) -> pd.DataFrame:
    long_frame = latest_vintage_series(dataset, root=root)
    pivot = long_frame.pivot_table(
        index="observation_date",
        columns="label",
        values="value",
        aggfunc="last",
    ).sort_index()
    pivot.index.name = "Date"
    return pivot


def treasury_curve(*, latest_only: bool = False, root: Path | None = None) -> pd.DataFrame:
    view = "gold_treasury_curve_latest" if latest_only else "bronze_treasury_par_yield_curve"
    frame = query_frame(
        f"""
        SELECT observation_date, tenor, value, unit, curve_type,
               _retrieved_at, _source_url, _raw_sha256
        FROM {view}
        ORDER BY observation_date, tenor
        """,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable("Canonical Treasury curve is empty")
    frame["observation_date"] = pd.to_datetime(frame["observation_date"])
    return frame


def sec_filings(
    *,
    entity_names: Iterable[str] | None = None,
    forms: Iterable[str] | None = None,
    root: Path | None = None,
) -> pd.DataFrame:
    clauses: list[str] = []
    parameters: list[object] = []
    names = list(entity_names or [])
    form_values = list(forms or [])
    if names:
        clauses.append("entity_name IN (" + ",".join("?" for _ in names) + ")")
        parameters.extend(names)
    if form_values:
        clauses.append("form IN (" + ",".join("?" for _ in form_values) + ")")
        parameters.extend(form_values)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    frame = query_frame(
        f"""
        SELECT entity_name, entity_cik, accession_number, filing_date,
               report_date, acceptance_datetime, form, primary_document,
               primary_doc_description, _retrieved_at, _source_url,
               _raw_sha256
        FROM bronze_sec_filings
        {where}
        ORDER BY filing_date DESC, acceptance_datetime DESC
        """,
        parameters,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable("No matching SEC filings are available")
    for column in (
        "filing_date",
        "report_date",
        "acceptance_datetime",
        "_retrieved_at",
    ):
        frame[column] = pd.to_datetime(frame[column])
    return frame


def sec_company_facts(
    *,
    entity_name: str,
    concepts: Iterable[str] | None = None,
    root: Path | None = None,
) -> pd.DataFrame:
    clauses = ["entity_name = ?"]
    parameters: list[object] = [entity_name]
    concept_values = list(concepts or [])
    if concept_values:
        clauses.append("concept IN (" + ",".join("?" for _ in concept_values) + ")")
        parameters.extend(concept_values)
    frame = query_frame(
        f"""
        SELECT fact_id, entity_name, entity_cik, taxonomy, concept, label,
               unit, value, start_date, end_date, filed_date, form,
               fiscal_year, fiscal_period, frame, accession_number,
               _retrieved_at, _source_url, _raw_sha256
        FROM bronze_sec_company_facts
        WHERE {" AND ".join(clauses)}
        ORDER BY end_date DESC NULLS LAST, filed_date DESC NULLS LAST
        """,
        parameters,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable(f"No SEC company facts for {entity_name}")
    for column in ("start_date", "end_date", "filed_date", "_retrieved_at"):
        frame[column] = pd.to_datetime(frame[column])
    return frame


def sec_13f_holdings(
    *,
    entity_names: Iterable[str] | None = None,
    latest_only: bool = False,
    root: Path | None = None,
) -> pd.DataFrame:
    view = "gold_sec_13f_holdings_latest" if latest_only else "bronze_sec_13f_holdings"
    names = list(entity_names or [])
    where = ""
    parameters: list[object] = []
    if names:
        where = "WHERE entity_name IN (" + ",".join("?" for _ in names) + ")"
        parameters.extend(names)
    frame = query_frame(
        f"""
        SELECT holding_id, entity_name, entity_cik, accession_number,
               report_date, filing_date, issuer, title_of_class, cusip,
               figi, reported_value, reported_value_unit,
               shares_or_principal, shares_or_principal_type, put_call,
               investment_discretion, other_manager, voting_sole,
               voting_shared, voting_none, source_document_url,
               _retrieved_at, _source_url, _raw_sha256
        FROM {view}
        {where}
        ORDER BY entity_name, report_date DESC, reported_value DESC NULLS LAST
        """,
        parameters,
        root=root,
    )
    if frame.empty:
        raise CanonicalDataUnavailable("No matching SEC 13F holdings are available")
    for column in ("report_date", "filing_date", "_retrieved_at"):
        frame[column] = pd.to_datetime(frame[column])
    return frame
