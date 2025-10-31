# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 140
- ETFs with sufficient data: 126
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 25.01%
- Portfolio annual volatility: 14.90%
- Portfolio Sharpe ratio: 1.678
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 25.01% | 14.90% | 1.678 | 0.30% | Yes |
| low_volatility | 27.32% | 17.13% | 1.595 | 0.30% |  |
| cost_focus | 25.45% | 15.65% | 1.626 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16619090
- Current loan ratio: 0.602
- Buffer to 70%: 14.04% drop
- Buffer to 85%: 29.21% drop
- Max drawdown (history): -48.13%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,957,181 | 0.669 | No | No |
| -20% | ¥13,295,272 | 0.752 | Yes | No |
| -30% | ¥11,633,363 | 0.860 | Yes | Yes |
| -40% | ¥9,971,454 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 543
- Forced liquidation events: 371

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
