# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 70
- ETFs with sufficient data: 10
- Candidate universe after filtering: 10
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 10
- Excluded 58 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 12.10%
- Portfolio annual volatility: 10.07%
- Portfolio Sharpe ratio: 1.202
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.10% | 10.07% | 1.202 | 0.17% | Yes |
| low_volatility | 12.10% | 10.07% | 1.202 | 0.17% |  |
| cost_focus | 12.10% | 10.07% | 1.202 | 0.17% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18247381
- Current loan ratio: 0.548
- Buffer to 70%: 21.71% drop
- Buffer to 85%: 35.53% drop
- Max drawdown (history): -16.59%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,422,643 | 0.609 | No | No |
| -20% | ¥14,597,905 | 0.685 | No | No |
| -30% | ¥12,773,167 | 0.783 | Yes | No |
| -40% | ¥10,948,429 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 2488
- Forced liquidation events: 2273

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
