# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 19
- Candidate universe after filtering: 14
- Selected ETFs (max_sharpe): 14
- Excluded 15 ETF(s) with volatility > 25.0%
- Portfolio annual return: 0.90%
- Portfolio annual volatility: 15.14%
- Portfolio Sharpe ratio: 0.059
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 0.90% | 15.14% | 0.059 | 0.25% | Yes |
| low_volatility | 4.64% | 15.24% | 0.304 | 0.26% |  |
| cost_focus | 3.04% | 15.47% | 0.196 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16622694
- Current loan ratio: 0.602
- Buffer to 70%: 14.06% drop
- Buffer to 85%: 29.23% drop
- Max drawdown (history): -28.51%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,960,425 | 0.668 | No | No |
| -20% | ¥13,298,155 | 0.752 | Yes | No |
| -30% | ¥11,635,886 | 0.859 | Yes | Yes |
| -40% | ¥9,973,617 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 23
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
