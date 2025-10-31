# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 99
- ETFs with sufficient data: 78
- Candidate universe after filtering: 37
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 10
- Excluded 15 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 8.11%
- Portfolio annual volatility: 9.97%
- Portfolio Sharpe ratio: 0.813
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.11% | 9.97% | 0.813 | 0.23% | Yes |
| low_volatility | 9.49% | 12.05% | 0.787 | 0.23% |  |
| cost_focus | 16.95% | 13.95% | 1.215 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18255650
- Current loan ratio: 0.548
- Buffer to 70%: 21.75% drop
- Buffer to 85%: 35.56% drop
- Max drawdown (history): -16.93%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,430,085 | 0.609 | No | No |
| -20% | ¥14,604,520 | 0.685 | No | No |
| -30% | ¥12,778,955 | 0.782 | Yes | No |
| -40% | ¥10,953,390 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 395
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
