# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 34
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 7
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 5 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.92%
- Portfolio annual volatility: 12.60%
- Portfolio Sharpe ratio: 0.946
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.92% | 12.60% | 0.946 | 0.23% | Yes |
| low_volatility | 10.78% | 11.57% | 0.931 | 0.24% |  |
| cost_focus | 9.66% | 11.78% | 0.820 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18298853
- Current loan ratio: 0.546
- Buffer to 70%: 21.93% drop
- Buffer to 85%: 35.71% drop
- Max drawdown (history): -13.48%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,468,968 | 0.607 | No | No |
| -20% | ¥14,639,082 | 0.683 | No | No |
| -30% | ¥12,809,197 | 0.781 | Yes | No |
| -40% | ¥10,979,312 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 186
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
