from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

from ai_trading_crew.use_cases.securities_collateral_loan.config import SecuritiesCollateralLoanConfig
from ai_trading_crew.use_cases.securities_collateral_loan.insights import build_insight_markdown


class SecuritiesCollateralLoanReporter:
    def __init__(self, config: SecuritiesCollateralLoanConfig, processed_dir: Path, report_dir: Path) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, analysis_payload: Dict[str, object]) -> Dict[str, Path]:
        prices: pd.DataFrame = analysis_payload["prices"]
        positions: pd.DataFrame = analysis_payload["positions"]
        portfolio_value: pd.Series = analysis_payload["portfolio_value"]
        loan_ratio_series: pd.Series = analysis_payload["loan_ratio_series"]
        warning_events: pd.DataFrame = analysis_payload["warning_events"]
        liquidation_events: pd.DataFrame = analysis_payload["liquidation_events"]
        scenarios: List[Dict[str, float]] = analysis_payload["scenarios"]
        summary: Dict[str, object] = analysis_payload["summary"]
        asset_breakdown: pd.DataFrame = analysis_payload["asset_breakdown"]

        stored_paths: Dict[str, Path] = {}

        prices_path = self.processed_dir / "prices.parquet"
        prices.to_parquet(prices_path)
        stored_paths["prices"] = prices_path

        positions_path = self.processed_dir / "positions.parquet"
        positions.to_parquet(positions_path)
        stored_paths["positions"] = positions_path

        portfolio_path = self.processed_dir / "portfolio_value.parquet"
        portfolio_value.to_frame(name="portfolio_value").to_parquet(portfolio_path)
        stored_paths["portfolio_value"] = portfolio_path

        ratio_path = self.processed_dir / "loan_ratio.parquet"
        loan_ratio_series.to_frame(name="loan_ratio").to_parquet(ratio_path)
        stored_paths["loan_ratio"] = ratio_path

        warning_path = self.processed_dir / "warning_events.parquet"
        warning_events.to_parquet(warning_path)
        stored_paths["warning_events"] = warning_path

        liquidation_path = self.processed_dir / "liquidation_events.parquet"
        liquidation_events.to_parquet(liquidation_path)
        stored_paths["liquidation_events"] = liquidation_path

        breakdown_path = self.processed_dir / "asset_breakdown.parquet"
        asset_breakdown.to_parquet(breakdown_path)
        stored_paths["asset_breakdown"] = breakdown_path

        scenario_path = self.processed_dir / "scenarios.parquet"
        pd.DataFrame(scenarios).to_parquet(scenario_path)
        stored_paths["scenarios"] = scenario_path

        report_path = self.report_dir / "securities_collateral_loan_report.md"
        report_path.write_text(self._build_report(summary, asset_breakdown, scenarios, warning_events, liquidation_events))
        stored_paths["report"] = report_path

        insight_path = self.report_dir / "securities_collateral_loan_insights.md"
        insight_path.write_text(build_insight_markdown(analysis_payload))
        stored_paths["insights"] = insight_path

        return stored_paths

    def _build_report(
        self,
        summary: Dict[str, object],
        asset_breakdown: pd.DataFrame,
        scenarios: List[Dict[str, float]],
        warning_events: pd.DataFrame,
        liquidation_events: pd.DataFrame,
    ) -> str:
        lines: List[str] = []
        lines.append("# Securities Collateral Loan Risk Report")
        lines.append("")
        lines.append("## Overview")
        lines.append(f"- Loan amount: ¥{summary['loan_amount']:,}")
        lines.append(f"- Annual interest rate: {self.config.annual_interest_rate * 100:.3f}%")
        lines.append(f"- Collateral period evaluated: {self.config.period}")
        lines.append(f"- Current collateral market value: ¥{summary['current_collateral_value']:.0f}")
        lines.append(f"- Current loan ratio: {summary['current_loan_ratio']:.3f}")
        lines.append(f"- Max allowable borrowing ratio (Rakuten Securities): {self.config.ltv_limit:.2f}")
        lines.append(f"- Margin call (補充) threshold: {self.config.warning_ratio:.2f}")
        lines.append(f"- Forced liquidation threshold: {self.config.liquidation_ratio:.2f}")
        if summary["buffer_to_warning_pct"] is not None:
            lines.append(f"- Buffer to margin call: {summary['buffer_to_warning_pct'] * 100:.2f}% drop from current value")
        if summary["buffer_to_liquidation_pct"] is not None:
            lines.append(f"- Buffer to forced liquidation: {summary['buffer_to_liquidation_pct'] * 100:.2f}% drop from current value")
        lines.append(f"- Historical max drawdown (portfolio): {summary['max_drawdown'] * 100:.2f}%")
        lines.append("")

        lines.append("## Collateral Breakdown")
        lines.append("| Ticker | Description | Quantity | Price | Market Value |")
        lines.append("| --- | --- | --- | --- | --- |")
        for _, row in asset_breakdown.iterrows():
            lines.append(
                f"| {row['ticker']} | {row['description']} | {row['quantity']:.0f} | "
                f"¥{row['latest_price']:.2f} | ¥{row['market_value']:.0f} |"
            )
        lines.append("")

        lines.append("## Interest Projection")
        lines.append("| Days | Interest (¥) |")
        lines.append("| --- | --- |")
        for horizon in summary["interest_projection"]:
            lines.append(f"| {horizon['days']} | ¥{horizon['interest']:.2f} |")
        lines.append("")

        lines.append("## Stress Scenarios")
        lines.append("| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |")
        lines.append("| --- | --- | --- | --- | --- |")
        for scenario in scenarios:
            warning_flag = "Yes" if scenario["breach_warning"] else "No"
            liquidation_flag = "Yes" if scenario["breach_liquidation"] else "No"
            lines.append(
                f"| {scenario['label']} | ¥{scenario['post_value']:.0f} | {scenario['loan_ratio']:.3f} | "
                f"{warning_flag} | {liquidation_flag} |"
            )
        lines.append("")

        lines.append("## Historical Breaches")
        if warning_events.empty and liquidation_events.empty:
            lines.append("No historical instances exceeded Rakuten Securities thresholds within the observation window.")
        else:
            if not warning_events.empty:
                lines.append("### Margin Call Alerts (>= 70%)")
                lines.append("| Date | Loan Ratio |")
                lines.append("| --- | --- |")
                for _, row in warning_events.iterrows():
                    lines.append(f"| {row['date'].date()} | {row['loan_ratio']:.3f} |")
                lines.append("")
            if not liquidation_events.empty:
                lines.append("### Forced Liquidation Events (>= 85%)")
                lines.append("| Date | Loan Ratio |")
                lines.append("| --- | --- |")
                for _, row in liquidation_events.iterrows():
                    lines.append(f"| {row['date'].date()} | {row['loan_ratio']:.3f} |")
                lines.append("")

        lines.append("## Notes")
        lines.append("- Loan ratio is calculated as outstanding balance divided by collateral market value.")
        lines.append("- Rakuten Securities/Rakuten Bank requires top-up within 2 business days once the ratio reaches 70%, and may liquidate collateral immediately at 85%+.")
        lines.append("- Borrowing limit is capped at approximately 60% of collateral value; ensure new acquisitions keep the loan ratio below 0.60 after execution.")
        lines.append("- Interest is estimated on a simple basis and excludes taxes or transaction costs.")
        lines.append("")

        return "\n".join(lines)
