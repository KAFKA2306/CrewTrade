# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 40
- ETFs with sufficient data: 24
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 6
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 5 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 8.78%
- Portfolio annual volatility: 14.77%
- Portfolio Sharpe ratio: 0.594
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.78% | 14.77% | 0.594 | 0.23% | Yes |
| low_volatility | 6.55% | 12.84% | 0.510 | 0.27% |  |
| cost_focus | 6.81% | 14.83% | 0.459 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18315548
- Current loan ratio: 0.546
- Buffer to 70%: 22.00% drop
- Buffer to 85%: 35.77% drop
- Max drawdown (history): -11.22%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,483,993 | 0.607 | No | No |
| -20% | ¥14,652,438 | 0.682 | No | No |
| -30% | ¥12,820,884 | 0.780 | Yes | No |
| -40% | ¥10,989,329 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 340
- Forced liquidation events: 340

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
