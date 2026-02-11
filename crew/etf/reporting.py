from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import pandas as pd
from crew.etf.config import (
    IndexETFComparisonConfig,
)
class IndexETFComparisonReporter:
    def __init__(
        self, config: IndexETFComparisonConfig, processed_dir: Path, report_dir: Path
    ) -> None:
        self.config = config
        self.processed_dir = Path(processed_dir)
        self.report_dir = Path(report_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
    def persist(self, analysis_payload: Dict[str, Any]) -> Dict[str, Path]:
        index_results = analysis_payload["index_results"]
        stored_paths = {}
        for index_name, result in index_results.items():
            metrics = result["metrics"]
            if metrics.empty:
                continue
            index_id = self._sanitize_filename(index_name)
            metrics_path = self.processed_dir / f"index_{index_id}_metrics.parquet"
            metrics.to_parquet(metrics_path, index=False)
            stored_paths[f"{index_id}_metrics"] = metrics_path
            report_path = self.report_dir / f"index_{index_id}_report.md"
            forecasts = result.get("forecasts", {})
            report_path.write_text(self._build_report(index_name, metrics, forecasts))
            stored_paths[f"{index_id}_report"] = report_path
        summary_path = self.report_dir / "index_etf_comparison_summary.md"
        summary_path.write_text(self._build_summary(index_results))
        stored_paths["summary"] = summary_path
        return stored_paths
    def _sanitize_filename(self, name: str) -> str:
        sanitized = (
            name.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
        )
        sanitized = sanitized.replace("・", "_").replace("®", "").replace("　", "_")
        return sanitized
    def _build_report(
        self, index_name: str, metrics: pd.DataFrame, forecasts: Dict[str, Any] = None
    ) -> str:
        lines = []
        lines.append(f"
        lines.append("")
        lines.append("
        lines.append(f"- 該当ETF数: {len(metrics)}")
        lines.append(
            f"- データポイント範囲: {metrics['data_points'].min():.0f} - {metrics['data_points'].max():.0f}日"
        )
        lines.append("")
        lines.append("
        lines.append(
            "| ランク | ティッカー | 名称 | 運用会社 | 経費率 | 年率リターン | 年率ボラティリティ | シャープ比 | 平均出来高 |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for rank, (_, row) in enumerate(metrics.iterrows(), 1):
            expense = row.get("expense_ratio")
            expense_display = (
                f"{expense * 100:.2f}%"
                if expense is not None and pd.notna(expense)
                else "N/A"
            )
            avg_volume = row.get("avg_volume", 0)
            volume_display = f"{avg_volume:,.0f}" if avg_volume > 0 else "N/A"
            lines.append(
                f"| {rank} | {row['ticker']} | {row['name'][:40]} | {row['provider'][:20]} | "
                f"{expense_display} | {row['annual_return'] * 100:.2f}% | "
                f"{row['annual_volatility'] * 100:.2f}% | {row['sharpe_ratio']:.3f} | {volume_display} |"
            )
        lines.append("")
        if not metrics.empty and "expense_ratio" in metrics.columns:
            lines.append("
            expense_sorted = metrics.dropna(subset=["expense_ratio"]).sort_values(
                "expense_ratio"
            )
            if not expense_sorted.empty:
                lines.append("| ランク | ティッカー | 名称 | 経費率 |")
                lines.append("| --- | --- | --- | --- |")
                for rank, (_, row) in enumerate(expense_sorted.head(10).iterrows(), 1):
                    lines.append(
                        f"| {rank} | {row['ticker']} | {row['name'][:40]} | {row['expense_ratio'] * 100:.2f}% |"
                    )
                lines.append("")
        lines.append("
        lines.append(
            f"- 平均年率リターン: {metrics['annual_return'].mean() * 100:.2f}%"
        )
        lines.append(
            f"- 平均年率ボラティリティ: {metrics['annual_volatility'].mean() * 100:.2f}%"
        )
        lines.append(f"- 平均シャープ比: {metrics['sharpe_ratio'].mean():.3f}")
        if not metrics["expense_ratio"].isna().all():
            lines.append(f"- 平均経費率: {metrics['expense_ratio'].mean() * 100:.2f}%")
        lines.append("")
        if forecasts:
            lines.append("
            for ticker, forecast_data in forecasts.items():
                if isinstance(forecast_data, dict) and "error" in forecast_data:
                    lines.append(f"
                    lines.append(f"Error: {forecast_data['error']}")
                    continue
                if not forecast_data:
                    continue
                last_forecast = forecast_data[-1]
                lines.append(f"
                lines.append(f"- Prediction End: {last_forecast.get('date', 'N/A')}")
                lines.append(
                    f"- Predicted Close: {last_forecast.get('close', 'N/A'):.2f}"
                )
                lines.append("")
        return "\n".join(lines)
    def _build_summary(self, index_results: Dict[str, Dict[str, Any]]) -> str:
        lines = []
        lines.append("
        lines.append("")
        lines.append("
        lines.append("| 指数名 | ETF数 |")
        lines.append("| --- | --- |")
        for index_name, result in index_results.items():
            metrics = result["metrics"]
            lines.append(f"| {index_name} | {len(metrics)} |")
        lines.append("")
        lines.append("
        lines.append("")
        for index_name in index_results.keys():
            index_id = self._sanitize_filename(index_name)
            lines.append(f"- [{index_name}](index_{index_id}_report.md)")
        lines.append("")
        return "\n".join(lines)
