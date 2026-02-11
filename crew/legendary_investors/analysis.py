"""Analysis module for legendary investors portfolios."""
from dataclasses import dataclass
from typing import Any, Dict, List
import numpy as np
import pandas as pd
from .config import LegendaryInvestorsConfig
from .deep_research import LegendaryInvestorsResearcher
@dataclass
class HoldingMetrics:
    symbol: str
    current_price: float
    return_1m: float
    return_3m: float
    return_6m: float
    return_12m: float
    ytd_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    fundamentals: str = ""
    news_summary: str = ""
    reason_why: str = ""
    evaluation: str = ""
    rumor: str = ""
    earnings: str = ""
    alpha: str = ""
class LegendaryInvestorsAnalyzer:
    """Analyzer for legendary investors' top holdings."""
    RISK_FREE_RATE = 0.045
    def __init__(
        self, config: LegendaryInvestorsConfig, raw_data_dir: Any = None
    ) -> None:
        self.config = config
        self.researcher = LegendaryInvestorsResearcher()
        self.raw_data_dir = raw_data_dir
    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        price_frames = data_payload.get("price_frames", {})
        if not price_frames and self.raw_data_dir:
            from pathlib import Path
            raw = Path(self.raw_data_dir)
            tickers = list(
                set(
                    self.config.soros_holdings
                    + self.config.druckenmiller_holdings
                    + [self.config.benchmark]
                )
            )
            for t in tickers:
                p = raw / f"{t}.parquet"
                if p.exists():
                    price_frames[t] = pd.read_parquet(p)
        if not price_frames:
            return {"error": "No price data available"}
        soros_metrics = self._analyze_portfolio(
            self.config.soros_holdings, price_frames
        )
        druckenmiller_metrics = self._analyze_portfolio(
            self.config.druckenmiller_holdings, price_frames
        )
        return {
            "soros_metrics": soros_metrics,
            "druckenmiller_metrics": druckenmiller_metrics,
            "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d"),
        }
    def _analyze_portfolio(
        self, tickers: List[str], frames: Dict[str, pd.DataFrame]
    ) -> List[HoldingMetrics]:
        metrics_list = []
        for ticker in tickers:
            df = frames.get(ticker)
            if df is None or df.empty:
                continue
            col = "Adj Close" if "Adj Close" in df.columns else "Close"
            prices = df[col].dropna()
            if len(prices) < 20:
                continue
            current_price = float(prices.iloc[-1])
            ret_1m = self._calc_period_return(prices, 21)
            ret_3m = self._calc_period_return(prices, 63)
            ret_6m = self._calc_period_return(prices, 126)
            ret_12m = self._calc_period_return(prices, 252)
            ytd = self._calc_ytd_return(prices)
            returns = prices.pct_change().dropna()
            vol = float(returns.std() * np.sqrt(252))
            excess_return = ret_12m - self.RISK_FREE_RATE
            sharpe = excess_return / vol if vol > 0 else 0.0
            cummax = prices.cummax()
            drawdown = (prices - cummax) / cummax
            max_dd = float(drawdown.min())
            research_data = self.researcher.get_research_for_ticker(ticker)
            metrics_list.append(
                HoldingMetrics(
                    symbol=ticker,
                    current_price=current_price,
                    return_1m=ret_1m,
                    return_3m=ret_3m,
                    return_6m=ret_6m,
                    return_12m=ret_12m,
                    ytd_return=ytd,
                    volatility=vol,
                    sharpe_ratio=sharpe,
                    max_drawdown=max_dd,
                    fundamentals=research_data.get("fundamentals", ""),
                    news_summary=research_data.get("news_summary", ""),
                    reason_why=research_data.get("reason_why", ""),
                    evaluation=research_data.get("evaluation", ""),
                    rumor=research_data.get("rumor", ""),
                    earnings=research_data.get("earnings", ""),
                    alpha=research_data.get("alpha", ""),
                )
            )
        metrics_list.sort(key=lambda x: x.return_12m, reverse=True)
        return metrics_list
    def _calc_period_return(self, prices: pd.Series, days: int) -> float:
        if len(prices) < days:
            days = len(prices)
        start = float(prices.iloc[-days])
        end = float(prices.iloc[-1])
        return (end - start) / start if start > 0 else 0.0
    def _calc_ytd_return(self, prices: pd.Series) -> float:
        current_year = pd.Timestamp.now().year
        ytd = prices[prices.index.year == current_year]
        if len(ytd) < 2:
            return 0.0
        start = float(ytd.iloc[0])
        end = float(ytd.iloc[-1])
        return (end - start) / start if start > 0 else 0.0
