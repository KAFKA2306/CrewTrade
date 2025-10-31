# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 215
- ETFs with sufficient data: 174
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 39.07%
- Portfolio annual volatility: 11.44%
- Portfolio Sharpe ratio: 3.415
- Weighted expense ratio: 0.34%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 39.07% | 11.44% | 3.415 | 0.34% | Yes |
| low_volatility | 36.17% | 9.59% | 3.772 | 0.40% |  |
| cost_focus | 41.12% | 11.27% | 3.650 | 0.30% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16569604
- Current loan ratio: 0.604
- Buffer to 70%: 13.78% drop
- Buffer to 85%: 29.00% drop
- Max drawdown (history): -3.87%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,912,644 | 0.671 | No | No |
| -20% | ¥13,255,683 | 0.754 | Yes | No |
| -30% | ¥11,598,723 | 0.862 | Yes | Yes |
| -40% | ¥9,941,762 | 1.006 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 79
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
