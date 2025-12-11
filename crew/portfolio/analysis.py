from typing import Dict

import pandas as pd

from crew.loan import optimizer
from crew.portfolio.config import Index7PortfolioConfig


class Index7PortfolioAnalyzer:
    def __init__(self, config: Index7PortfolioConfig):
        self.config = config

    def evaluate(self, data_payload: Dict) -> Dict:
        prices = data_payload["prices"]
        index_master = data_payload["index_master"]

        if self.config.optimization.enabled:
            base_target = self.config.loan_amount / self.config.ltv_limit

            if self.config.optimization.max_drawdown_buffer > 0:
                safety_factor = 1.0 / (1 - self.config.optimization.max_drawdown_buffer)
                target_value = base_target * safety_factor
            else:
                target_value = base_target

            optimization_result = optimizer.optimize_collateral_portfolio(
                prices=prices,
                etf_master=index_master,
                objective_weights=self.config.optimization.objective_weights,
                constraints=self.config.optimization.constraints,
                sample_size=self.config.optimization.sample_size,
                target_value=target_value,
                max_assets=len(self.config.indices),
                min_assets=len(self.config.indices),
                use_hrp=False,
            )

            portfolio_df = optimization_result["portfolio"]
            if (
                "name" not in portfolio_df.columns
                or "category" not in portfolio_df.columns
            ):
                portfolio_df = portfolio_df.merge(
                    index_master[["ticker", "name", "category"]],
                    on="ticker",
                    how="left",
                )
        else:
            equal_weight = 1.0 / len(self.config.indices)
            portfolio_df = pd.DataFrame(
                {
                    "ticker": [idx.ticker for idx in self.config.indices],
                    "name": [idx.name for idx in self.config.indices],
                    "category": [idx.category for idx in self.config.indices],
                    "weight": [equal_weight] * len(self.config.indices),
                }
            )

        if "allocation_value" in portfolio_df.columns:
            portfolio_value = portfolio_df["allocation_value"].sum()
        else:
            target_value = self.config.loan_amount
            latest_prices = prices.iloc[-1]
            portfolio_value = sum(
                latest_prices[row["ticker"]] * row["weight"] * target_value
                for _, row in portfolio_df.iterrows()
                if row["ticker"] in latest_prices.index
            )

        current_ltv = (
            self.config.loan_amount / portfolio_value
            if portfolio_value > 0
            else float("inf")
        )

        return {
            "portfolio": portfolio_df,
            "prices": prices,
            "index_master": index_master,
            "portfolio_value": portfolio_value,
            "current_ltv": current_ltv,
            "loan_amount": self.config.loan_amount,
            "ltv_limit": self.config.ltv_limit,
            "warning_ratio": self.config.warning_ratio,
            "liquidation_ratio": self.config.liquidation_ratio,
        }
