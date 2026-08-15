from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.evidence import build_report_evidence, export_report_evidence
from crew.data_platform.storage import DataPlatformStorage

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_CONFIG = PROJECT_ROOT / "config" / "data_platform.yaml"
MIGRATION_CONFIG = PROJECT_ROOT / "config" / "use_case_data_status.yaml"
_REQUIRED = (
    "rates_macro",
    "treasury_par_yield_curve",
    "treasury_par_real_yield_curve",
)


def _materialize(root: Path) -> None:
    storage = DataPlatformStorage(root)
    run_id = "20260815T000000Z-evidence"
    storage.start_run(run_id, ["fixture"])
    persisted = []
    for dataset in _REQUIRED:
        batch = DatasetBatch(
            dataset=dataset,
            source="fixture",
            frame=pd.DataFrame([{"id": f"{dataset}-1", "value": 1.0}]),
            primary_key=("id",),
            source_url=f"https://example.com/{dataset}",
            raw_payload=dataset.encode("utf-8"),
            metadata={"retrieval_mode": "fixture"},
        )
        persisted.append(storage.persist(run_id, batch))
    storage.write_manifest(run_id, persisted)
    storage.finish_run(run_id, status="success")


def test_ready_for_review_binds_report_and_required_lineage(tmp_path: Path) -> None:
    root = tmp_path / "platform"
    _materialize(root)
    report = tmp_path / "report.md"
    report.write_text("# deterministic report\n", encoding="utf-8")

    payload = build_report_evidence(
        use_case="yield_spread",
        report_path=report,
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=root,
    )

    assert payload["decision"] == "READY_FOR_REVIEW"
    assert payload["required_datasets"] == list(_REQUIRED)
    assert [row["dataset"] for row in payload["datasets"]] == list(_REQUIRED)
    assert all(row["quality_status"] == "ok" for row in payload["datasets"])
    assert payload["report"]["sha256"] == hashlib.sha256(report.read_bytes()).hexdigest()
    assert len(payload["evidence_fingerprint"]) == 64

    output = tmp_path / "evidence.json"
    summary = tmp_path / "evidence-summary.html"
    exported = export_report_evidence(
        output_path=output,
        use_case="yield_spread",
        report_path=report,
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=root,
        summary_output_path=summary,
    )
    assert output.is_file()
    assert summary.is_file()
    assert exported["evidence_fingerprint"] == payload["evidence_fingerprint"]

    rendered = summary.read_text(encoding="utf-8")
    assert "READY_FOR_REVIEW" in rendered
    assert payload["evidence_fingerprint"] in rendered
    assert payload["report"]["sha256"] in rendered
    for dataset in _REQUIRED:
        assert dataset in rendered
        assert f"https://example.com/{dataset}" in rendered


def test_missing_snapshot_fails_closed(tmp_path: Path) -> None:
    report = tmp_path / "report.md"
    report.write_text("# report without lineage\n", encoding="utf-8")
    payload = build_report_evidence(
        use_case="yield_spread",
        report_path=report,
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=tmp_path / "missing",
    )
    assert payload["decision"] == "UNVERIFIED_DATA"
    assert payload["missing_datasets"] == list(_REQUIRED)


def test_governed_block_is_not_promoted_by_report_presence(tmp_path: Path) -> None:
    report = tmp_path / "credit.md"
    report.write_text("# credit\n", encoding="utf-8")
    payload = build_report_evidence(
        use_case="credit",
        report_path=report,
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=tmp_path / "missing",
    )
    assert payload["decision"] == "CONTROLLED_BLOCK"
