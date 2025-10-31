# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 37
- ETFs with sufficient data: 37
- Candidate universe after filtering: 30
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 8.67%
- Portfolio annual volatility: 17.09%
- Portfolio Sharpe ratio: 0.507
- Weighted expense ratio: 0.28%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.67% | 17.09% | 0.507 | 0.28% | Yes |
| low_volatility | 9.68% | 14.50% | 0.667 | 0.30% |  |
| cost_focus | 10.22% | 15.80% | 0.647 | 0.31% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16602353
- Current loan ratio: 0.602
- Buffer to 70%: 13.95% drop
- Buffer to 85%: 29.14% drop
- Max drawdown (history): -37.78%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,942,118 | 0.669 | No | No |
| -20% | ¥13,281,882 | 0.753 | Yes | No |
| -30% | ¥11,621,647 | 0.861 | Yes | Yes |
| -40% | ¥9,961,412 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 53
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
