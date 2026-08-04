from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from build_static import DOCS_DIR, create_environment


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATUS_SOURCE = PROJECT_ROOT / "web" / "generated" / "data-platform-status.json"
STATUS_OUTPUT = DOCS_DIR / "data-status" / "index.html"
MANIFEST_PATH = DOCS_DIR / "site-manifest.json"

STATE_LABELS = {
    "ok": "正準稼働",
    "awaiting_snapshot": "取得待ち",
    "governed_blocked": "契約待ち・停止",
    "governed_partial": "一部利用可能",
    "private_input_required": "非公開入力待ち",
}


def build() -> None:
    status = json.loads(STATUS_SOURCE.read_text(encoding="utf-8"))
    _validate_status(status)
    env = create_environment()
    generated_at = datetime.fromisoformat(status["generated_at"]).astimezone(
        ZoneInfo("Asia/Tokyo")
    )
    overall_ok = status["overall_status"] == "ok"
    html = env.get_template("data_status.html").render(
        status=status,
        generated_label=generated_at.strftime("%Y-%m-%d %H:%M JST"),
        overall_label="OK · 正準データ経路は運用可能"
        if overall_ok
        else "DEGRADED · 一次スナップショット待ち",
        overall_description=(
            "正準接続済み分析は最新スナップショットを参照し、残りは理由付きの統制状態です。"
            if overall_ok
            else "構成と停止契約は有効です。正準接続済み分析の一部データがまだ取得されていません。"
        ),
        state_labels=STATE_LABELS,
    )
    STATUS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    STATUS_OUTPUT.write_text(html, encoding="utf-8")
    _inject_home_link()
    _extend_manifest(status)
    print(
        f"Built data status page: overall={status['overall_status']} "
        f"canonical_ok={status['summary']['canonical_ok']}"
    )


def _validate_status(status: dict[str, object]) -> None:
    if status.get("schema_version") != 1:
        raise ValueError("Unsupported data platform status schema")
    use_cases = status.get("use_cases")
    if not isinstance(use_cases, list) or len(use_cases) != 10:
        raise ValueError("Public status must contain exactly 10 use cases")
    slugs = [str(row.get("slug")) for row in use_cases if isinstance(row, dict)]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Public status contains duplicate use-case slugs")
    if any(
        not isinstance(row, dict) or not row.get("runtime_state")
        for row in use_cases
    ):
        raise ValueError("Every use case must expose a runtime state")


def _inject_home_link() -> None:
    index_path = DOCS_DIR / "index.html"
    text = index_path.read_text(encoding="utf-8")
    if 'href="data-status/index.html"' not in text:
        marker = '<a href="#reading-protocol">読み方</a>'
        replacement = marker + '\n        <a href="data-status/index.html">データ状態</a>'
        if marker not in text:
            raise ValueError("Could not locate the home navigation marker")
        text = text.replace(marker, replacement, 1)
        index_path.write_text(text, encoding="utf-8")


def _extend_manifest(status: dict[str, object]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["data_platform"] = {
        "path": "data-status/index.html",
        "overall_status": status["overall_status"],
        "generated_at": status["generated_at"],
        "summary": status["summary"],
        "catalog_present": status["catalog_present"],
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
