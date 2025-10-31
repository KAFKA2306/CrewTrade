# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 56
- Candidate universe after filtering: 27
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 20
- Excluded 14 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 4.56%
- Portfolio annual volatility: 12.55%
- Portfolio Sharpe ratio: 0.363
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.56% | 12.55% | 0.363 | 0.26% | Yes |
| low_volatility | 5.39% | 13.10% | 0.412 | 0.24% |  |
| cost_focus | 6.71% | 11.67% | 0.575 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18160165
- Current loan ratio: 0.551
- Buffer to 70%: 21.33% drop
- Buffer to 85%: 35.22% drop
- Max drawdown (history): -30.60%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,344,148 | 0.612 | No | No |
| -20% | ¥14,528,132 | 0.688 | No | No |
| -30% | ¥12,712,116 | 0.787 | Yes | No |
| -40% | ¥10,896,099 | 0.918 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 13
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
