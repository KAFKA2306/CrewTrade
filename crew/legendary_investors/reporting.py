"""Reporting module for legendary investors use case."""
from pathlib import Path
from typing import Any, Dict
from .analysis import HoldingMetrics
class LegendaryInvestorsReporter:
    """Generates markdown reports for legendary investors analysis."""
    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        druckenmiller = analysis_payload.get("druckenmiller_metrics", [])
        date = analysis_payload.get("analysis_date", "Unknown Date")
        forecasts = analysis_payload.get("forecasts", {})
        md_lines = [
            f"
            "",
            "
            "Top holdings based on recent 13F filings.",
            "",
            self._make_detailed_section(soros),
            "",
            "
            "Top holdings based on recent 13F filings.",
            "",
            self._make_detailed_section(druckenmiller),
            "",
            self._make_forecast_section(forecasts),
            "",
        ]
        report_content = "\n".join(md_lines)
        report_file = self.report_dir / "report.md"
        report_file.write_text(report_content, encoding="utf-8")
        return {"report_file": str(report_file)}
    def _make_detailed_section(self, metrics_list: list[HoldingMetrics]) -> str:
        if not metrics_list:
            return "No data available."
        sections = []
        for m in metrics_list:
            section = [
                f"
                f"**Price**: ${m.current_price:.2f} | **YTD**: {m.ytd_return:.1%} | **12m**: {m.return_12m:.1%} | **Sharpe**: {m.sharpe_ratio:.2f}",
                "",
                "
                m.reason_why if m.reason_why else "N/A",
                "",
                "
                m.evaluation if m.evaluation else "N/A",
                "",
                "
                m.rumor if m.rumor else "N/A",
                "",
                "
                m.earnings if m.earnings else "N/A",
                "",
                "
                m.alpha if m.alpha else "N/A",
                "",
                "
                m.fundamentals if m.fundamentals else "No fundamental data.",
                "",
                "
                m.news_summary if m.news_summary else "No recent news.",
                "",
                "---",
            ]
            sections.append("\n".join(section))
        return "\n".join(sections)
    def _make_forecast_section(self, forecasts: Dict[str, Any]) -> str:
        if not forecasts:
            return ""
        lines = ["
        for ticker, data in forecasts.items():
            if isinstance(data, dict) and "error" in data:
                lines.append(f"
                continue
            if not data:
                continue
            last = data[-1]
            lines.append(f"
            lines.append(f"- Prediction End: {last.get('date', 'N/A')}")
            lines.append(f"- Predicted Close: {last.get('close', 'N/A'):.2f}")
            lines.append("")
        return "\n".join(lines)
