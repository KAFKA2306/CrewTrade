from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import markdown
from catalog import describe_case, format_report_date, purpose_rank
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

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


def report_priority(path: Path, slug: str) -> int:
    """Rank Markdown files by their likelihood of being the public report."""
    name = path.name.lower()
    slug = slug.lower()

    if name == "report.md":
        return 1000
    if name == "analysis_report.md":
        return 950
    if name == f"{slug}_report.md":
        return 900
    if name in {f"{slug}_summary.md", f"{slug}_overview.md"}:
        return 875
    if name.startswith(f"{slug}_") and any(token in name for token in ("summary", "overview")):
        return 850

    score = 0
    if name.endswith("_report.md"):
        score = 800
    if any(token in name for token in ("summary", "overview", "insight")):
        score = max(score, 700)
    if name in {"analysis.md", "results.md", "result.md"}:
        score = max(score, 650)

    companion_tokens = (
        "validation",
        "audit",
        "signal",
        "appendix",
        "detail",
        "raw",
        "data",
        "diagnostic",
        "check",
    )
    if any(token in name for token in companion_tokens):
        score -= 400

    return score


def report_source(report_dir: Path) -> Path | None:
    candidates = sorted(report_dir.glob("*.md"))
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    slug = report_dir.parent.name
    ranked = sorted(
        ((report_priority(path, slug), path) for path in candidates),
        key=lambda item: (-item[0], item[1].name),
    )
    top_score = ranked[0][0]
    top = [path for score, path in ranked if score == top_score]
    if len(top) == 1:
        selected = top[0]
        names = ", ".join(path.name for path in candidates)
        print(
            f"Selected {selected.name} as the public report for "
            f"{report_dir.relative_to(OUTPUT_DIR)} from: {names}"
        )
        return selected

    ranking = ", ".join(f"{path.name}={score}" for score, path in ranked)
    raise RuntimeError(
        f"Ambiguous report source in {report_dir}: {ranking}. "
        "Add report.md to explicitly identify the public report."
    )


def get_report_dates(use_case: str) -> list[str]:
    case_dir = OUTPUT_DIR / use_case
    dates = [
        directory.name
        for directory in case_dir.iterdir()
        if directory.is_dir() and report_source(directory) is not None
    ]
    return sorted(dates, reverse=True)


def add_rewrite_aliases(rewrites: dict[str, str], source: str, target: str) -> None:
    rewrites[source] = target
    if not source.startswith("./"):
        rewrites[f"./{source}"] = target


def companion_output_names(report_dir: Path, selected_source: Path, date: str) -> list[str]:
    return [
        f"{date}-{companion.stem}.html"
        for companion in sorted(report_dir.glob("*.md"))
        if companion != selected_source
    ]


def prepare_report_assets(
    report_dir: Path,
    case_docs_dir: Path,
    date: str,
    selected_source: Path,
) -> dict[str, str]:
    """Copy binary assets and map companion Markdown files to generated HTML."""
    rewrites: dict[str, str] = {}

    for source in sorted(report_dir.rglob("*")):
        if not source.is_file() or source.suffix.lower() == ".md":
            continue
        relative = source.relative_to(report_dir)
        target = case_docs_dir / "assets" / date / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        add_rewrite_aliases(
            rewrites,
            relative.as_posix(),
            f"assets/{date}/{relative.as_posix()}",
        )

    for companion in sorted(report_dir.glob("*.md")):
        if companion == selected_source:
            continue
        output_name = f"{date}-{companion.stem}.html"
        add_rewrite_aliases(rewrites, companion.name, output_name)

    return rewrites


def rewrite_asset_links(markdown_text: str, rewrites: dict[str, str]) -> str:
    updated = markdown_text
    for source, target in sorted(rewrites.items(), key=lambda item: -len(item[0])):
        updated = updated.replace(f"]({source})", f"]({target})")
        updated = updated.replace(f'src="{source}"', f'src="{target}"')
        updated = updated.replace(f"src='{source}'", f"src='{target}'")
        updated = updated.replace(f'href="{source}"', f'href="{target}"')
        updated = updated.replace(f"href='{source}'", f"href='{target}'")
    return updated


def markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


def render_report_page(
    env: Environment,
    *,
    case: dict[str, object],
    date: str,
    dates: list[str],
    source: Path,
    rewrites: dict[str, str],
) -> str:
    raw_markdown = rewrite_asset_links(source.read_text(encoding="utf-8"), rewrites)
    return env.get_template("static_report.html").render(
        case=case,
        date=date,
        dates=dates,
        content=markdown_to_html(raw_markdown),
        source_name=source.name,
    )


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
        sources: dict[str, str] = {}
        companions: dict[str, list[str]] = {}
        for date in dates:
            report_dir = OUTPUT_DIR / slug / date
            source = report_source(report_dir)
            if source is None:
                continue
            sources[date] = source.name
            companions[date] = companion_output_names(report_dir, source, date)

        cards.append(
            {
                **meta,
                "report_count": len(dates),
                "latest_date": dates[0],
                "latest_date_label": format_report_date(dates[0]),
            }
        )
        report_index.append(
            {
                "slug": slug,
                "dates": dates,
                "sources": sources,
                "companions": companions,
                **meta,
            }
        )

    if not cards:
        raise RuntimeError("No publishable Markdown reports were found under output/use_cases.")

    cards.sort(key=lambda item: (purpose_rank(str(item["purpose"])), str(item["title"])))
    site_latest_date = max(str(card["latest_date"]) for card in cards)
    for card in cards:
        card["freshness"] = "current" if card["latest_date"] == site_latest_date else "archive"

    purposes: list[str] = []
    for card in cards:
        purpose = str(card["purpose"])
        if purpose not in purposes:
            purposes.append(purpose)

    index_html = env.get_template("static_index.html").render(
        cases=cards,
        purposes=purposes,
        total_reports=sum(int(card["report_count"]) for card in cards),
        site_latest_date=site_latest_date,
        site_latest_date_label=format_report_date(site_latest_date),
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

            rewrites = prepare_report_assets(report_dir, case_docs_dir, date, source)
            report_html = render_report_page(
                env,
                case=case,
                date=date,
                dates=dates,
                source=source,
                rewrites=rewrites,
            )
            (case_docs_dir / f"{date}.html").write_text(report_html, encoding="utf-8")

            for companion in sorted(report_dir.glob("*.md")):
                if companion == source:
                    continue
                companion_html = render_report_page(
                    env,
                    case=case,
                    date=date,
                    dates=dates,
                    source=companion,
                    rewrites=rewrites,
                )
                output_name = f"{date}-{companion.stem}.html"
                (case_docs_dir / output_name).write_text(companion_html, encoding="utf-8")

    manifest = {
        "schema_version": 2,
        "source_revision": os.environ.get("GITHUB_SHA", "local"),
        "site_latest_date": site_latest_date,
        "purposes": purposes,
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
