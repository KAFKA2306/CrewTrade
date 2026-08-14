from __future__ import annotations

import json
from typing import Any, Mapping, Sequence

import pandas as pd

from crew.data_platform.contracts import DatasetBatch, utc_now


class GovernedManualSource:
    """Registers licensed, contractual, or human-supplied sources without fabricating data."""

    name = "governed_manual"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config

    def fetch(self) -> Sequence[DatasetBatch]:
        rows: list[dict[str, object]] = []
        sources = dict(self.config.get("datasets", {}))
        for source_id, source_config in sources.items():
            rows.append(
                {
                    "source_id": str(source_id),
                    "use_cases": json.dumps(source_config.get("use_cases", []), ensure_ascii=False),
                    "owner": source_config.get("owner"),
                    "source_url": source_config.get("source_url"),
                    "access_mode": source_config.get("access_mode", "manual"),
                    "license_status": source_config.get("license_status", "unverified"),
                    "refresh_policy": source_config.get("refresh_policy"),
                    "required_fields": json.dumps(
                        source_config.get("required_fields", []), ensure_ascii=False
                    ),
                    "automation_status": source_config.get("automation_status", "blocked"),
                    "block_reason": source_config.get("block_reason"),
                    "checked_on": pd.to_datetime(source_config.get("checked_on")).date()
                    if source_config.get("checked_on")
                    else None,
                }
            )
        frame = pd.DataFrame.from_records(rows)
        raw_payload = json.dumps({"datasets": sources}, ensure_ascii=False, sort_keys=True).encode(
            "utf-8"
        )
        return [
            DatasetBatch(
                dataset="governed_source_registry",
                source=self.name,
                frame=frame,
                primary_key=("source_id",),
                source_url=str(
                    self.config.get(
                        "registry_url",
                        "https://github.com/KAFKA2306/CrewTrade/blob/main/config/data_platform.yaml",
                    )
                ),
                raw_payload=raw_payload,
                content_type="application/json",
                retrieved_at=utc_now(),
                metadata={"registered_sources": len(rows)},
            )
        ]
