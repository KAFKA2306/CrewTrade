# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 8
- Candidate universe after filtering: 6
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 56 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 8.81%
- Portfolio annual volatility: 11.73%
- Portfolio Sharpe ratio: 0.752
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.81% | 11.73% | 0.752 | 0.18% | Yes |
| low_volatility | 8.81% | 11.73% | 0.752 | 0.18% |  |
| cost_focus | 8.81% | 11.73% | 0.752 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18314479
- Current loan ratio: 0.546
- Buffer to 70%: 22.00% drop
- Buffer to 85%: 35.76% drop
- Max drawdown (history): -21.30%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,483,031 | 0.607 | No | No |
| -20% | ¥14,651,583 | 0.682 | No | No |
| -30% | ¥12,820,135 | 0.780 | Yes | No |
| -40% | ¥10,988,688 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 347
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
