from __future__ import annotations

import json
import os
from typing import Any, Mapping, Sequence

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient


class FredSource:
    name = "fred"
    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        api_key_env = str(config.get("api_key_env", "FRED_API_KEY"))
        self.api_key = os.environ.get(api_key_env, "").strip()
        if not self.api_key:
            raise RuntimeError(f"FRED API key is required in {api_key_env}.")
        self.client = HttpClient(
            user_agent=str(config.get("user_agent", "CrewTrade data-platform")),
            min_interval_seconds=float(config.get("min_interval_seconds", 0.25)),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        batches: list[DatasetBatch] = []
        for dataset_name, dataset_config in dict(self.config.get("datasets", {})).items():
            rows: list[dict[str, object]] = []
            raw_bundle: dict[str, object] = {"dataset": dataset_name, "series": {}}
            latest_url = ""
            latest_retrieved_at = None
            series_map = dict(dataset_config.get("series", {}))
            for label, series_id_value in series_map.items():
                series_id = str(series_id_value)
                metadata_payload = self.client.get(
                    f"{self.BASE_URL}/series",
                    params={
                        "api_key": self.api_key,
                        "file_type": "json",
                        "series_id": series_id,
                    },
                )
                observations_payload = self.client.get(
                    f"{self.BASE_URL}/series/observations",
                    params={
                        "api_key": self.api_key,
                        "file_type": "json",
                        "series_id": series_id,
                        "observation_start": dataset_config.get(
                            "observation_start", "1900-01-01"
                        ),
                        "sort_order": "asc",
                        "output_type": 1,
                    },
                )
                metadata_json = json.loads(metadata_payload.body)
                observations_json = json.loads(observations_payload.body)
                raw_bundle["series"][series_id] = {
                    "label": label,
                    "metadata": metadata_json,
                    "observations": observations_json,
                }
                rows.extend(
                    parse_fred_series(
                        label=label,
                        series_id=series_id,
                        metadata=metadata_json,
                        observations=observations_json,
                    )
                )
                latest_url = observations_payload.url
                latest_retrieved_at = observations_payload.retrieved_at
            frame = pd.DataFrame.from_records(rows)
            batches.append(
                DatasetBatch(
                    dataset=str(dataset_name),
                    source=self.name,
                    frame=frame,
                    primary_key=(
                        "series_id",
                        "observation_date",
                        "realtime_start",
                        "realtime_end",
                    ),
                    source_url=latest_url or f"{self.BASE_URL}/series/observations",
                    raw_payload=json.dumps(
                        raw_bundle, ensure_ascii=False, sort_keys=True
                    ).encode("utf-8"),
                    content_type="application/json",
                    retrieved_at=latest_retrieved_at
                    if latest_retrieved_at is not None
                    else pd.Timestamp.utcnow().to_pydatetime(),
                    metadata={"series_count": len(series_map)},
                )
            )
        return batches


def parse_fred_series(
    *,
    label: str,
    series_id: str,
    metadata: Mapping[str, Any],
    observations: Mapping[str, Any],
) -> list[dict[str, object]]:
    series_records = list(metadata.get("seriess", []))
    series_meta = series_records[0] if series_records else {}
    rows: list[dict[str, object]] = []
    for observation in observations.get("observations", []):
        value_text = str(observation.get("value", "."))
        if value_text in {".", "", "nan", "NaN"}:
            continue
        rows.append(
            {
                "series_id": series_id,
                "label": label,
                "observation_date": pd.to_datetime(observation["date"]).date(),
                "value": float(value_text),
                "realtime_start": pd.to_datetime(
                    observation.get("realtime_start")
                ).date(),
                "realtime_end": pd.to_datetime(
                    observation.get("realtime_end")
                ).date(),
                "frequency": series_meta.get("frequency"),
                "units": series_meta.get("units"),
                "seasonal_adjustment": series_meta.get("seasonal_adjustment"),
                "last_updated": series_meta.get("last_updated"),
                "title": series_meta.get("title"),
            }
        )
    return rows
