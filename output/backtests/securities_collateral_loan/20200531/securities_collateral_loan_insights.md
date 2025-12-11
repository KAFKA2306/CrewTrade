# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 92
- ETFs with sufficient data: 15
- Candidate universe after filtering: 15
- Selected ETFs (max_sharpe): 6
- Excluded 18 ETF(s) with volatility > 25.0%
- Excluded 53 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 7.53%
- Portfolio annual volatility: 7.65%
- Portfolio Sharpe ratio: 0.985
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.53% | 7.65% | 0.985 | 0.17% | Yes |
| low_volatility | 6.38% | 6.80% | 0.938 | 0.14% |  |
| cost_focus | 7.02% | 7.34% | 0.956 | 0.15% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18300807
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.71% drop
- Max drawdown (history): -10.84%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,470,726 | 0.607 | No | No |
| -20% | ¥14,640,646 | 0.683 | No | No |
| -30% | ¥12,810,565 | 0.781 | Yes | No |
| -40% | ¥10,980,484 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 135
- Forced liquidation events: 135

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
