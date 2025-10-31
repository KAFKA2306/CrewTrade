# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 34
- Candidate universe after filtering: 23
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 7 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 18.15%
- Portfolio annual volatility: 14.07%
- Portfolio Sharpe ratio: 1.290
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.15% | 14.07% | 1.290 | 0.25% | Yes |
| low_volatility | 14.14% | 12.11% | 1.167 | 0.27% |  |
| cost_focus | 18.23% | 14.95% | 1.219 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18291710
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -16.24%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,462,539 | 0.607 | No | No |
| -20% | ¥14,633,368 | 0.683 | No | No |
| -30% | ¥12,804,197 | 0.781 | Yes | No |
| -40% | ¥10,975,026 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 559
- Forced liquidation events: 197

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
