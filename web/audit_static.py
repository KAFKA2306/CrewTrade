from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


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
        DOCS_DIR / "assets" / "site.js",
        DOCS_DIR / "site-manifest.json",
    ]
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing generated site files: {', '.join(missing)}")

    manifest = json.loads((DOCS_DIR / "site-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise RuntimeError("Unsupported or missing site manifest schema_version.")
    if not manifest.get("cases") or not manifest.get("total_reports"):
        raise RuntimeError("Generated site manifest contains no reports.")

    failures: list[str] = []
    manifest_report_count = 0
    for case in manifest["cases"]:
        slug = case.get("slug")
        dates = case.get("dates", [])
        if not slug or not dates:
            failures.append(f"manifest: invalid case entry {case!r}")
            continue
        if not (DOCS_DIR / slug / "index.html").is_file():
            failures.append(f"manifest: missing {slug}/index.html")
        for date in dates:
            manifest_report_count += 1
            if not (DOCS_DIR / slug / f"{date}.html").is_file():
                failures.append(f"manifest: missing {slug}/{date}.html")

    if manifest_report_count != manifest["total_reports"]:
        failures.append(
            "manifest: total_reports does not match report entries "
            f"({manifest['total_reports']} != {manifest_report_count})"
        )

    html_files = sorted(DOCS_DIR.rglob("*.html"))
    if len(html_files) != manifest_report_count + len(manifest["cases"]) + 1:
        failures.append(
            "generated HTML count does not match manifest "
            f"({len(html_files)} files)"
        )

    for html_path in html_files:
        text = html_path.read_text(encoding="utf-8")
        relative = html_path.relative_to(DOCS_DIR)
        if '<html lang="ja">' not in text:
            failures.append(f"{relative}: html language is not ja")
        if "{{" in text or "{%" in text:
            failures.append(f"{relative}: unresolved Jinja template marker")
        if "#0d1117" in text or "Select a use case" in text:
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
        f"{manifest['total_reports']} reports / {len(manifest['cases'])} cases / "
        f"{len(html_files)} HTML files"
    )


if __name__ == "__main__":
    audit()
