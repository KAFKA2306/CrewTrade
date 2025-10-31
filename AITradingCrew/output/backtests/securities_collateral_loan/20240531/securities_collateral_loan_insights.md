# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 156
- ETFs with sufficient data: 122
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 7
- Excluded 6 ETF(s) with volatility > 25.0%
- Portfolio annual return: 22.06%
- Portfolio annual volatility: 9.13%
- Portfolio Sharpe ratio: 2.417
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 22.06% | 9.13% | 2.417 | 0.18% | Yes |
| low_volatility | 23.96% | 9.31% | 2.574 | 0.23% |  |
| cost_focus | 21.19% | 9.31% | 2.276 | 0.19% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18277365
- Current loan ratio: 0.547
- Buffer to 70%: 21.84% drop
- Buffer to 85%: 35.63% drop
- Max drawdown (history): -8.09%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,449,628 | 0.608 | No | No |
| -20% | ¥14,621,892 | 0.684 | No | No |
| -30% | ¥12,794,156 | 0.782 | Yes | No |
| -40% | ¥10,966,419 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 492
- Forced liquidation events: 294

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
