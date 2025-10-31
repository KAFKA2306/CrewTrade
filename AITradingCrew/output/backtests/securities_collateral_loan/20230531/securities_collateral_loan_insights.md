# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 160
- ETFs with sufficient data: 142
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 16.66%
- Portfolio annual volatility: 13.14%
- Portfolio Sharpe ratio: 1.268
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 16.66% | 13.14% | 1.268 | 0.30% | Yes |
| low_volatility | 17.05% | 12.23% | 1.394 | 0.29% |  |
| cost_focus | 16.66% | 12.42% | 1.341 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16605538
- Current loan ratio: 0.602
- Buffer to 70%: 13.97% drop
- Buffer to 85%: 29.15% drop
- Max drawdown (history): -12.11%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,944,984 | 0.669 | No | No |
| -20% | ¥13,284,430 | 0.753 | Yes | No |
| -30% | ¥11,623,876 | 0.860 | Yes | Yes |
| -40% | ¥9,963,323 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 580
- Forced liquidation events: 191

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
