# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 52
- ETFs with sufficient data: 37
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 14
- Excluded 13 ETF(s) with volatility > 25.0%
- Excluded 2 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 19.82%
- Portfolio annual volatility: 14.85%
- Portfolio Sharpe ratio: 1.334
- Weighted expense ratio: 0.32%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 19.82% | 14.85% | 1.334 | 0.32% | Yes |
| low_volatility | 20.04% | 13.21% | 1.517 | 0.34% |  |
| cost_focus | 20.00% | 15.11% | 1.324 | 0.31% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16592763
- Current loan ratio: 0.603
- Buffer to 70%: 13.90% drop
- Buffer to 85%: 29.10% drop
- Max drawdown (history): -15.81%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,933,487 | 0.670 | No | No |
| -20% | ¥13,274,210 | 0.753 | Yes | No |
| -30% | ¥11,614,934 | 0.861 | Yes | Yes |
| -40% | ¥9,955,658 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 670
- Forced liquidation events: 576

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
