from typing import Dict

import pandas as pd

from ai_trading_crew.use_cases.index_7_portfolio.config import Index7PortfolioConfig
from ai_trading_crew.use_cases.securities_collateral_loan import optimizer


class Index7PortfolioAnalyzer:
    def __init__(self, config: Index7PortfolioConfig):
        self.config = config

    def evaluate(self, data_payload: Dict) -> Dict:
        prices = data_payload["prices"]
        index_master = data_payload["index_master"]

        if self.config.optimization.enabled:
            optimization_result = optimizer.optimize_collateral_portfolio(
                prices=prices,
                etf_master=index_master,
                objective_weights=self.config.optimization.objective_weights,
                constraints=self.config.optimization.constraints,
                sample_size=self.config.optimization.sample_size,
                target_value=(self.config.loan_amount / self.config.ltv_limit) * 1.10,
                max_assets=len(self.config.indices),
                min_assets=len(self.config.indices),
                use_hrp=False,
            )

            portfolio_df = optimization_result["portfolio"]
            if "name" not in portfolio_df.columns or "category" not in portfolio_df.columns:
                portfolio_df = portfolio_df.merge(
                    index_master[["ticker", "name", "category"]], on="ticker", how="left"
                )
        else:
            equal_weight = 1.0 / len(self.config.indices)
            portfolio_df = pd.DataFrame({
                "ticker": [idx.ticker for idx in self.config.indices],
                "name": [idx.name for idx in self.config.indices],
                "category": [idx.category for idx in self.config.indices],
                "weight": [equal_weight] * len(self.config.indices),
            })

        latest_prices = prices.iloc[-1]
        portfolio_value = sum(
            latest_prices[row["ticker"]] * row["weight"] * 10_000_000
            for _, row in portfolio_df.iterrows()
            if row["ticker"] in latest_prices.index
        )

        current_ltv = self.config.loan_amount / portfolio_value if portfolio_value > 0 else float("inf")

        return {
            "portfolio": portfolio_df,
            "prices": prices,
            "portfolio_value": portfolio_value,
            "current_ltv": current_ltv,
            "loan_amount": self.config.loan_amount,
            "ltv_limit": self.config.ltv_limit,
            "warning_ratio": self.config.warning_ratio,
            "liquidation_ratio": self.config.liquidation_ratio,
        }
