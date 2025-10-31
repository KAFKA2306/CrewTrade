# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 96
- ETFs with sufficient data: 92
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 6.45%
- Portfolio annual volatility: 5.58%
- Portfolio Sharpe ratio: 1.155
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 6.45% | 5.58% | 1.155 | 0.24% | Yes |
| low_volatility | 5.27% | 4.94% | 1.068 | 0.25% |  |
| cost_focus | 6.73% | 5.66% | 1.190 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16638606
- Current loan ratio: 0.601
- Buffer to 70%: 14.14% drop
- Buffer to 85%: 29.29% drop
- Max drawdown (history): -43.59%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,974,746 | 0.668 | No | No |
| -20% | ¥13,310,885 | 0.751 | Yes | No |
| -30% | ¥11,647,024 | 0.859 | Yes | Yes |
| -40% | ¥9,983,164 | 1.002 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 336
- Forced liquidation events: 102

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
