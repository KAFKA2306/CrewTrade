from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "use_cases"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def get_use_cases():
    return sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()])


def get_report_dates(use_case: str):
    case_dir = OUTPUT_DIR / use_case
    return (
        sorted([d.name for d in case_dir.iterdir() if d.is_dir()], reverse=True)
        if case_dir.exists()
        else []
    )


def get_report_content(use_case: str, date: str):
    for f in (OUTPUT_DIR / use_case / date).glob("*.md"):
        return f.read_text(encoding="utf-8")
    return None


def build():
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    DOCS_DIR.mkdir(exist_ok=True)

    use_cases = get_use_cases()

    # Index page
    index_html = env.get_template("static_index.html").render(use_cases=use_cases)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # Use case pages
    for uc in use_cases:
        uc_dir = DOCS_DIR / uc
        uc_dir.mkdir(exist_ok=True)
        dates = get_report_dates(uc)

        for date in dates:
            content = get_report_content(uc, date)
            if content:
                html_content = markdown.markdown(
                    content, extensions=["tables", "fenced_code"]
                )
                page = env.get_template("static_report.html").render(
                    name=uc, date=date, content=html_content, dates=dates
                )
                (uc_dir / f"{date}.html").write_text(page, encoding="utf-8")

        if dates:
            (uc_dir / "index.html").write_text(
                env.get_template("static_use_case.html").render(name=uc, dates=dates),
                encoding="utf-8",
            )

    print(f"Built static site in {DOCS_DIR}")


if __name__ == "__main__":
    build()
