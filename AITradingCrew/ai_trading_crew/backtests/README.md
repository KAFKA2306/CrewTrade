# Securities Collateral Loan Backtest

This directory contains the backtesting script for the securities collateral loan use case.

## Function

The `securities_collateral_loan_backtest.py` script runs a historical backtest for the securities collateral loan strategy. It iterates through a series of anchor dates, and for each date, it performs the following steps:

1.  **Data Collection**: Gathers historical market data and other relevant information.
2.  **Analysis**: Evaluates the data using the defined strategy to generate an optimized portfolio.
3.  **Forward Testing**: Simulates the performance of the generated portfolio over a subsequent period.
4.  **Reporting**: Saves the results of the analysis and forward test, including key performance metrics and visualizations.

## Execution Command

To run the backtest, use the following command from the root of the `AITradingCrew` directory:

```bash
python ai_trading_crew/backtests/securities_collateral_loan_backtest.py securities_collateral_loan
```

You can also specify the number of years to backtest using the `--years` argument:

```bash
python ai_trading_crew/backtests/securities_collateral_loan_backtest.py securities_collateral_loan --years 5
```

## Summary

This script automates the historical backtesting of the securities collateral loan strategy, providing insights into its performance over various periods.