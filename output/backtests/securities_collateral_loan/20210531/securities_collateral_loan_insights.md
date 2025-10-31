# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 4
- Candidate universe after filtering: 4
- Selected ETFs (max_sharpe): 4
- Excluded 6 ETF(s) with volatility > 25.0%
- Excluded 54 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 7.96%
- Portfolio annual volatility: 12.07%
- Portfolio Sharpe ratio: 0.660
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.96% | 12.07% | 0.660 | 0.21% | Yes |
| low_volatility | 6.96% | 11.91% | 0.584 | 0.22% |  |
| cost_focus | 7.05% | 12.39% | 0.569 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18324885
- Current loan ratio: 0.546
- Buffer to 70%: 22.04% drop
- Buffer to 85%: 35.80% drop
- Max drawdown (history): -19.04%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,492,396 | 0.606 | No | No |
| -20% | ¥14,659,908 | 0.682 | No | No |
| -30% | ¥12,827,420 | 0.780 | Yes | No |
| -40% | ¥10,994,931 | 0.909 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 237
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
