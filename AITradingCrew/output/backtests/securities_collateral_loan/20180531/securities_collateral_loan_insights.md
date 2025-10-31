# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 82
- ETFs with sufficient data: 80
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 21.13%
- Portfolio annual volatility: 11.20%
- Portfolio Sharpe ratio: 1.887
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 21.13% | 11.20% | 1.887 | 0.25% | Yes |
| low_volatility | 20.78% | 10.91% | 1.905 | 0.28% |  |
| cost_focus | 21.33% | 11.14% | 1.914 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16558422
- Current loan ratio: 0.604
- Buffer to 70%: 13.73% drop
- Buffer to 85%: 28.95% drop
- Max drawdown (history): -22.10%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,902,579 | 0.671 | No | No |
| -20% | ¥13,246,737 | 0.755 | Yes | No |
| -30% | ¥11,590,895 | 0.863 | Yes | Yes |
| -40% | ¥9,935,053 | 1.006 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 466
- Forced liquidation events: 29

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
