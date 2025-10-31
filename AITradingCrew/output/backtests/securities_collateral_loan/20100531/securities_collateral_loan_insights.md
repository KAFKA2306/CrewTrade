# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 30
- ETFs with sufficient data: 19
- Candidate universe after filtering: 14
- Selected ETFs (max_sharpe): 14
- Excluded 11 ETF(s) with volatility > 25.0%
- Portfolio annual return: 0.90%
- Portfolio annual volatility: 15.14%
- Portfolio Sharpe ratio: 0.059
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 0.90% | 15.14% | 0.059 | 0.25% | Yes |
| low_volatility | 7.02% | 14.82% | 0.474 | 0.24% |  |
| cost_focus | 5.62% | 14.59% | 0.385 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18286811
- Current loan ratio: 0.547
- Buffer to 70%: 21.88% drop
- Buffer to 85%: 35.67% drop
- Max drawdown (history): -28.51%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,458,129 | 0.608 | No | No |
| -20% | ¥14,629,448 | 0.684 | No | No |
| -30% | ¥12,800,767 | 0.781 | Yes | No |
| -40% | ¥10,972,086 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 3
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
