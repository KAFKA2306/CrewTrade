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
        soros = analysis_payload.get("soros_metrics", [])
        druckenmiller = analysis_payload.get("druckenmiller_metrics", [])
        date = analysis_payload.get("analysis_date", "Unknown Date")

        md_lines = [
            f"# Legendary Investors Portfolio Tracking - {date}",
            "",
            "## 1. George Soros (Soros Fund Management)",
            "Top holdings based on recent 13F filings.",
            "",
            self._make_detailed_section(soros),
            "",
            "## 2. Stanley Druckenmiller (Duquesne Family Office)",
            "Top holdings based on recent 13F filings.",
            "",
            self._make_detailed_section(druckenmiller),
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
                f"### {m.symbol}",
                f"**Price**: ${m.current_price:.2f} | **YTD**: {m.ytd_return:.1%} | **12m**: {m.return_12m:.1%} | **Sharpe**: {m.sharpe_ratio:.2f}",
                "",
                "#### Reason Why",
                m.reason_why if m.reason_why else "N/A",
                "",
                "#### Evaluation",
                m.evaluation if m.evaluation else "N/A",
                "",
                "#### Rumor",
                m.rumor if m.rumor else "N/A",
                "",
                "#### Earnings",
                m.earnings if m.earnings else "N/A",
                "",
                "#### Alpha",
                m.alpha if m.alpha else "N/A",
                "",
                "#### Fundamental Context",
                m.fundamentals if m.fundamentals else "No fundamental data.",
                "",
                "#### Recent News",
                m.news_summary if m.news_summary else "No recent news.",
                "",
                "---"
            ]
            sections.append("\n".join(section))
        
        return "\n".join(sections)
