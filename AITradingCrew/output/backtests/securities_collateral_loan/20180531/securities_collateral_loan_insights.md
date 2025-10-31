# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 82
- ETFs with sufficient data: 72
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Excluded 8 ETF(s) with volatility > 25.0%
- Portfolio annual return: 19.83%
- Portfolio annual volatility: 10.87%
- Portfolio Sharpe ratio: 1.824
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 19.83% | 10.87% | 1.824 | 0.26% | Yes |
| low_volatility | 18.98% | 10.57% | 1.796 | 0.27% |  |
| cost_focus | 20.36% | 10.87% | 1.872 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16577250
- Current loan ratio: 0.603
- Buffer to 70%: 13.82% drop
- Buffer to 85%: 29.03% drop
- Max drawdown (history): -21.97%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,919,525 | 0.670 | No | No |
| -20% | ¥13,261,800 | 0.754 | Yes | No |
| -30% | ¥11,604,075 | 0.862 | Yes | Yes |
| -40% | ¥9,946,350 | 1.005 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 416
- Forced liquidation events: 82

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
