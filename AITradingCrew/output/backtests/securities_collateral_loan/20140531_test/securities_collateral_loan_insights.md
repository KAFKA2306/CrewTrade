# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 7
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 14.74%
- Portfolio annual volatility: 12.50%
- Portfolio Sharpe ratio: 1.179
- Weighted expense ratio: 0.28%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.74% | 12.50% | 1.179 | 0.28% | Yes |
| low_volatility | 16.83% | 13.56% | 1.241 | 0.25% |  |
| cost_focus | 15.78% | 12.95% | 1.218 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18304440
- Current loan ratio: 0.546
- Buffer to 70%: 21.95% drop
- Buffer to 85%: 35.73% drop
- Max drawdown (history): -14.77%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,473,996 | 0.607 | No | No |
| -20% | ¥14,643,552 | 0.683 | No | No |
| -30% | ¥12,813,108 | 0.780 | Yes | No |
| -40% | ¥10,982,664 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 395
- Forced liquidation events: 21

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
