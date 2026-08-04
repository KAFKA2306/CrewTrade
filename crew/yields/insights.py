from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def build_insight_markdown(analysis_payload: Dict[str, Any]) -> str:
    """Return a compact optional summary for canonical Treasury output."""

    snapshot = analysis_payload.get("spread_snapshot", pd.DataFrame())
    signals = analysis_payload.get("signals", pd.DataFrame())
    lines = ["## 正準カーブ・スプレッド", ""]
    if not isinstance(snapshot, pd.DataFrame) or snapshot.empty:
        lines.append("正準カーブ・スプレッドはありません。")
        return "\n".join(lines)

    lines.extend(
        [
            "| 指標 | 観測日 | 短期 | 長期 | スプレッド | 20日変化 | z値 |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for _, row in snapshot.sort_values("spread").iterrows():
        lines.append(
            "| {spread} | {date} | {short:.2f}% | {long:.2f}% | "
            "{level:+.1f}bp | {change} | {z} |".format(
                spread=row["spread"],
                date=pd.Timestamp(row["latest_date"]).date(),
                short=float(row["short_rate_pct"]),
                long=float(row["long_rate_pct"]),
                level=float(row["spread_bp"]),
                change=_format_bp(row.get("change_20d_bp")),
                z=_format_number(row.get("z_score")),
            )
        )
    signal_count = len(signals) if isinstance(signals, pd.DataFrame) else 0
    lines.extend(["", f"閾値超過イベント: {signal_count}件"])
    return "\n".join(lines)


def _format_bp(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.1f}bp"


def _format_number(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.2f}"
