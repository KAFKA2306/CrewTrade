# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 56
- Candidate universe after filtering: 37
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 14 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 9.14%
- Portfolio annual volatility: 11.26%
- Portfolio Sharpe ratio: 0.812
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.14% | 11.26% | 0.812 | 0.24% | Yes |
| low_volatility | 8.87% | 9.75% | 0.910 | 0.22% |  |
| cost_focus | 9.13% | 13.10% | 0.697 | 0.15% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18283686
- Current loan ratio: 0.547
- Buffer to 70%: 21.87% drop
- Buffer to 85%: 35.65% drop
- Max drawdown (history): -20.43%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,455,317 | 0.608 | No | No |
| -20% | ¥14,626,948 | 0.684 | No | No |
| -30% | ¥12,798,580 | 0.781 | Yes | No |
| -40% | ¥10,970,211 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 571
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
