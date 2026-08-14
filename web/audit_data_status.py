from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
STATUS_SOURCE = PROJECT_ROOT / "web" / "generated" / "data-platform-status.json"
STATUS_PAGE = DOCS_DIR / "data-status" / "index.html"
MANIFEST = DOCS_DIR / "site-manifest.json"
ALLOWED_STATES = {
    "ok",
    "awaiting_snapshot",
    "governed_blocked",
    "governed_partial",
    "private_input_required",
}


def audit() -> None:
    failures: list[str] = []
    for path in (STATUS_SOURCE, STATUS_PAGE, MANIFEST, DOCS_DIR / "index.html"):
        if not path.is_file():
            failures.append(f"missing required file: {path.relative_to(PROJECT_ROOT)}")
    if failures:
        raise RuntimeError("Data status audit failed:\n- " + "\n- ".join(failures))

    status = json.loads(STATUS_SOURCE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    page = STATUS_PAGE.read_text(encoding="utf-8")
    index = (DOCS_DIR / "index.html").read_text(encoding="utf-8")

    if status.get("schema_version") != 1:
        failures.append("status schema_version must be 1")
    use_cases = status.get("use_cases")
    if not isinstance(use_cases, list) or len(use_cases) != 10:
        failures.append("status must contain exactly 10 use cases")
        use_cases = []
    slugs = [str(row.get("slug")) for row in use_cases if isinstance(row, dict)]
    if len(slugs) != len(set(slugs)):
        failures.append("status contains duplicate use-case slugs")
    for row in use_cases:
        if not isinstance(row, dict):
            failures.append("invalid use-case status row")
            continue
        if row.get("runtime_state") not in ALLOWED_STATES:
            failures.append(f"invalid state for {row.get('slug')}: {row.get('runtime_state')}")
        if not row.get("owner_source") or not row.get("note"):
            failures.append(f"missing owner/note for {row.get('slug')}")
        if row.get("declared_state") == "canonical_active" and not row.get("required_datasets"):
            failures.append(f"canonical use case has no datasets: {row.get('slug')}")

    summary = status.get("summary", {})
    if summary.get("use_case_count") != 10:
        failures.append("summary use_case_count must be 10")
    if status.get("overall_status") == "ok":
        if (
            summary.get("canonical_ok") != 1
            or summary.get("controlled_blocks") != 9
            or summary.get("awaiting_snapshot") != 0
        ):
            failures.append(
                "OK requires one reachable canonical use case, nine controlled states, "
                "and no pending snapshot"
            )
    elif status.get("overall_status") != "degraded":
        failures.append("overall_status must be ok or degraded")

    required_page_markers = {
        '<html lang="ja">': "Japanese language",
        'id="data-platform-status"': "data platform landmark",
        'id="use-case-status"': "use-case status section",
        'class="case-table data-use-case-table"': "use-case table",
        "data-platform-overall=": "overall status marker",
        'href="../assets/site.css"': "site stylesheet",
        'href="../index.html"': "home link",
    }
    for marker, label in required_page_markers.items():
        if marker not in page:
            failures.append(f"status page missing {label}")

    datasets = status.get("datasets", [])
    if datasets:
        if 'class="case-table data-status-table"' not in page:
            failures.append("status page missing dataset table")
    elif "公開用スナップショット未生成" not in page:
        failures.append("status page missing explicit empty dataset state")

    if 'href="data-status/index.html"' not in index:
        failures.append("home page has no data-status link")

    manifest_status = manifest.get("data_platform")
    if not isinstance(manifest_status, dict):
        failures.append("site manifest has no data_platform entry")
    else:
        if manifest_status.get("path") != "data-status/index.html":
            failures.append("manifest data platform path is incorrect")
        if manifest_status.get("overall_status") != status.get("overall_status"):
            failures.append("manifest/status overall values differ")

    forbidden_public_keys = (
        '"market_price"',
        '"quantity"',
        '"collateral_haircut"',
        '"contract_version"',
    )
    source_text = STATUS_SOURCE.read_text(encoding="utf-8")
    for forbidden in forbidden_public_keys:
        if forbidden in source_text:
            failures.append(f"public status exposes private field {forbidden}")

    if failures:
        raise RuntimeError("Data status audit failed:\n- " + "\n- ".join(failures))
    print(
        "Data status audit passed: "
        f"overall={status['overall_status']} / use_cases=10 / "
        f"canonical_ok={summary['canonical_ok']} / "
        f"controlled={summary['controlled_blocks']}"
    )


if __name__ == "__main__":
    audit()
