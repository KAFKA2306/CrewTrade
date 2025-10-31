# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after filtering: 18
- Selected ETFs (max_sharpe): 6
- Excluded 13 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 15.34%
- Portfolio annual volatility: 13.20%
- Portfolio Sharpe ratio: 1.162
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.34% | 13.20% | 1.162 | 0.30% | Yes |
| low_volatility | 15.99% | 13.29% | 1.204 | 0.28% |  |
| cost_focus | 15.45% | 13.52% | 1.143 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18308011
- Current loan ratio: 0.546
- Buffer to 70%: 21.97% drop
- Buffer to 85%: 35.74% drop
- Max drawdown (history): -11.82%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,477,210 | 0.607 | No | No |
| -20% | ¥14,646,409 | 0.683 | No | No |
| -30% | ¥12,815,608 | 0.780 | Yes | No |
| -40% | ¥10,984,807 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 614
- Forced liquidation events: 51

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
