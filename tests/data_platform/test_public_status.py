from __future__ import annotations

from pathlib import Path

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.public_status import build_public_status, export_public_status
from crew.data_platform.storage import DataPlatformStorage


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_CONFIG = PROJECT_ROOT / "config" / "data_platform.yaml"
MIGRATION_CONFIG = PROJECT_ROOT / "config" / "use_case_data_status.yaml"


def test_status_is_degraded_before_first_snapshot(tmp_path: Path) -> None:
    status = build_public_status(
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=tmp_path / "missing",
    )
    assert status["overall_status"] == "degraded"
    assert status["summary"] == {
        "use_case_count": 10,
        "canonical_ok": 0,
        "controlled_blocks": 9,
        "awaiting_snapshot": 1,
    }


def test_status_is_ok_when_all_canonical_datasets_exist(tmp_path: Path) -> None:
    root = tmp_path / "platform"
    storage = DataPlatformStorage(root)
    run_id = "20260805T000000Z-status"
    storage.start_run(run_id, ["fixture"])
    for dataset in (
        "rates_macro",
        "treasury_par_yield_curve",
        "treasury_par_real_yield_curve",
    ):
        batch = DatasetBatch(
            dataset=dataset,
            source="fixture",
            frame=pd.DataFrame([{"id": f"{dataset}-1", "value": 1.0}]),
            primary_key=("id",),
            source_url=f"https://example.com/{dataset}",
            raw_payload=dataset.encode("utf-8"),
            metadata={"retrieval_mode": "fixture"},
        )
        storage.persist(run_id, batch)
    storage.finish_run(run_id, status="success")

    output = tmp_path / "status.json"
    status = export_public_status(
        output_path=output,
        platform_config_path=PLATFORM_CONFIG,
        migration_config_path=MIGRATION_CONFIG,
        root=root,
    )
    assert output.is_file()
    assert status["overall_status"] == "ok"
    assert status["summary"]["canonical_ok"] == 1
    assert status["summary"]["controlled_blocks"] == 9
    assert status["summary"]["awaiting_snapshot"] == 0
    assert all(row["operational"] for row in status["use_cases"])
