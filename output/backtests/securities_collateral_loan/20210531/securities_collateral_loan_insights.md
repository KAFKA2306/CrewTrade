# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 53
- Candidate universe after filtering: 26
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 11
- Excluded 11 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 9.11%
- Portfolio annual volatility: 12.77%
- Portfolio Sharpe ratio: 0.713
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.11% | 12.77% | 0.713 | 0.25% | Yes |
| low_volatility | 9.03% | 11.76% | 0.768 | 0.26% |  |
| cost_focus | 11.86% | 13.50% | 0.879 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18259470
- Current loan ratio: 0.548
- Buffer to 70%: 21.76% drop
- Buffer to 85%: 35.57% drop
- Max drawdown (history): -25.23%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,433,523 | 0.609 | No | No |
| -20% | ¥14,607,576 | 0.685 | No | No |
| -30% | ¥12,781,629 | 0.782 | Yes | No |
| -40% | ¥10,955,682 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 256
- Forced liquidation events: 1

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
