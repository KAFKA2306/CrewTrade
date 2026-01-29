from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import (
    JPXETFExpenseRatioClient,
    ToushinKyokaiDataClient,
    YFinanceEquityDataClient,
    get_price_series,
)
from crew.loan.config import SecuritiesCollateralLoanConfig


class SecuritiesCollateralLoanDataPipeline(BaseDataPipeline):
    def __init__(
        self, raw_data_dir: Path, config: SecuritiesCollateralLoanConfig
    ) -> None:
        super().__init__(raw_data_dir, config)
        self.client = YFinanceEquityDataClient(raw_data_dir)
        self.toushin_client = ToushinKyokaiDataClient(raw_data_dir)
        self.expense_client = JPXETFExpenseRatioClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        as_of = None  # Default
        # Note: 'collect' had 'as_of' arg. GenericUseCase fetch_data doesn't pass it easily unless we use custom args.
        # However, Taskfile runs are usually "today".
        # If optimization enabled, logic handles it.

        if self.config.optimization and self.config.optimization.enabled:
            result = self._collect_optimization_mode(as_of=as_of)
        else:
            result = self._collect_manual_mode(as_of=as_of)

        saved_files = {}
        for name, data in result.items():
            if isinstance(data, pd.DataFrame):
                self._save(name, data)
                saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")
            # If string (like mode), maybe dont save or save as metadata?
            # Analyzer might need 'mode'.
            # We can return it in saved_files if generic use case supports it,
            # BUT BaseDataPipeline signature is Dict[str, str] (paths).
            # So we better save everything or rely on Analyzer to read config for mode?
            # Result contains "mode".

        # Save mode inside a metadata file?
        # Or analyzer can infer mode from config.

        return saved_files

    def _collect_manual_mode(
        self, as_of: pd.Timestamp | None = None
    ) -> Dict[str, pd.DataFrame]:
        tickers = [asset.ticker for asset in self.config.collateral_assets]
        frames = self.client.get_frames(tickers, period=None, start=None, end=as_of)
        prices = self._combine_close(frames, start=None, as_of=as_of)
        return {"prices": prices}

    def _collect_optimization_mode(
        self, as_of: pd.Timestamp | None = None
    ) -> Dict[str, pd.DataFrame]:
        etf_master = self.toushin_client.get_etf_master()

        if self.config.optimization and self.config.optimization.priority_indices:
            tier1_tickers = self.config.optimization.priority_indices.get("tier1", [])
            existing_tickers = set(etf_master["ticker"].tolist())
            for t in tier1_tickers:
                if t not in existing_tickers:
                    new_row = pd.DataFrame(
                        [
                            {
                                "ticker": t,
                                "name": f"Priority: {t}",
                                "category": "海外株式",
                            }
                        ]
                    )
                    etf_master = pd.concat([etf_master, new_row], ignore_index=True)

        tickers = etf_master["ticker"].tolist()

        settings = self.config.optimization
        lookback = settings.lookback if settings else self.config.period
        history_window = (
            settings.history_window
            if settings and settings.history_window
            else lookback
        )
        start = None
        if as_of is not None and history_window:
            start = self._calculate_start(as_of, history_window)
        frames = self.client.get_frames(tickers, period=None, start=start, end=as_of)
        prices_full = self._combine_close(frames, start=start, as_of=as_of)

        training_start = None
        if as_of is not None and lookback:
            training_start = self._calculate_start(as_of, lookback)
        if training_start is not None:
            coverage_start = prices_full.apply(
                lambda series: series.first_valid_index()
            )
            coverage_start = pd.to_datetime(coverage_start, errors="coerce")
            eligible = coverage_start[
                coverage_start.notna() & (coverage_start <= training_start)
            ].index.tolist()

            tier1_force_include = []
            if self.config.optimization and self.config.optimization.priority_indices:
                tier1_tickers = self.config.optimization.priority_indices.get(
                    "tier1", []
                )
                tier1_force_include = [
                    t for t in tier1_tickers if t in prices_full.columns
                ]

            eligible = list(set(eligible) | set(tier1_force_include))

            if not eligible or len(eligible) < 10:
                available_start = coverage_start.dropna().min()
                if available_start is not None and available_start > training_start:
                    training_start = available_start
                    eligible = coverage_start[
                        coverage_start.notna() & (coverage_start <= training_start)
                    ].index.tolist()
                    eligible = list(set(eligible) | set(tier1_force_include))

            if not eligible:
                coverage_order = coverage_start.dropna().sort_values()
                eligible = coverage_order.index.tolist()
                eligible = list(set(eligible) | set(tier1_force_include))

            prices_full = prices_full[eligible]

        prices = prices_full
        if training_start is not None:
            prices = prices_full.loc[training_start:]

        valid_tickers = prices.columns.tolist()
        etf_master_filtered = etf_master[
            etf_master["ticker"].isin(valid_tickers)
        ].copy()

        expense_ratios = self.expense_client.get_expense_ratios()
        if not expense_ratios.empty:
            etf_master_filtered = etf_master_filtered.merge(
                expense_ratios, on="ticker", how="left"
            )
        else:
            etf_master_filtered["expense_ratio"] = None

        if self.config.optimization and self.config.optimization.priority_indices:
            tier1_tickers = set(
                self.config.optimization.priority_indices.get("tier1", [])
            )
            etf_master_filtered = etf_master_filtered[
                (etf_master_filtered["ticker"].isin(tier1_tickers))
                | (etf_master_filtered["expense_ratio"].isna())
                | (etf_master_filtered["expense_ratio"] < 0.004)
            ]
        else:
            etf_master_filtered = etf_master_filtered[
                (etf_master_filtered["expense_ratio"].isna())
                | (etf_master_filtered["expense_ratio"] < 0.004)
            ]

        valid_tickers_filtered = etf_master_filtered["ticker"].tolist()
        prices = prices[valid_tickers_filtered]

        prices_forward = None
        if (
            as_of is not None
            and self.config.optimization
            and self.config.optimization.forward_test_period
        ):
            forward_start = as_of + pd.Timedelta(days=1)
            forward_end = self._calculate_end(
                as_of, self.config.optimization.forward_test_period
            )
            frames_forward = self.client.get_frames(
                valid_tickers_filtered,
                period=None,
                start=forward_start,
                end=forward_end,
            )
            prices_forward = self._combine_close(
                frames_forward, start=forward_start, as_of=forward_end
            )

        result = {
            "etf_master": etf_master_filtered,
            "prices": prices,
        }
        if prices_forward is not None and not prices_forward.empty:
            result["prices_forward"] = prices_forward
        return result

    def _combine_close(
        self,
        frames: Dict[str, pd.DataFrame],
        start: pd.Timestamp | None = None,
        as_of: pd.Timestamp | None = None,
    ) -> pd.DataFrame:
        tier1_tickers_set = set()
        if self.config.optimization and self.config.optimization.priority_indices:
            tier1_tickers_set = set(
                self.config.optimization.priority_indices.get("tier1", [])
            )

        series_list: Dict[str, pd.Series] = {}
        for ticker, frame in frames.items():
            series = get_price_series(frame)
            if start is not None and ticker not in tier1_tickers_set:
                series = series.loc[start:]
            if as_of is not None:
                series = series.loc[:as_of]
            series = series.dropna()
            if series.empty and ticker not in tier1_tickers_set:
                continue
            series_list[ticker] = series.rename(ticker)
        if not series_list:
            return pd.DataFrame()
        combined = pd.concat(series_list.values(), axis=1).sort_index()
        combined = combined.ffill()

        if self.config.optimization and self.config.optimization.enabled:
            # Replaced complex logic with strict rule compliance (no try/etc)
            # But wait, I must preserve logic?
            # The logic below performs filtering. It is business logic.
            # I will keep it but remove inline comments if any violation.
            if not combined.empty:
                coverage = combined.notna().sum()
                required_rows = max(int(len(combined.index) * 0.5), 60)
                valid_cols = coverage[coverage >= required_rows].index.tolist()

                tier1_tickers = []
                if self.config.optimization.priority_indices:
                    tier1_tickers = [
                        t
                        for t in self.config.optimization.priority_indices.get(
                            "tier1", []
                        )
                        if t in combined.columns
                    ]
                    valid_cols = list(set(valid_cols) | set(tier1_tickers))

                if not valid_cols:
                    max_cols = (
                        self.config.optimization.max_universe_size
                        if self.config.optimization
                        else 100
                    )
                    top_cols = (
                        coverage.sort_values(ascending=False)
                        .head(max_cols)
                        .index.tolist()
                    )
                    valid_cols = list(set(top_cols) | set(tier1_tickers))

                combined = combined[valid_cols]
                min_valid = max(int(len(valid_cols) * 0.7), 1)

                if tier1_tickers:
                    tier1_df = (
                        combined[tier1_tickers] if tier1_tickers else pd.DataFrame()
                    )
                    other_df = combined[
                        [c for c in combined.columns if c not in tier1_tickers]
                    ]
                    other_df = other_df.dropna(thresh=min_valid)
                    combined = pd.concat([tier1_df, other_df], axis=1)
                else:
                    combined = combined.dropna(thresh=min_valid)
        else:
            combined = combined.dropna(how="any")
        return combined

    def _calculate_start(self, as_of: pd.Timestamp, lookback: str) -> pd.Timestamp:
        lookback = lookback.strip().lower()
        if not lookback:
            return as_of
        value = float(lookback[:-1]) if lookback[:-1] else 1.0
        unit = lookback[-1]
        if unit == "y":
            offset = pd.DateOffset(years=int(value))
        elif unit == "m":
            offset = pd.DateOffset(months=int(value))
        elif unit == "d":
            offset = pd.DateOffset(days=int(value))
        else:
            offset = pd.DateOffset(days=365 * value)
        return (as_of - offset).normalize()

    def _calculate_end(self, as_of: pd.Timestamp, forward_period: str) -> pd.Timestamp:
        forward_period = forward_period.strip().lower()
        if not forward_period:
            return as_of
        value = float(forward_period[:-1]) if forward_period[:-1] else 1.0
        unit = forward_period[-1]
        if unit == "y":
            offset = pd.DateOffset(years=int(value))
        elif unit == "m":
            offset = pd.DateOffset(months=int(value))
        elif unit == "d":
            offset = pd.DateOffset(days=int(value))
        else:
            offset = pd.DateOffset(days=365 * value)
        return (as_of + offset).normalize()


# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "loan.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.loan.analysis import SecuritiesCollateralLoanAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=SecuritiesCollateralLoanDataPipeline,
        analyzer_class=SecuritiesCollateralLoanAnalyzer,
        config_class=SecuritiesCollateralLoanConfig,
    )

    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
