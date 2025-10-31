# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 121
- ETFs with sufficient data: 102
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 7 ETF(s) with volatility > 25.0%
- Portfolio annual return: 8.60%
- Portfolio annual volatility: 6.93%
- Portfolio Sharpe ratio: 1.242
- Weighted expense ratio: 0.16%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.60% | 6.93% | 1.242 | 0.16% | Yes |
| low_volatility | 14.32% | 8.96% | 1.598 | 0.17% |  |
| cost_focus | 11.95% | 8.16% | 1.465 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18323797
- Current loan ratio: 0.546
- Buffer to 70%: 22.04% drop
- Buffer to 85%: 35.80% drop
- Max drawdown (history): -15.43%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,491,418 | 0.606 | No | No |
| -20% | ¥14,659,038 | 0.682 | No | No |
| -30% | ¥12,826,658 | 0.780 | Yes | No |
| -40% | ¥10,994,278 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 3
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
