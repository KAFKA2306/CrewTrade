from pathlib import Path
from typing import Any, Dict, List

from .models import FinancialParams, ProjectedQuarter


class OracleEarningsReporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        projections = analysis_payload["projections"]
        base: FinancialParams = analysis_payload["base_quarter"]

        report = "# Oracle Quarterly Financial Projections\n\n"

        # 1. Facts Section
        report += "## 1. Facts (Baseline Data)\n"
        report += "These figures are based on FY2026 Q2 actuals provided.\n\n"
        report += f"- **Period:** {base.period}\n"
        report += f"- **Revenue:** ${base.revenue_B}B\n"
        report += f"- **Operating Income:** ${base.operating_income_B}B (Margin: {base.operating_income_B / base.revenue_B:.1%})\n"
        report += f"- **CAPEX (TTM):** ${base.capex_last_4q_B}B (Intensity: ~{base.current_capex_intensity:.1%})\n"
        report += f"- **Cloud Growth:** {base.cloud_revenue_growth_yoy_pct}% YoY\n"
        report += f"- **RPO:** ${base.rpo_B}B\n\n"

        report += "## 2. Scenarios\n\n"

        for scenario_name, quarters in projections.items():
            quarters: List[ProjectedQuarter] = quarters
            report += f"### Scenario: {scenario_name.capitalize()}\n\n"

            report += "**Projections:**\n"
            report += "| Period | Revenue ($B) | Op Ex ($B) | Op Inc ($B) | Margin | CAPEX ($B) | RPO ($B) |\n"
            report += "|---|---|---|---|---|---|---|\n"

            for q in quarters:
                op_ex = q.revenue_B - q.operating_income_B
                margin = q.operating_income_B / q.revenue_B
                report += f"| {q.period_label} | {q.revenue_B:.2f} | {op_ex:.2f} | {q.operating_income_B:.2f} | {margin:.1%} | {q.capex_B:.2f} | {q.rpo_B:.1f} |\n"

            report += "\n"

        output_path = self.report_dir / "oracle_earnings_report.md"
        with open(output_path, "w") as f:
            f.write(report)

        return {"report_content": report, "report_file": str(output_path)}
