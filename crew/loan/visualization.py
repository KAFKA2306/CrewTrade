from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter


class SecuritiesCollateralLoanVisualizer:
    """Generate quick-look charts for the collateral loan report."""

    def __init__(self, output_dir: Path) -> None:
        self.graphs_dir = output_dir / "graphs"
        self.graphs_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_charts(
        self,
        asset_breakdown: pd.DataFrame | None,
        loan_ratio_series: pd.Series | pd.DataFrame | None,
        scenarios: Iterable[dict] | pd.DataFrame | None,
        portfolio_value: pd.Series | pd.DataFrame | None,
        *,
        ltv_limit: float,
        warning_ratio: float,
        liquidation_ratio: float,
    ) -> Dict[str, Path]:
        chart_paths: Dict[str, Path] = {}

        if isinstance(asset_breakdown, pd.DataFrame) and not asset_breakdown.empty:
            try:
                chart_paths["allocation"] = self._plot_collateral_allocation(
                    asset_breakdown
                )
            except Exception:
                pass

        loan_ratio = self._coerce_series(loan_ratio_series)
        if loan_ratio is not None and not loan_ratio.empty:
            try:
                chart_paths["loan_ratio"] = self._plot_loan_ratio(
                    loan_ratio,
                    ltv_limit=ltv_limit,
                    warning_ratio=warning_ratio,
                    liquidation_ratio=liquidation_ratio,
                )
            except Exception:
                pass

        scenario_df = self._coerce_frame(scenarios)
        if scenario_df is not None and not scenario_df.empty:
            try:
                chart_paths["scenarios"] = self._plot_stress_scenarios(
                    scenario_df,
                    warning_ratio=warning_ratio,
                    liquidation_ratio=liquidation_ratio,
                )
            except Exception:
                pass

        portfolio_series = self._coerce_series(portfolio_value)
        if portfolio_series is not None and not portfolio_series.empty:
            try:
                chart_paths["portfolio_value"] = self._plot_portfolio_value(
                    portfolio_series
                )
            except Exception:
                pass

        return chart_paths

    def _plot_collateral_allocation(self, asset_breakdown: pd.DataFrame) -> Path:
        df = asset_breakdown.copy()
        if "weight" not in df.columns and "market_value" in df.columns:
            total = df["market_value"].sum()
            df["weight"] = df["market_value"] / total if total else 0

        df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["weight"])
        df = df.sort_values("weight", ascending=False).head(15)

        fig, ax = plt.subplots(figsize=(9, 6))
        ax.barh(df["ticker"], df["weight"] * 100, color="#1f77b4")
        ax.invert_yaxis()
        ax.set_xlabel("Portfolio Weight (%)")
        ax.set_title("Top Collateral Holdings")

        for idx, (ticker, weight) in enumerate(zip(df["ticker"], df["weight"])):
            ax.text(
                weight * 100 + 0.5, idx, f"{weight * 100:.1f}%", va="center", fontsize=9
            )

        fig.tight_layout()
        path = self.graphs_dir / "01_collateral_allocation.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        return path

    def _plot_loan_ratio(
        self,
        series: pd.Series,
        *,
        ltv_limit: float,
        warning_ratio: float,
        liquidation_ratio: float,
    ) -> Path:
        data = series.replace([np.inf, -np.inf], np.nan).dropna()
        if data.empty:
            raise ValueError("Loan ratio data empty after filtering")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            data.index, data.values, color="#005f99", linewidth=1.6, label="Loan Ratio"
        )

        threshold_specs = [
            (ltv_limit, "LTV Limit", "#2ca02c"),
            (warning_ratio, "Margin Call", "#ff7f0e"),
            (liquidation_ratio, "Liquidation", "#d62728"),
        ]

        for value, label, color in threshold_specs:
            ax.axhline(value, color=color, linestyle="--", linewidth=1.1, label=label)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y * 100:.0f}%"))
        ax.set_ylim(0, max(liquidation_ratio * 1.2, data.max() * 1.1))
        ax.set_ylabel("Loan-to-Value Ratio")
        ax.set_title("Loan Ratio History")
        ax.legend(loc="upper right", frameon=False)
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )
        fig.autofmt_xdate()

        fig.tight_layout()
        path = self.graphs_dir / "02_loan_ratio_history.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        return path

    def _plot_stress_scenarios(
        self,
        scenarios: pd.DataFrame,
        *,
        warning_ratio: float,
        liquidation_ratio: float,
    ) -> Path:
        needed_cols = {"label", "loan_ratio"}
        if not needed_cols.issubset(scenarios.columns):
            raise ValueError("Scenario data missing required columns")

        df = scenarios.copy()
        df = df.sort_values("loan_ratio", ascending=True)

        colors = []
        for value in df["loan_ratio"]:
            if value >= liquidation_ratio:
                colors.append("#d62728")
            elif value >= warning_ratio:
                colors.append("#ff7f0e")
            else:
                colors.append("#2ca02c")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df["label"], df["loan_ratio"] * 100, color=colors)
        ax.axhline(
            warning_ratio * 100,
            color="#ff7f0e",
            linestyle="--",
            linewidth=1.1,
            label="Margin Call",
        )
        ax.axhline(
            liquidation_ratio * 100,
            color="#d62728",
            linestyle="--",
            linewidth=1.1,
            label="Liquidation",
        )
        ax.set_ylabel("Loan Ratio (%)")
        ax.set_title("Stress Scenario Loan Ratios")
        ax.legend(frameon=False)

        for idx, value in enumerate(df["loan_ratio"]):
            ax.text(
                idx, value * 100 + 1.5, f"{value * 100:.1f}%", ha="center", fontsize=9
            )

        fig.tight_layout()
        path = self.graphs_dir / "03_stress_scenarios.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        return path

    def _plot_portfolio_value(self, series: pd.Series) -> Path:
        data = series.replace([np.inf, -np.inf], np.nan).dropna()
        if data.empty:
            raise ValueError("Portfolio value series empty")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data.values / 1_000_000, color="#1f77b4", linewidth=1.6)
        ax.set_ylabel("Value (Millions of ¥)")
        ax.set_title("Portfolio Value History")
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )
        fig.autofmt_xdate()
        fig.tight_layout()

        path = self.graphs_dir / "04_portfolio_value.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        return path

    @staticmethod
    def _coerce_series(data: pd.Series | pd.DataFrame | None) -> pd.Series | None:
        if data is None:
            return None
        if isinstance(data, pd.Series):
            return data.sort_index()
        if isinstance(data, pd.DataFrame) and not data.empty:
            if data.shape[1] == 1:
                return data.iloc[:, 0].sort_index()
            if "value" in data.columns:
                return data["value"].sort_index()
        return None

    @staticmethod
    def _coerce_frame(
        data: Iterable[dict] | pd.DataFrame | None,
    ) -> pd.DataFrame | None:
        if data is None:
            return None
        if isinstance(data, pd.DataFrame):
            return data
        try:
            df = pd.DataFrame(list(data))
            return df
        except Exception:
            return None
