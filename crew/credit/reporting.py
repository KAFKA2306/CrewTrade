from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
from crew.credit.config import CreditSpreadConfig
from crew.credit.insights import build_insight_markdown
class CreditSpreadReporter:
    def __init__(
        self, config: CreditSpreadConfig, processed_dir: Path, report_dir: Path
    ) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
    def persist(self, analysis_payload: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        prices = analysis_payload["prices"]
        metrics = analysis_payload["metrics"]
        edges = analysis_payload["edges"]
        snapshot = analysis_payload["snapshot"]
        stored_paths: Dict[str, Path] = {}
        prices_path = self.processed_dir / "prices.parquet"
        prices.to_parquet(prices_path)
        stored_paths["prices"] = prices_path
        metrics_path = self.processed_dir / "metrics.parquet"
        metrics.to_parquet(metrics_path)
        stored_paths["metrics"] = metrics_path
        snapshot_path = self.processed_dir / "snapshot.parquet"
        snapshot.to_parquet(snapshot_path)
        stored_paths["snapshot"] = snapshot_path
        edges_path = self.processed_dir / "edges.parquet"
        edges.to_parquet(edges_path)
        stored_paths["edges"] = edges_path
        report_path = self.report_dir / "spread_signals.md"
        report_content = self._format_report(edges, snapshot)
        if "forecasts" in analysis_payload:
            report_content += "\n
            for asset, forecast_data in analysis_payload["forecasts"].items():
                if isinstance(forecast_data, dict) and "error" in forecast_data:
                    report_content += f"
                    continue
                if not forecast_data:
                    continue
                last_forecast = forecast_data[-1]
                report_content += f"
                report_content += (
                    f"Prediction End: {last_forecast.get('date', 'N/A')}\n"
                )
                report_content += (
                    f"Predicted Close: {last_forecast.get('close', 'N/A'):.2f}\n"
                )
        report_path.write_text(report_content)
        stored_paths["report"] = report_path
        insight_path = self.report_dir / "spread_insights.md"
        insight_markdown = build_insight_markdown(analysis_payload)
        insight_path.write_text(insight_markdown)
        stored_paths["insights"] = insight_path
        return stored_paths
    def _format_report(self, edges: pd.DataFrame, snapshot: pd.DataFrame) -> str:
        lines = ["
        if snapshot.empty:
            lines.append("十分なデータがなく、スナップショットを生成できませんでした。")
            return "\n".join(lines)
        lines.append("
        lines.append("| Pair | Junk | Treasury | Date | Z | Ratio | Return Gap % |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for _, row in snapshot.sort_values(
            "z_score", key=lambda s: s.abs(), ascending=False
        ).iterrows():
            date_str = row["latest_date"].date()
            z = row["z_score"]
            ratio = row["ratio"]
            return_gap = row["return_gap"] * 100
            lines.append(
                f"| {row['pair']} | {row['junk']} | {row['treasury']} | {date_str} | {z:.2f} | {ratio:.4f} | {return_gap:.2f} |"
            )
        lines.append("")
        if edges.empty:
            lines.append("
            lines.append("しきい値を超えるスプレッドシグナルは検出されていません。")
            return "\n".join(lines)
        lines.append("
        lines.append("| Date | Pair | Signal | Z | Ratio | Return Gap % |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for _, row in edges.sort_values("date").iterrows():
            date_str = row["date"].strftime("%Y-%m-%d")
            z = row["z_score"]
            ratio = row["ratio"]
            return_gap = row["return_gap"] * 100
            lines.append(
                f"| {date_str} | {row['pair']} | {row['signal']} | {z:.2f} | {ratio:.4f} | {return_gap:.2f} |"
            )
        lines.append("")
        return "\n".join(lines)
