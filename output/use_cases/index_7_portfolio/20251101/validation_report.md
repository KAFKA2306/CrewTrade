# Index 7-Portfolio Validation Report
**Generated:** 2025-11-01 09:29:22.727388

## 1. Walk-Forward Test
- **Periods tested:** 2
- **Avg Out-of-Sample Sharpe:** 1.043 ± 1.560
- **Avg Annual Return:** 9.93%
- **Avg Max Drawdown:** -15.88%
- **Stability Score:** 0.391

## 2. Benchmark Comparison
| Strategy | Annual Return | Sharpe | Max DD | Calmar |
|----------|---------------|--------|--------|--------|
| optimized | 12.18% | 1.254 | -18.28% | 0.666 |
| equal_weight | 11.42% | 1.086 | -20.89% | 0.547 |
| 60_40 | 8.01% | 0.836 | -24.82% | 0.323 |

## 3. Stress Test
### 2008_financial_crisis
- Error: データ不足

### 2020_covid_crash
- **Total Return:** -3.50%
- **Max Drawdown:** -20.63%
- **LTV Warning Breaches:** 0
- **LTV Liquidation Breaches:** 63

### 2022_inflation_shock
- **Total Return:** -12.26%
- **Max Drawdown:** -14.97%
- **LTV Warning Breaches:** 0
- **LTV Liquidation Breaches:** 215

## 4. Sensitivity Analysis
| Config | Annual Return | Sharpe | Max DD |
|--------|---------------|--------|--------|
| base | 12.50% | 1.266 | -19.25% |
| min_weight_10pct | 11.94% | 1.188 | -20.26% |
| max_weight_40pct | 12.67% | 1.311 | -18.36% |
| max_volatility_20pct | 12.60% | 1.250 | -18.96% |
| sharpe_weight_80pct | 13.17% | 1.292 | -19.39% |
