# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 132
- ETFs with sufficient data: 106
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 8
- Excluded 10 ETF(s) with volatility > 25.0%
- Portfolio annual return: 12.46%
- Portfolio annual volatility: 9.23%
- Portfolio Sharpe ratio: 1.350
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.46% | 9.23% | 1.350 | 0.24% | Yes |
| low_volatility | 9.03% | 7.35% | 1.229 | 0.19% |  |
| cost_focus | 11.33% | 9.17% | 1.235 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18285151
- Current loan ratio: 0.547
- Buffer to 70%: 21.87% drop
- Buffer to 85%: 35.66% drop
- Max drawdown (history): -4.88%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,456,636 | 0.608 | No | No |
| -20% | ¥14,628,121 | 0.684 | No | No |
| -30% | ¥12,799,606 | 0.781 | Yes | No |
| -40% | ¥10,971,091 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 329
- Forced liquidation events: 27

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
