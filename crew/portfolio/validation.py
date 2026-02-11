from pathlib import Path
from typing import Dict, List
import numpy as np
import pandas as pd
from crew.portfolio.analysis import Index7PortfolioAnalyzer
from crew.portfolio.config import Index7PortfolioConfig
from crew.portfolio.data_pipeline import (
    Index7PortfolioDataPipeline,
)
class Index7PortfolioValidator:
    def __init__(self, config: Index7PortfolioConfig, raw_data_dir: Path):
        self.config = config
        self.pipeline = Index7PortfolioDataPipeline(raw_data_dir, config)
    def walk_forward_test(
        self,
        train_years: int = 10,
        test_years: int = 2,
        rebalance_freq: str = "Q",
    ) -> Dict:
        data_payload = self.pipeline.collect(as_of=None)
        prices = data_payload["prices"]
        prices.index = pd.to_datetime(prices.index, errors="coerce")
        prices = prices[prices.index.notna()]
        prices = prices.sort_index()
        index_master = data_payload["index_master"]
        start_date = prices.index.min()
        end_date = prices.index.max()
        total_years = (end_date - start_date).days / 365.25
        if total_years < train_years + test_years:
            raise ValueError(
                f"データ期間不足: {total_years:.1f}年 < {train_years + test_years}年"
            )
        results = []
        current_train_end = start_date + pd.DateOffset(years=train_years)
        while current_train_end + pd.DateOffset(years=test_years) <= end_date:
            test_end = current_train_end + pd.DateOffset(years=test_years)
            train_prices = prices.loc[:current_train_end]
            test_prices = prices.loc[current_train_end:test_end]
            if len(train_prices) < 252 or len(test_prices) < 60:
                current_train_end += pd.DateOffset(years=2)
                continue
            analyzer = Index7PortfolioAnalyzer(self.config)
            train_data = {"prices": train_prices, "index_master": index_master}
            optimization_result = analyzer.evaluate(train_data)
            portfolio_weights = (
                optimization_result["portfolio"].set_index("ticker")["weight"].to_dict()
            )
            test_perf = self._simulate_period(
                test_prices,
                portfolio_weights,
                rebalance_freq=rebalance_freq,
            )
            results.append(
                {
                    "train_start": start_date,
                    "train_end": current_train_end,
                    "test_start": current_train_end,
                    "test_end": test_end,
                    "portfolio_weights": portfolio_weights,
                    "test_performance": test_perf,
                }
            )
            current_train_end += pd.DateOffset(years=2)
        return {
            "walk_forward_results": results,
            "summary": self._summarize_walk_forward(results),
        }
    def _simulate_period(
        self,
        prices: pd.DataFrame,
        initial_weights: Dict[str, float],
        rebalance_freq: str = "Q",
    ) -> Dict:
        daily_returns = prices.pct_change()
        valid_index = prices.index[prices.index.notna()]
        if valid_index.empty:
            raise ValueError("No valid dates in simulation period")
        portfolio_value = [100.0]
        weights = {
            ticker: initial_weights.get(ticker, 0.0) for ticker in prices.columns
        }
        rebalance_dates = pd.date_range(
            valid_index.min(),
            valid_index.max(),
            freq=rebalance_freq,
        )
        rebalance_set = set(rebalance_dates)
        ltv_breaches = {"warning": 0, "liquidation": 0}
        loan_amount = self.config.loan_amount
        for date in valid_index[1:]:
            if date in rebalance_set:
                weights = {
                    ticker: initial_weights.get(ticker, 0.0)
                    for ticker in prices.columns
                }
            current_day_allocations = []
            for ticker in daily_returns.columns:
                if ticker not in weights:
                    continue
                w = weights.get(ticker, 0.0)
                ret = daily_returns.loc[date, ticker]
                if pd.isna(ret):
                    ret = 0.0
                current_day_allocations.append(w * ret)
            day_return = sum(current_day_allocations)
            new_value = portfolio_value[-1] * (1 + day_return)
            portfolio_value.append(new_value)
            current_ltv = loan_amount / new_value if new_value > 0 else float("inf")
            if current_ltv >= self.config.liquidation_ratio:
                ltv_breaches["liquidation"] += 1
            elif current_ltv >= self.config.warning_ratio:
                ltv_breaches["warning"] += 1
        portfolio_series = pd.Series(portfolio_value, index=valid_index)
        total_return = (portfolio_series.iloc[-1] / portfolio_series.iloc[0]) - 1
        annual_return = (1 + total_return) ** (252 / len(portfolio_series)) - 1
        daily_ret_series = portfolio_series.pct_change().dropna()
        annual_volatility = daily_ret_series.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
        cummax = portfolio_series.expanding().max()
        drawdown = (portfolio_series - cummax) / cummax
        max_drawdown = drawdown.min()
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        win_rate = (daily_ret_series > 0).sum() / len(daily_ret_series)
        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "annual_volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "calmar_ratio": calmar_ratio,
            "win_rate": win_rate,
            "ltv_breaches": ltv_breaches,
        }
    def _summarize_walk_forward(self, results: List[Dict]) -> Dict:
        if not results:
            return {}
        sharpe_ratios = [r["test_performance"]["sharpe_ratio"] for r in results]
        annual_returns = [r["test_performance"]["annual_return"] for r in results]
        max_drawdowns = [r["test_performance"]["max_drawdown"] for r in results]
        calmar_ratios = [r["test_performance"]["calmar_ratio"] for r in results]
        return {
            "num_periods": len(results),
            "avg_sharpe": np.mean(sharpe_ratios),
            "std_sharpe": np.std(sharpe_ratios),
            "avg_annual_return": np.mean(annual_returns),
            "avg_max_drawdown": np.mean(max_drawdowns),
            "avg_calmar_ratio": np.mean(calmar_ratios),
            "stability_score": 1 / (1 + np.std(sharpe_ratios)),
        }
    def benchmark_comparison(self) -> Dict:
        data_payload = self.pipeline.collect(as_of=None)
        prices = data_payload["prices"]
        index_master = data_payload["index_master"]
        analyzer = Index7PortfolioAnalyzer(self.config)
        optimized_result = analyzer.evaluate(data_payload)
        optimized_weights = (
            optimized_result["portfolio"].set_index("ticker")["weight"].to_dict()
        )
        equal_weights = {ticker: 1.0 / len(prices.columns) for ticker in prices.columns}
        equity_tickers = [
            ticker
            for ticker in prices.columns
            if index_master[index_master["ticker"] == ticker]["category"].values[0]
            == "equity"
        ]
        bond_tickers = [
            ticker
            for ticker in prices.columns
            if index_master[index_master["ticker"] == ticker]["category"].values[0]
            == "bonds"
        ]
        sixty_forty_weights = {}
        if equity_tickers and bond_tickers:
            equity_weight = 0.6 / len(equity_tickers)
            bond_weight = 0.4 / len(bond_tickers)
            for ticker in prices.columns:
                if ticker in equity_tickers:
                    sixty_forty_weights[ticker] = equity_weight
                elif ticker in bond_tickers:
                    sixty_forty_weights[ticker] = bond_weight
                else:
                    sixty_forty_weights[ticker] = 0.0
        else:
            sixty_forty_weights = equal_weights
        benchmarks = {
            "optimized": optimized_weights,
            "equal_weight": equal_weights,
            "60_40": sixty_forty_weights,
        }
        results = {}
        for name, weights in benchmarks.items():
            perf = self._simulate_period(prices, weights, rebalance_freq="Q")
            results[name] = perf
        return results
    def stress_test(self) -> Dict:
        data_payload = self.pipeline.collect(as_of=None)
        prices = data_payload["prices"]
        analyzer = Index7PortfolioAnalyzer(self.config)
        optimized_result = analyzer.evaluate(data_payload)
        optimized_weights = (
            optimized_result["portfolio"].set_index("ticker")["weight"].to_dict()
        )
        stress_periods = [
            ("2008_financial_crisis", "2008-09-01", "2009-03-31"),
            ("2020_covid_crash", "2020-02-01", "2020-04-30"),
            ("2022_inflation_shock", "2022-01-01", "2022-10-31"),
        ]
        results = {}
        for period_name, start, end in stress_periods:
            try:
                period_prices = prices.loc[start:end]
                if len(period_prices) < 30:
                    results[period_name] = {"error": "データ不足"}
                    continue
                perf = self._simulate_period(
                    period_prices, optimized_weights, rebalance_freq="M"
                )
                results[period_name] = perf
            except Exception as e:
                results[period_name] = {"error": str(e)}
        return results
    def sensitivity_analysis(self) -> Dict:
        data_payload = self.pipeline.collect(as_of=None)
        prices = data_payload["prices"]
        index_master = data_payload["index_master"]
        base_config = self.config
        configs = {
            "base": base_config,
            "min_weight_10pct": self._modify_config(base_config, "min_weight", 0.10),
            "max_weight_40pct": self._modify_config(base_config, "max_weight", 0.40),
            "max_volatility_20pct": self._modify_config(
                base_config, "max_volatility", 0.20
            ),
            "sharpe_weight_80pct": self._modify_config(
                base_config, "sharpe_weight", 0.80
            ),
        }
        results = {}
        for config_name, config in configs.items():
            analyzer = Index7PortfolioAnalyzer(config)
            analysis_result = analyzer.evaluate(
                {"prices": prices, "index_master": index_master}
            )
            weights = (
                analysis_result["portfolio"].set_index("ticker")["weight"].to_dict()
            )
            perf = self._simulate_period(prices, weights, rebalance_freq="Q")
            results[config_name] = {
                "portfolio": analysis_result["portfolio"],
                "performance": perf,
            }
        return results
    def _modify_config(
        self, config: Index7PortfolioConfig, param: str, value: float
    ) -> Index7PortfolioConfig:
        import copy
        new_config = copy.deepcopy(config)
        if param == "min_weight":
            new_config.optimization.constraints["min_weight"] = value
        elif param == "max_weight":
            new_config.optimization.constraints["max_weight"] = value
        elif param == "max_volatility":
            new_config.optimization.constraints["max_volatility"] = value
        elif param == "sharpe_weight":
            new_config.optimization.objective_weights["sharpe"] = value
            new_config.optimization.objective_weights["volatility"] = 1.0 - value
        return new_config
    def generate_validation_report(self, output_dir: Path) -> Path:
        report_lines = ["
        report_lines.append(f"**Generated:** {pd.Timestamp.now()}\n\n")
        report_lines.append("
        wf_results = self.walk_forward_test(
            train_years=5, test_years=2, rebalance_freq="Q"
        )
        summary = wf_results["summary"]
        report_lines.append(f"- **Periods tested:** {summary['num_periods']}\n")
        report_lines.append(
            f"- **Avg Out-of-Sample Sharpe:** {summary['avg_sharpe']:.3f} ± {summary['std_sharpe']:.3f}\n"
        )
        report_lines.append(
            f"- **Avg Annual Return:** {summary['avg_annual_return'] * 100:.2f}%\n"
        )
        report_lines.append(
            f"- **Avg Max Drawdown:** {summary['avg_max_drawdown'] * 100:.2f}%\n"
        )
        report_lines.append(
            f"- **Stability Score:** {summary['stability_score']:.3f}\n\n"
        )
        report_lines.append("
        benchmark_results = self.benchmark_comparison()
        report_lines.append("| Strategy | Annual Return | Sharpe | Max DD | Calmar |\n")
        report_lines.append("|----------|---------------|--------|--------|--------|\n")
        for name, perf in benchmark_results.items():
            report_lines.append(
                f"| {name} | {perf['annual_return'] * 100:.2f}% | "
                f"{perf['sharpe_ratio']:.3f} | {perf['max_drawdown'] * 100:.2f}% | "
                f"{perf['calmar_ratio']:.3f} |\n"
            )
        report_lines.append("\n")
        report_lines.append("
        stress_results = self.stress_test()
        for period_name, perf in stress_results.items():
            report_lines.append(f"
            if "error" in perf:
                report_lines.append(f"- Error: {perf['error']}\n\n")
            else:
                report_lines.append(
                    f"- **Total Return:** {perf['total_return'] * 100:.2f}%\n"
                )
                report_lines.append(
                    f"- **Max Drawdown:** {perf['max_drawdown'] * 100:.2f}%\n"
                )
                report_lines.append(
                    f"- **LTV Warning Breaches:** {perf['ltv_breaches']['warning']}\n"
                )
                report_lines.append(
                    f"- **LTV Liquidation Breaches:** {perf['ltv_breaches']['liquidation']}\n\n"
                )
        report_lines.append("
        sensitivity_results = self.sensitivity_analysis()
        report_lines.append("| Config | Annual Return | Sharpe | Max DD |\n")
        report_lines.append("|--------|---------------|--------|--------|\n")
        for config_name, result in sensitivity_results.items():
            perf = result["performance"]
            report_lines.append(
                f"| {config_name} | {perf['annual_return'] * 100:.2f}% | "
                f"{perf['sharpe_ratio']:.3f} | {perf['max_drawdown'] * 100:.2f}% |\n"
            )
        report_path = output_dir / "validation_report.md"
        report_path.write_text("".join(report_lines), encoding="utf-8")
        return report_path
