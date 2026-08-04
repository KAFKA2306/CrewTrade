from __future__ import annotations

from pathlib import Path

import duckdb


_LATEST_BY_SERIES = {"credit_oas", "rates_macro"}


def refresh_gold_views(catalog_path: Path) -> None:
    """Create deterministic point-in-time views for datasets already in the catalogue."""

    with duckdb.connect(str(catalog_path)) as connection:
        datasets = {
            row[0]
            for row in connection.execute(
                "SELECT DISTINCT dataset FROM dataset_files"
            ).fetchall()
        }
        for dataset in sorted(_LATEST_BY_SERIES.intersection(datasets)):
            connection.execute(
                f"""
                CREATE OR REPLACE VIEW gold_{dataset}_latest AS
                SELECT * EXCLUDE (_rank)
                FROM (
                    SELECT *,
                           row_number() OVER (
                               PARTITION BY series_id
                               ORDER BY observation_date DESC,
                                        realtime_start DESC,
                                        _retrieved_at DESC
                           ) AS _rank
                    FROM bronze_{dataset}
                )
                WHERE _rank = 1
                """
            )

        if "treasury_par_yield_curve" in datasets:
            connection.execute(
                """
                CREATE OR REPLACE VIEW gold_treasury_curve_latest AS
                SELECT * EXCLUDE (_rank)
                FROM (
                    SELECT *,
                           row_number() OVER (
                               PARTITION BY tenor
                               ORDER BY observation_date DESC, _retrieved_at DESC
                           ) AS _rank
                    FROM bronze_treasury_par_yield_curve
                )
                WHERE _rank = 1
                """
            )

        if "sec_filings" in datasets:
            connection.execute(
                """
                CREATE OR REPLACE VIEW gold_sec_filings_latest AS
                SELECT * EXCLUDE (_rank)
                FROM (
                    SELECT *,
                           row_number() OVER (
                               PARTITION BY entity_cik, form
                               ORDER BY filing_date DESC,
                                        acceptance_datetime DESC,
                                        _retrieved_at DESC
                           ) AS _rank
                    FROM bronze_sec_filings
                )
                WHERE _rank = 1
                """
            )

        if "sec_company_facts" in datasets:
            connection.execute(
                """
                CREATE OR REPLACE VIEW gold_sec_company_facts_latest AS
                SELECT * EXCLUDE (_rank)
                FROM (
                    SELECT *,
                           row_number() OVER (
                               PARTITION BY entity_cik, taxonomy, concept, unit
                               ORDER BY end_date DESC NULLS LAST,
                                        filed_date DESC NULLS LAST,
                                        _retrieved_at DESC
                           ) AS _rank
                    FROM bronze_sec_company_facts
                )
                WHERE _rank = 1
                """
            )
