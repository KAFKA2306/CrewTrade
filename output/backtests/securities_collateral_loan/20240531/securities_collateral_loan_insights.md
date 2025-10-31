# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 99
- ETFs with sufficient data: 80
- Candidate universe after filtering: 38
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 11
- Excluded 13 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 15.25%
- Portfolio annual volatility: 11.77%
- Portfolio Sharpe ratio: 1.295
- Weighted expense ratio: 0.20%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.25% | 11.77% | 1.295 | 0.20% | Yes |
| low_volatility | 14.71% | 11.52% | 1.276 | 0.20% |  |
| cost_focus | 19.39% | 14.53% | 1.335 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18250992
- Current loan ratio: 0.548
- Buffer to 70%: 21.73% drop
- Buffer to 85%: 35.54% drop
- Max drawdown (history): -19.04%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,425,893 | 0.609 | No | No |
| -20% | ¥14,600,793 | 0.685 | No | No |
| -30% | ¥12,775,694 | 0.783 | Yes | No |
| -40% | ¥10,950,595 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 969
- Forced liquidation events: 418

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
