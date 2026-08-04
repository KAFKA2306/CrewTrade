from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
CONTENT_REFRESH_DATE = "20260804"
CONTENT_REFRESH_LABEL = "更新基準日: 2026-08-04"
REQUIRED_CASE_FIELDS = {
    "slug",
    "title",
    "category",
    "purpose",
    "scope",
    "period",
    "status",
    "summary",
    "question",
    "warning",
    "change_summary",
    "accent",
}
REQUIRED_REPORT_SECTIONS = {
    "## データ": "data section",
    "## 定量分析": "quantitative analysis section",
    "## 評価": "evaluation section",
    "## 限界": "limitations section",
    "## 一次情報": "primary-source section",
}


class LocalReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.references.append(("href", values["href"] or ""))
        if tag in {"img", "script", "source"} and values.get("src"):
            self.references.append(("src", values["src"] or ""))


def resolve_local_reference(html_path: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:", "data:")):
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return None

    if path_text.startswith("/"):
        candidate = DOCS_DIR / path_text.lstrip("/")
    else:
        candidate = html_path.parent / path_text

    candidate = candidate.resolve()
    docs_root = DOCS_DIR.resolve()
    if docs_root not in candidate.parents and candidate != docs_root:
        raise RuntimeError(f"Reference escapes docs root: {reference}")

    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


def audit() -> None:
    required = [
        DOCS_DIR / "index.html",
        DOCS_DIR / "assets" / "site.css",
        DOCS_DIR / "assets" / "table.css",
        DOCS_DIR / "assets" / "site.js",
        DOCS_DIR / "site-manifest.json",
    ]
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing generated site files: {', '.join(missing)}")

    manifest = json.loads((DOCS_DIR / "site-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 2:
        raise RuntimeError("Unsupported or missing site manifest schema_version 2.")
    if not manifest.get("cases") or not manifest.get("total_reports"):
        raise RuntimeError("Generated site manifest contains no reports.")
    if manifest.get("site_latest_date") != CONTENT_REFRESH_DATE:
        raise RuntimeError("site_latest_date does not match the audited content refresh date.")
    if not manifest.get("purposes"):
        raise RuntimeError("Generated site manifest contains no research purposes.")

    failures: list[str] = []
    index_text = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
    required_index_markers = {
        'class="skip-link"': "skip link",
        'id="research-catalogue"': "catalogue landmark",
        'data-case-controls': "catalogue controls",
        'data-purpose-filter': "purpose filter",
        'data-freshness-filter': "freshness filter",
        'data-clear-filters': "clear filters action",
        'data-empty-state': "empty state",
        'data-case-view="table"': "table view container",
        'data-case-view="cards"': "card view container",
        'data-view-button="table"': "table view button",
        'data-view-button="cards"': "card view button",
        'class="case-table"': "research comparison table",
        'data-purpose-section': "purpose groups",
        'href="assets/table.css"': "table stylesheet",
    }
    for marker, label in required_index_markers.items():
        if marker not in index_text:
            failures.append(f"index.html: missing {label}")

    manifest_report_count = 0
    manifest_companion_count = 0
    for case in manifest["cases"]:
        missing_fields = sorted(REQUIRED_CASE_FIELDS.difference(case))
        if missing_fields:
            failures.append(f"manifest: {case.get('slug', '<unknown>')} missing {missing_fields}")

        slug = case.get("slug")
        dates = case.get("dates", [])
        source_map = case.get("sources", {})
        companion_map = case.get("companions", {})
        if not slug or not dates:
            failures.append(f"manifest: invalid case entry {case!r}")
            continue

        if dates[0] != CONTENT_REFRESH_DATE:
            failures.append(
                f"manifest: {slug} latest report is {dates[0]}, expected {CONTENT_REFRESH_DATE}"
            )

        if case.get("purpose") not in manifest["purposes"]:
            failures.append(f"manifest: {slug} purpose is not registered")

        case_index = DOCS_DIR / slug / "index.html"
        if not case_index.is_file():
            failures.append(f"manifest: missing {slug}/index.html")
        else:
            case_text = case_index.read_text(encoding="utf-8")
            for marker, label in {
                'class="skip-link"': "skip link",
                'id="report-history"': "report history target",
                'class="report-table"': "report table",
                'href="../assets/table.css"': "table stylesheet",
            }.items():
                if marker not in case_text:
                    failures.append(f"{slug}/index.html: missing {label}")

        latest_date = dates[0]
        latest_source_name = source_map.get(latest_date)
        if not latest_source_name:
            failures.append(f"manifest: missing source mapping for {slug}/{latest_date}")
        else:
            latest_source = (
                PROJECT_ROOT
                / "output"
                / "use_cases"
                / slug
                / latest_date
                / latest_source_name
            )
            if not latest_source.is_file():
                failures.append(
                    f"manifest: missing source report {slug}/{latest_date}/{latest_source_name}"
                )
            else:
                source_text = latest_source.read_text(encoding="utf-8")
                if CONTENT_REFRESH_LABEL not in source_text:
                    failures.append(
                        f"{slug}/{latest_date}/{latest_source_name}: missing content refresh marker"
                    )
                for marker, label in REQUIRED_REPORT_SECTIONS.items():
                    if marker not in source_text:
                        failures.append(
                            f"{slug}/{latest_date}/{latest_source_name}: missing {label}"
                        )
                primary_source_section = source_text.split("## 一次情報", maxsplit=1)
                if len(primary_source_section) != 2 or "https://" not in primary_source_section[1]:
                    failures.append(
                        f"{slug}/{latest_date}/{latest_source_name}: primary-source section has no URL"
                    )

        latest_report = DOCS_DIR / slug / f"{latest_date}.html"
        if latest_report.is_file():
            latest_text = latest_report.read_text(encoding="utf-8")
            if CONTENT_REFRESH_LABEL not in latest_text:
                failures.append(
                    f"{slug}/{latest_date}.html: missing content refresh marker"
                )
            if 'id="report-content"' not in latest_text:
                failures.append(f"{slug}/{latest_date}.html: missing report content target")

        for date in dates:
            manifest_report_count += 1
            if not (DOCS_DIR / slug / f"{date}.html").is_file():
                failures.append(f"manifest: missing {slug}/{date}.html")
            companions = companion_map.get(date, [])
            if not isinstance(companions, list):
                failures.append(f"manifest: invalid companions for {slug}/{date}")
                continue
            for companion in companions:
                manifest_companion_count += 1
                if not (DOCS_DIR / slug / companion).is_file():
                    failures.append(f"manifest: missing {slug}/{companion}")

    if manifest_report_count != manifest["total_reports"]:
        failures.append(
            "manifest: total_reports does not match report entries "
            f"({manifest['total_reports']} != {manifest_report_count})"
        )

    html_files = sorted(DOCS_DIR.rglob("*.html"))
    expected_html_count = manifest_report_count + manifest_companion_count + len(manifest["cases"]) + 1
    if len(html_files) != expected_html_count:
        failures.append(
            "generated HTML count does not match manifest "
            f"({len(html_files)} != {expected_html_count})"
        )

    for html_path in html_files:
        text = html_path.read_text(encoding="utf-8")
        relative = html_path.relative_to(DOCS_DIR)
        if '<html lang="ja">' not in text:
            failures.append(f"{relative}: html language is not ja")
        if 'class="skip-link"' not in text:
            failures.append(f"{relative}: missing skip link")
        if "<main" not in text or "</main>" not in text:
            failures.append(f"{relative}: missing main landmark")
        if "{{" in text or "{%" in text:
            failures.append(f"{relative}: unresolved Jinja template marker")
        if "#0d1117" in text or "Select a use case" in text or "View analysis reports" in text:
            failures.append(f"{relative}: legacy dashboard content remains")

        parser = LocalReferenceParser()
        parser.feed(text)
        for attribute, reference in parser.references:
            try:
                target = resolve_local_reference(html_path, reference)
            except RuntimeError as error:
                failures.append(f"{relative}: {error}")
                continue
            if target is not None and not target.is_file():
                failures.append(
                    f"{relative}: broken local {attribute}={reference!r} "
                    f"-> {target.relative_to(DOCS_DIR.resolve())}"
                )

    if failures:
        raise RuntimeError("Static site audit failed:\n- " + "\n- ".join(failures))

    print(
        "Static site audit passed: "
        f"{manifest['total_reports']} reports / "
        f"{manifest_companion_count} companion pages / "
        f"{len(manifest['cases'])} cases / {len(html_files)} HTML files / "
        f"decision catalogue enabled / quantitative evidence contract enabled / "
        f"content refreshed {CONTENT_REFRESH_DATE}"
    )


if __name__ == "__main__":
    audit()
