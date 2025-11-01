# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 26
- Candidate universe after filtering: 11
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 11
- Excluded 15 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 18.53%
- Portfolio annual volatility: 14.96%
- Portfolio Sharpe ratio: 1.239
- Weighted expense ratio: 0.28%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.53% | 14.96% | 1.239 | 0.28% | Yes |
| low_volatility | 18.53% | 14.96% | 1.239 | 0.28% |  |
| cost_focus | 18.21% | 14.98% | 1.215 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18262368
- Current loan ratio: 0.548
- Buffer to 70%: 21.78% drop
- Buffer to 85%: 35.58% drop
- Max drawdown (history): -17.78%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,436,131 | 0.608 | No | No |
| -20% | ¥14,609,895 | 0.684 | No | No |
| -30% | ¥12,783,658 | 0.782 | Yes | No |
| -40% | ¥10,957,421 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 596
- Forced liquidation events: 214

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
