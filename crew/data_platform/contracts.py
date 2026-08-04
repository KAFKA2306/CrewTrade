from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol, Sequence

import pandas as pd


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class HttpPayload:
    body: bytes
    url: str
    status_code: int
    content_type: str
    retrieved_at: datetime
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DatasetBatch:
    """One immutable ingestion result and its normalized tabular representation."""

    dataset: str
    source: str
    frame: pd.DataFrame
    primary_key: tuple[str, ...]
    source_url: str
    raw_payload: bytes
    content_type: str = "application/octet-stream"
    retrieved_at: datetime = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QualityCheck:
    name: str
    passed: bool
    details: str


@dataclass(frozen=True)
class PersistedBatch:
    dataset: str
    source: str
    row_count: int
    raw_path: str
    parquet_path: str
    raw_sha256: str
    checks: Sequence[QualityCheck]


class SourceAdapter(Protocol):
    name: str

    def fetch(self) -> Sequence[DatasetBatch]: ...
