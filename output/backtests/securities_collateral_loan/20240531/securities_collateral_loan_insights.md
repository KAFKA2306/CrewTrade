# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 98
- ETFs with sufficient data: 60
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 7
- Excluded 5 ETF(s) with volatility > 35.0%
- Excluded 27 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 15.68%
- Portfolio annual volatility: 12.91%
- Portfolio Sharpe ratio: 1.214
- Weighted expense ratio: 0.15%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.68% | 12.91% | 1.214 | 0.15% | Yes |
| low_volatility | 12.05% | 8.49% | 1.419 | 0.20% |  |
| cost_focus | 15.84% | 12.24% | 1.294 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18269277
- Current loan ratio: 0.547
- Buffer to 70%: 21.80% drop
- Buffer to 85%: 35.60% drop
- Max drawdown (history): -18.90%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,442,349 | 0.608 | No | No |
| -20% | ¥14,615,422 | 0.684 | No | No |
| -30% | ¥12,788,494 | 0.782 | Yes | No |
| -40% | ¥10,961,566 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 968
- Forced liquidation events: 363

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
