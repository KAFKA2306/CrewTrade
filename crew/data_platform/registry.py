from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from crew.data_platform.config_schema import load_validated_config
from crew.data_platform.contracts import PersistedBatch, SourceAdapter
from crew.data_platform.gold import refresh_gold_views
from crew.data_platform.sources import (
    FredSource,
    GovernedManualSource,
    JpxEtfMasterSource,
    SecSource,
    TreasuryYieldCurveSource,
)
from crew.data_platform.storage import DataPlatformStorage

_ADAPTERS = {
    "fred": FredSource,
    "treasury_yield_curve": TreasuryYieldCurveSource,
    "sec": SecSource,
    "governed_manual": GovernedManualSource,
    "jpx_etf_master": JpxEtfMasterSource,
}


def load_config(path: Path) -> dict[str, Any]:
    return load_validated_config(path)


def build_adapters(
    config: Mapping[str, Any], selected_sources: Sequence[str] | None = None
) -> list[SourceAdapter]:
    selected = set(selected_sources or [])
    adapters: list[SourceAdapter] = []
    for source_name, source_config_value in dict(config.get("sources", {})).items():
        if selected and source_name not in selected:
            continue
        source_config = dict(source_config_value or {})
        if not bool(source_config.get("enabled", False)):
            continue
        adapter_name = str(source_config.get("adapter", source_name))
        adapter_class = _ADAPTERS.get(adapter_name)
        if adapter_class is None:
            raise ValueError(f"Unknown adapter {adapter_name!r} for source {source_name!r}")
        adapters.append(adapter_class(source_config))
    if selected:
        built_names = {
            source_name
            for source_name, source_config in dict(config.get("sources", {})).items()
            if source_name in selected and bool(source_config.get("enabled", False))
        }
        missing = selected.difference(built_names)
        if missing:
            raise ValueError(f"Unknown or disabled sources: {sorted(missing)}")
    return adapters


def sync(
    *,
    config_path: Path,
    selected_sources: Sequence[str] | None = None,
    root_override: Path | None = None,
) -> tuple[str, list[PersistedBatch], Path]:
    config = load_config(config_path)
    root = root_override or Path(config["storage"]["root"])
    storage = DataPlatformStorage(root)
    adapters = build_adapters(config, selected_sources)
    contracts = dict(config.get("contracts", {}))
    requested = list(selected_sources or config.get("sources", {}).keys())
    run_id = _new_run_id()
    storage.start_run(run_id, requested)
    persisted: list[PersistedBatch] = []
    try:
        for adapter in adapters:
            for batch in adapter.fetch():
                contract = contracts.get(batch.dataset)
                if contract is None:
                    raise ValueError(
                        f"Dataset {batch.dataset!r} from {batch.source!r} has no executable contract"
                    )
                persisted.append(storage.persist(run_id, replace(batch, contract=contract)))
        refresh_gold_views(storage.catalog_path)
        manifest_path = storage.write_manifest(run_id, persisted)
        storage.finish_run(run_id, status="success")
        return run_id, persisted, manifest_path
    except Exception as error:
        storage.finish_run(run_id, status="failed", error=str(error))
        raise


def _new_run_id() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"
