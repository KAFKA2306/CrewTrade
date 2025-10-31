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

        forward_test = analysis_payload.get("forward_test")
        if isinstance(forward_test, dict):
            series = forward_test.get("series")
            if isinstance(series, pd.DataFrame) and not series.empty:
                forward_path = self.processed_dir / "forward_performance.parquet"
                series.to_parquet(forward_path)
                stored_paths["forward_performance"] = forward_path

        mode = analysis_payload.get("mode", "manual")
        if mode == "optimization":
            risk_metrics = analysis_payload.get("risk_metrics")
            if isinstance(risk_metrics, pd.DataFrame):
                risk_path = self.processed_dir / "etf_risk_metrics.parquet"
                risk_metrics.to_parquet(risk_path)
                stored_paths["etf_risk_metrics"] = risk_path

            candidate_universe = analysis_payload.get("candidate_universe")
            if isinstance(candidate_universe, pd.DataFrame):
                candidate_path = self.processed_dir / "candidate_universe.parquet"
                candidate_universe.to_parquet(candidate_path)
                stored_paths["candidate_universe"] = candidate_path

            profile_results = analysis_payload.get("optimization_profile_results", {})
            primary_profile = analysis_payload.get("primary_profile")
            profile_paths: Dict[str, Path] = {}
            for name, result in profile_results.items():
                portfolio = result.get("portfolio") if isinstance(result, dict) else None
                if isinstance(portfolio, pd.DataFrame):
                    path = self.processed_dir / f"optimized_portfolio_{name}.parquet"
                    portfolio.to_parquet(path)
                    stored_paths[f"optimized_portfolio_{name}"] = path
                    profile_paths[name] = path

            if primary_profile and primary_profile in profile_paths:
                stored_paths["optimized_portfolio"] = profile_paths[primary_profile]
            else:
                optimized_portfolio = analysis_payload.get("optimized_portfolio")
                if isinstance(optimized_portfolio, pd.DataFrame):
                    opt_path = self.processed_dir / "optimized_portfolio.parquet"
                    optimized_portfolio.to_parquet(opt_path)
                    stored_paths["optimized_portfolio"] = opt_path

        report_path = self.report_dir / "securities_collateral_loan_report.md"
        report_path.write_text(
            self._build_report(
                summary,
                asset_breakdown,
                scenarios,
                warning_events,
                liquidation_events,
                analysis_payload,
            )
        )
        stored_paths["report"] = report_path

        insight_path = self.report_dir / "securities_collateral_loan_insights.md"
        insight_path.write_text(build_insight_markdown(analysis_payload))
        stored_paths["insights"] = insight_path

        return stored_paths

    def _format_backtest_vs_forward_comparison(
        self,
        backtest_metrics: Dict[str, float],
        forward_metrics: Dict[str, float],
        constraints: Dict[str, float],
    ) -> List[str]:
        lines = []
        lines.append("")
        lines.append("### Backtest vs Forward Comparison")
        lines.append("")
        lines.append("| Metric | Backtest Period | Forward Period | Difference | Status |")
        lines.append("| --- | --- | --- | --- | --- |")

        bt_return = backtest_metrics.get("annual_return", 0)
        fw_return = forward_metrics.get("annualized_return", 0)
        if fw_return != 0:
            diff_return = fw_return - bt_return
            lines.append(
                f"| Annual Return | {bt_return * 100:.2f}% | {fw_return * 100:.2f}% | "
                f"{diff_return * 100:+.2f}% | {'⚠️' if abs(diff_return) > 0.05 else '✓'} |"
            )

        bt_vol = backtest_metrics.get("annual_volatility", 0)
        fw_vol = forward_metrics.get("annualized_volatility", 0)
        max_vol = constraints.get("max_volatility", 0.15)
        if fw_vol != 0:
            diff_vol = fw_vol - bt_vol
            status = "⚠️ BREACH" if fw_vol > max_vol else "✓"
            lines.append(
                f"| Annual Volatility | {bt_vol * 100:.2f}% | {fw_vol * 100:.2f}% | "
                f"{diff_vol * 100:+.2f}% | {status} |"
            )

        bt_sharpe = backtest_metrics.get("sharpe_ratio", 0)
        fw_sharpe = forward_metrics.get("sharpe_ratio", 0)
        if fw_sharpe != 0:
            diff_sharpe = fw_sharpe - bt_sharpe
            lines.append(
                f"| Sharpe Ratio | {bt_sharpe:.3f} | {fw_sharpe:.3f} | "
                f"{diff_sharpe:+.3f} | {'⚠️' if diff_sharpe < -0.5 else '✓'} |"
            )

        bt_dd = backtest_metrics.get("max_drawdown", 0)
        fw_dd = forward_metrics.get("max_drawdown", 0)
        if fw_dd != 0:
            diff_dd = fw_dd - bt_dd
            lines.append(
                f"| Max Drawdown | {bt_dd * 100:.2f}% | {fw_dd * 100:.2f}% | "
                f"{diff_dd * 100:+.2f}% | {'⚠️' if abs(diff_dd) > 0.10 else '✓'} |"
            )

        return lines

    def _build_report(
        self,
        summary: Dict[str, object],
        asset_breakdown: pd.DataFrame,
        scenarios: List[Dict[str, float]],
        warning_events: pd.DataFrame,
        liquidation_events: pd.DataFrame,
        analysis_payload: Dict[str, object] = None,
    ) -> str:
        lines: List[str] = []
        lines.append("# Securities Collateral Loan Risk Report")
        lines.append("")

        mode = analysis_payload.get("mode", "manual") if analysis_payload else "manual"
        if mode == "optimization":
            lines.append("*Generated via automated portfolio optimization*")
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

        if mode == "optimization" and analysis_payload:
            primary_profile = analysis_payload.get("primary_profile")
            ranked_etfs = analysis_payload.get("ranked_etfs")
            candidate_universe = analysis_payload.get("candidate_universe")
            optimization_profiles = analysis_payload.get("optimization_profiles", {})
            etf_master = analysis_payload.get("etf_master")

            lines.append("## Optimization Summary")
            if isinstance(etf_master, pd.DataFrame):
                lines.append(f"- Total ETFs evaluated: {len(etf_master)}")
            if isinstance(ranked_etfs, pd.DataFrame):
                lines.append(f"- ETFs with sufficient data: {len(ranked_etfs)}")
            if isinstance(candidate_universe, pd.DataFrame):
                lines.append(
                    f"- Candidate universe after correlation filter: {len(candidate_universe)} "
                    f"(threshold {self.config.optimization.correlation_threshold:.2f})"
                )
            hedged_excluded = analysis_payload.get("hedged_excluded") or []
            if hedged_excluded:
                excluded_items = ", ".join(
                    f"{item.get('ticker')}({(item.get('name') or '')[:15]})" for item in hedged_excluded
                )
                lines.append(f"- Excluded hedged ETFs: {excluded_items}")
            constraints = self.config.optimization.constraints if self.config.optimization else {}
            max_asset_volatility = constraints.get("max_asset_volatility") if constraints else None
            volatility_excluded = analysis_payload.get("volatility_excluded") or []
            if volatility_excluded:
                excluded_items = ", ".join(
                    f"{item.get('ticker')}({(item.get('name') or '')[:15]})" for item in volatility_excluded
                )
                threshold_note = f" (> {max_asset_volatility * 100:.1f}% annualized volatility)" if max_asset_volatility is not None else ""
                lines.append(f"- Excluded high-volatility ETFs{threshold_note}: {excluded_items}")
            max_asset_drawdown = constraints.get("max_asset_drawdown") if constraints else None
            drawdown_excluded = analysis_payload.get("drawdown_excluded") or []
            if drawdown_excluded:
                excluded_items = ", ".join(
                    f"{item.get('ticker')}({(item.get('name') or '')[:15]})" for item in drawdown_excluded
                )
                threshold_note = ""
                if max_asset_drawdown is not None:
                    threshold_note = f" (drawdown worse than -{max_asset_drawdown * 100:.1f}%)"
                lines.append(f"- Excluded deep-drawdown ETFs{threshold_note}: {excluded_items}")
            if primary_profile:
                lines.append(f"- Selected profile: {primary_profile}")

            opt_metrics = analysis_payload.get("optimization_metrics") or {}
            if opt_metrics:
                metrics_parts = [
                    f"return {opt_metrics.get('annual_return', 0) * 100:.2f}%",
                    f"volatility {opt_metrics.get('annual_volatility', 0) * 100:.2f}%",
                    f"Sharpe {opt_metrics.get('sharpe_ratio', 0):.3f}",
                ]
                if opt_metrics.get("expense_ratio") is not None:
                    metrics_parts.append(f"expense {opt_metrics['expense_ratio'] * 100:.2f}%")
                lines.append(f"- Selected portfolio metrics (backtest period): {', '.join(metrics_parts)}")
                lines.append("")

            prices_df = analysis_payload.get("prices") if analysis_payload else None
            backtest_start = None
            backtest_end = None
            if isinstance(prices_df, pd.DataFrame) and not prices_df.empty:
                backtest_start = prices_df.index.min()
                backtest_end = prices_df.index.max()

            lines.append("## Part 1: BACKTEST PERIOD ANALYSIS")
            lines.append("")
            lines.append("**Purpose**: Portfolio construction and constraint validation")
            if backtest_start and backtest_end:
                duration_days = (backtest_end - backtest_start).days
                duration_years = duration_days / 365.25
                lines.append(f"**Period**: {backtest_start.date()} to {backtest_end.date()} ({duration_years:.1f} years)")
            else:
                lines.append(f"**Period**: Lookback period ({self.config.period})")
            lines.append("**Important**: These metrics are based on **historical data** used for optimization.")
            lines.append("They do NOT guarantee future performance.")
            lines.append("")

            if opt_metrics:
                lines.append("### Backtest Period Metrics")
                lines.append("| Metric | Value | Constraint | Status |")
                lines.append("| --- | --- | --- | --- |")

                ann_return = opt_metrics.get('annual_return', 0)
                lines.append(f"| Annual Return | {ann_return * 100:.2f}% | - | - |")

                ann_vol = opt_metrics.get('annual_volatility', 0)
                constraints = self.config.optimization.constraints if self.config.optimization else {}
                max_vol = constraints.get("max_volatility", 0.15)
                vol_status = "✅" if ann_vol <= max_vol else "❌"
                lines.append(f"| Annual Volatility | {ann_vol * 100:.2f}% | ≤ {max_vol * 100:.0f}% | {vol_status} |")

                sharpe = opt_metrics.get('sharpe_ratio', 0)
                lines.append(f"| Sharpe Ratio | {sharpe:.3f} | - | - |")

                expense_value = opt_metrics.get("expense_ratio")
                if expense_value is not None:
                    exp_status = "✅" if expense_value < 0.004 else "❌"
                    lines.append(f"| Weighted Expense Ratio | {expense_value * 100:.2f}% | < 0.40% | {exp_status} |")

                lines.append("")
            lines.append("")

            if optimization_profiles:
                lines.append("### Profile Metrics")
                lines.append("| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |")
                lines.append("| --- | --- | --- | --- | --- | --- |")
                for name, metrics in optimization_profiles.items():
                    if not metrics:
                        continue
                    expense_ratio = metrics.get("expense_ratio")
                    expense_display = f"{expense_ratio * 100:.2f}%" if expense_ratio is not None else "N/A"
                    lines.append(
                        f"| {name} | {metrics.get('annual_return', 0) * 100:.2f}% | "
                        f"{metrics.get('annual_volatility', 0) * 100:.2f}% | "
                        f"{metrics.get('sharpe_ratio', 0):.3f} | {expense_display} | "
                        f"{'Yes' if name == primary_profile else ''} |"
                    )
                lines.append("")

            if isinstance(ranked_etfs, pd.DataFrame) and not ranked_etfs.empty:
                lines.append("### Top 10 ETFs by Composite Score")
                lines.append("| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |")
                lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
                for i, (_, row) in enumerate(ranked_etfs.head(10).iterrows(), 1):
                    expense = row.get("expense_ratio")
                    expense_display = f"{expense * 100:.2f}%" if expense is not None and not pd.isna(expense) else "N/A"
                    lines.append(
                        f"| {i} | {row['ticker']} | {row.get('name', '')[:30]} | "
                        f"{row['annual_return'] * 100:.2f}% | {row['annual_volatility'] * 100:.2f}% | "
                        f"{row['sharpe_ratio']:.3f} | {expense_display} | {row['composite_score']:.3f} |"
                    )
                lines.append("")

        lines.append("## Part 2: PORTFOLIO CONSTRUCTION")
        lines.append("")
        lines.append("**Purpose**: Selected ETFs and portfolio composition at anchor date")
        lines.append("")
        lines.append("### Collateral Breakdown")
        asset_breakdown_sorted = asset_breakdown.sort_values("market_value", ascending=False)

        if mode == "optimization" and "category" in asset_breakdown.columns:
            category_summary = asset_breakdown.groupby("category").agg(
                market_value=("market_value", "sum"),
                count=("ticker", "count"),
            )
            category_summary["weight"] = category_summary["market_value"] / category_summary["market_value"].sum()
            category_summary = category_summary.sort_values("market_value", ascending=False)

            lines.append("### By Category")
            lines.append("| Category | ETF Count | Market Value | Weight |")
            lines.append("| --- | --- | --- | --- |")
            for cat, row in category_summary.iterrows():
                lines.append(
                    f"| {cat} | {int(row['count'])} | ¥{row['market_value']:,.0f} | {row['weight']*100:.1f}% |"
                )
            lines.append("")

            lines.append(f"### Top Holdings (out of {len(asset_breakdown)} ETFs)")

        lines.append("| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

        display_count = min(20, len(asset_breakdown_sorted))
        for _, row in asset_breakdown_sorted.head(display_count).iterrows():
            weight = row.get("weight_realized", row.get("weight"))
            weight_display = f"{weight * 100:.1f}%" if weight is not None and not pd.isna(weight) else "N/A"
            expense = row.get("expense_ratio")
            expense_display = f"{expense * 100:.2f}%" if expense is not None and not pd.isna(expense) else "N/A"
            name = row.get("description") or row.get("name") or ""
            ret = row.get("annual_return")
            ret_display = f"{ret * 100:.2f}%" if ret is not None and not pd.isna(ret) else "N/A"
            vol = row.get("annual_volatility")
            vol_display = f"{vol * 100:.2f}%" if vol is not None and not pd.isna(vol) else "N/A"
            sharpe = row.get("sharpe_ratio")
            sharpe_display = f"{sharpe:.3f}" if sharpe is not None and not pd.isna(sharpe) else "N/A"
            lines.append(
                f"| {row['ticker']} | {name[:40]} | {row['quantity']:.0f} | "
                f"¥{row['latest_price']:.2f} | ¥{row['market_value']:.0f} | "
                f"{weight_display} | {expense_display} | {ret_display} | {vol_display} | {sharpe_display} |"
            )

        total_value = asset_breakdown["market_value"].sum()
        lines.append("")
        lines.append(f"*Total: {len(asset_breakdown)} ETFs, Portfolio value: ¥{total_value:,.0f}*")
        lines.append("")

        annual_asset_returns = analysis_payload.get("annual_asset_returns") or []
        if annual_asset_returns:
            lines.append("### Annual Performance by ETF")
            lines.append("| Year | Ticker | Name | Return | Volatility | Sharpe |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for row in annual_asset_returns:
                ret_display = f"{row['annual_return'] * 100:.2f}%"
                vol_display = f"{row['annual_volatility'] * 100:.2f}%" if row["annual_volatility"] is not None else "N/A"
                sharpe_value = row.get("sharpe_ratio")
                sharpe_display = f"{sharpe_value:.3f}" if sharpe_value is not None else "N/A"
                lines.append(
                    f"| {row['year']} | {row['ticker']} | {row.get('name', '')[:40]} | {ret_display} | {vol_display} | {sharpe_display} |"
                )
            lines.append("")

        annual_portfolio_returns = analysis_payload.get("annual_portfolio_returns") or []
        if annual_portfolio_returns:
            lines.append("### Annual Portfolio Performance")
            lines.append("| Year | Return | Volatility | Sharpe |")
            lines.append("| --- | --- | --- | --- |")
            for row in annual_portfolio_returns:
                ret_display = f"{row['annual_return'] * 100:.2f}%"
                vol_display = f"{row['annual_volatility'] * 100:.2f}%" if row["annual_volatility"] is not None else "N/A"
                sharpe_value = row.get("sharpe_ratio")
                sharpe_display = f"{sharpe_value:.3f}" if sharpe_value is not None else "N/A"
                lines.append(f"| {row['year']} | {ret_display} | {vol_display} | {sharpe_display} |")
            lines.append("")

        forward_test = analysis_payload.get("forward_test") if analysis_payload else None
        if isinstance(forward_test, dict):
            summary_forward = forward_test.get("summary", {})
            start = summary_forward.get("start")
            end = summary_forward.get("end")

            lines.append("## Part 3: FORWARD PERIOD PERFORMANCE ⭐")
            lines.append("")
            lines.append("**Purpose**: Actual realized risk and return during holding period")
            if start and end:
                duration_days = (end - start).days
                duration_years = duration_days / 365.25
                lines.append(f"**Period**: {start.date()} to {end.date()} ({duration_years:.1f} years)")
            lines.append("**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.")
            lines.append("")

            lines.append("### Forward Period Metrics")
            lines.append("| Metric | Value |")
            lines.append("| --- | --- |")
            if summary_forward.get("cumulative_return") is not None:
                lines.append(f"| Cumulative Return | {summary_forward['cumulative_return'] * 100:.2f}% |")
            if summary_forward.get("annualized_return") is not None:
                lines.append(f"| Annualized Return | {summary_forward['annualized_return'] * 100:.2f}% |")
            if summary_forward.get("annualized_volatility") is not None:
                fw_vol = summary_forward['annualized_volatility']
                constraints = self.config.optimization.constraints if self.config.optimization else {}
                max_vol = constraints.get("max_volatility", 0.15)
                vol_note = " ⚠️ (Exceeds constraint)" if fw_vol > max_vol else ""
                lines.append(f"| Annualized Volatility | {fw_vol * 100:.2f}%{vol_note} |")
            if summary_forward.get("max_drawdown") is not None:
                lines.append(f"| Max Drawdown | {summary_forward['max_drawdown'] * 100:.2f}% |")
            if summary_forward.get("sharpe_ratio") is not None:
                lines.append(f"| Sharpe Ratio | {summary_forward['sharpe_ratio']:.3f} |")
            lines.append("")

            opt_metrics = analysis_payload.get("optimization_metrics") if analysis_payload else {}
            if opt_metrics and summary_forward:
                constraints = self.config.optimization.constraints if self.config.optimization else {}
                comparison_lines = self._format_backtest_vs_forward_comparison(
                    opt_metrics, summary_forward, constraints
                )
                lines.extend(comparison_lines)
                lines.append("")

                fw_vol = summary_forward.get("annualized_volatility", 0)
                bt_vol = opt_metrics.get("annual_volatility", 0)
                max_vol = constraints.get("max_volatility", 0.15)
                if fw_vol > max_vol or abs(fw_vol - bt_vol) > 0.03:
                    lines.append("### ⚠️ Forward-Looking Bias Warning")
                    lines.append("")
                    if fw_vol > max_vol:
                        lines.append(
                            f"**IMPORTANT**: Forward period volatility ({fw_vol * 100:.2f}%) "
                            f"**EXCEEDED** the backtest constraint ({max_vol * 100:.0f}%)."
                        )
                    if abs(fw_vol - bt_vol) > 0.03:
                        diff_pct = (fw_vol - bt_vol) / bt_vol * 100 if bt_vol > 0 else 0
                        lines.append(
                            f"Forward volatility changed by {diff_pct:+.1f}% relative to backtest period."
                        )
                    lines.append("")
                    lines.append("This demonstrates that **historical constraints do NOT guarantee future compliance**.")
                    lines.append("Market regime changes can significantly alter risk characteristics.")
                    lines.append("")

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

        if len(warning_events) > 0 or len(liquidation_events) > 0:
            lines.append("## Historical Breaches")
            if len(warning_events) > 0:
                lines.append("### Margin Call Summary (>= 70%)")
                lines.append(f"- Total events: {len(warning_events)} days")
                lines.append(f"- First breach: {warning_events['date'].min().date()}")
                lines.append(f"- Last breach: {warning_events['date'].max().date()}")
                lines.append(f"- Max ratio: {warning_events['loan_ratio'].max():.3f}")
                lines.append("")
                lines.append("**First 5 events:**")
                lines.append("| Date | Loan Ratio |")
                lines.append("| --- | --- |")
                for _, row in warning_events.head(5).iterrows():
                    lines.append(f"| {row['date'].date()} | {row['loan_ratio']:.3f} |")
                lines.append("")
                lines.append("**Last 5 events:**")
                lines.append("| Date | Loan Ratio |")
                lines.append("| --- | --- |")
                for _, row in warning_events.tail(5).iterrows():
                    lines.append(f"| {row['date'].date()} | {row['loan_ratio']:.3f} |")
                lines.append("")

            if len(liquidation_events) > 0:
                lines.append("### Forced Liquidation Summary (>= 85%)")
                lines.append(f"- Total events: {len(liquidation_events)} days")
                lines.append("")

        return "\n".join(lines)
