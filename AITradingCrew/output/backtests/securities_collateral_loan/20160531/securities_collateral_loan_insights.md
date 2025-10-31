# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 34
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 6
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 5 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 8.98%
- Portfolio annual volatility: 10.69%
- Portfolio Sharpe ratio: 0.841
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.98% | 10.69% | 0.841 | 0.23% | Yes |
| low_volatility | 12.17% | 12.81% | 0.950 | 0.25% |  |
| cost_focus | 10.09% | 11.71% | 0.862 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18313633
- Current loan ratio: 0.546
- Buffer to 70%: 21.99% drop
- Buffer to 85%: 35.76% drop
- Max drawdown (history): -13.11%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,482,270 | 0.607 | No | No |
| -20% | ¥14,650,906 | 0.683 | No | No |
| -30% | ¥12,819,543 | 0.780 | Yes | No |
| -40% | ¥10,988,180 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 186
- Forced liquidation events: 178

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
