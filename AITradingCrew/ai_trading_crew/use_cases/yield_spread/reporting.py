from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.yield_spread.config import YieldSpreadConfig
from ai_trading_crew.use_cases.yield_spread.insights import build_insight_markdown


class YieldSpreadReporter:
    def __init__(self, config: YieldSpreadConfig, processed_dir: Path, report_dir: Path) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, analysis_payload: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        series_frame = analysis_payload["series"]
        metrics_frame = analysis_payload["metrics"]
        edges_frame = analysis_payload["edges"]
        snapshot_frame = analysis_payload["snapshot"]

        stored_paths: Dict[str, Path] = {}

        series_path = self.processed_dir / "yield_series.parquet"
        series_frame.to_parquet(series_path)
        stored_paths["series"] = series_path

        metrics_path = self.processed_dir / "metrics.parquet"
        metrics_frame.to_parquet(metrics_path)
        stored_paths["metrics"] = metrics_path

        edges_path = self.processed_dir / "edges.parquet"
        edges_frame.to_parquet(edges_path)
        stored_paths["edges"] = edges_path

        snapshot_path = self.processed_dir / "snapshot.parquet"
        snapshot_frame.to_parquet(snapshot_path)
        stored_paths["snapshot"] = snapshot_path

        report_path = self.report_dir / "yield_spread_report.md"
        report_markdown = self._build_report(snapshot_frame, edges_frame)
        report_path.write_text(report_markdown)
        stored_paths["report"] = report_path

        insight_path = self.report_dir / "yield_spread_insights.md"
        insight_markdown = build_insight_markdown(analysis_payload)
        insight_path.write_text(insight_markdown)
        stored_paths["insights"] = insight_path

        return stored_paths

    def _build_report(self, snapshot: pd.DataFrame, edges: pd.DataFrame) -> str:
        lines = ["# Yield Spread Signal Report", ""]
        if snapshot.empty:
            lines.append("データが不足しているため、スナップショットを生成できませんでした。")
            return "\n".join(lines)

        lines.append("## Latest Snapshot")
        lines.append("| Pair | Date | Spread (bp) | Z | Junk % | Treasury % |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for _, row in snapshot.sort_values("z_score", key=lambda s: s.abs(), ascending=False).iterrows():
            date_str = row["latest_date"].date()
            lines.append(
                f"| {row['pair']} | {date_str} | {row['spread_bp']:.1f} | {row['z_score']:.2f} | "
                f"{row['junk_yield']:.2f} | {row['treasury_yield']:.2f} |"
            )
        lines.append("")

        lines.append("## Triggered Signals")
        if edges.empty:
            lines.append("しきい値を超えるイールドスプレッドのイベントは検出されませんでした。")
            return "\n".join(lines)

        lines.append("| Date | Pair | Direction | Spread (bp) | Z | Junk % | Treasury % |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for _, row in edges.sort_values("date").iterrows():
            date_str = row["date"].strftime("%Y-%m-%d")
            lines.append(
                f"| {date_str} | {row['pair']} | {row['direction']} | {row['spread_bp']:.1f} | "
                f"{row['z_score']:.2f} | {row['junk_yield']:.2f} | {row['treasury_yield']:.2f} |"
            )
        lines.append("")
        return "\n".join(lines)
