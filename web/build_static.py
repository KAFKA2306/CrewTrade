from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from catalog import describe_case, format_report_date

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "use_cases"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"


def create_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["report_date"] = format_report_date
    return env


def get_use_cases() -> list[str]:
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(f"Analysis output directory does not exist: {OUTPUT_DIR}")
    return sorted(directory.name for directory in OUTPUT_DIR.iterdir() if directory.is_dir())


def report_source(report_dir: Path) -> Path | None:
    candidates = sorted(report_dir.glob("*.md"))
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    preferred = [path for path in candidates if path.name in {"report.md", "analysis_report.md"}]
    if len(preferred) == 1:
        return preferred[0]

    names = ", ".join(path.name for path in candidates)
    raise RuntimeError(
        f"Ambiguous report source in {report_dir}: {names}. "
        "Keep one Markdown file or name the intended file report.md."
    )


def get_report_dates(use_case: str) -> list[str]:
    case_dir = OUTPUT_DIR / use_case
    dates = [
        directory.name
        for directory in case_dir.iterdir()
        if directory.is_dir() and report_source(directory) is not None
    ]
    return sorted(dates, reverse=True)


def copy_report_assets(report_dir: Path, case_docs_dir: Path, date: str) -> dict[str, str]:
    rewrites: dict[str, str] = {}
    for source in sorted(report_dir.rglob("*")):
        if not source.is_file() or source.suffix.lower() == ".md":
            continue
        relative = source.relative_to(report_dir)
        target = case_docs_dir / "assets" / date / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rewrites[relative.as_posix()] = f"assets/{date}/{relative.as_posix()}"
    return rewrites


def rewrite_asset_links(markdown_text: str, rewrites: dict[str, str]) -> str:
    updated = markdown_text
    for source, target in rewrites.items():
        updated = updated.replace(f"]({source})", f"]({target})")
        updated = updated.replace(f'src="{source}"', f'src="{target}"')
        updated = updated.replace(f"src='{source}'", f"src='{target}'")
        updated = updated.replace(f'href="{source}"', f'href="{target}"')
        updated = updated.replace(f"href='{source}'", f"href='{target}'")
    return updated


def reset_docs_dir() -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    preserved = {"CNAME", ".nojekyll"}
    for path in DOCS_DIR.iterdir():
        if path.name in preserved:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def copy_site_assets() -> None:
    target = DOCS_DIR / "assets"
    target.mkdir(parents=True, exist_ok=True)
    for source in sorted(STATIC_DIR.iterdir()):
        if source.is_file():
            shutil.copy2(source, target / source.name)


def build() -> None:
    env = create_environment()
    reset_docs_dir()
    copy_site_assets()

    use_cases = get_use_cases()
    cards: list[dict[str, object]] = []
    report_index: list[dict[str, object]] = []

    for slug in use_cases:
        dates = get_report_dates(slug)
        if not dates:
            continue
        meta = describe_case(slug)
        cards.append(
            {
                **meta,
                "report_count": len(dates),
                "latest_date": dates[0],
                "latest_date_label": format_report_date(dates[0]),
            }
        )
        report_index.append({"slug": slug, "dates": dates, **meta})

    if not cards:
        raise RuntimeError("No publishable Markdown reports were found under output/use_cases.")

    index_html = env.get_template("static_index.html").render(
        cases=cards,
        total_reports=sum(int(card["report_count"]) for card in cards),
    )
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for case in cards:
        slug = str(case["slug"])
        dates = get_report_dates(slug)
        case_docs_dir = DOCS_DIR / slug
        case_docs_dir.mkdir(exist_ok=True)

        use_case_html = env.get_template("static_use_case.html").render(case=case, dates=dates)
        (case_docs_dir / "index.html").write_text(use_case_html, encoding="utf-8")

        for date in dates:
            report_dir = OUTPUT_DIR / slug / date
            source = report_source(report_dir)
            if source is None:
                continue
            raw_markdown = source.read_text(encoding="utf-8")
            rewrites = copy_report_assets(report_dir, case_docs_dir, date)
            raw_markdown = rewrite_asset_links(raw_markdown, rewrites)
            html_content = markdown.markdown(
                raw_markdown,
                extensions=["tables", "fenced_code", "sane_lists"],
                output_format="html5",
            )
            report_html = env.get_template("static_report.html").render(
                case=case,
                date=date,
                dates=dates,
                content=html_content,
                source_name=source.name,
            )
            (case_docs_dir / f"{date}.html").write_text(report_html, encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "source_revision": os.environ.get("GITHUB_SHA", "local"),
        "cases": report_index,
        "total_reports": sum(len(item["dates"]) for item in report_index),
    }
    (DOCS_DIR / "site-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {manifest['total_reports']} reports across {len(cards)} cases in {DOCS_DIR}")


if __name__ == "__main__":
    build()
