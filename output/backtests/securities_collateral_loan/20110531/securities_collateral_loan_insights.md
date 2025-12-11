# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 32
- ETFs with sufficient data: 22
- Candidate universe after filtering: 7
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 7
- Excluded 10 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 3.26%
- Portfolio annual volatility: 15.20%
- Portfolio Sharpe ratio: 0.215
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 3.26% | 15.20% | 0.215 | 0.25% | Yes |
| low_volatility | 3.26% | 15.20% | 0.215 | 0.25% |  |
| cost_focus | 3.26% | 15.20% | 0.215 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18301637
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -29.65%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,471,473 | 0.607 | No | No |
| -20% | ¥14,641,309 | 0.683 | No | No |
| -30% | ¥12,811,146 | 0.781 | Yes | No |
| -40% | ¥10,980,982 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 59
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
