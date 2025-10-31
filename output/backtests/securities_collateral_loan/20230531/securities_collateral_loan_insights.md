# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 43
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 7
- Excluded 4 ETF(s) with volatility > 35.0%
- Excluded 37 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 10.87%
- Portfolio annual volatility: 10.79%
- Portfolio Sharpe ratio: 1.007
- Weighted expense ratio: 0.19%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.87% | 10.79% | 1.007 | 0.19% | Yes |
| low_volatility | 7.51% | 7.10% | 1.057 | 0.16% |  |
| cost_focus | 11.38% | 11.91% | 0.955 | 0.19% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18276328
- Current loan ratio: 0.547
- Buffer to 70%: 21.83% drop
- Buffer to 85%: 35.63% drop
- Max drawdown (history): -14.81%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,448,695 | 0.608 | No | No |
| -20% | ¥14,621,062 | 0.684 | No | No |
| -30% | ¥12,793,430 | 0.782 | Yes | No |
| -40% | ¥10,965,797 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 589
- Forced liquidation events: 171

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
