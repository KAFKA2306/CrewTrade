from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from crew.data_platform.public_status import build_public_status


def build_report_evidence(
    *,
    use_case: str,
    report_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
    migration = yaml.safe_load(migration_config_path.read_text(encoding="utf-8"))
    definitions = dict((migration or {}).get("use_cases", {}))
    if use_case not in definitions:
        raise ValueError(f"Unknown use case: {use_case}")

    status = build_public_status(
        platform_config_path=platform_config_path,
        migration_config_path=migration_config_path,
        root=root,
    )
    use_case_row = next(row for row in status["use_cases"] if row["slug"] == use_case)
    dataset_by_name = {row["dataset"]: row for row in status["datasets"]}
    required = list(use_case_row["required_datasets"])
    datasets = [dataset_by_name[name] for name in required if name in dataset_by_name]

    report_exists = report_path.is_file()
    report_sha256 = hashlib.sha256(report_path.read_bytes()).hexdigest() if report_exists else None
    if use_case_row["declared_state"] != "canonical_active":
        decision = "CONTROLLED_BLOCK"
    elif not report_exists:
        decision = "UNVERIFIED_REPORT"
    elif use_case_row["runtime_state"] != "ok":
        decision = "UNVERIFIED_DATA"
    else:
        decision = "READY_FOR_REVIEW"

    payload: dict[str, Any] = {
        "schema_version": 1,
        "decision": decision,
        "use_case": use_case,
        "report": {
            "path": report_path.as_posix(),
            "exists": report_exists,
            "sha256": report_sha256,
        },
        "declared_state": use_case_row["declared_state"],
        "runtime_state": use_case_row["runtime_state"],
        "required_datasets": required,
        "missing_datasets": list(use_case_row["missing_datasets"]),
        "failed_datasets": list(use_case_row["failed_datasets"]),
        "datasets": datasets,
        "scope": (
            "READY_FOR_REVIEW proves that the report artifact is identified and all declared "
            "canonical datasets have current passing lineage records. It does not prove that "
            "the report's financial conclusions are correct or authorize publication."
        ),
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["evidence_fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def export_report_evidence(
    *,
    output_path: Path,
    use_case: str,
    report_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
    payload = build_report_evidence(
        use_case=use_case,
        report_path=report_path,
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
