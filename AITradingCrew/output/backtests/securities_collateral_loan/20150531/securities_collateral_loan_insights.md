# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 44
- ETFs with sufficient data: 40
- Candidate universe after filtering: 32
- Selected ETFs (max_sharpe): 6
- Excluded 4 ETF(s) with volatility > 25.0%
- Portfolio annual return: 17.35%
- Portfolio annual volatility: 10.00%
- Portfolio Sharpe ratio: 1.735
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 17.35% | 10.00% | 1.735 | 0.24% | Yes |
| low_volatility | 16.86% | 9.54% | 1.768 | 0.22% |  |
| cost_focus | 22.05% | 11.31% | 1.950 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18304855
- Current loan ratio: 0.546
- Buffer to 70%: 21.96% drop
- Buffer to 85%: 35.73% drop
- Max drawdown (history): -14.07%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,474,370 | 0.607 | No | No |
| -20% | ¥14,643,884 | 0.683 | No | No |
| -30% | ¥12,813,398 | 0.780 | Yes | No |
| -40% | ¥10,982,913 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 396
- Forced liquidation events: 147

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
