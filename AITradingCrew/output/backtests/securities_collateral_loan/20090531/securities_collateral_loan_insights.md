# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 26
- ETFs with sufficient data: 26
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: -18.28%
- Portfolio annual volatility: 38.23%
- Portfolio Sharpe ratio: -0.478
- Weighted expense ratio: 0.31%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | -18.28% | 38.23% | -0.478 | 0.31% | Yes |
| low_volatility | -17.67% | 32.39% | -0.546 | 0.31% |  |
| cost_focus | -17.88% | 33.85% | -0.528 | 0.31% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16609683
- Current loan ratio: 0.602
- Buffer to 70%: 13.99% drop
- Buffer to 85%: 29.17% drop
- Max drawdown (history): -45.58%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,948,714 | 0.669 | No | No |
| -20% | ¥13,287,746 | 0.753 | Yes | No |
| -30% | ¥11,626,778 | 0.860 | Yes | Yes |
| -40% | ¥9,965,810 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 24
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
