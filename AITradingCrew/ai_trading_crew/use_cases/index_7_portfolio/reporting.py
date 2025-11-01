from pathlib import Path
from typing import Dict

import pandas as pd


class Index7PortfolioReporter:
    def __init__(self, report_dir: Path):
        self.output_dir = report_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, analysis_payload: Dict) -> Dict:
        portfolio = analysis_payload["portfolio"]
        portfolio_value = analysis_payload["portfolio_value"]
        current_ltv = analysis_payload["current_ltv"]
        loan_amount = analysis_payload["loan_amount"]
        ltv_limit = analysis_payload["ltv_limit"]
        warning_ratio = analysis_payload["warning_ratio"]
        liquidation_ratio = analysis_payload["liquidation_ratio"]

        portfolio_path = self.output_dir / "optimized_portfolio.parquet"
        portfolio.to_parquet(portfolio_path, index=False)

        report_lines = []
        report_lines.append("# Index 7-Portfolio Optimization Report\n")
        report_lines.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("## Portfolio Allocation\n")
        report_lines.append("| Ticker | Name | Category | Weight |")
        report_lines.append("|--------|------|----------|--------|")

        for _, row in portfolio.iterrows():
            report_lines.append(
                f"| {row['ticker']} | {row['name']} | {row['category']} | {row['weight']*100:.2f}% |"
            )

        report_lines.append(f"\n## Risk Metrics\n")
        report_lines.append(f"- **Portfolio Value:** ¥{portfolio_value:,.0f}")
        report_lines.append(f"- **Loan Amount:** ¥{loan_amount:,.0f}")
        report_lines.append(f"- **Current LTV:** {current_ltv*100:.2f}%")
        report_lines.append(f"- **LTV Limit:** {ltv_limit*100:.0f}%")
        report_lines.append(f"- **Warning Ratio:** {warning_ratio*100:.0f}%")
        report_lines.append(f"- **Liquidation Ratio:** {liquidation_ratio*100:.0f}%")

        if current_ltv >= liquidation_ratio:
            report_lines.append(f"\n⚠️ **CRITICAL:** LTV exceeds liquidation threshold!")
        elif current_ltv >= warning_ratio:
            report_lines.append(f"\n⚠️ **WARNING:** LTV exceeds warning threshold")
        else:
            report_lines.append(f"\n✅ **HEALTHY:** LTV within safe limits")

        report_content = "\n".join(report_lines)
        report_path = self.output_dir / "index_7_portfolio_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        return {
            "portfolio_path": str(portfolio_path),
            "report_path": str(report_path),
        }
