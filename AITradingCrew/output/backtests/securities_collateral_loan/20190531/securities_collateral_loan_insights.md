# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 81
- ETFs with sufficient data: 67
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 7
- Excluded 4 ETF(s) with volatility > 25.0%
- Excluded 7 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.60%
- Portfolio annual volatility: 5.48%
- Portfolio Sharpe ratio: 1.022
- Weighted expense ratio: 0.19%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.60% | 5.48% | 1.022 | 0.19% | Yes |
| low_volatility | 4.08% | 5.76% | 0.709 | 0.21% |  |
| cost_focus | 4.42% | 6.47% | 0.683 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18320323
- Current loan ratio: 0.546
- Buffer to 70%: 22.02% drop
- Buffer to 85%: 35.78% drop
- Max drawdown (history): -6.23%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,488,291 | 0.607 | No | No |
| -20% | ¥14,656,258 | 0.682 | No | No |
| -30% | ¥12,824,226 | 0.780 | Yes | No |
| -40% | ¥10,992,194 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 61
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
