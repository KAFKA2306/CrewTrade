# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 47
- ETFs with sufficient data: 47
- Candidate universe after filtering: 39
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 1.41%
- Portfolio annual volatility: 13.94%
- Portfolio Sharpe ratio: 0.101
- Weighted expense ratio: 0.31%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 1.41% | 13.94% | 0.101 | 0.31% | Yes |
| low_volatility | 0.75% | 13.38% | 0.056 | 0.28% |  |
| cost_focus | 2.79% | 14.18% | 0.197 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16620760
- Current loan ratio: 0.602
- Buffer to 70%: 14.05% drop
- Buffer to 85%: 29.22% drop
- Max drawdown (history): -16.12%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,958,684 | 0.668 | No | No |
| -20% | ¥13,296,608 | 0.752 | Yes | No |
| -30% | ¥11,634,532 | 0.860 | Yes | Yes |
| -40% | ¥9,972,456 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 263
- Forced liquidation events: 114

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
