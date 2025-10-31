# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 40
- ETFs with sufficient data: 24
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 6
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 5 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.73%
- Portfolio annual volatility: 11.99%
- Portfolio Sharpe ratio: 0.478
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.73% | 11.99% | 0.478 | 0.30% | Yes |
| low_volatility | 9.62% | 14.95% | 0.643 | 0.24% |  |
| cost_focus | 5.45% | 13.14% | 0.415 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18323288
- Current loan ratio: 0.546
- Buffer to 70%: 22.04% drop
- Buffer to 85%: 35.79% drop
- Max drawdown (history): -10.33%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,490,959 | 0.606 | No | No |
| -20% | ¥14,658,630 | 0.682 | No | No |
| -30% | ¥12,826,302 | 0.780 | Yes | No |
| -40% | ¥10,993,973 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
