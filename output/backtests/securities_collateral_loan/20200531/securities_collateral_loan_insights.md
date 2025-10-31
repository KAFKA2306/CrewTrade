# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 55
- ETFs with sufficient data: 39
- Candidate universe after filtering: 21
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 16 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 4.52%
- Portfolio annual volatility: 13.65%
- Portfolio Sharpe ratio: 0.331
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.52% | 13.65% | 0.331 | 0.26% | Yes |
| low_volatility | 5.43% | 12.97% | 0.419 | 0.25% |  |
| cost_focus | 4.14% | 13.20% | 0.314 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18295830
- Current loan ratio: 0.547
- Buffer to 70%: 21.92% drop
- Buffer to 85%: 35.70% drop
- Max drawdown (history): -23.02%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,466,247 | 0.607 | No | No |
| -20% | ¥14,636,664 | 0.683 | No | No |
| -30% | ¥12,807,081 | 0.781 | Yes | No |
| -40% | ¥10,977,498 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 240
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
