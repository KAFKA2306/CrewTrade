from __future__ import annotations

import io
import json
import os
from typing import Any, Mapping, Sequence

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient


class FredSource:
    name = "fred"
    BASE_URL = "https://api.stlouisfed.org/fred"
    PUBLIC_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        api_key_env = str(config.get("api_key_env", "FRED_API_KEY"))
        self.api_key = os.environ.get(api_key_env, "").strip()
        self.client = HttpClient(
            user_agent=str(config.get("user_agent", "CrewTrade data-platform")),
            min_interval_seconds=float(config.get("min_interval_seconds", 0.25)),
            timeout_seconds=float(config.get("timeout_seconds", 60.0)),
            max_attempts=int(config.get("max_attempts", 3)),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        batches: list[DatasetBatch] = []
        for dataset_name, dataset_config in dict(
            self.config.get("datasets", {})
        ).items():
            rows: list[dict[str, object]] = []
            retrieval_mode = (
                "api_vintage" if self.api_key else "public_csv_snapshot"
            )
            raw_bundle: dict[str, object] = {
                "dataset": dataset_name,
                "retrieval_mode": retrieval_mode,
                "series": {},
            }
            series_map = {
                str(label): str(series_id)
                for label, series_id in dict(
                    dataset_config.get("series", {})
                ).items()
            }
            observation_start = str(
                dataset_config.get("observation_start", "1900-01-01")
            )
            latest_url = ""
            latest_retrieved_at = None

            if self.api_key:
                for label, series_id in series_map.items():
                    series_rows, raw_record, source_url, retrieved_at = (
                        self._fetch_api_series(
                            label=label,
                            series_id=series_id,
                            observation_start=observation_start,
                        )
                    )
                    rows.extend(series_rows)
                    raw_bundle["series"][series_id] = raw_record
                    latest_url = source_url
                    latest_retrieved_at = retrieved_at
            else:
                rows, raw_record, latest_url, latest_retrieved_at = (
                    self._fetch_public_csv_dataset(
                        series_map=series_map,
                        observation_start=observation_start,
                    )
                )
                raw_bundle["batch"] = raw_record

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
                    source_url=latest_url
                    or f"{self.BASE_URL}/series/observations",
                    raw_payload=json.dumps(
                        raw_bundle, ensure_ascii=False, sort_keys=True
                    ).encode("utf-8"),
                    content_type="application/json",
                    retrieved_at=(
                        latest_retrieved_at
                        if latest_retrieved_at is not None
                        else pd.Timestamp.utcnow().to_pydatetime()
                    ),
                    metadata={
                        "series_count": len(series_map),
                        "retrieval_mode": retrieval_mode,
                        "point_in_time_vintage": bool(self.api_key),
                        "http_request_count": len(series_map) * 2
                        if self.api_key
                        else 1,
                    },
                )
            )
        return batches

    def _fetch_api_series(
        self, *, label: str, series_id: str, observation_start: str
    ) -> tuple[list[dict[str, object]], dict[str, object], str, object]:
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
                "observation_start": observation_start,
                "sort_order": "asc",
                "output_type": 1,
            },
        )
        metadata_json = json.loads(metadata_payload.body)
        observations_json = json.loads(observations_payload.body)
        return (
            parse_fred_series(
                label=label,
                series_id=series_id,
                metadata=metadata_json,
                observations=observations_json,
            ),
            {
                "label": label,
                "metadata": metadata_json,
                "observations": observations_json,
            },
            observations_payload.url,
            observations_payload.retrieved_at,
        )

    def _fetch_public_csv_dataset(
        self,
        *,
        series_map: Mapping[str, str],
        observation_start: str,
    ) -> tuple[list[dict[str, object]], dict[str, object], str, object]:
        series_ids = list(series_map.values())
        payload = self.client.get(
            self.PUBLIC_CSV_URL,
            params={
                "id": ",".join(series_ids),
                "cosd": observation_start,
            },
        )
        retrieval_date = pd.Timestamp(payload.retrieved_at).date()
        rows = parse_fred_public_csv_batch(
            series_map=series_map,
            payload=payload.body,
            retrieval_date=retrieval_date,
        )
        return (
            rows,
            {
                "retrieval_mode": "public_csv_snapshot",
                "series_ids": series_ids,
                "csv": payload.body.decode("utf-8"),
            },
            payload.url,
            payload.retrieved_at,
        )


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


def parse_fred_public_csv_batch(
    *,
    series_map: Mapping[str, str],
    payload: bytes,
    retrieval_date: object,
) -> list[dict[str, object]]:
    frame = pd.read_csv(io.BytesIO(payload))
    date_column = _date_column(frame)
    missing = sorted(set(series_map.values()).difference(frame.columns))
    if missing:
        raise ValueError(
            f"FRED CSV is missing requested series {missing}; columns={list(frame.columns)}"
        )
    frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")
    snapshot_date = pd.to_datetime(retrieval_date).date()
    rows: list[dict[str, object]] = []
    for label, series_id in series_map.items():
        series_frame = frame[[date_column, series_id]].copy()
        series_frame[series_id] = pd.to_numeric(
            series_frame[series_id], errors="coerce"
        )
        series_frame = series_frame.dropna(subset=[date_column, series_id])
        for record in series_frame.to_dict(orient="records"):
            rows.append(
                {
                    "series_id": series_id,
                    "label": label,
                    "observation_date": pd.Timestamp(
                        record[date_column]
                    ).date(),
                    "value": float(record[series_id]),
                    "realtime_start": snapshot_date,
                    "realtime_end": snapshot_date,
                    "frequency": None,
                    "units": None,
                    "seasonal_adjustment": None,
                    "last_updated": snapshot_date,
                    "title": series_id,
                }
            )
    return rows


def parse_fred_public_csv(
    *,
    label: str,
    series_id: str,
    payload: bytes,
    retrieval_date: object,
) -> list[dict[str, object]]:
    return parse_fred_public_csv_batch(
        series_map={label: series_id},
        payload=payload,
        retrieval_date=retrieval_date,
    )


def _date_column(frame: pd.DataFrame) -> str:
    date_column = next(
        (
            candidate
            for candidate in ("observation_date", "DATE", "date")
            if candidate in frame.columns
        ),
        None,
    )
    if date_column is None:
        raise ValueError(
            f"Unexpected FRED CSV date columns: {list(frame.columns)}"
        )
    return date_column
