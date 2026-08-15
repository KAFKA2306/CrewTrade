from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from crew.data_platform.contracts import DatasetBatch, QualityCheck


def validate_batch(batch: DatasetBatch) -> list[QualityCheck]:
    checks: list[QualityCheck] = []
    frame = batch.frame

    checks.append(QualityCheck("non_empty", not frame.empty, f"rows={len(frame)}"))

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
            QualityCheck("primary_key_not_null", null_key_rows == 0, f"null_key_rows={null_key_rows}")
        )
        checks.append(
            QualityCheck("primary_key_unique", duplicate_rows == 0, f"duplicate_rows={duplicate_rows}")
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
        QualityCheck("raw_payload_present", bool(batch.raw_payload), f"bytes={len(batch.raw_payload)}")
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

    if batch.contract is not None:
        checks.extend(_validate_contract(batch, batch.contract))
    return checks


def _validate_contract(batch: DatasetBatch, contract: Mapping[str, object]) -> list[QualityCheck]:
    checks: list[QualityCheck] = []
    frame = batch.frame
    expected_source = str(contract.get("source", ""))
    expected_pk = tuple(str(value) for value in contract.get("primary_key", []))
    fields = dict(contract.get("fields", {}))

    checks.append(
        QualityCheck(
            "contract_source",
            batch.source == expected_source,
            f"expected={expected_source} actual={batch.source}",
        )
    )
    checks.append(
        QualityCheck(
            "contract_primary_key",
            batch.primary_key == expected_pk,
            f"expected={expected_pk} actual={batch.primary_key}",
        )
    )

    missing_columns = sorted(set(fields).difference(frame.columns))
    checks.append(
        QualityCheck(
            "contract_columns_present",
            not missing_columns,
            f"missing={missing_columns}" if missing_columns else "all present",
        )
    )
    if bool(contract.get("strict_columns", True)):
        unexpected = sorted(set(frame.columns).difference(fields))
        checks.append(
            QualityCheck(
                "contract_no_unexpected_columns",
                not unexpected,
                f"unexpected={unexpected}" if unexpected else "none",
            )
        )

    for column, raw_spec in fields.items():
        if column not in frame.columns:
            continue
        spec = dict(raw_spec) if isinstance(raw_spec, Mapping) else {}
        series = frame[column]
        nullable = bool(spec.get("nullable", True))
        null_count = int(series.isna().sum())
        checks.append(
            QualityCheck(
                f"contract_{column}_nullable",
                nullable or null_count == 0,
                f"nullable={nullable} nulls={null_count}",
            )
        )
        non_null = series.dropna()
        expected_type = str(spec.get("type", "any"))
        type_ok = _series_matches_type(non_null, expected_type)
        checks.append(
            QualityCheck(
                f"contract_{column}_type",
                type_ok,
                f"expected={expected_type} dtype={series.dtype}",
            )
        )

        allowed = spec.get("allowed")
        if allowed is not None:
            allowed_values = list(allowed) if isinstance(allowed, list) else []
            invalid = sorted({str(value) for value in non_null if value not in allowed_values})
            checks.append(
                QualityCheck(
                    f"contract_{column}_allowed",
                    not invalid,
                    f"invalid={invalid[:10]}" if invalid else "all allowed",
                )
            )

        minimum = spec.get("minimum")
        maximum = spec.get("maximum")
        if (minimum is not None or maximum is not None) and not non_null.empty:
            numeric = pd.to_numeric(non_null, errors="coerce")
            range_ok = bool(numeric.notna().all())
            if range_ok and minimum is not None:
                range_ok = bool((numeric >= float(minimum)).all())
            if range_ok and maximum is not None:
                range_ok = bool((numeric <= float(maximum)).all())
            checks.append(
                QualityCheck(
                    f"contract_{column}_range",
                    range_ok,
                    f"minimum={minimum} maximum={maximum}",
                )
            )

        pattern = spec.get("pattern")
        if pattern is not None:
            compiled = re.compile(str(pattern))
            invalid_count = sum(not bool(compiled.fullmatch(str(value))) for value in non_null)
            checks.append(
                QualityCheck(
                    f"contract_{column}_pattern",
                    invalid_count == 0,
                    f"invalid={invalid_count} pattern={pattern}",
                )
            )

    required_metadata = [str(value) for value in contract.get("required_metadata", [])]
    missing_metadata = sorted(
        key for key in required_metadata if key not in batch.metadata or batch.metadata[key] is None
    )
    checks.append(
        QualityCheck(
            "contract_required_metadata",
            not missing_metadata,
            f"missing={missing_metadata}" if missing_metadata else "all present",
        )
    )

    freshness = contract.get("freshness")
    if isinstance(freshness, Mapping):
        field = str(freshness.get("field", ""))
        max_age_days = int(freshness.get("max_age_days", 0))
        if field not in frame.columns or frame.empty:
            checks.append(QualityCheck("contract_freshness", False, f"field={field} unavailable"))
        else:
            timestamps = pd.to_datetime(frame[field], errors="coerce")
            latest = timestamps.max()
            if pd.isna(latest):
                checks.append(QualityCheck("contract_freshness", False, f"field={field} no dates"))
            else:
                age_days = (batch.retrieved_at.date() - pd.Timestamp(latest).date()).days
                checks.append(
                    QualityCheck(
                        "contract_freshness",
                        age_days <= max_age_days,
                        f"field={field} age_days={age_days} max_age_days={max_age_days}",
                    )
                )
    return checks


def _series_matches_type(series: pd.Series, expected_type: str) -> bool:
    if series.empty or expected_type == "any":
        return True
    if expected_type == "string":
        return bool(series.map(lambda value: isinstance(value, str)).all())
    if expected_type == "number":
        return bool(pd.to_numeric(series, errors="coerce").notna().all())
    if expected_type == "integer":
        numeric = pd.to_numeric(series, errors="coerce")
        return bool(numeric.notna().all() and (numeric % 1 == 0).all())
    if expected_type in {"date", "datetime"}:
        return bool(pd.to_datetime(series, errors="coerce").notna().all())
    if expected_type == "boolean":
        return bool(series.map(lambda value: isinstance(value, (bool, np.bool_))).all())
    if expected_type == "json":
        try:
            for value in series:
                json.loads(str(value))
        except (TypeError, ValueError, json.JSONDecodeError):
            return False
        return True
    return False


def assert_quality(checks: Iterable[QualityCheck]) -> None:
    failures = [check for check in checks if not check.passed]
    if failures:
        details = "; ".join(f"{item.name}: {item.details}" for item in failures)
        raise ValueError(f"Data quality checks failed: {details}")
