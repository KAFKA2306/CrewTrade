# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 55
- ETFs with sufficient data: 20
- Candidate universe after filtering: 11
- Selected ETFs (max_sharpe): 11
- Excluded 3 ETF(s) with volatility > 35.0%
- Excluded 32 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 4.81%
- Portfolio annual volatility: 14.89%
- Portfolio Sharpe ratio: 0.323
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.81% | 14.89% | 0.323 | 0.21% | Yes |
| low_volatility | 7.71% | 14.16% | 0.545 | 0.22% |  |
| cost_focus | 6.80% | 14.23% | 0.478 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18247350
- Current loan ratio: 0.548
- Buffer to 70%: 21.71% drop
- Buffer to 85%: 35.53% drop
- Max drawdown (history): -24.09%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,422,615 | 0.609 | No | No |
| -20% | ¥14,597,880 | 0.685 | No | No |
| -30% | ¥12,773,145 | 0.783 | Yes | No |
| -40% | ¥10,948,410 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 214
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
