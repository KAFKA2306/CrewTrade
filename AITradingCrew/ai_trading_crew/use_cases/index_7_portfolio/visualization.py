from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Index7PortfolioVisualizer:
    def __init__(self, output_dir: Path):
        self.graphs_dir = output_dir / "graphs"
        self.graphs_dir.mkdir(parents=True, exist_ok=True)
        plt.style.use("seaborn-v0_8-darkgrid")
        sns.set_palette("husl")

    def generate_all_charts(self, analysis_payload: Dict, validator) -> Dict:
        portfolio = analysis_payload["portfolio"]
        prices = analysis_payload["prices"]
        loan_amount = analysis_payload["loan_amount"]
        warning_ratio = analysis_payload["warning_ratio"]
        liquidation_ratio = analysis_payload["liquidation_ratio"]

        chart_paths = {}

        chart_paths["allocation"] = self._plot_allocation(portfolio)

        benchmark_results = validator.benchmark_comparison()
        chart_paths["cumulative_returns"] = self._plot_cumulative_returns(prices, portfolio, benchmark_results)

        chart_paths["drawdown"] = self._plot_drawdown(prices, portfolio)

        stress_results = validator.stress_test()
        chart_paths["ltv_stress"] = self._plot_ltv_stress(
            prices, portfolio, loan_amount, warning_ratio, liquidation_ratio, stress_results
        )

        chart_paths["asset_contribution"] = self._plot_asset_contribution(prices, portfolio)

        chart_paths["risk_return"] = self._plot_risk_return_scatter(prices, portfolio)

        chart_paths["rolling_sharpe"] = self._plot_rolling_sharpe(prices, portfolio)

        chart_paths["correlation"] = self._plot_correlation_heatmap(prices)

        return chart_paths

    def _plot_allocation(self, portfolio: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(10, 7))

        labels = [f"{row['ticker']}\n{row['name'][:15]}" for _, row in portfolio.iterrows()]
        weights = portfolio["weight"].values
        colors = sns.color_palette("Set3", len(portfolio))

        wedges, texts, autotexts = ax.pie(
            weights,
            labels=labels,
            autopct=lambda pct: f"{pct:.1f}%",
            startangle=90,
            colors=colors,
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(10)
            autotext.set_weight("bold")

        for text in texts:
            text.set_fontsize(9)

        ax.set_title("Portfolio Allocation by Asset", fontsize=14, weight="bold", pad=20)

        plt.tight_layout()
        path = self.graphs_dir / "01_allocation.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_cumulative_returns(
        self, prices: pd.DataFrame, portfolio: pd.DataFrame, benchmark_results: Dict
    ) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()

        daily_returns = prices.pct_change().dropna()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )
        cumulative_optimized = (1 + portfolio_returns).cumprod()

        equal_weights = {ticker: 1.0 / len(prices.columns) for ticker in prices.columns}
        equal_returns = daily_returns.apply(
            lambda row: sum(equal_weights.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )
        cumulative_equal = (1 + equal_returns).cumprod()

        ax.plot(cumulative_optimized.index, cumulative_optimized.values, label="Optimized Portfolio", linewidth=2)
        ax.plot(cumulative_equal.index, cumulative_equal.values, label="Equal Weight", linewidth=2, linestyle="--")

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Cumulative Return (Base=1)", fontsize=12)
        ax.set_title("Cumulative Returns: Portfolio Strategies Comparison", fontsize=14, weight="bold")
        ax.legend(loc="upper left", fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        path = self.graphs_dir / "02_cumulative_returns.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_drawdown(self, prices: pd.DataFrame, portfolio: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )
        cumulative = (1 + portfolio_returns).cumprod()

        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        ax.fill_between(drawdown.index, drawdown.values, 0, alpha=0.4, color="red", label="Drawdown")
        ax.plot(drawdown.index, drawdown.values, color="darkred", linewidth=1.5)

        ax.axhline(y=drawdown.min(), color="black", linestyle="--", linewidth=1, alpha=0.7)
        ax.text(
            drawdown.index[len(drawdown) // 2],
            drawdown.min() - 0.01,
            f"Max DD: {drawdown.min()*100:.2f}%",
            fontsize=10,
            ha="center",
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Drawdown (%)", fontsize=12)
        ax.set_title("Portfolio Drawdown Evolution", fontsize=14, weight="bold")
        ax.legend(loc="lower left", fontsize=11)
        ax.grid(True, alpha=0.3)

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.0f}%"))

        plt.tight_layout()
        path = self.graphs_dir / "03_drawdown.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_ltv_stress(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        loan_amount: float,
        warning_ratio: float,
        liquidation_ratio: float,
        stress_results: Dict,
    ) -> Path:
        fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )

        initial_value = loan_amount / 0.6
        portfolio_value = initial_value * (1 + portfolio_returns).cumprod()
        ltv_series = loan_amount / portfolio_value

        stress_periods = [
            ("2020_covid_crash", "2020-02-01", "2020-04-30", "COVID-19 Crash"),
            ("2022_inflation_shock", "2022-01-01", "2022-10-31", "2022 Inflation Shock"),
        ]

        for idx, (period_key, start, end, label) in enumerate(stress_periods):
            ax = axes[idx]

            period_ltv = ltv_series.loc[start:end]

            if len(period_ltv) > 0:
                ax.plot(period_ltv.index, period_ltv.values * 100, linewidth=2, label="Portfolio LTV", color="blue")

                ax.axhline(y=warning_ratio * 100, color="orange", linestyle="--", linewidth=1.5, label=f"Warning ({warning_ratio*100:.0f}%)")
                ax.axhline(y=liquidation_ratio * 100, color="red", linestyle="--", linewidth=1.5, label=f"Liquidation ({liquidation_ratio*100:.0f}%)")

                if period_key in stress_results and "ltv_breaches" in stress_results[period_key]:
                    breaches = stress_results[period_key]["ltv_breaches"]
                    ax.text(
                        0.02, 0.98,
                        f"Liquidation breaches: {breaches.get('liquidation', 0)} days\nWarning breaches: {breaches.get('warning', 0)} days",
                        transform=ax.transAxes,
                        fontsize=9,
                        verticalalignment="top",
                        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
                    )

                ax.set_ylabel("LTV (%)", fontsize=11)
                ax.set_title(f"LTV During {label}", fontsize=12, weight="bold")
                ax.legend(loc="upper right", fontsize=9)
                ax.grid(True, alpha=0.3)
            else:
                ax.text(0.5, 0.5, f"No data for {label}", ha="center", va="center", fontsize=12)

        axes[-1].set_xlabel("Date", fontsize=12)

        plt.tight_layout()
        path = self.graphs_dir / "04_ltv_stress.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_asset_contribution(self, prices: pd.DataFrame, portfolio: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()

        asset_contributions = {}
        for ticker in portfolio["ticker"]:
            if ticker in daily_returns.columns:
                contribution = daily_returns[ticker] * weights_dict[ticker]
                cumulative_contribution = (1 + contribution).cumprod() - 1
                asset_contributions[ticker] = cumulative_contribution

        contribution_df = pd.DataFrame(asset_contributions)

        ax.stackplot(
            contribution_df.index,
            *[contribution_df[col].values for col in contribution_df.columns],
            labels=contribution_df.columns,
            alpha=0.7,
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Cumulative Contribution", fontsize=12)
        ax.set_title("Asset Contribution to Portfolio Returns", fontsize=14, weight="bold")
        ax.legend(loc="upper left", fontsize=9, ncol=2)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        path = self.graphs_dir / "05_asset_contribution.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_risk_return_scatter(self, prices: pd.DataFrame, portfolio: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(10, 7))

        daily_returns = prices.pct_change().dropna()

        asset_metrics = []
        for ticker in portfolio["ticker"]:
            if ticker in daily_returns.columns:
                annual_return = daily_returns[ticker].mean() * 252
                annual_vol = daily_returns[ticker].std() * np.sqrt(252)
                asset_metrics.append({
                    "ticker": ticker,
                    "return": annual_return,
                    "volatility": annual_vol,
                })

        metrics_df = pd.DataFrame(asset_metrics)

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )
        portfolio_annual_return = portfolio_returns.mean() * 252
        portfolio_annual_vol = portfolio_returns.std() * np.sqrt(252)

        ax.scatter(
            metrics_df["volatility"] * 100,
            metrics_df["return"] * 100,
            s=100,
            alpha=0.7,
            label="Individual Assets",
        )

        for _, row in metrics_df.iterrows():
            ax.annotate(
                row["ticker"],
                (row["volatility"] * 100, row["return"] * 100),
                fontsize=9,
                xytext=(5, 5),
                textcoords="offset points",
            )

        ax.scatter(
            portfolio_annual_vol * 100,
            portfolio_annual_return * 100,
            s=300,
            color="red",
            marker="*",
            label="Optimized Portfolio",
            edgecolors="black",
            linewidths=1.5,
            zorder=5,
        )

        ax.set_xlabel("Annual Volatility (%)", fontsize=12)
        ax.set_ylabel("Annual Return (%)", fontsize=12)
        ax.set_title("Risk-Return Profile", fontsize=14, weight="bold")
        ax.legend(loc="best", fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        path = self.graphs_dir / "06_risk_return.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_rolling_sharpe(self, prices: pd.DataFrame, portfolio: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))

        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index),
            axis=1,
        )

        window = 252
        rolling_mean = portfolio_returns.rolling(window=window).mean() * 252
        rolling_std = portfolio_returns.rolling(window=window).std() * np.sqrt(252)
        rolling_sharpe = rolling_mean / rolling_std

        ax.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=2, color="purple")
        ax.axhline(y=0, color="black", linestyle="--", linewidth=1, alpha=0.5)
        ax.axhline(y=1, color="green", linestyle="--", linewidth=1, alpha=0.5, label="Sharpe = 1")

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Sharpe Ratio", fontsize=12)
        ax.set_title("Rolling Sharpe Ratio (252-day window)", fontsize=14, weight="bold")
        ax.legend(loc="best", fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        path = self.graphs_dir / "07_rolling_sharpe.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path

    def _plot_correlation_heatmap(self, prices: pd.DataFrame) -> Path:
        fig, ax = plt.subplots(figsize=(10, 8))

        daily_returns = prices.pct_change().dropna()
        correlation_matrix = daily_returns.corr()

        sns.heatmap(
            correlation_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax,
        )

        ax.set_title("Asset Return Correlation Matrix", fontsize=14, weight="bold", pad=20)

        plt.tight_layout()
        path = self.graphs_dir / "08_correlation.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()

        return path
