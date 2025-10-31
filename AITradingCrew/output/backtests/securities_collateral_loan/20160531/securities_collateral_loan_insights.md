# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 63
- ETFs with sufficient data: 63
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 12.78%
- Portfolio annual volatility: 14.55%
- Portfolio Sharpe ratio: 0.878
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.78% | 14.55% | 0.878 | 0.26% | Yes |
| low_volatility | 13.78% | 14.94% | 0.922 | 0.29% |  |
| cost_focus | 13.74% | 14.84% | 0.926 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16639308
- Current loan ratio: 0.601
- Buffer to 70%: 14.14% drop
- Buffer to 85%: 29.30% drop
- Max drawdown (history): -17.24%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,975,377 | 0.668 | No | No |
| -20% | ¥13,311,446 | 0.751 | Yes | No |
| -30% | ¥11,647,516 | 0.859 | Yes | Yes |
| -40% | ¥9,983,585 | 1.002 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 313
- Forced liquidation events: 178

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
