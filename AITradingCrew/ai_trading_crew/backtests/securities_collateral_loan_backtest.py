from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from ai_trading_crew.use_case_runner import build_config
from ai_trading_crew.use_cases.base import UseCasePaths
from ai_trading_crew.use_cases.securities_collateral_loan.analysis import (
    SecuritiesCollateralLoanAnalyzer,
)
from ai_trading_crew.use_cases.securities_collateral_loan.config import PortfolioMetadata
from ai_trading_crew.use_cases.securities_collateral_loan.data_pipeline import (
    SecuritiesCollateralLoanDataPipeline,
)
from ai_trading_crew.use_cases.securities_collateral_loan.reporting import (
    SecuritiesCollateralLoanReporter,
)


@dataclass
class BacktestResult:
    anchor_date: pd.Timestamp
    report_path: Path | None = None


class SecuritiesCollateralLoanBacktester:
    def __init__(
        self,
        config,
        raw_data_dir: Path,
        processed_base_dir: Path,
        report_base_dir: Path,
    ) -> None:
        self.config = config
        self.raw_data_dir = raw_data_dir
        self.processed_base_dir = processed_base_dir
        self.report_base_dir = report_base_dir
        self.processed_base_dir.mkdir(parents=True, exist_ok=True)
        self.report_base_dir.mkdir(parents=True, exist_ok=True)

    def run(self, anchors: List[pd.Timestamp] | None = None) -> List[BacktestResult]:
        results: List[BacktestResult] = []

        if anchors is None:
            settings = getattr(self.config, "optimization", None)
            years = None
            if settings and settings.walkforward_years:
                years = settings.walkforward_years
            if years is None:
                years = 1
            anchors = build_anchor_dates(years)

        for year_index, anchor in enumerate(anchors):
            config_snapshot = self.config.model_copy(deep=True)
            processed_dir = self.processed_base_dir / anchor.strftime("%Y%m%d")
            report_dir = self.report_base_dir / anchor.strftime("%Y%m%d")
            processed_dir.mkdir(parents=True, exist_ok=True)
            report_dir.mkdir(parents=True, exist_ok=True)

            pipeline = SecuritiesCollateralLoanDataPipeline(config_snapshot, self.raw_data_dir)
            analyzer = SecuritiesCollateralLoanAnalyzer(config_snapshot)
            reporter = SecuritiesCollateralLoanReporter(config_snapshot, processed_dir, report_dir)

            data_payload = pipeline.collect(as_of=anchor)

            prev_portfolio, prev_metadata = self._load_previous_portfolio(anchor)
            data_payload['previous_portfolio'] = prev_portfolio
            data_payload['previous_metadata'] = prev_metadata
            data_payload['year_index'] = year_index
            prices = data_payload.get("prices")
            if prices is None or prices.empty:
                continue

            try:
                analysis_payload = analyzer.evaluate(data_payload)
            except Exception:
                continue

            forward_test = self._compute_forward_test(anchor, analysis_payload, pipeline)
            if forward_test is not None:
                analysis_payload["forward_test"] = forward_test

            report_payload = reporter.persist(analysis_payload)
            results.append(BacktestResult(anchor, report_payload.get("report")))

        return results

    def _compute_forward_test(self, anchor: pd.Timestamp, analysis_payload: dict, pipeline: SecuritiesCollateralLoanDataPipeline) -> dict | None:
        optimized_portfolio = analysis_payload.get("optimized_portfolio")
        if optimized_portfolio is None or optimized_portfolio.empty:
            return None

        tickers = optimized_portfolio["ticker"].tolist()
        frames_forward = pipeline.client.get_frames(tickers, start=anchor, end=None)
        forward_prices = pipeline._combine_close(frames_forward, as_of=None)
        if forward_prices.empty:
            return None
        forward_prices = forward_prices.loc[forward_prices.index >= anchor]
        if forward_prices.empty:
            return None

        settings = pipeline.config.optimization
        if settings and settings.forward_test_period:
            end_limit = pipeline._calculate_end(anchor, settings.forward_test_period)
            forward_prices = forward_prices.loc[:end_limit]
            if forward_prices.empty:
                return None

        quantities = optimized_portfolio.set_index("ticker")["quantity"]
        aligned_prices = forward_prices[tickers].dropna(how="all")
        if aligned_prices.empty:
            return None

        portfolio_values = aligned_prices.mul(quantities, axis=1).sum(axis=1).dropna()
        if portfolio_values.empty:
            return None

        returns = portfolio_values / portfolio_values.iloc[0] - 1.0
        rolling_peak = portfolio_values.cummax()
        drawdown = portfolio_values / rolling_peak - 1.0

        start_value = float(portfolio_values.iloc[0])
        end_value = float(portfolio_values.iloc[-1])
        days = max((portfolio_values.index[-1] - portfolio_values.index[0]).days, 1)
        annualized_return = (end_value / start_value) ** (365 / days) - 1.0 if start_value > 0 else None
        daily_returns = portfolio_values.pct_change().dropna()
        annualized_vol = float(daily_returns.std() * (252 ** 0.5)) if not daily_returns.empty else None
        cumulative_return = float(end_value / start_value - 1.0)
        max_drawdown = float(drawdown.min())

        series = pd.DataFrame(
            {
                "portfolio_value": portfolio_values,
                "cumulative_return": returns,
                "drawdown": drawdown,
            }
        )

        summary = {
            "start": portfolio_values.index[0],
            "end": portfolio_values.index[-1],
            "start_value": start_value,
            "end_value": end_value,
            "cumulative_return": cumulative_return,
            "annualized_return": annualized_return,
            "annualized_volatility": annualized_vol,
            "max_drawdown": max_drawdown,
        }

        return {
            "anchor_date": anchor,
            "series": series,
            "summary": summary,
        }

    def _load_previous_portfolio(self, anchor: pd.Timestamp) -> Tuple[pd.DataFrame | None, PortfolioMetadata | None]:
        prev_year = anchor.year - 1
        prev_anchor = pd.Timestamp(year=prev_year, month=anchor.month, day=anchor.day)

        prev_dir = self.processed_base_dir / prev_anchor.strftime("%Y%m%d")
        portfolio_path = prev_dir / "optimized_portfolio.parquet"
        metadata_path = prev_dir / "portfolio_metadata.json"

        if not portfolio_path.exists():
            return None, None

        portfolio = pd.read_parquet(portfolio_path)
        metadata = None
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata_dict = json.load(f)
                metadata = PortfolioMetadata(**metadata_dict)

        return portfolio, metadata


