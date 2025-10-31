# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 34
- Candidate universe after filtering: 28
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 9.89%
- Portfolio annual volatility: 18.26%
- Portfolio Sharpe ratio: 0.542
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.89% | 18.26% | 0.542 | 0.30% | Yes |
| low_volatility | 4.92% | 17.27% | 0.285 | 0.26% |  |
| cost_focus | 6.55% | 16.63% | 0.394 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16629126
- Current loan ratio: 0.601
- Buffer to 70%: 14.09% drop
- Buffer to 85%: 29.25% drop
- Max drawdown (history): -34.18%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,966,213 | 0.668 | No | No |
| -20% | ¥13,303,300 | 0.752 | Yes | No |
| -30% | ¥11,640,388 | 0.859 | Yes | Yes |
| -40% | ¥9,977,475 | 1.002 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 105
- Forced liquidation events: 4

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
