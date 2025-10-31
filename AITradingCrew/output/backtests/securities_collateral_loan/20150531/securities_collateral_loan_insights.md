# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 56
- ETFs with sufficient data: 56
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 28.47%
- Portfolio annual volatility: 12.05%
- Portfolio Sharpe ratio: 2.363
- Weighted expense ratio: 0.31%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 28.47% | 12.05% | 2.363 | 0.31% | Yes |
| low_volatility | 30.26% | 11.92% | 2.539 | 0.35% |  |
| cost_focus | 31.19% | 12.81% | 2.434 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16569341
- Current loan ratio: 0.604
- Buffer to 70%: 13.78% drop
- Buffer to 85%: 29.00% drop
- Max drawdown (history): -14.86%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,912,407 | 0.671 | No | No |
| -20% | ¥13,255,473 | 0.754 | Yes | No |
| -30% | ¥11,598,539 | 0.862 | Yes | Yes |
| -40% | ¥9,941,605 | 1.006 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 627
- Forced liquidation events: 507

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