def build_anchor_dates(years: int, reference_date: datetime | None = None) -> List[pd.Timestamp]:
    if reference_date is None:
        reference_date = datetime.utcnow()
    anchors: List[pd.Timestamp] = []
    for year_offset in range(years):
        year = reference_date.year - year_offset
        anchor = pd.Timestamp(year=year, month=5, day=31)
        if anchor > pd.Timestamp(reference_date):
            continue
        anchors.append(anchor)
    return sorted(anchors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Use case name", default="securities_collateral_loan")
    parser.add_argument("--config", dest="config_path")
    parser.add_argument("--years", dest="years", type=int)
    args = parser.parse_args()

    config = build_config(args.name, args.config_path)
    base_data_dir_local = Path("resources") / "data" / "use_cases" / args.name
    base_data_dir_repo = Path(__file__).resolve().parent.parent / "resources" / "data" / "use_cases" / args.name
    local_raw = base_data_dir_local / "raw"
    repo_raw = base_data_dir_repo / "raw"
    local_ready = local_raw.exists() and any(local_raw.iterdir())
    repo_ready = repo_raw.exists() and any(repo_raw.iterdir())
    if repo_ready:
        base_data_dir = base_data_dir_repo
    elif local_ready:
        base_data_dir = base_data_dir_local
    else:
        base_data_dir = base_data_dir_local if base_data_dir_local.exists() else base_data_dir_repo
    raw_data_dir = base_data_dir / "raw"
    processed_base_dir = base_data_dir / "processed_backtests"
    report_base_dir = Path("output") / "backtests" / args.name

    backtester = SecuritiesCollateralLoanBacktester(
        config=config,
        raw_data_dir=raw_data_dir,
        processed_base_dir=processed_base_dir,
        report_base_dir=report_base_dir,
    )

    anchors = build_anchor_dates(args.years) if args.years else None
    backtester.run(anchors)


if __name__ == "__main__":
    main()
