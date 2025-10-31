# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 62
- ETFs with sufficient data: 46
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 6
- Excluded 15 ETF(s) with volatility > 25.0%
- Excluded 1 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 4.72%
- Portfolio annual volatility: 11.12%
- Portfolio Sharpe ratio: 0.425
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.72% | 11.12% | 0.425 | 0.22% | Yes |
| low_volatility | 3.65% | 9.55% | 0.382 | 0.23% |  |
| cost_focus | 6.25% | 13.20% | 0.473 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18324056
- Current loan ratio: 0.546
- Buffer to 70%: 22.04% drop
- Buffer to 85%: 35.80% drop
- Max drawdown (history): -10.01%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,491,650 | 0.606 | No | No |
| -20% | ¥14,659,245 | 0.682 | No | No |
| -30% | ¥12,826,839 | 0.780 | Yes | No |
| -40% | ¥10,994,434 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 208
- Forced liquidation events: 115

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
