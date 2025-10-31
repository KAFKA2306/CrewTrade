# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after filtering: 18
- Selected ETFs (max_sharpe): 7
- Excluded 13 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 16.29%
- Portfolio annual volatility: 13.75%
- Portfolio Sharpe ratio: 1.185
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 16.29% | 13.75% | 1.185 | 0.24% | Yes |
| low_volatility | 16.32% | 13.75% | 1.187 | 0.23% |  |
| cost_focus | 14.33% | 12.82% | 1.118 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18321382
- Current loan ratio: 0.546
- Buffer to 70%: 22.03% drop
- Buffer to 85%: 35.79% drop
- Max drawdown (history): -11.33%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,489,244 | 0.607 | No | No |
| -20% | ¥14,657,106 | 0.682 | No | No |
| -30% | ¥12,824,967 | 0.780 | Yes | No |
| -40% | ¥10,992,829 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 605
- Forced liquidation events: 97

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
