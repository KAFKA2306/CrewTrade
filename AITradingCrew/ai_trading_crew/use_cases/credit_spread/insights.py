from __future__ import annotations

from typing import Dict, List

import pandas as pd


def build_insight_markdown(analysis_payload: Dict[str, pd.DataFrame]) -> str:
    prices = analysis_payload["prices"]
    metrics = analysis_payload["metrics"]
    snapshot = analysis_payload["snapshot"]
    edges = analysis_payload["edges"]

    date_start = prices.index.min()
    date_end = prices.index.max()

    lines: List[str] = []
    lines.append("# Credit Spread Insight Report")
    lines.append("")
    lines.append("## Data Coverage")
    lines.append(f"- Price range: {date_start.date()} → {date_end.date()}")
    lines.append(f"- Pairs analysed: {len(snapshot)}")
    lines.append("")

    if snapshot.empty:
        lines.append("No sufficient data to compute spreads.")
        return "\n".join(lines)

    snapshot_table = snapshot.copy()
    snapshot_table["latest_date"] = snapshot_table["latest_date"].dt.date
    snapshot_table["z_score"] = snapshot_table["z_score"].round(2)
    snapshot_table["ratio"] = snapshot_table["ratio"].round(4)
    snapshot_table["return_gap"] = (snapshot_table["return_gap"] * 100).round(2)
    lines.append("## Latest Snapshot")
    lines.append(_format_table(snapshot_table, ["pair", "latest_date", "z_score", "ratio", "return_gap"], ["Pair", "Date", "Z", "Ratio", "Return Gap %"]))
    lines.append("")

    if edges.empty:
        lines.append("## Signals")
        lines.append("No |z|-score breaches within the sampled horizon.")
        return "\n".join(lines)

    lines.append("## Signals")
    lines.append(f"- Total signals: {len(edges)}")
    lines.append("")
    counts = edges.groupby(["pair", "signal"]).size().reset_index(name="signals")
    lines.append(_format_table(counts, ["pair", "signal", "signals"], ["Pair", "Signal", "Count"]))
    lines.append("")

    recent_start = edges["date"].max() - pd.Timedelta(days=90)
    recent_edges = edges[edges["date"] >= recent_start]
    lines.append("## 90-Day Activity")
    if recent_edges.empty:
        lines.append("No breaches recorded in the last 90 days.")
    else:
        recent_counts = recent_edges.groupby("pair").size().reset_index(name="signals")
        recent_median = recent_edges.groupby("pair")["z_score"].median().reset_index(name="median_z")
        merged = pd.merge(recent_counts, recent_median, on="pair", how="left")
        merged["median_z"] = merged["median_z"].round(2)
        lines.append(_format_table(merged, ["pair", "signals", "median_z"], ["Pair", "Signals", "Median |Z|"]))
    lines.append("")

    vol_stats = (
        metrics.stack(level=0)["z_score"]
        .dropna()
        .groupby(level=1)
        .agg(["mean", "std", "max"])
        .reset_index()
        .rename(columns={"level_1": "pair"})
    )
    if not vol_stats.empty:
        vol_stats["mean"] = vol_stats["mean"].round(2)
        vol_stats["std"] = vol_stats["std"].round(2)
        vol_stats["max"] = vol_stats["max"].round(2)
        lines.append("## Z-Score Distribution")
        lines.append(_format_table(vol_stats, ["pair", "mean", "std", "max"], ["Pair", "Mean", "Std", "Max"]))
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
