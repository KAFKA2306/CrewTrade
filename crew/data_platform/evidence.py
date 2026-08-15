from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from crew.data_platform.public_status import build_public_status


def build_report_evidence(
    *,
    use_case: str,
    report_path: Path,
    platform_config_path: Path,
    migration_config_path: Path,
    root: Path | None = None,
) -> dict[str, Any]:
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

    payload: dict[str, Any] = {
        "schema_version": 1,
        "decision": decision,
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

    missing = ", ".join(map(str, payload["missing_datasets"])) or "なし"
    failed = ", ".join(map(str, payload["failed_datasets"])) or "なし"
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
            f"<p><strong>判定:</strong> {esc(payload['decision'])}</p>",
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
