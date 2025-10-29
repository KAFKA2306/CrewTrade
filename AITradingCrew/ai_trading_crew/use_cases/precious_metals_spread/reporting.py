from pathlib import Path
from typing import Dict
import pandas as pd
from ai_trading_crew.use_cases.precious_metals_spread.config import PreciousMetalsSpreadConfig


class PreciousMetalsSpreadReporter:
    def __init__(self, config: PreciousMetalsSpreadConfig, processed_dir: Path, report_dir: Path) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, analysis_payload: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        aligned_frames = analysis_payload["aligned"]
        theoretical_frame = analysis_payload["theoretical"]
        metrics_frame = analysis_payload["metrics"]
        edges_frame = analysis_payload["edges"]
        stored_paths: Dict[str, Path] = {}
        for name, frame in aligned_frames.items():
            path = self.processed_dir / f"aligned_{name}.parquet"
            frame.to_parquet(path)
            stored_paths[f"aligned_{name}"] = path
        theoretical_path = self.processed_dir / "theoretical_prices.parquet"
        theoretical_frame.to_parquet(theoretical_path)
        stored_paths["theoretical_prices"] = theoretical_path
        metrics_path = self.processed_dir / "metrics.parquet"
        metrics_frame.to_parquet(metrics_path)
        stored_paths["metrics"] = metrics_path
        edges_path = self.processed_dir / "edges.parquet"
        edges_frame.to_parquet(edges_path)
        stored_paths["edges"] = edges_path
        report_path = self.report_dir / "edge_report.md"
        markdown = self._format_report(edges_frame)
        report_path.write_text(markdown)
        stored_paths["report"] = report_path
        return stored_paths

    def _format_report(self, edges_frame: pd.DataFrame) -> str:
        lines = ["# Precious Metals Spread Edge Report", ""]
        if len(edges_frame) == 0:
            lines.append("検出された乖離シグナルはありません。")
            return "\n".join(lines)
        grouped = edges_frame.groupby("ticker")
        for ticker, frame in grouped:
            lines.append(f"## {ticker}")
            lines.append("")
            lines.append("| date | gap | gap_pct | z_score | direction |")
            lines.append("| --- | --- | --- | --- | --- |")
            for _, row in frame.iterrows():
                date_str = row["date"].strftime("%Y-%m-%d")
                gap_str = f"{row['gap']:.2f}"
                gap_pct_str = f"{row['gap_pct']:.4f}"
                z_score_str = f"{row['z_score']:.2f}"
                direction_str = row["direction"]
                lines.append(f"| {date_str} | {gap_str} | {gap_pct_str} | {z_score_str} | {direction_str} |")
            lines.append("")
        return "\n".join(lines)
