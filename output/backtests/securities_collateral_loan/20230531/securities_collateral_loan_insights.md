# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 72
- Candidate universe after filtering: 31
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 10
- Excluded 12 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 7.65%
- Portfolio annual volatility: 13.66%
- Portfolio Sharpe ratio: 0.560
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.65% | 13.66% | 0.560 | 0.23% | Yes |
| low_volatility | 6.73% | 12.48% | 0.539 | 0.25% |  |
| cost_focus | 8.36% | 11.04% | 0.757 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18238975
- Current loan ratio: 0.548
- Buffer to 70%: 21.67% drop
- Buffer to 85%: 35.50% drop
- Max drawdown (history): -31.26%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,415,077 | 0.609 | No | No |
| -20% | ¥14,591,180 | 0.685 | No | No |
| -30% | ¥12,767,282 | 0.783 | Yes | No |
| -40% | ¥10,943,385 | 0.914 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 466
- Forced liquidation events: 10

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
