# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 53
- ETFs with sufficient data: 53
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 25.53%
- Portfolio annual volatility: 13.83%
- Portfolio Sharpe ratio: 1.845
- Weighted expense ratio: 0.28%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 25.53% | 13.83% | 1.845 | 0.28% | Yes |
| low_volatility | 23.83% | 13.23% | 1.801 | 0.29% |  |
| cost_focus | 26.62% | 14.29% | 1.863 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16599681
- Current loan ratio: 0.602
- Buffer to 70%: 13.94% drop
- Buffer to 85%: 29.13% drop
- Max drawdown (history): -16.47%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,939,713 | 0.669 | No | No |
| -20% | ¥13,279,745 | 0.753 | Yes | No |
| -30% | ¥11,619,777 | 0.861 | Yes | Yes |
| -40% | ¥9,959,809 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 473
- Forced liquidation events: 395

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
