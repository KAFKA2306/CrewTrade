from pathlib import Path
from typing import Dict, Iterable, List
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
class Index7PortfolioVisualizer:
    CATEGORY_ORDER = ["us_equity", "jp_equity", "em_equity", "bonds", "gold", "other"]
    CATEGORY_DISPLAY = {
        "us_equity": "US Equity",
        "jp_equity": "Japan Equity",
        "em_equity": "Emerging Equity",
        "bonds": "Bonds",
        "gold": "Gold",
        "other": "Other",
    }
    CATEGORY_PALETTE_NAMES = {
        "us_equity": "Blues",
        "jp_equity": "Reds",
        "em_equity": "Greens",
        "bonds": "Purples",
        "gold": "Oranges",
        "other": "Greys",
    }
    DEFAULT_COLOR = sns.color_palette("Greys", 3)[1]
    TICKER_CATEGORY_OVERRIDES = {
        "^GSPC": "us_equity",
        "^NDX": "us_equity",
        "SPY": "us_equity",
        "1655.T": "us_equity",
        "2840.T": "us_equity",
        "^N225": "jp_equity",
        "1364.T": "jp_equity",
        "1478.T": "jp_equity",
        "399A.T": "jp_equity",
        "EEM": "em_equity",
        "2520.T": "em_equity",
        "TLT": "bonds",
        "2511.T": "bonds",
        "GC=F": "gold",
        "314A.T": "gold",
    }
    def __init__(self, output_dir: Path):
        self.graphs_dir = output_dir / "graphs"
        self.graphs_dir.mkdir(parents=True, exist_ok=True)
        plt.style.use("seaborn-v0_8-darkgrid")
        sns.set_palette("husl")
    def generate_all_charts(
        self,
        analysis_payload: Dict,
        validator,
        walk_forward_results: Dict | None = None,
    ) -> Dict:
        portfolio = analysis_payload["portfolio"]
        prices = analysis_payload["prices"]
        prices.index = pd.to_datetime(prices.index)
        prices = prices.sort_index()
        index_master = analysis_payload.get("index_master")
        loan_amount = analysis_payload["loan_amount"]
        warning_ratio = analysis_payload["warning_ratio"]
        liquidation_ratio = analysis_payload["liquidation_ratio"]
        if isinstance(prices, pd.DataFrame):
            sorted_tickers = self._sort_tickers(prices.columns, index_master)
            prices = prices.reindex(columns=sorted_tickers)
        else:
            sorted_tickers = list(portfolio["ticker"])
        color_map = self._build_color_map(sorted_tickers, index_master)
        reference_portfolios = self._build_reference_portfolios(
            prices, portfolio, index_master, walk_forward_results
        )
        chart_paths = {}
        chart_paths["allocation"] = self._plot_allocation(
            portfolio, index_master, reference_portfolios, color_map
        )
        chart_paths["cumulative_returns"] = self._plot_cumulative_returns(
            prices, portfolio, reference_portfolios
        )
        chart_paths["drawdown"] = self._plot_drawdown(
            prices, portfolio, index_master, color_map
        )
        stress_results = validator.stress_test()
        chart_paths["ltv_stress"] = self._plot_ltv_stress(
            prices,
            portfolio,
            loan_amount,
            warning_ratio,
            liquidation_ratio,
            stress_results,
        )
        chart_paths["asset_contribution"] = self._plot_asset_contribution(
            prices, portfolio, index_master, color_map
        )
        chart_paths["risk_return"] = self._plot_risk_return_scatter(
            prices, portfolio, index_master, reference_portfolios, color_map
        )
        chart_paths["rolling_sharpe"] = self._plot_rolling_sharpe(prices, portfolio)
        chart_paths["correlation"] = self._plot_correlation_heatmap(prices)
        if walk_forward_results:
            chart_paths["historical_allocation"] = self._plot_historical_allocation(
                walk_forward_results, index_master, color_map
            )
        return chart_paths
    def _plot_historical_allocation(
        self,
        walk_forward_results: Dict,
        index_master: pd.DataFrame | None = None,
        color_map: Dict | None = None,
    ) -> Path:
        wf_entries = walk_forward_results.get("walk_forward_results", [])
        if not wf_entries:
            return Path("")
        rows = []
        all_tickers = set()
        for entry in wf_entries:
            period_label = f"{entry['test_start'].date().year}"
            weights = entry.get("portfolio_weights", {})
            row = {"Period": period_label}
            for ticker, w in weights.items():
                if w > 0.001:
                    row[ticker] = w * 100
                    all_tickers.add(ticker)
            rows.append(row)
        df = pd.DataFrame(rows).set_index("Period").fillna(0)
        sorted_tickers = self._sort_tickers(list(all_tickers), index_master)
        df = df.reindex(columns=sorted_tickers)
        fig, ax = plt.subplots(figsize=(14, 8))
        colors = [
            self._color_for(ticker, color_map, index_master) for ticker in df.columns
        ]
        df.plot(
            kind="bar",
            stacked=True,
            ax=ax,
            color=colors,
            width=0.8,
            edgecolor="white",
            linewidth=0.5,
        )
        ax.set_title(
            "Historical Portfolio Allocation (Walk-Forward)", fontsize=16, weight="bold"
        )
        ax.set_ylabel("Weight (%)", fontsize=12)
        ax.set_xlabel("Year (Out-of-Sample)", fontsize=12)
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0f}%"))
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.15),
            ncol=min(6, len(df.columns)),
            frameon=False,
            fontsize=9,
        )
        plt.tight_layout()
        path = self.graphs_dir / "09_historical_allocation.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _plot_allocation(
        self,
        portfolio: pd.DataFrame,
        index_master: pd.DataFrame | None = None,
        reference_portfolios: Dict | None = None,
        color_map: Dict | None = None,
    ) -> Path:
        if not reference_portfolios:
            reference_portfolios = {
                "Optimized": {
                    "weights": portfolio.set_index("ticker")["weight"],
                    "display": "Optimized (Latest)",
                    "axis_label": "Optimized",
                }
            }
        tickers_order: list[str] = list(portfolio["ticker"])
        for spec in reference_portfolios.values():
            weights = spec["weights"]
            for ticker in weights.index:
                if ticker not in tickers_order:
                    tickers_order.append(ticker)
        axis_label_to_weights: Dict[str, pd.Series] = {}
        axis_label_display: Dict[str, str] = {}
        axis_labels: list[str] = []
        for key, spec in reference_portfolios.items():
            axis_label = spec.get("axis_label", key)
            axis_labels.append(axis_label)
            axis_label_to_weights[axis_label] = spec["weights"]
            axis_label_display[axis_label] = spec.get("display", axis_label)
        weight_df = pd.DataFrame(
            {
                axis_label: axis_label_to_weights[axis_label]
                .reindex(tickers_order)
                .fillna(0.0)
                for axis_label in axis_labels
            }
        )
        weight_df = weight_df.clip(lower=0.0)
        sorted_index = self._sort_tickers(weight_df.index, index_master)
        weight_df = weight_df.loc[sorted_index]
        asset_names: Dict[str, str] = {}
        for _, row in portfolio.iterrows():
            asset_names[row["ticker"]] = row.get("name", row["ticker"])
        if index_master is not None:
            for _, row in index_master.iterrows():
                asset_names.setdefault(row["ticker"], row.get("name", row["ticker"]))
        display_index = []
        for ticker in weight_df.index:
            category_key = self._resolve_category(ticker, index_master)
            category_label = self.CATEGORY_DISPLAY.get(category_key, "Other")
            display_index.append(f"{ticker}\n{category_label}")
        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(bottom=0.27)
        colors = [
            self._color_for(ticker, color_map, index_master)
            for ticker in weight_df.index
        ]
        bottoms = np.zeros(len(axis_labels))
        x_positions = np.arange(len(axis_labels))
        formatted_labels = [axis_label_display[label] for label in axis_labels]
        for idx, (ticker, display_label) in enumerate(
            zip(weight_df.index, display_index)
        ):
            heights = weight_df.loc[ticker].values * 100
            ax.bar(
                x_positions,
                heights,
                bottom=bottoms,
                color=colors[idx % len(colors)],
                label=display_label,
                edgecolor="white",
                linewidth=0.6,
            )
            bottoms += heights
        ax.set_ylim(0, 100)
        ax.set_ylabel("Weight (%)", fontsize=12)
        ax.set_title(
            "Portfolio Allocation (100% Stacked)", fontsize=14, weight="bold", pad=16
        )
        ax.set_xticks(x_positions)
        ax.set_xticklabels(formatted_labels, rotation=45, ha="right", fontsize=10)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0f}%"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.set_axisbelow(True)
        handles, labels = ax.get_legend_handles_labels()
        legend_cols = min(max(len(labels) // 2, 3), 5)
        ax.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.2),
            fontsize=9,
            frameon=False,
            ncol=legend_cols,
        )
        plt.tight_layout()
        path = self.graphs_dir / "01_allocation.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _plot_cumulative_returns(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        reference_portfolios: Dict | None = None,
    ) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))
        daily_returns = prices.pct_change().dropna()
        strategy_order = [
            "Optimized",
            "Inverse-Vol",
            "Max Sharpe",
            "Min Variance",
            "Min Volatility",
            "Min Drawdown",
            "Max Kelly",
        ]
        strategy_values: Dict[str, pd.Series] = {}
        optimized_weights = (
            portfolio.set_index("ticker")["weight"]
            .reindex(daily_returns.columns)
            .fillna(0.0)
        )
        optimized_returns = daily_returns.mul(optimized_weights, axis=1).sum(axis=1)
        strategy_values["Optimized"] = (1 + optimized_returns).cumprod()
        if reference_portfolios:
            for key in strategy_order[1:]:
                if key not in reference_portfolios:
                    continue
                weights = (
                    reference_portfolios[key]["weights"]
                    .reindex(daily_returns.columns)
                    .fillna(0.0)
                )
                strat_ret = daily_returns.mul(weights, axis=1).sum(axis=1)
                strategy_values[key] = (1 + strat_ret).cumprod()
        value_df = pd.DataFrame(strategy_values)
        value_df = value_df.dropna()
        share_df = value_df.div(value_df.sum(axis=1), axis=0) * 100.0
        base_colors = sns.color_palette("Set2", len(value_df.columns))
        area_colors = [
            tuple(min(1.0, c + (1.0 - c) * 0.15) for c in color)
            for color in base_colors
        ]
        line_colors = [tuple(max(0.0, c * 0.9) for c in color) for color in base_colors]
        ax.stackplot(
            value_df.index,
            *[share_df[col].values for col in value_df.columns],
            labels=value_df.columns,
            colors=area_colors,
            alpha=0.85,
        )
        ax.set_ylabel("Share of Total (%)", fontsize=12)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0f}%"))
        ax.set_xlabel("Date", fontsize=12)
        ax.set_title("Cumulative Return Share by Strategy", fontsize=14, weight="bold")
        ax.grid(True, axis="y", linestyle="--", alpha=0.3)
        ax2 = ax.twinx()
        for color, col in zip(line_colors, value_df.columns):
            ax2.plot(
                value_df.index,
                value_df[col].values,
                color=color,
                linewidth=1.4,
                linestyle="-",
                alpha=0.95,
            )
        ax2.set_ylabel("Cumulative Return (Base=1)", fontsize=12)
        ax2.set_yscale("log")
        ax2.grid(False)
        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.18),
            ncol=min(4, len(value_df.columns)),
            fontsize=10,
            frameon=False,
        )
        plt.tight_layout()
        path = self.graphs_dir / "02_cumulative_returns.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _plot_drawdown(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        index_master: pd.DataFrame | None = None,
        color_map: Dict | None = None,
    ) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))
        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        sorted_tickers = self._sort_tickers(prices.columns, index_master)
        normalized_prices = prices[sorted_tickers] / prices[sorted_tickers].iloc[0]
        asset_values = normalized_prices.mul(pd.Series(weights_dict))
        portfolio_value = asset_values.sum(axis=1)
        peak_asset_values = pd.DataFrame(
            index=asset_values.index, columns=asset_values.columns, dtype=float
        )
        current_peak_value = portfolio_value.iloc[0]
        current_peak_assets = asset_values.iloc[0]
        peak_asset_values.iloc[0] = current_peak_assets
        for idx in range(1, len(asset_values)):
            if portfolio_value.iloc[idx] >= current_peak_value - 1e-12:
                current_peak_value = portfolio_value.iloc[idx]
                current_peak_assets = asset_values.iloc[idx]
            peak_asset_values.iloc[idx] = current_peak_assets
        shortfall = (peak_asset_values - asset_values).clip(lower=0.0)
        total_shortfall = shortfall.sum(axis=1)
        peak_total = peak_asset_values.sum(axis=1)
        shortfall_pct = pd.DataFrame(
            0.0, index=shortfall.index, columns=shortfall.columns
        )
        mask = peak_total > 0
        shortfall_pct.loc[mask] = (
            shortfall.loc[mask].div(peak_total.loc[mask], axis=0) * 100.0
        )
        colors = [
            self._color_for(ticker, color_map, index_master)
            for ticker in shortfall_pct.columns
        ]
        ax.stackplot(
            shortfall_pct.index,
            *[shortfall_pct[col].values for col in shortfall_pct.columns],
            labels=[f"{ticker}" for ticker in shortfall_pct.columns],
            colors=colors,
            alpha=0.85,
        )
        drawdown_pct = (total_shortfall / peak_total).fillna(0.0) * 100.0
        ax.plot(
            drawdown_pct.index,
            drawdown_pct.values,
            color="black",
            linewidth=1.5,
            label="Total Drawdown",
        )
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Drawdown Contribution (%)", fontsize=12)
        ax.set_title(
            "Stacked Drawdown Contributions by Asset", fontsize=14, weight="bold"
        )
        ax.set_ylim(0, max(5, drawdown_pct.max() * 1.1))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0f}%"))
        ax.grid(True, alpha=0.3)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            handles,
            labels,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=10,
            frameon=False,
        )
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
        initial_value = loan_amount / 0.6
        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        start_prices = prices.iloc[0]
        initial_quantities = pd.Series(index=weights_dict.keys(), dtype=float)
        for ticker, weight in weights_dict.items():
            if (
                ticker in start_prices
                and not pd.isna(start_prices[ticker])
                and start_prices[ticker] > 0
            ):
                initial_quantities[ticker] = (initial_value * weight) / start_prices[
                    ticker
                ]
            else:
                initial_quantities[ticker] = 0.0
        valid_tickers = [t for t in initial_quantities.index if t in prices.columns]
        relevant_prices = prices[valid_tickers]
        relevant_quantities = initial_quantities[valid_tickers]
        portfolio_value = relevant_prices.mul(relevant_quantities).sum(axis=1)
        ltv_series = loan_amount / portfolio_value
        ltv_series.index = pd.to_datetime(ltv_series.index, errors="coerce")
        ltv_series = ltv_series[ltv_series.index.notna()]
        ltv_series = ltv_series[~ltv_series.index.duplicated(keep="first")]
        ltv_series = ltv_series.sort_index()
        stress_periods = [
            ("2020_covid_crash", "2020-02-01", "2020-04-30", "COVID-19 Crash"),
            (
                "2022_inflation_shock",
                "2022-01-01",
                "2022-10-31",
                "2022 Inflation Shock",
            ),
        ]
        for idx, (period_key, start, end, label) in enumerate(stress_periods):
            ax = axes[idx]
            period_ltv = ltv_series.loc[start:end]
            if len(period_ltv) > 0:
                ax.plot(
                    period_ltv.index,
                    period_ltv.values * 100,
                    linewidth=2,
                    label="Portfolio LTV",
                    color="blue",
                )
                ax.axhline(
                    y=warning_ratio * 100,
                    color="orange",
                    linestyle="--",
                    linewidth=1.5,
                    label=f"Warning ({warning_ratio * 100:.0f}%)",
                )
                ax.axhline(
                    y=liquidation_ratio * 100,
                    color="red",
                    linestyle="--",
                    linewidth=1.5,
                    label=f"Liquidation ({liquidation_ratio * 100:.0f}%)",
                )
                if (
                    period_key in stress_results
                    and "ltv_breaches" in stress_results[period_key]
                ):
                    breaches = stress_results[period_key]["ltv_breaches"]
                    ax.text(
                        0.02,
                        0.98,
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
                ax.text(
                    0.5,
                    0.5,
                    f"No data for {label}",
                    ha="center",
                    va="center",
                    fontsize=12,
                )
        axes[-1].set_xlabel("Date", fontsize=12)
        plt.tight_layout()
        path = self.graphs_dir / "04_ltv_stress.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _plot_asset_contribution(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        index_master: pd.DataFrame | None = None,
        color_map: Dict | None = None,
    ) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))
        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()
        contribution_df = daily_returns.mul(pd.Series(weights_dict))
        contribution_df = contribution_df[
            [
                col
                for col in self._sort_tickers(contribution_df.columns, index_master)
                if col in contribution_df
            ]
        ]
        monthly_df = contribution_df.resample("M").sum() * 100.0
        colors = [
            self._color_for(ticker, color_map, index_master)
            for ticker in monthly_df.columns
        ]
        ax.axhline(0, color="
        pos_base = np.zeros(len(monthly_df.index))
        neg_base = np.zeros(len(monthly_df.index))
        legend_handles = []
        for ticker, color in zip(monthly_df.columns, colors):
            values = monthly_df[ticker].values
            pos = np.where(values > 0, values, 0)
            neg = np.where(values < 0, values, 0)
            if np.any(pos > 0):
                ax.fill_between(
                    monthly_df.index,
                    pos_base,
                    pos_base + pos,
                    color=color,
                    alpha=0.55,
                )
                pos_base += pos
            if np.any(neg < 0):
                ax.fill_between(
                    monthly_df.index,
                    neg_base,
                    neg_base + neg,
                    color=color,
                    alpha=0.55,
                )
                neg_base += neg
            legend_handles.append(
                plt.Line2D([0], [0], color=color, linewidth=6, label=ticker)
            )
        net_line = monthly_df.sum(axis=1)
        ax.plot(
            monthly_df.index,
            net_line.values,
            color="black",
            linewidth=1.6,
            linestyle="-",
            label="Net",
        )
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Monthly Contribution (%)", fontsize=12)
        ax.set_title(
            "Monthly Asset Contribution (Positive / Negative)",
            fontsize=14,
            weight="bold",
        )
        legend_handles.append(
            plt.Line2D([0], [0], color="black", linewidth=2, label="Net")
        )
        if legend_handles:
            ax.legend(
                handles=legend_handles,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.2),
                ncol=min(4, len(legend_handles)),
                fontsize=9,
                frameon=False,
            )
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_locator(
            mdates.MonthLocator(interval=max(1, len(monthly_df.index) // 12))
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        plt.tight_layout()
        path = self.graphs_dir / "05_asset_contribution.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _plot_risk_return_scatter(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        index_master: pd.DataFrame | None = None,
        reference_portfolios: Dict | None = None,
        color_map: Dict | None = None,
    ) -> Path:
        fig, ax = plt.subplots(figsize=(10, 7))
        daily_returns = prices.pct_change().dropna()
        asset_metrics = []
        for ticker in portfolio["ticker"]:
            if ticker in daily_returns.columns:
                annual_return = daily_returns[ticker].mean() * 252
                annual_vol = daily_returns[ticker].std() * np.sqrt(252)
                asset_metrics.append(
                    {
                        "ticker": ticker,
                        "return": annual_return,
                        "volatility": annual_vol,
                    }
                )
        metrics_df = pd.DataFrame(asset_metrics)
        ticker_list = metrics_df["ticker"].tolist() if not metrics_df.empty else []
        asset_colors = [
            self._color_for(ticker, color_map, index_master) for ticker in ticker_list
        ]
        def compute_portfolio_stats(
            weights: pd.Series,
            label: str,
            annotation: str | None = None,
            style_key: str | None = None,
        ) -> Dict[str, float]:
            weights = weights.reindex(daily_returns.columns).fillna(0.0)
            portfolio_returns = daily_returns.mul(weights, axis=1).sum(axis=1)
            annual_return = portfolio_returns.mean() * 252
            annual_vol = portfolio_returns.std() * np.sqrt(252)
            sharpe = annual_return / annual_vol if annual_vol > 0 else 0
            return {
                "label": label,
                "annotation": annotation or label,
                "style_key": style_key or label,
                "annual_return": annual_return,
                "annual_volatility": annual_vol,
                "sharpe": sharpe,
            }
        if reference_portfolios is None:
            reference_portfolios = {}
        portfolio_points = []
        wf_styles: Dict[str, Dict] = {}
        wf_keys = [key for key in reference_portfolios.keys() if key.startswith("WF
        if wf_keys:
            palette = sns.color_palette("dark", len(wf_keys))
            for idx, (key, color) in enumerate(zip(wf_keys, palette), start=1):
                wf_styles[key] = {
                    "marker": "o",
                    "color": color,
                    "offset": (14, 14 if idx % 2 else -18),
                }
        for key, spec in reference_portfolios.items():
            legend_label = spec.get("legend", f"{key} Portfolio")
            annotation = spec.get("annotation", legend_label)
            style_key = spec.get("style_key", key)
            weights_series = spec["weights"]
            portfolio_points.append(
                compute_portfolio_stats(
                    weights_series,
                    legend_label,
                    annotation=annotation,
                    style_key=style_key,
                )
            )
        if not metrics_df.empty:
            ax.scatter(
                metrics_df["volatility"] * 100,
                metrics_df["return"] * 100,
                s=90,
                alpha=0.6,
                label="Individual Assets",
                c=asset_colors,
                edgecolors="none",
            )
        for _, row in metrics_df.iterrows():
            ax.annotate(
                row["ticker"],
                (row["volatility"] * 100, row["return"] * 100),
                fontsize=9,
                xytext=(5, 5),
                textcoords="offset points",
            )
        style_map = {
            "Optimized": {"marker": "*", "color": "
            "Inverse-Vol": {"marker": "X", "color": "
            "Min Variance": {"marker": "D", "color": "
            "Max Sharpe": {"marker": "^", "color": "
            "Min Volatility": {"marker": ">", "color": "
            "Min Drawdown": {"marker": "<", "color": "
            "Max Kelly": {"marker": "h", "color": "
        }
        style_map.update(wf_styles)
        fallback_markers = ["o", "v", "H", "p", "*"]
        fallback_colors = sns.color_palette("tab10", len(fallback_markers))
        for idx, point in enumerate(portfolio_points):
            style_key = point.get("style_key", point["label"])
            style = style_map.get(style_key, {})
            marker = style.get("marker", fallback_markers[idx % len(fallback_markers)])
            color = style.get("color", fallback_colors[idx % len(fallback_colors)])
            offset = style.get("offset", (10, 10))
            ax.scatter(
                point["annual_volatility"] * 100,
                point["annual_return"] * 100,
                s=320,
                color=color,
                marker=marker,
                label=point["label"],
                edgecolors="
                linewidths=1.2,
                zorder=5 + idx,
                alpha=0.9,
            )
            ax.annotate(
                f"{point['annotation']} (Sharpe {point['sharpe']:.2f})",
                (point["annual_volatility"] * 100, point["annual_return"] * 100),
                fontsize=9,
                xytext=offset,
                textcoords="offset points",
                bbox=dict(
                    boxstyle="round,pad=0.25",
                    facecolor="white",
                    alpha=0.6,
                    edgecolor=color,
                ),
            )
        ax.set_xlabel("Annual Volatility (%)", fontsize=12)
        ax.set_ylabel("Annual Return (%)", fontsize=12)
        ax.set_title("Risk-Return Profile", fontsize=14, weight="bold")
        ax.set_facecolor("
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            handles,
            labels,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=11,
            frameon=False,
        )
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        path = self.graphs_dir / "06_risk_return.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _build_reference_portfolios(
        self,
        prices: pd.DataFrame,
        portfolio: pd.DataFrame,
        index_master: pd.DataFrame | None,
        walk_forward_results: Dict | None,
    ) -> Dict[str, Dict]:
        daily_returns = prices.pct_change().dropna()
        asset_columns = (
            daily_returns.columns if not daily_returns.empty else portfolio["ticker"]
        )
        base_weights = portfolio.set_index("ticker")["weight"]
        portfolios: Dict[str, Dict] = {}
        portfolios["Optimized"] = {
            "weights": base_weights,
            "legend": "Optimized",
            "annotation": "Optimized (Latest)",
            "display": "Optimized (Latest)",
            "axis_label": "Optimized",
            "style_key": "Optimized",
        }
        if index_master is not None and not index_master.empty:
            equity_tickers = index_master[index_master["category"] == "equity"][
                "ticker"
            ].tolist()
            defensive_tickers = [
                ticker
                for ticker in index_master["ticker"]
                if ticker not in equity_tickers
            ]
        else:
            equity_tickers = []
            defensive_tickers = []
        equity_tickers = [t for t in equity_tickers if t in asset_columns]
        defensive_tickers = [t for t in defensive_tickers if t in asset_columns]
        if not daily_returns.empty:
            asset_vol = daily_returns.std()
            inv_vol = 1 / asset_vol.replace(0, np.nan)
            if inv_vol.notna().any():
                inv_vol = inv_vol.fillna(0)
                inv_vol_weight = inv_vol / inv_vol.sum()
                portfolios["Inverse-Vol"] = {
                    "weights": inv_vol_weight,
                    "legend": "Inverse-Vol",
                    "annotation": "Inverse-Vol",
                    "display": "Inverse-Vol",
                    "axis_label": "Inverse-Vol",
                    "style_key": "Inverse-Vol",
                }
            mean_returns = daily_returns.mean()
            cov_matrix = daily_returns.cov()
            min_var_weights = self._solve_mean_variance_weights(
                mean_returns, cov_matrix, objective="min_variance"
            )
            if min_var_weights is not None:
                portfolios["Min Variance"] = {
                    "weights": min_var_weights,
                    "legend": "Min Variance",
                    "annotation": "Min Variance",
                    "display": "Min Variance",
                    "axis_label": "Min Variance",
                    "style_key": "Min Variance",
                }
            max_sharpe_weights = self._solve_mean_variance_weights(
                mean_returns, cov_matrix, objective="max_sharpe"
            )
            if max_sharpe_weights is not None:
                portfolios["Max Sharpe"] = {
                    "weights": max_sharpe_weights,
                    "legend": "Max Sharpe",
                    "annotation": "Max Sharpe",
                    "display": "Max Sharpe",
                    "axis_label": "Max Sharpe",
                    "style_key": "Max Sharpe",
                }
            extreme_candidates = self._random_extreme_portfolios(
                daily_returns, num_samples=5000
            )
            for label, weights in extreme_candidates.items():
                portfolios[label] = {
                    "weights": weights,
                    "legend": label,
                    "annotation": label,
                    "display": label,
                    "axis_label": label,
                    "style_key": label,
                }
        if walk_forward_results:
            wf_entries = walk_forward_results.get("walk_forward_results", [])
            for idx, period in enumerate(wf_entries, start=1):
                weights = pd.Series(period["portfolio_weights"])
                key = f"WF
                annotation = f"WF
                display = f"WF
                axis_label = f"WF
                portfolios[key] = {
                    "weights": weights,
                    "legend": f"WF
                    "annotation": annotation,
                    "display": display,
                    "axis_label": axis_label,
                    "style_key": key,
                }
        return portfolios
    def _solve_mean_variance_weights(
        self,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        objective: str,
    ) -> pd.Series | None:
        if cov_matrix.empty:
            return None
        cov_values = cov_matrix.values
        inv_cov = np.linalg.pinv(cov_values)
        ones = np.ones(len(mean_returns))
        if objective == "min_variance":
            raw = inv_cov @ ones
        elif objective == "max_sharpe":
            raw = inv_cov @ mean_returns.values
        else:
            return None
        raw = np.clip(raw, 0, None)
        if raw.sum() == 0:
            raw = ones
        weights = raw / raw.sum()
        return pd.Series(weights, index=mean_returns.index)
    def _random_extreme_portfolios(
        self,
        daily_returns: pd.DataFrame,
        num_samples: int = 5000,
    ) -> Dict[str, pd.Series]:
        cols = daily_returns.columns
        if len(cols) == 0:
            return {}
        rng = np.random.default_rng(42)
        weight_samples = rng.dirichlet(np.ones(len(cols)), size=num_samples)
        returns_matrix = daily_returns.values @ weight_samples.T
        std_returns = returns_matrix.std(axis=0)
        with np.errstate(divide="ignore", invalid="ignore"):
            log_growth = np.log1p(returns_matrix)
        log_growth_mean = np.nanmean(log_growth, axis=0)
        cumulative = np.cumprod(1 + returns_matrix, axis=0)
        running_max = np.maximum.accumulate(cumulative, axis=0)
        drawdowns = (cumulative - running_max) / running_max
        max_drawdowns = drawdowns.min(axis=0)
        results: Dict[str, pd.Series] = {}
        def add_candidate(idx: int | None, label: str):
            if idx is None:
                return
            weights = pd.Series(weight_samples[idx], index=cols)
            results[label] = weights
        idx_min_vol = (
            np.nanargmin(std_returns) if np.isfinite(std_returns).any() else None
        )
        idx_min_dd = (
            np.nanargmax(max_drawdowns) if np.isfinite(max_drawdowns).any() else None
        )
        idx_max_kelly = (
            np.nanargmax(log_growth_mean)
            if np.isfinite(log_growth_mean).any()
            else None
        )
        add_candidate(idx_min_vol, "Min Volatility")
        add_candidate(idx_min_dd, "Min Drawdown")
        add_candidate(idx_max_kelly, "Max Kelly")
        return results
    def _plot_rolling_sharpe(
        self, prices: pd.DataFrame, portfolio: pd.DataFrame
    ) -> Path:
        fig, ax = plt.subplots(figsize=(14, 7))
        weights_dict = portfolio.set_index("ticker")["weight"].to_dict()
        daily_returns = prices.pct_change().dropna()
        portfolio_returns = daily_returns.apply(
            lambda row: sum(
                weights_dict.get(ticker, 0) * row[ticker] for ticker in row.index
            ),
            axis=1,
        )
        window = 252
        min_periods = max(1, window // 2)
        rolling_mean = (
            portfolio_returns.rolling(window=window, min_periods=min_periods).mean()
            * 252
        )
        rolling_std = portfolio_returns.rolling(
            window=window, min_periods=min_periods
        ).std() * np.sqrt(252)
        rolling_sharpe = rolling_mean / rolling_std.replace(0, np.nan)
        ax.plot(
            rolling_sharpe.index, rolling_sharpe.values, linewidth=2, color="purple"
        )
        ax.axhline(y=0, color="black", linestyle="--", linewidth=1, alpha=0.5)
        ax.axhline(
            y=1,
            color="green",
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label="Sharpe = 1",
        )
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Sharpe Ratio", fontsize=12)
        ax.set_title(
            "Rolling Sharpe Ratio (252-day window)", fontsize=14, weight="bold"
        )
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
        ax.set_title(
            "Asset Return Correlation Matrix", fontsize=14, weight="bold", pad=20
        )
        plt.tight_layout()
        path = self.graphs_dir / "08_correlation.png"
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        return path
    def _resolve_category(
        self, ticker: str, index_master: pd.DataFrame | None = None
    ) -> str:
        if ticker in self.TICKER_CATEGORY_OVERRIDES:
            return self.TICKER_CATEGORY_OVERRIDES[ticker]
        if index_master is not None:
            match = index_master[index_master["ticker"] == ticker]
            if not match.empty:
                base_category = match["category"].iloc[0]
                base_category_map = {
                    "commodity": "gold",
                    "bonds": "bonds",
                    "equity": "em_equity",
                }
                mapped = base_category_map.get(base_category.lower(), None)
                if mapped:
                    return mapped
        return "other"
    def _sort_tickers(
        self,
        tickers: Iterable[str],
        index_master: pd.DataFrame | None = None,
    ) -> List[str]:
        def sort_key(ticker: str):
            category = self._resolve_category(ticker, index_master)
            if category in self.CATEGORY_ORDER:
                order = self.CATEGORY_ORDER.index(category)
            else:
                order = len(self.CATEGORY_ORDER)
            return (order, ticker)
        return sorted(list(tickers), key=sort_key)
    def _build_color_map(
        self,
        tickers: Iterable[str],
        index_master: pd.DataFrame | None = None,
    ) -> Dict[str, tuple]:
        color_map: Dict[str, tuple] = {}
        category_groups: Dict[str, List[str]] = {}
        for ticker in tickers:
            category = self._resolve_category(ticker, index_master)
            category_groups.setdefault(category, []).append(ticker)
        for category, cat_tickers in category_groups.items():
            palette = self._palette_for_category(category, len(cat_tickers))
            for idx, ticker in enumerate(sorted(cat_tickers)):
                color_map[ticker] = palette[idx % len(palette)]
        return color_map
    def _palette_for_category(self, category: str, size: int) -> List[tuple]:
        palette_name = self.CATEGORY_PALETTE_NAMES.get(category, "Greys")
        total_colors = max(size + 4, 5)
        palette = sns.color_palette(palette_name, total_colors)
        if size >= total_colors:
            return palette
        start = max((total_colors - size) // 2, 0)
        end = start + size
        if end > len(palette):
            end = len(palette)
            start = end - size
        return palette[start:end]
    def _color_for(
        self,
        ticker: str,
        color_map: Dict[str, tuple] | None,
        index_master: pd.DataFrame | None = None,
    ) -> tuple:
        if color_map and ticker in color_map:
            return color_map[ticker]
        palette = self._palette_for_category(
            self._resolve_category(ticker, index_master),
            1,
        )
        return palette[0] if palette else self.DEFAULT_COLOR
