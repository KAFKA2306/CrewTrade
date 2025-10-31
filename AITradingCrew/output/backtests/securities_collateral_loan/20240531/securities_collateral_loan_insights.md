# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 187
- ETFs with sufficient data: 149
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Excluded 7 ETF(s) with volatility > 25.0%
- Excluded 1 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 22.84%
- Portfolio annual volatility: 10.95%
- Portfolio Sharpe ratio: 2.085
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 22.84% | 10.95% | 2.085 | 0.22% | Yes |
| low_volatility | 22.37% | 9.85% | 2.270 | 0.26% |  |
| cost_focus | 23.58% | 10.35% | 2.280 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16533563
- Current loan ratio: 0.605
- Buffer to 70%: 13.60% drop
- Buffer to 85%: 28.84% drop
- Max drawdown (history): -10.22%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,880,207 | 0.672 | No | No |
| -20% | ¥13,226,850 | 0.756 | Yes | No |
| -30% | ¥11,573,494 | 0.864 | Yes | Yes |
| -40% | ¥9,920,138 | 1.008 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 627
- Forced liquidation events: 429

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
