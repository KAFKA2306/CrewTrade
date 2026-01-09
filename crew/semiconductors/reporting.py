"""Reporting module for semiconductor stock analysis."""

from pathlib import Path
from typing import Any, Dict, List

from .analysis import StockMetrics


class SemiconductorsReporter:
    """Generate markdown reports for semiconductor stock analysis."""

    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the analysis report."""
        stock_metrics: List[StockMetrics] = analysis_payload.get("stock_metrics", [])
        rankings = analysis_payload.get("rankings", {})
        sector_averages = analysis_payload.get("sector_averages", {})
        benchmark = analysis_payload.get("benchmark_symbol", "SOXX")
        analysis_date = analysis_payload.get("analysis_date", "")

        report = self._build_report(
            stock_metrics, rankings, sector_averages, benchmark, analysis_date
        )

        output_path = self.report_dir / "semiconductor_analysis_report.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        return {"report_content": report, "report_file": str(output_path)}

    def _build_report(
        self,
        stock_metrics: List[StockMetrics],
        rankings: Dict[str, List[StockMetrics]],
        sector_averages: Dict[str, float],
        benchmark: str,
        analysis_date: str,
    ) -> str:
        """Build the markdown report content."""
        lines = []
        lines.append("# Top 10 Semiconductor Stocks Analysis Report")
        lines.append(f"\n**Analysis Date:** {analysis_date}")
        lines.append(f"**Benchmark:** {benchmark} (iShares Semiconductor ETF)")
        lines.append("")

        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append("This report analyzes the top 10 semiconductor stocks driving the AI and advanced computing revolution. ")
        lines.append("Key themes include: AI GPU dominance, advanced node manufacturing, HBM memory demand, and semiconductor equipment growth.")
        lines.append("")

        # Sector Averages
        lines.append("### Sector Performance Snapshot")
        lines.append("")
        lines.append(f"- **Average 12M Return:** {sector_averages.get('return_12m', 0):.1%}")
        lines.append(f"- **Average Volatility:** {sector_averages.get('volatility', 0):.1%}")
        lines.append(f"- **Average Sharpe Ratio:** {sector_averages.get('sharpe_ratio', 0):.2f}")
        lines.append("")

        # Performance Summary Table
        lines.append("## Performance Summary")
        lines.append("")
        lines.append("| Rank | Symbol | Company | Price | YTD | 3M | 6M | 12M | Vol | Sharpe | Beta |")
        lines.append("|------|--------|---------|-------|-----|----|----|-----|-----|--------|------|")

        by_return = rankings.get("by_return", stock_metrics)
        for i, m in enumerate(by_return, 1):
            lines.append(
                f"| {i} | **{m.symbol}** | {m.name[:20]} | ${m.current_price:.2f} | "
                f"{m.ytd_return:+.1%} | {m.return_3m:+.1%} | {m.return_6m:+.1%} | "
                f"{m.return_12m:+.1%} | {m.volatility:.1%} | {m.sharpe_ratio:.2f} | {m.beta_vs_benchmark:.2f} |"
            )
        lines.append("")

        # Rankings Section
        lines.append("## Rankings")
        lines.append("")

        lines.append("### By Risk-Adjusted Return (Sharpe Ratio)")
        lines.append("")
        by_sharpe = rankings.get("by_sharpe", [])
        for i, m in enumerate(by_sharpe[:5], 1):
            lines.append(f"{i}. **{m.symbol}** - Sharpe: {m.sharpe_ratio:.2f}")
        lines.append("")

        lines.append("### By Lowest Volatility")
        lines.append("")
        by_vol = rankings.get("by_volatility", [])
        for i, m in enumerate(by_vol[:5], 1):
            lines.append(f"{i}. **{m.symbol}** - Volatility: {m.volatility:.1%}")
        lines.append("")

        # Individual Stock Analysis
        lines.append("## Individual Stock Analysis")
        lines.append("")

        for m in by_return:
            lines.append(f"### {m.symbol} - {m.name}")
            lines.append("")

            if m.profile:
                lines.append(f"**Focus:** {m.profile.focus_area}")
                lines.append(f"**AI Exposure:** {m.profile.ai_exposure.upper()}")
                lines.append(f"**Analyst Rating:** {m.profile.analyst_rating}")
                lines.append("")

                lines.append("**Key Products:**")
                for product in m.profile.key_products:
                    lines.append(f"- {product}")
                lines.append("")

                lines.append("**Growth Drivers:**")
                for driver in m.profile.growth_drivers:
                    lines.append(f"- {driver}")
                lines.append("")

                lines.append("**Key Metrics (Fundamental):**")
                for key, val in m.profile.key_metrics.items():
                    lines.append(f"- {key}: {val}")
                lines.append("")

            lines.append("**Technical Metrics:**")
            lines.append(f"- Current Price: ${m.current_price:.2f}")
            lines.append(f"- 12M Return: {m.return_12m:+.1%}")
            lines.append(f"- Volatility: {m.volatility:.1%}")
            lines.append(f"- Max Drawdown: {m.max_drawdown:.1%}")
            lines.append(f"- Beta vs {benchmark}: {m.beta_vs_benchmark:.2f}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # Methodology
        lines.append("## Methodology")
        lines.append("")
        lines.append("- **Data Source:** Yahoo Finance via yfinance")
        lines.append("- **Period:** 1 year historical data")
        lines.append("- **Volatility:** Annualized standard deviation of daily returns")
        lines.append("- **Sharpe Ratio:** (12M Return - Risk-Free Rate) / Volatility")
        lines.append("- **Risk-Free Rate:** 4.5% (approximate T-bill rate)")
        lines.append("- **Beta:** Covariance with SOXX / Variance of SOXX")
        lines.append("")

        # Disclaimer
        lines.append("## Disclaimer")
        lines.append("")
        lines.append("This report is for informational purposes only and does not constitute investment advice. ")
        lines.append("Past performance is not indicative of future results. ")
        lines.append("Investors should conduct their own due diligence before making investment decisions.")
        lines.append("")

        return "\n".join(lines)
