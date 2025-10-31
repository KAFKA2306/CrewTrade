# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after filtering: 18
- Selected ETFs (max_sharpe): 8
- Excluded 1 ETF(s) with volatility > 35.0%
- Excluded 13 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 15.99%
- Portfolio annual volatility: 14.64%
- Portfolio Sharpe ratio: 1.092
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.99% | 14.64% | 1.092 | 0.25% | Yes |
| low_volatility | 13.69% | 13.39% | 1.023 | 0.26% |  |
| cost_focus | 13.82% | 13.21% | 1.046 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18311179
- Current loan ratio: 0.546
- Buffer to 70%: 21.98% drop
- Buffer to 85%: 35.75% drop
- Max drawdown (history): -20.08%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,480,061 | 0.607 | No | No |
| -20% | ¥14,648,943 | 0.683 | No | No |
| -30% | ¥12,817,825 | 0.780 | Yes | No |
| -40% | ¥10,986,707 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 615
- Forced liquidation events: 433

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
