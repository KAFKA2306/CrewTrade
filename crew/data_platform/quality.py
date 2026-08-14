from __future__ import annotations

import math
from collections.abc import Iterable
from urllib.parse import urlparse

import numpy as np

from crew.data_platform.contracts import DatasetBatch, QualityCheck


def validate_batch(batch: DatasetBatch) -> list[QualityCheck]:
    checks: list[QualityCheck] = []
    frame = batch.frame

    checks.append(
        QualityCheck(
            "non_empty",
            not frame.empty,
            f"rows={len(frame)}",
        )
    )

    missing_keys = [key for key in batch.primary_key if key not in frame.columns]
    checks.append(
        QualityCheck(
            "primary_key_columns",
            not missing_keys,
            "missing=" + ",".join(missing_keys) if missing_keys else "all present",
        )
    )

    if not missing_keys and batch.primary_key:
        null_key_rows = int(frame[list(batch.primary_key)].isna().any(axis=1).sum())
        duplicate_rows = int(frame.duplicated(list(batch.primary_key), keep=False).sum())
        checks.append(
            QualityCheck(
                "primary_key_not_null",
                null_key_rows == 0,
                f"null_key_rows={null_key_rows}",
            )
        )
        checks.append(
            QualityCheck(
                "primary_key_unique",
                duplicate_rows == 0,
                f"duplicate_rows={duplicate_rows}",
            )
        )

    parsed_url = urlparse(batch.source_url)
    checks.append(
        QualityCheck(
            "source_url_https",
            parsed_url.scheme == "https" and bool(parsed_url.netloc),
            batch.source_url,
        )
    )
    checks.append(
        QualityCheck(
            "raw_payload_present",
            bool(batch.raw_payload),
            f"bytes={len(batch.raw_payload)}",
        )
    )

    numeric_columns = frame.select_dtypes(include=[np.number]).columns
    invalid_numeric: list[str] = []
    for column in numeric_columns:
        values = frame[column].dropna().to_numpy()
        if any(not math.isfinite(float(value)) for value in values):
            invalid_numeric.append(str(column))
    checks.append(
        QualityCheck(
            "finite_numeric_values",
            not invalid_numeric,
            "invalid=" + ",".join(invalid_numeric) if invalid_numeric else "all finite",
        )
    )

    return checks


def assert_quality(checks: Iterable[QualityCheck]) -> None:
    failures = [check for check in checks if not check.passed]
    if failures:
        details = "; ".join(f"{item.name}: {item.details}" for item in failures)
        raise ValueError(f"Data quality checks failed: {details}")
