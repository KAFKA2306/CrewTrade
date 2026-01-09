from pathlib import Path
from flask import Flask, render_template, abort
import markdown

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "use_cases"


def get_use_cases():
    return sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()])


def get_report_dates(use_case: str):
    case_dir = OUTPUT_DIR / use_case
    if not case_dir.exists():
        return []
    return sorted([d.name for d in case_dir.iterdir() if d.is_dir()], reverse=True)


def get_report_content(use_case: str, date: str):
    report_dir = OUTPUT_DIR / use_case / date
    for f in report_dir.glob("*.md"):
        return f.read_text(encoding="utf-8")
    return None


@app.route("/")
def index():
    use_cases = get_use_cases()
    return render_template("index.html", use_cases=use_cases)


@app.route("/use_case/<name>")
def use_case(name: str):
    dates = get_report_dates(name)
    if not dates:
        abort(404)
    return render_template("use_case.html", name=name, dates=dates)


@app.route("/report/<name>/<date>")
def report(name: str, date: str):
    content = get_report_content(name, date)
    if content is None:
        abort(404)
    html_content = markdown.markdown(content, extensions=["tables", "fenced_code"])
    return render_template("report_fragment.html", content=html_content)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
