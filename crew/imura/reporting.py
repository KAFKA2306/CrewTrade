from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt


class ImuraFundReporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, str]:
        metrics = analysis_payload["metrics"]
        period = analysis_payload["period"]

        report_md = f"# Imura Fund Analysis Report\n\n**Period:** {period['start'].date()} to {period['end'].date()} ({period['days']} days)\n\n"
        report_md += "| Asset | Return | CAGR | Volatility | Sharpe | MaxDD |\n|---|---|---|---|---|---|\n"
        for asset, m in metrics.items():
            report_md += f"| {asset} | {m['Total Return']:.2%} | {m['CAGR']:.2%} | {m['Volatility']:.2%} | {m['Sharpe']:.2f} | {m['MaxDD']:.2%} |\n"

        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [3, 1]}
        )

        for col in analysis_payload["normalized_data"].columns:
            is_fund = "BK311251" in col or "Fundnote" in col
            ax1.plot(
                analysis_payload["normalized_data"].index,
                analysis_payload["normalized_data"][col],
                label=col,
                linewidth=3.0 if is_fund else 1.5,
                alpha=1.0 if is_fund else 0.7,
            )
        ax1.set_title("Performance Comparison (Base=100)")
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.6)

        for col in analysis_payload["drawdown_data"].columns:
            is_fund = "BK311251" in col or "Fundnote" in col
            ax2.plot(
                analysis_payload["drawdown_data"].index,
                analysis_payload["drawdown_data"][col],
                label=col,
                linewidth=2.0 if is_fund else 1.0,
                alpha=1.0 if is_fund else 0.5,
            )
        ax2.set_title("Drawdown")
        ax2.grid(True, linestyle="--", alpha=0.6)

        plt.tight_layout()
        plot_path = self.report_dir / "fund_comparison_quant.png"
        plt.savefig(plot_path)
        plt.close(fig)

        report_md += f"\n![Performance Chart]({plot_path.name})\n"
        report_file = self.report_dir / "report.md"
        with open(report_file, "w") as f:
            f.write(report_md)

        return {
            "report_content": report_md,
            "report_file": str(report_file),
            "plot_file": str(plot_path),
        }
