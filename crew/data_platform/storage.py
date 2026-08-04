from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import duckdb

from crew.data_platform.contracts import DatasetBatch, PersistedBatch, QualityCheck
from crew.data_platform.quality import assert_quality, validate_batch


_SAFE_NAME = re.compile(r"[^a-zA-Z0-9_]+")


def _safe_name(value: str) -> str:
    normalized = _SAFE_NAME.sub("_", value).strip("_").lower()
    if not normalized:
        raise ValueError(f"Unsafe empty dataset name derived from {value!r}")
    return normalized


class DataPlatformStorage:
    """Immutable raw/Parquet storage with a small DuckDB control catalogue."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.raw_dir = root / "raw"
        self.bronze_dir = root / "bronze"
        self.manifest_dir = root / "manifests"
        self.catalog_path = root / "catalog.duckdb"
        for path in (self.raw_dir, self.bronze_dir, self.manifest_dir):
            path.mkdir(parents=True, exist_ok=True)
        self._initialize_catalog()

    def start_run(self, run_id: str, requested_sources: Iterable[str]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO ingestion_runs
                    (run_id, started_at, status, requested_sources)
                VALUES (?, ?, 'running', ?)
                """,
                [
                    run_id,
                    datetime.now(timezone.utc),
                    json.dumps(sorted(set(requested_sources)), ensure_ascii=False),
                ],
            )

    def finish_run(
        self,
        run_id: str,
        *,
        status: str,
        error: str | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE ingestion_runs
                SET completed_at = ?, status = ?, error = ?
                WHERE run_id = ?
                """,
                [datetime.now(timezone.utc), status, error, run_id],
            )

    def persist(self, run_id: str, batch: DatasetBatch) -> PersistedBatch:
        checks = validate_batch(batch)
        self._record_checks(run_id, batch, checks)
        assert_quality(checks)

        dataset = _safe_name(batch.dataset)
        source = _safe_name(batch.source)
        raw_sha256 = hashlib.sha256(batch.raw_payload).hexdigest()
        raw_suffix = self._raw_suffix(batch.content_type)
        raw_path = (
            self.raw_dir
            / f"source={source}"
            / f"dataset={dataset}"
            / f"run_id={run_id}"
            / f"payload-{raw_sha256[:16]}{raw_suffix}"
        )
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(batch.raw_payload)

        frame = batch.frame.copy()
        frame["_run_id"] = run_id
        frame["_retrieved_at"] = batch.retrieved_at
        frame["_source_url"] = batch.source_url
        frame["_raw_sha256"] = raw_sha256

        parquet_path = (
            self.bronze_dir
            / f"dataset={dataset}"
            / f"source={source}"
            / f"run_id={run_id}"
            / "part-000.parquet"
        )
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(parquet_path, index=False)

        schema_json = json.dumps(
            {column: str(dtype) for column, dtype in frame.dtypes.items()},
            ensure_ascii=False,
            sort_keys=True,
        )
        metadata_json = json.dumps(dict(batch.metadata), ensure_ascii=False, sort_keys=True)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO dataset_files
                    (run_id, dataset, source, row_count, raw_path, parquet_path,
                     raw_sha256, source_url, retrieved_at, schema_json, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    run_id,
                    dataset,
                    source,
                    len(frame),
                    str(raw_path.relative_to(self.root)),
                    str(parquet_path.relative_to(self.root)),
                    raw_sha256,
                    batch.source_url,
                    batch.retrieved_at,
                    schema_json,
                    metadata_json,
                ],
            )
        self.refresh_dataset_view(dataset)
        return PersistedBatch(
            dataset=dataset,
            source=source,
            row_count=len(frame),
            raw_path=str(raw_path),
            parquet_path=str(parquet_path),
            raw_sha256=raw_sha256,
            checks=checks,
        )

    def write_manifest(self, run_id: str, persisted: list[PersistedBatch]) -> Path:
        manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "catalog": str(self.catalog_path),
            "batches": [
                {
                    **asdict(batch),
                    "checks": [asdict(check) for check in batch.checks],
                }
                for batch in persisted
            ],
        }
        path = self.manifest_dir / f"{run_id}.json"
        path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    def refresh_dataset_view(self, dataset: str) -> None:
        dataset = _safe_name(dataset)
        glob_path = (self.bronze_dir / f"dataset={dataset}" / "**" / "*.parquet").as_posix()
        view_name = f"bronze_{dataset}"
        with self._connect() as connection:
            connection.execute(
                f"""
                CREATE OR REPLACE VIEW {view_name} AS
                SELECT *
                FROM read_parquet('{glob_path}', union_by_name=true, hive_partitioning=true)
                """
            )

    def _record_checks(
        self,
        run_id: str,
        batch: DatasetBatch,
        checks: list[QualityCheck],
    ) -> None:
        with self._connect() as connection:
            for check in checks:
                connection.execute(
                    """
                    INSERT INTO quality_results
                        (run_id, dataset, source, check_name, passed, details, checked_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        run_id,
                        batch.dataset,
                        batch.source,
                        check.name,
                        check.passed,
                        check.details,
                        datetime.now(timezone.utc),
                    ],
                )

    def _initialize_catalog(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ingestion_runs (
                    run_id VARCHAR PRIMARY KEY,
                    started_at TIMESTAMPTZ NOT NULL,
                    completed_at TIMESTAMPTZ,
                    status VARCHAR NOT NULL,
                    requested_sources JSON NOT NULL,
                    error VARCHAR
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS dataset_files (
                    run_id VARCHAR NOT NULL,
                    dataset VARCHAR NOT NULL,
                    source VARCHAR NOT NULL,
                    row_count BIGINT NOT NULL,
                    raw_path VARCHAR NOT NULL,
                    parquet_path VARCHAR NOT NULL,
                    raw_sha256 VARCHAR NOT NULL,
                    source_url VARCHAR NOT NULL,
                    retrieved_at TIMESTAMPTZ NOT NULL,
                    schema_json JSON NOT NULL,
                    metadata_json JSON NOT NULL,
                    PRIMARY KEY (run_id, dataset, source, parquet_path)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS quality_results (
                    run_id VARCHAR NOT NULL,
                    dataset VARCHAR NOT NULL,
                    source VARCHAR NOT NULL,
                    check_name VARCHAR NOT NULL,
                    passed BOOLEAN NOT NULL,
                    details VARCHAR NOT NULL,
                    checked_at TIMESTAMPTZ NOT NULL
                )
                """
            )

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.catalog_path))

    @staticmethod
    def _raw_suffix(content_type: str) -> str:
        lowered = content_type.lower()
        if "json" in lowered:
            return ".json"
        if "xml" in lowered:
            return ".xml"
        if "csv" in lowered:
            return ".csv"
        if "html" in lowered:
            return ".html"
        return ".bin"
