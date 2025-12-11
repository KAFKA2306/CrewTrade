# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 31
- ETFs with sufficient data: 21
- Candidate universe after filtering: 8
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 9
- Excluded 10 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.18%
- Portfolio annual volatility: 14.41%
- Portfolio Sharpe ratio: 0.776
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.18% | 14.41% | 0.776 | 0.18% | Yes |
| low_volatility | 11.18% | 14.41% | 0.776 | 0.18% |  |
| cost_focus | 11.18% | 14.41% | 0.776 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18942576
- Current loan ratio: 0.528
- Buffer to 70%: 24.58% drop
- Buffer to 85%: 37.89% drop
- Max drawdown (history): -18.94%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥17,048,318 | 0.587 | No | No |
| -20% | ¥15,154,061 | 0.660 | No | No |
| -30% | ¥13,259,803 | 0.754 | Yes | No |
| -40% | ¥11,365,545 | 0.880 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 108
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
