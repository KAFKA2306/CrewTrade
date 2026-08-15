from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from crew.data_platform.public_status import build_public_status


def _dataset_rights(platform: dict[str, Any], required: list[str]) -> list[dict[str, Any]]:
    """Project configured rights metadata onto the datasets used by a report.

    This function deliberately does not infer permission from publisher identity, URL, or
    data availability. Missing rights metadata remains missing evidence.
    """

    configured: dict[str, dict[str, Any]] = {}
    for source_name, source_config in dict(platform.get("sources", {})).items():
        if not isinstance(source_config, dict):
            continue

        for key in ("dataset", "real_dataset", "rates_dataset"):
            dataset = source_config.get(key)
            if dataset:
                configured[str(dataset)] = {
                    "dataset": str(dataset),
                    "source": source_name,
                    "license_status": source_config.get("license_status"),
                    "rights_source_url": source_config.get("rights_source_url"),
                }

        for dataset, dataset_config in dict(source_config.get("datasets", {})).items():
            if not isinstance(dataset_config, dict):
                continue
            configured[str(dataset)] = {
                "dataset": str(dataset),
                "source": source_name,
                "license_status": dataset_config.get("license_status"),
                "rights_source_url": dataset_config.get("rights_source_url")
                or dataset_config.get("source_url"),
            }

    rows = []
    for dataset in required:
        row = configured.get(dataset, {"dataset": dataset, "source": None})
        rows.append(
            {
                **row,
                "rights_evidence_status": (
                    "declared" if row.get("license_status") and row.get("rights_source_url") else "not_declared"
                ),
            }
        )
    return rows


def build_report_evidence(
    *,
    use_case: str,
    report_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
    platform = yaml.safe_load(platform_config_path.read_text(encoding="utf-8")) or {}
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

    rights = _dataset_rights(platform, required)
    missing_rights = [row["dataset"] for row in rights if row["rights_evidence_status"] != "declared"]
    if decision != "READY_FOR_REVIEW":
        distribution_decision = "NOT_EVALUATED"
    elif missing_rights:
        distribution_decision = "RIGHTS_UNVERIFIED"
    else:
        distribution_decision = "RIGHTS_REVIEW_REQUIRED"

    payload: dict[str, Any] = {
        "schema_version": 2,
        "decision": decision,
        "distribution_decision": distribution_decision,
        "external_distribution_authorized": False,
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
        "rights": {
            "datasets": rights,
            "missing_declarations": missing_rights,
            "scope": (
                "Rights evidence is read only from explicit repository configuration. The pack never "
                "infers redistribution permission from an official publisher, a reachable URL, or a "
                "successful data fetch. RIGHTS_REVIEW_REQUIRED still requires an explicit human "
                "publication decision."
            ),
        },
        "scope": (
            "READY_FOR_REVIEW proves that the report artifact is identified and all declared "
            "canonical datasets have current passing lineage records. It does not prove that "
            "the report's financial conclusions are correct or authorize publication."
        ),
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["evidence_fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def render_report_evidence_html(payload: dict[str, Any]) -> str:
    """Render the JSON evidence pack without creating a second source of truth."""

    def esc(value: Any) -> str:
        return html.escape("" if value is None else str(value), quote=True)

    def source_reference(value: Any) -> str:
        raw = "" if value is None else str(value)
        escaped = esc(raw)
        parsed = urlparse(raw)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return f'<a href="{escaped}">{escaped}</a>'
        return escaped or "—"

    rows = []
    for dataset in payload["datasets"]:
        rows.append(
            "<tr>"
            f"<td>{esc(dataset.get('dataset'))}</td>"
            f"<td>{esc(dataset.get('quality_status'))}</td>"
            f"<td>{source_reference(dataset.get('source_url'))}</td>"
            f"<td><code>{esc(dataset.get('raw_sha256'))}</code></td>"
            f"<td>{esc(dataset.get('retrieved_at'))}</td>"
            "</tr>"
        )

    rights_rows = []
    for dataset in payload["rights"]["datasets"]:
        rights_rows.append(
            "<tr>"
            f"<td>{esc(dataset.get('dataset'))}</td>"
            f"<td>{esc(dataset.get('rights_evidence_status'))}</td>"
            f"<td>{esc(dataset.get('license_status')) or '—'}</td>"
            f"<td>{source_reference(dataset.get('rights_source_url'))}</td>"
            "</tr>"
        )

    missing = ", ".join(map(str, payload["missing_datasets"])) or "なし"
    failed = ", ".join(map(str, payload["failed_datasets"])) or "なし"
    missing_rights = ", ".join(map(str, payload["rights"]["missing_declarations"])) or "なし"
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="ja">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width,initial-scale=1">',
            f"<title>Evidence Pack — {esc(payload['use_case'])}</title>",
            "</head>",
            "<body>",
            '<a class="skip-link" href="#main-content">本文へ移動</a>',
            '<main id="main-content">',
            f"<h1>Evidence Pack — {esc(payload['use_case'])}</h1>",
            f"<p><strong>系譜判定:</strong> {esc(payload['decision'])}</p>",
            f"<p><strong>外部配布判定:</strong> {esc(payload['distribution_decision'])}</p>",
            f"<p>{esc(payload['scope'])}</p>",
            "<h2>レポート識別情報</h2>",
            f"<p><code>{esc(payload['report']['path'])}</code></p>",
            f"<p>SHA-256: <code>{esc(payload['report']['sha256'])}</code></p>",
            f"<p>Evidence fingerprint: <code>{esc(payload['evidence_fingerprint'])}</code></p>",
            "<h2>データ系譜</h2>",
            f"<p>不足データセット: {esc(missing)}<br>失敗データセット: {esc(failed)}</p>",
            "<table>",
            "<thead><tr><th>Dataset</th><th>Quality</th><th>Source</th><th>Input SHA-256</th><th>Retrieved</th></tr></thead>",
            f"<tbody>{''.join(rows)}</tbody>",
            "</table>",
            "<h2>利用権エビデンス</h2>",
            f"<p>{esc(payload['rights']['scope'])}</p>",
            f"<p>宣言不足: {esc(missing_rights)}</p>",
            "<table>",
            "<thead><tr><th>Dataset</th><th>Evidence</th><th>License status</th><th>Authority</th></tr></thead>",
            f"<tbody>{''.join(rights_rows)}</tbody>",
            "</table>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def export_report_evidence(
    *,
    output_path: Path,
    use_case: str,
    report_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
    summary_output_path: Path | None = None,
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
    if summary_output_path is not None:
        summary_output_path.parent.mkdir(parents=True, exist_ok=True)
        summary_output_path.write_text(render_report_evidence_html(payload), encoding="utf-8")
    return payload
