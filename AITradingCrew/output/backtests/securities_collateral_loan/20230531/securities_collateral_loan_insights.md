# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 132
- ETFs with sufficient data: 106
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 10 ETF(s) with volatility > 25.0%
- Portfolio annual return: 10.64%
- Portfolio annual volatility: 8.01%
- Portfolio Sharpe ratio: 1.329
- Weighted expense ratio: 0.19%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.64% | 8.01% | 1.329 | 0.19% | Yes |
| low_volatility | 12.56% | 9.95% | 1.263 | 0.27% |  |
| cost_focus | 10.90% | 9.02% | 1.208 | 0.20% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18308002
- Current loan ratio: 0.546
- Buffer to 70%: 21.97% drop
- Buffer to 85%: 35.74% drop
- Max drawdown (history): -5.16%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,477,201 | 0.607 | No | No |
| -20% | ¥14,646,401 | 0.683 | No | No |
| -30% | ¥12,815,601 | 0.780 | Yes | No |
| -40% | ¥10,984,801 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 344
- Forced liquidation events: 344

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
