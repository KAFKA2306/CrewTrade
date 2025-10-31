# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 109
- ETFs with sufficient data: 82
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 16 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.41%
- Portfolio annual volatility: 13.33%
- Portfolio Sharpe ratio: 0.856
- Weighted expense ratio: 0.19%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.41% | 13.33% | 0.856 | 0.19% | Yes |
| low_volatility | 12.64% | 9.61% | 1.316 | 0.18% |  |
| cost_focus | 9.96% | 10.84% | 0.919 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18317522
- Current loan ratio: 0.546
- Buffer to 70%: 22.01% drop
- Buffer to 85%: 35.77% drop
- Max drawdown (history): -17.95%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,485,770 | 0.607 | No | No |
| -20% | ¥14,654,018 | 0.682 | No | No |
| -30% | ¥12,822,265 | 0.780 | Yes | No |
| -40% | ¥10,990,513 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 403
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
