from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import yaml

from crew.data_platform.consumer import resolve_root


_ALLOWED_CONTROLLED_STATES = {
    "canonical_active",
    "governed_blocked",
    "governed_partial",
    "private_input_required",
}


def build_public_status(
    *,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
    platform_config = _load_yaml(platform_config_path)
    migration_config = _load_yaml(migration_config_path)
    platform_root = resolve_root(root)
    catalog_path = platform_root / "catalog.duckdb"
    dataset_status, latest_run = _catalog_status(catalog_path)

    governed_contracts = dict(
        platform_config.get("sources", {}).get("governed_manual", {}).get("datasets", {})
    )
    use_case_rows: list[dict[str, Any]] = []
    active_missing = False
    invalid_state = False
    for slug, definition_value in dict(migration_config.get("use_cases", {})).items():
        definition = dict(definition_value or {})
        declared_state = str(definition.get("state", "unknown"))
        invalid_state |= declared_state not in _ALLOWED_CONTROLLED_STATES
        required_datasets = list(definition.get("required_datasets", []))
        required_contracts = list(definition.get("required_contracts", []))
        missing_datasets = [
            dataset for dataset in required_datasets if dataset not in dataset_status
        ]
        failed_datasets = [
            dataset
            for dataset in required_datasets
            if dataset in dataset_status and dataset_status[dataset]["quality_status"] != "ok"
        ]
        contract_rows = []
        for contract_name in required_contracts:
            contract = dict(governed_contracts.get(contract_name, {}))
            contract_rows.append(
                {
                    "name": contract_name,
                    "automation_status": contract.get("automation_status", "unregistered"),
                    "checked_on": contract.get("checked_on"),
                    "source_url": contract.get("source_url"),
                    "block_reason": contract.get("block_reason"),
                }
            )

        if declared_state == "canonical_active":
            runtime_state = (
                "ok" if not missing_datasets and not failed_datasets else "awaiting_snapshot"
            )
            active_missing |= bool(missing_datasets or failed_datasets)
        else:
            runtime_state = declared_state
        use_case_rows.append(
            {
                "slug": slug,
                "title": definition.get("title", slug),
                "declared_state": declared_state,
                "runtime_state": runtime_state,
                "operational": runtime_state != "awaiting_snapshot",
                "owner_source": definition.get("owner_source"),
                "note": definition.get("note"),
                "required_datasets": required_datasets,
                "missing_datasets": missing_datasets,
                "failed_datasets": failed_datasets,
                "required_contracts": contract_rows,
            }
        )

    overall_status = "ok"
    if invalid_state or active_missing:
        overall_status = "degraded"
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "catalog_present": catalog_path.is_file(),
        "latest_run": latest_run,
        "datasets": sorted(dataset_status.values(), key=lambda row: row["dataset"]),
        "use_cases": use_case_rows,
        "summary": {
            "use_case_count": len(use_case_rows),
            "canonical_ok": sum(row["runtime_state"] == "ok" for row in use_case_rows),
            "controlled_blocks": sum(
                row["runtime_state"]
                in {
                    "governed_blocked",
                    "governed_partial",
                    "private_input_required",
                }
                for row in use_case_rows
            ),
            "awaiting_snapshot": sum(
                row["runtime_state"] == "awaiting_snapshot" for row in use_case_rows
            ),
        },
    }


def export_public_status(
    *,
    output_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
    payload = build_public_status(
        platform_config_path=platform_config_path,
        migration_config_path=migration_config_path,
        root=root,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def _catalog_status(
    catalog_path: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    if not catalog_path.is_file():
        return {}, None
    with duckdb.connect(str(catalog_path), read_only=True) as connection:
        dataset_rows = connection.execute(
            """
            WITH latest_files AS (
                SELECT *,
                       row_number() OVER (
                           PARTITION BY dataset
                           ORDER BY retrieved_at DESC, run_id DESC
                       ) AS dataset_rank
                FROM dataset_files
            ),
            quality AS (
                SELECT dataset, run_id,
                       count(*) FILTER (WHERE passed = false) AS failed_checks
                FROM quality_results
                GROUP BY dataset, run_id
            )
            SELECT files.dataset, files.source, files.row_count,
                   files.raw_sha256, files.source_url, files.retrieved_at,
                   files.metadata_json, files.run_id,
                   coalesce(quality.failed_checks, 0) AS failed_checks
            FROM latest_files AS files
            LEFT JOIN quality
              ON files.dataset = quality.dataset
             AND files.run_id = quality.run_id
            WHERE files.dataset_rank = 1
            ORDER BY files.dataset
            """
        ).fetchall()
        latest_run_row = connection.execute(
            """
            SELECT run_id, started_at, completed_at, status, error
            FROM ingestion_runs
            ORDER BY started_at DESC
            LIMIT 1
            """
        ).fetchone()

    status: dict[str, dict[str, Any]] = {}
    for row in dataset_rows:
        metadata = _metadata_mapping(row[6])
        status[str(row[0])] = {
            "dataset": str(row[0]),
            "source": str(row[1]),
            "row_count": int(row[2]),
            "raw_sha256": str(row[3]),
            "source_url": str(row[4]),
            "retrieved_at": _iso(row[5]),
            "run_id": str(row[7]),
            "quality_status": "ok" if int(row[8]) == 0 else "failed",
            "retrieval_mode": metadata.get("retrieval_mode"),
            "point_in_time_vintage": metadata.get("point_in_time_vintage"),
        }
    latest_run = None
    if latest_run_row:
        latest_run = {
            "run_id": str(latest_run_row[0]),
            "started_at": _iso(latest_run_row[1]),
            "completed_at": _iso(latest_run_row[2]),
            "status": str(latest_run_row[3]),
            "error": latest_run_row[4],
        }
    return status, latest_run


def _metadata_mapping(value: object) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if value is None or value == "":
        return {}
    parsed = json.loads(str(value))
    if not isinstance(parsed, Mapping):
        raise ValueError("dataset metadata must be a JSON object")
    return dict(parsed)


def _load_yaml(path: Path) -> Mapping[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError(f"Expected YAML mapping: {path}")
    return payload


def _iso(value: object) -> str | None:
    if value is None:
        return None
    method = getattr(value, "isoformat", None)
    return method() if callable(method) else str(value)
