# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 225
- ETFs with sufficient data: 182
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 27.64%
- Portfolio annual volatility: 17.72%
- Portfolio Sharpe ratio: 1.559
- Weighted expense ratio: 0.34%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 27.64% | 17.72% | 1.559 | 0.34% | Yes |
| low_volatility | 25.87% | 16.04% | 1.613 | 0.28% |  |
| cost_focus | 27.29% | 16.75% | 1.630 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16534050
- Current loan ratio: 0.605
- Buffer to 70%: 13.60% drop
- Buffer to 85%: 28.85% drop
- Max drawdown (history): -19.12%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,880,645 | 0.672 | No | No |
| -20% | ¥13,227,240 | 0.756 | Yes | No |
| -30% | ¥11,573,835 | 0.864 | Yes | Yes |
| -40% | ¥9,920,430 | 1.008 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 457
- Forced liquidation events: 146

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
