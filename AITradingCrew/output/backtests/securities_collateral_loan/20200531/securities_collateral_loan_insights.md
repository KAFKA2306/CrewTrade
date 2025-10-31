# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 108
- ETFs with sufficient data: 101
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 5.85%
- Portfolio annual volatility: 10.42%
- Portfolio Sharpe ratio: 0.561
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.85% | 10.42% | 0.561 | 0.21% | Yes |
| low_volatility | 6.87% | 7.39% | 0.929 | 0.20% |  |
| cost_focus | 6.86% | 9.02% | 0.761 | 0.20% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16598452
- Current loan ratio: 0.602
- Buffer to 70%: 13.93% drop
- Buffer to 85%: 29.12% drop
- Max drawdown (history): -61.49%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,938,606 | 0.669 | No | No |
| -20% | ¥13,278,761 | 0.753 | Yes | No |
| -30% | ¥11,618,916 | 0.861 | Yes | Yes |
| -40% | ¥9,959,071 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 147
- Forced liquidation events: 84

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
