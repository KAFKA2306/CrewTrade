"""Analysis module for semiconductor stocks."""

from typing import Any, Dict, List
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import SemiconductorsConfig
from .company_profiles import get_company_profile, CompanyProfile


@dataclass
class StockMetrics:
    """Computed metrics for a single stock."""

    symbol: str
    name: str
    current_price: float
    ytd_return: float
    return_3m: float
    return_6m: float
    return_12m: float
    volatility: float  # annualized
    sharpe_ratio: float
    beta_vs_benchmark: float
    max_drawdown: float
    profile: CompanyProfile | None


class SemiconductorsAnalyzer:
    """Analyzer for semiconductor stock performance."""

    RISK_FREE_RATE = 0.045  # ~4.5% risk-free rate

    def __init__(self, config: SemiconductorsConfig, raw_data_dir: Any = None) -> None:
        self.config = config
        self.raw_data_dir = raw_data_dir

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis on price data."""
        price_frames: Dict[str, pd.DataFrame] = data_payload.get("price_frames", {})

        if not price_frames and self.raw_data_dir:
            # Try load from disk
            from pathlib import Path

            raw_path = Path(self.raw_data_dir)
            for symbol in self.config.tickers + [self.config.benchmark]:
                p = raw_path / f"{symbol}.parquet"
                if p.exists():
                    price_frames[symbol] = pd.read_parquet(p)

        if not price_frames:
            return {"error": "No price data available"}

        # Get benchmark data
        benchmark_symbol = self.config.benchmark
        benchmark_frame = price_frames.get(benchmark_symbol)

        stock_metrics: List[StockMetrics] = []
        for symbol in self.config.tickers:
            frame = price_frames.get(symbol)
            if frame is None or frame.empty:
                continue

            metrics = self._calculate_metrics(symbol, frame, benchmark_frame)
            if metrics:
                stock_metrics.append(metrics)

        # Sort by various criteria
        by_return = sorted(stock_metrics, key=lambda x: x.return_12m, reverse=True)
        by_sharpe = sorted(stock_metrics, key=lambda x: x.sharpe_ratio, reverse=True)
        by_volatility = sorted(stock_metrics, key=lambda x: x.volatility)

        # Calculate sector averages
        avg_return_12m = (
            np.mean([m.return_12m for m in stock_metrics]) if stock_metrics else 0
        )
        avg_volatility = (
            np.mean([m.volatility for m in stock_metrics]) if stock_metrics else 0
        )
        avg_sharpe = (
            np.mean([m.sharpe_ratio for m in stock_metrics]) if stock_metrics else 0
        )

        return {
            "stock_metrics": stock_metrics,
            "rankings": {
                "by_return": by_return,
                "by_sharpe": by_sharpe,
                "by_volatility": by_volatility,
            },
            "sector_averages": {
                "return_12m": avg_return_12m,
                "volatility": avg_volatility,
                "sharpe_ratio": avg_sharpe,
            },
            "benchmark_symbol": benchmark_symbol,
            "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d"),
        }

    def _calculate_metrics(
        self,
        symbol: str,
        frame: pd.DataFrame,
        benchmark_frame: pd.DataFrame | None,
    ) -> StockMetrics | None:
        """Calculate metrics for a single stock."""
        try:
            # Use Adj Close if available, otherwise Close
            price_col = "Adj Close" if "Adj Close" in frame.columns else "Close"
            prices = frame[price_col].dropna()

            if len(prices) < 20:
                return None

            current_price = float(prices.iloc[-1])

            # Calculate returns
            returns = prices.pct_change().dropna()

            # Period returns
            ytd_return = self._calculate_ytd_return(prices)
            return_3m = self._calculate_period_return(prices, 63)  # ~3 months
            return_6m = self._calculate_period_return(prices, 126)  # ~6 months
            return_12m = self._calculate_period_return(prices, 252)  # ~12 months

            # Volatility (annualized)
            volatility = float(returns.std() * np.sqrt(252))

            # Sharpe ratio
            excess_return = return_12m - self.RISK_FREE_RATE
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0

            # Beta vs benchmark
            beta = (
                self._calculate_beta(returns, benchmark_frame)
                if benchmark_frame is not None
                else 1.0
            )

            # Max drawdown
            max_drawdown = self._calculate_max_drawdown(prices)

            # Get company profile
            profile = get_company_profile(symbol)

            return StockMetrics(
                symbol=symbol,
                name=profile.name if profile else symbol,
                current_price=current_price,
                ytd_return=ytd_return,
                return_3m=return_3m,
                return_6m=return_6m,
                return_12m=return_12m,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                beta_vs_benchmark=beta,
                max_drawdown=max_drawdown,
                profile=profile,
            )
        except Exception:
            return None

    def _calculate_period_return(self, prices: pd.Series, days: int) -> float:
        """Calculate return over a specified number of trading days."""
        if len(prices) < days:
            days = len(prices)
        start_price = float(prices.iloc[-days])
        end_price = float(prices.iloc[-1])
        return (end_price - start_price) / start_price if start_price > 0 else 0

    def _calculate_ytd_return(self, prices: pd.Series) -> float:
        """Calculate year-to-date return."""
        current_year = pd.Timestamp.now().year
        ytd_prices = prices[prices.index.year == current_year]
        if len(ytd_prices) < 2:
            return 0.0
        start_price = float(ytd_prices.iloc[0])
        end_price = float(ytd_prices.iloc[-1])
        return (end_price - start_price) / start_price if start_price > 0 else 0

    def _calculate_beta(
        self, stock_returns: pd.Series, benchmark_frame: pd.DataFrame
    ) -> float:
        """Calculate beta relative to benchmark."""
        try:
            price_col = (
                "Adj Close" if "Adj Close" in benchmark_frame.columns else "Close"
            )
            benchmark_prices = benchmark_frame[price_col].dropna()
            benchmark_returns = benchmark_prices.pct_change().dropna()

            # Align dates
            aligned = pd.concat([stock_returns, benchmark_returns], axis=1).dropna()
            if len(aligned) < 20:
                return 1.0

            stock_ret = aligned.iloc[:, 0]
            bench_ret = aligned.iloc[:, 1]

            covariance = np.cov(stock_ret, bench_ret)[0, 1]
            variance = np.var(bench_ret)
            return covariance / variance if variance > 0 else 1.0
        except Exception:
            return 1.0

    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate maximum drawdown."""
        cummax = prices.cummax()
        drawdown = (prices - cummax) / cummax
        return float(drawdown.min())


if __name__ == "__main__":
    # Standalone analysis runner
    from crew.use_case_runner import build_config, build_paths

    config = build_config("semiconductors", "config/use_cases/semiconductors.yaml")
    paths = build_paths("semiconductors")

    from .semiconductors_case import SemiconductorsUseCase

    use_case = SemiconductorsUseCase(config, paths)
    result = use_case.run()
    print("Analysis complete.")
