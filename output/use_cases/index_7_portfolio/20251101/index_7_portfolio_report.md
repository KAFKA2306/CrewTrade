# Index 7-Portfolio Optimization Report

**Generated:** 2025-11-01 10:07:22

## 代替ETF対応表

| 国内ETF | 代替指数 | オリジナル |
|---------|----------|-----------|
| 1655.T ｉＳ米国株 | S&P500指数 | ^GSPC |
| 2840.T ｉＦＥナ百無 | NASDAQ100 | ^NDX |
| 1364.T ｉシェア４百 | JPX日経400 | ^N225 |
| 314A.T ｉＳゴールド | LBMA Gold Price | GC=F |
| 2520.T 野村新興国株 | MSCIエマージング・マーケットIMI指数 | EEM |
| 2511.T 野村外国債券 | FTSE世界国債インデックス(除く日本) | TLT |
| 399A.T 上場高配５０ | 東証配当フォーカス100指数 | 1478.T |

**初期投資額:** ¥20,998,698（Max DD -20.63%バッファ込み、為替リスク排除、円建て運用）

## Portfolio Allocation

| Ticker | Name | Category | Weight |
|--------|------|----------|--------|
| ^GSPC | S&P 500 Index | equity | 10.15% |
| ^NDX | NASDAQ-100 Index | equity | 23.44% |
| ^N225 | Nikkei 225 Index | equity | 13.73% |
| GC=F | Gold Futures (COMEX) | commodity | 26.51% |
| EEM | iShares MSCI Emerging Markets ETF | equity | 5.75% |
| TLT | iShares 20+ Year Treasury Bond ETF | bonds | 9.90% |
| 1478.T | iShares MSCI Japan High Dividend ETF | equity | 10.53% |

## Risk Metrics

- **Portfolio Value:** ¥20,929,966
- **Loan Amount:** ¥10,000,000
- **Current LTV:** 47.78%
- **LTV Limit:** 60%
- **Warning Ratio:** 70%
- **Liquidation Ratio:** 85%

✅ **HEALTHY:** LTV within safe limits

## Visualizations

### Portfolio Allocation
![Portfolio Allocation](./graphs/01_allocation.png)

### Cumulative Returns Comparison
Performance of optimized portfolio vs benchmarks over the full period.
![Cumulative Returns](./graphs/02_cumulative_returns.png)

### Drawdown Evolution
Historical drawdown profile showing maximum decline periods.
![Drawdown](./graphs/03_drawdown.png)

### LTV Stress Tests
Loan-to-Value ratio during historical crisis periods (COVID-19, 2022 Inflation).
![LTV Stress](./graphs/04_ltv_stress.png)

### Asset Contribution to Returns
Cumulative contribution of each asset to overall portfolio performance.
![Asset Contribution](./graphs/05_asset_contribution.png)

### Risk-Return Profile
Scatter plot showing individual asset positions vs optimized portfolio on risk-return spectrum.
![Risk-Return](./graphs/06_risk_return.png)

### Rolling Sharpe Ratio
252-day rolling Sharpe ratio showing risk-adjusted performance stability over time.
![Rolling Sharpe](./graphs/07_rolling_sharpe.png)

### Asset Correlation Matrix
Correlation heatmap revealing diversification benefits between assets.
![Correlation](./graphs/08_correlation.png)
