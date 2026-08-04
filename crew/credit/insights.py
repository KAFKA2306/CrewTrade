from __future__ import annotations

from typing import Dict

import pandas as pd


_LABELS = {
    "us_corporate_oas": "米国社債OAS",
    "us_bbb_oas": "米国BBB社債OAS",
    "us_high_yield_oas": "米国ハイイールドOAS",
}


def build_insight_markdown(
    analysis_payload: Dict[str, pd.DataFrame],
) -> str:
    """Return a compact optional summary for canonical OAS output."""

    snapshot = analysis_payload.get("snapshot", pd.DataFrame())
    signals = analysis_payload.get("signals", pd.DataFrame())
    lines = ["## 正準OASスナップショット", ""]
    if snapshot.empty:
        lines.append("正準OASスナップショットはありません。")
        return "\n".join(lines)

    table = snapshot.copy().sort_values("series")
    lines.extend(
        [
            "| 系列 | 観測日 | 水準 | 20日変化 | z値 |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for _, row in table.iterrows():
        lines.append(
            "| {label} | {date} | {level:.2f}% | {change} | {z} |".format(
                label=_LABELS.get(str(row["series"]), str(row["series"])),
                date=pd.Timestamp(row["latest_date"]).date(),
                level=float(row["level_pct"]),
                change=_format_bp(row.get("change_20d_bp")),
                z=_format_number(row.get("z_score")),
            )
        )
    lines.extend(["", f"閾値超過イベント: {len(signals)}件"])
    return "\n".join(lines)


def _format_bp(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.1f}bp"


def _format_number(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.2f}"
