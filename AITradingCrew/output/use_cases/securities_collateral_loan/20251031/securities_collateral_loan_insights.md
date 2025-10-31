# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 223
- ETFs with sufficient data: 190
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 24.16%
- Portfolio annual volatility: 15.54%
- Portfolio Sharpe ratio: 1.555
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 24.16% | 15.54% | 1.555 | 0.23% | Yes |
| low_volatility | 26.52% | 15.73% | 1.686 | 0.20% |  |
| cost_focus | 24.03% | 14.99% | 1.603 | 0.19% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16481884
- Current loan ratio: 0.607
- Buffer to 70%: 13.32% drop
- Buffer to 85%: 28.62% drop
- Max drawdown (history): -16.63%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,833,696 | 0.674 | No | No |
| -20% | ¥13,185,507 | 0.758 | Yes | No |
| -30% | ¥11,537,319 | 0.867 | Yes | Yes |
| -40% | ¥9,889,130 | 1.011 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 670
- Forced liquidation events: 321

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
