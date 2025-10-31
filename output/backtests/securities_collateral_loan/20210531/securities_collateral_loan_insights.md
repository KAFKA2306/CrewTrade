# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 51
- Candidate universe after filtering: 34
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 7
- Excluded 13 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 11.54%
- Portfolio annual volatility: 12.93%
- Portfolio Sharpe ratio: 0.893
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.54% | 12.93% | 0.893 | 0.21% | Yes |
| low_volatility | 11.18% | 12.46% | 0.897 | 0.23% |  |
| cost_focus | 12.23% | 13.01% | 0.940 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18285313
- Current loan ratio: 0.547
- Buffer to 70%: 21.87% drop
- Buffer to 85%: 35.66% drop
- Max drawdown (history): -21.69%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,456,782 | 0.608 | No | No |
| -20% | ¥14,628,250 | 0.684 | No | No |
| -30% | ¥12,799,719 | 0.781 | Yes | No |
| -40% | ¥10,971,188 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 748
- Forced liquidation events: 91

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
