from pathlib import Path
from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.index_7_portfolio.config import Index7PortfolioConfig
from ai_trading_crew.use_cases.index_7_portfolio.validation import Index7PortfolioValidator
from ai_trading_crew.use_cases.index_7_portfolio.visualization import Index7PortfolioVisualizer


class Index7PortfolioReporter:
    def __init__(self, report_dir: Path, config: Index7PortfolioConfig = None):
        self.output_dir = report_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config

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

        chart_paths = {}
        walk_forward_results = None
        walk_forward_error = None
        if self.config is not None:
            print("  Generating visualizations...")
            validator = Index7PortfolioValidator(self.config)
            visualizer = Index7PortfolioVisualizer(self.output_dir)
            try:
                walk_forward_results = validator.walk_forward_test(train_years=5, test_years=2, rebalance_freq="Q")
            except Exception as exc:
                walk_forward_error = str(exc)
                walk_forward_results = None
            chart_paths = visualizer.generate_all_charts(analysis_payload, validator, walk_forward_results)
            print(f"  ✓ Generated {len(chart_paths)} charts")

        report_lines = []
        report_lines.append("# Index 7-Portfolio Optimization Report\n")
        report_lines.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report_lines.append("## 代替ETF対応表\n")
        report_lines.append("| 国内ETF | 代替指数 | オリジナル |")
        report_lines.append("|---------|----------|-----------|")
        report_lines.append("| 1655.T ｉＳ米国株 | S&P500指数 | ^GSPC |")
        report_lines.append("| 2840.T ｉＦＥナ百無 | NASDAQ100 | ^NDX |")
        report_lines.append("| 1364.T ｉシェア４百 | JPX日経400 | ^N225 |")
        report_lines.append("| 314A.T ｉＳゴールド | LBMA Gold Price | GC=F |")
        report_lines.append("| 2520.T 野村新興国株 | MSCIエマージング・マーケットIMI指数 | EEM |")
        report_lines.append("| 2511.T 野村外国債券 | FTSE世界国債インデックス(除く日本) | TLT |")
        report_lines.append("| 399A.T 上場高配５０ | 東証配当フォーカス100指数 | 1478.T |")
        report_lines.append("\n**初期投資額:** ¥20,998,698（Max DD -20.63%バッファ込み、為替リスク排除、円建て運用）\n")

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
            report_lines.append("\n⚠️ **CRITICAL:** LTV exceeds liquidation threshold!")
        elif current_ltv >= warning_ratio:
            report_lines.append("\n⚠️ **WARNING:** LTV exceeds warning threshold")
        else:
            report_lines.append("\n✅ **HEALTHY:** LTV within safe limits")

        if self.config is not None:
            opt_conf = self.config.optimization
            report_lines.append("\n## トレーニング設定と検証概要\n")
            report_lines.append(f"- **最適化サンプル数:** {opt_conf.sample_size:,}")
            report_lines.append(
                f"- **最適化目的関数ウェイト:** "
                + ", ".join(f"{k} {v*100:.0f}%" for k, v in opt_conf.objective_weights.items())
            )
            report_lines.append(
                f"- **制約条件:** "
                + ", ".join(f"{k}={v:.2f}" for k, v in opt_conf.constraints.items())
            )
            report_lines.append(f"- **リバランス頻度（検証時）:** 四半期（Q）")
            report_lines.append(f"- **訓練期間 / テスト期間:** 5年 / 2年（ローリング）")
            report_lines.append(f"- **最適化ルックバック:** {opt_conf.lookback}")
            report_lines.append(f"- **最大ドローダウンバッファ:** {opt_conf.max_drawdown_buffer*100:.2f}%")

            if walk_forward_results:
                summary = walk_forward_results.get("summary", {})
                report_lines.append("\n### ウォークフォワード検証サマリー\n")
                report_lines.append(f"- **評価期間数:** {summary.get('num_periods', 0)}")
                if summary:
                    report_lines.append(f"- **平均アウトオブサンプル Sharpe:** {summary.get('avg_sharpe', 0):.3f} ± {summary.get('std_sharpe', 0):.3f}")
                    report_lines.append(f"- **平均年率リターン:** {summary.get('avg_annual_return', 0)*100:.2f}%")
                    report_lines.append(f"- **平均最大ドローダウン:** {summary.get('avg_max_drawdown', 0)*100:.2f}%")
                    report_lines.append(f"- **Stability Score:** {summary.get('stability_score', 0):.3f}")

                report_lines.append("\n### 期間別ポートフォリオ構成（降順ウェイト）\n")
                report_lines.append("| Period | 訓練期間 | テスト期間 | ウェイト構成 | Sharpe | Max DD |")
                report_lines.append("|--------|-----------|------------|--------------|--------|--------|")
                for idx, period in enumerate(walk_forward_results.get("walk_forward_results", []), start=1):
                    weights = period["portfolio_weights"]
                    sorted_assets = sorted(weights.items(), key=lambda x: -x[1])
                    weight_lines = "<br>".join(f"{ticker} {weight*100:.1f}%" for ticker, weight in sorted_assets)
                    test_perf = period.get("test_performance", {})
                    report_lines.append(
                        f"| {idx} | {period['train_start'].date()}〜{period['train_end'].date()} | "
                        f"{period['test_start'].date()}〜{period['test_end'].date()} | {weight_lines} | "
                        f"{test_perf.get('sharpe_ratio', 0):.3f} | {test_perf.get('max_drawdown', 0)*100:.2f}% |"
                    )
            elif walk_forward_error:
                report_lines.append("\n### ウォークフォワード検証サマリー\n")
                report_lines.append(f"- 実行エラー: {walk_forward_error}")

        if chart_paths:
            report_lines.append("\n## Visualizations\n")

            report_lines.append("### Portfolio Allocation")
            report_lines.append(
                "100% stacked bar chart comparing asset weights across the optimized "
                "portfolio, reference strategies (Equal Weight, 60/40 Mix, Inverse-Vol, "
                "Min/Max variants), and walk-forward periods."
            )
            report_lines.append("![Portfolio Allocation](./graphs/01_allocation.png)\n")

            report_lines.append("### Cumulative Returns Comparison")
            report_lines.append(
                "Stacked area view of strategy share (Optimized, Equal Weight, reference mixes) with cumulative return overlay."
            )
            report_lines.append("![Cumulative Returns](./graphs/02_cumulative_returns.png)\n")

            report_lines.append("### Drawdown Evolution")
            report_lines.append(
                "Stacked drawdown contributions by asset category, with total drawdown overlay."
            )
            report_lines.append("![Drawdown](./graphs/03_drawdown.png)\n")

            report_lines.append("### LTV Stress Tests")
            report_lines.append("Loan-to-Value ratio during historical crisis periods (COVID-19, 2022 Inflation).")
            report_lines.append("![LTV Stress](./graphs/04_ltv_stress.png)\n")

            report_lines.append("### Asset Contribution to Returns")
            report_lines.append("Monthly positive/negative contribution by asset relative to category-colored baseline.")
            report_lines.append("![Asset Contribution](./graphs/05_asset_contribution.png)\n")

            report_lines.append("### Risk-Return Profile")
            report_lines.append(
                "Scatter plot comparing individual assets with multiple allocation strategies "
                "(Optimized, Equal Weight, 60/40 Mix, Inverse-Vol, Min Variance, Max Sharpe, "
                "Min Volatility, Min Drawdown, Max Kelly, Walk-Forward portfolios WF#1/WF#2)."
            )
            report_lines.append("![Risk-Return](./graphs/06_risk_return.png)\n")

            report_lines.append("### Rolling Sharpe Ratio")
            report_lines.append("252-day rolling Sharpe ratio showing risk-adjusted performance stability over time.")
            report_lines.append("![Rolling Sharpe](./graphs/07_rolling_sharpe.png)\n")

            report_lines.append("### Asset Correlation Matrix")
            report_lines.append("Correlation heatmap revealing diversification benefits between assets.")
            report_lines.append("![Correlation](./graphs/08_correlation.png)\n")

        report_content = "\n".join(report_lines)
        report_path = self.output_dir / "index_7_portfolio_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        return {
            "portfolio_path": str(portfolio_path),
            "report_path": str(report_path),
            "chart_paths": {k: str(v) for k, v in chart_paths.items()},
        }
