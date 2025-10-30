from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def build_insight_markdown(analysis_payload: Dict[str, object]) -> str:
    summary: Dict[str, object] = analysis_payload["summary"]
    scenarios: List[Dict[str, float]] = analysis_payload["scenarios"]
    warning_events: pd.DataFrame = analysis_payload["warning_events"]
    liquidation_events: pd.DataFrame = analysis_payload["liquidation_events"]

    lines: List[str] = []
    lines.append("# Securities Collateral Loan Insight")
    lines.append("")

    mode = analysis_payload.get("mode", "manual")
    if mode == "optimization":
        lines.append("## Optimization Summary")
        opt_metrics = analysis_payload.get("optimization_metrics", {})
        etf_master = analysis_payload.get("etf_master")
        ranked_etfs = analysis_payload.get("ranked_etfs")

        if etf_master is not None:
            lines.append(f"- Total ETFs evaluated: {len(etf_master)}")

        if ranked_etfs is not None and len(ranked_etfs) > 0:
            lines.append(f"- ETFs with sufficient data: {len(ranked_etfs)}")

        optimized_portfolio = analysis_payload.get("optimized_portfolio")
        if optimized_portfolio is not None:
            lines.append(f"- Selected ETFs: {len(optimized_portfolio)}")

        lines.append(f"- Portfolio annual return: {opt_metrics.get('annual_return', 0) * 100:.2f}%")
        lines.append(f"- Portfolio annual volatility: {opt_metrics.get('annual_volatility', 0) * 100:.2f}%")
        lines.append(f"- Portfolio Sharpe ratio: {opt_metrics.get('sharpe_ratio', 0):.3f}")
        lines.append("")

    lines.append("## Current Profile")
    lines.append(f"- Loan amount: ¥{summary['loan_amount']:,}")
    lines.append(f"- Current collateral value: ¥{summary['current_collateral_value']:.0f}")
    lines.append(f"- Current loan ratio: {summary['current_loan_ratio']:.3f}")
    lines.append(f"- Buffer to 70%: {summary['buffer_to_warning_pct'] * 100:.2f}% drop" if summary["buffer_to_warning_pct"] is not None else "- Buffer to 70%: N/A")
    lines.append(f"- Buffer to 85%: {summary['buffer_to_liquidation_pct'] * 100:.2f}% drop" if summary["buffer_to_liquidation_pct"] is not None else "- Buffer to 85%: N/A")
    lines.append(f"- Max drawdown (history): {summary['max_drawdown'] * 100:.2f}%")
    lines.append("")

    lines.append("## Stress Scenarios")
    scenario_table = pd.DataFrame(scenarios)
    if not scenario_table.empty:
        scenario_table["post_value"] = scenario_table["post_value"].map(lambda x: f"¥{x:,.0f}")
        scenario_table["loan_ratio"] = scenario_table["loan_ratio"].map(lambda x: f"{x:.3f}")
        scenario_table["breach_warning"] = scenario_table["breach_warning"].map(lambda x: "Yes" if x else "No")
        scenario_table["breach_liquidation"] = scenario_table["breach_liquidation"].map(lambda x: "Yes" if x else "No")
    lines.append(
        _format_table(
            scenario_table,
            ["label", "post_value", "loan_ratio", "breach_warning", "breach_liquidation"],
            ["Scenario", "Post Value", "Loan Ratio", "≥70%", "≥85%"],
        )
    )
    lines.append("")

    lines.append("## Historical Breach Counts")
    lines.append(f"- Margin call events: {len(warning_events)}")
    lines.append(f"- Forced liquidation events: {len(liquidation_events)}")
    lines.append("")

    lines.append("## Interest Projection (Simple)")
    interest_rows = []
    for entry in summary["interest_projection"]:
        interest_rows.append({"Days": entry["days"], "Interest": entry["interest"]})
    interest_df = pd.DataFrame(interest_rows)
    if not interest_df.empty:
        interest_df["Interest"] = interest_df["Interest"].map(lambda x: f"{x:,.2f}")
    lines.append(_format_table(interest_df, ["Days", "Interest"], ["Days", "Interest (¥)"]))
    lines.append("")

    return "\n".join(lines)


def _format_table(df: pd.DataFrame, columns: List[str], headers: List[str]) -> str:
    if df.empty:
        return "No data available."
    table_lines: List[str] = []
    table_lines.append("| " + " | ".join(headers) + " |")
    table_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df[columns].iterrows():
        formatted: List[str] = []
        for col in columns:
            value = row[col]
            if isinstance(value, float):
                formatted.append(f"{value:.4f}")
            elif isinstance(value, (int, np.integer)):
                formatted.append(str(int(value)))
            else:
                formatted.append(str(value))
        table_lines.append("| " + " | ".join(formatted) + " |")
    return "\n".join(table_lines)
