from __future__ import annotations

from typing import Dict, List

import pandas as pd


def build_insight_markdown(analysis_payload: Dict[str, pd.DataFrame]) -> str:
    metrics = analysis_payload["metrics"]
    snapshot = analysis_payload["snapshot"]
    edges = analysis_payload["edges"]

    # Determine coverage from underlying metrics index
    date_start = metrics.index.min()
    date_end = metrics.index.max()

    lines: List[str] = []
    lines.append("# Yield Spread Insight Report")
    lines.append("")
    lines.append("## Data Coverage")
    if pd.isna(date_start) or pd.isna(date_end):
        lines.append("Insufficient data to compute coverage.")
        return "\n".join(lines)
    lines.append(f"- Date range: {date_start.date()} → {date_end.date()}")
    lines.append(f"- Pairs analysed: {len(snapshot)}")
    lines.append("")

    if snapshot.empty:
        lines.append("No spreads available for summary.")
        return "\n".join(lines)

    latest_table = snapshot.copy()
    latest_table["latest_date"] = latest_table["latest_date"].dt.date
    latest_table["spread_bp"] = latest_table["spread_bp"].round(1)
    latest_table["spread"] = latest_table["spread"].round(4)
    latest_table["z_score"] = latest_table["z_score"].round(2)
    latest_table["junk_yield"] = latest_table["junk_yield"].round(2)
    latest_table["treasury_yield"] = latest_table["treasury_yield"].round(2)
    lines.append("## Latest Snapshot")
    lines.append(
        _format_table(
            latest_table,
            ["pair", "latest_date", "spread_bp", "z_score", "junk_yield", "treasury_yield"],
            ["Pair", "Date", "Spread (bp)", "Z", "Junk %", "Treasury %"],
        )
    )
    lines.append("")

    if edges.empty:
        lines.append("## Signals")
        lines.append("No z-score triggered events within the sampled window.")
        return "\n".join(lines)

    lines.append("## Signals")
    lines.append(f"- Total signals: {len(edges)}")
    lines.append("")
    counts = edges.groupby(["pair", "direction"]).size().reset_index(name="signals")
    lines.append(_format_table(counts, ["pair", "direction", "signals"], ["Pair", "Direction", "Count"]))
    lines.append("")

    recent_start = edges["date"].max() - pd.Timedelta(days=90)
    recent_edges = edges[edges["date"] >= recent_start]
    lines.append("## 90-Day Activity")
    if recent_edges.empty:
        lines.append("No signals in the last 90 days.")
    else:
        recent_stats = recent_edges.groupby("pair").agg(
            signals=("pair", "size"),
            median_z=("z_score", lambda x: float(pd.Series(x).abs().median())),
            median_spread_bp=("spread_bp", "median"),
        )
        recent_stats = recent_stats.reset_index()
        recent_stats["median_z"] = recent_stats["median_z"].round(2)
        recent_stats["median_spread_bp"] = recent_stats["median_spread_bp"].round(1)
        lines.append(
            _format_table(
                recent_stats,
                ["pair", "signals", "median_z", "median_spread_bp"],
                ["Pair", "Signals", "Median |Z|", "Median bp"],
            )
        )
    lines.append("")

    try:
        spread_bp = metrics.xs("spread_bp", axis=1, level=1)
    except (KeyError, ValueError):
        spread_bp = pd.DataFrame()
    if not spread_bp.empty:
        dist = spread_bp.agg(["mean", "median", "max", "min"]).T.reset_index()
        dist = dist.rename(
            columns={
                "index": "pair",
                "mean": "mean",
                "median": "median",
                "max": "max",
                "min": "min",
            }
        )
        dist["mean"] = dist["mean"].round(1)
        dist["median"] = dist["median"].round(1)
        dist["max"] = dist["max"].round(1)
        dist["min"] = dist["min"].round(1)
        lines.append("## Spread Distribution (bp)")
        lines.append(_format_table(dist, ["pair", "mean", "median", "max", "min"], ["Pair", "Mean", "Median", "Max", "Min"]))
        lines.append("")

    return "\n".join(lines)


def _format_table(df: pd.DataFrame, columns: List[str], headers: List[str]) -> str:
    table_lines: List[str] = []
    table_lines.append("| " + " | ".join(headers) + " |")
    table_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df[columns].iterrows():
        formatted: List[str] = []
        for col in columns:
            value = row[col]
            if isinstance(value, float):
                formatted.append(f"{value:.2f}")
            else:
                formatted.append(str(value))
        table_lines.append("| " + " | ".join(formatted) + " |")
    return "\n".join(table_lines)
