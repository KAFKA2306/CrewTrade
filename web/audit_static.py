from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


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
    for html_path in DOCS_DIR.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        relative = html_path.relative_to(DOCS_DIR)
        if '<html lang="ja">' not in text:
            failures.append(f"{relative}: html language is not ja")
        if "{{" in text or "{%" in text:
            failures.append(f"{relative}: unresolved Jinja template marker")
        if "#0d1117" in text or "Select a use case" in text:
            failures.append(f"{relative}: legacy dashboard content remains")

    if failures:
        raise RuntimeError("Static site audit failed:\n- " + "\n- ".join(failures))

    print(
        "Static site audit passed: "
        f"{manifest['total_reports']} reports / {len(manifest['cases'])} cases"
    )


if __name__ == "__main__":
    audit()
