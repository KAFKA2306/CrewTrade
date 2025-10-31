# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 51
- Candidate universe after filtering: 24
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 10
- Excluded 13 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 10.64%
- Portfolio annual volatility: 13.67%
- Portfolio Sharpe ratio: 0.778
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.64% | 13.67% | 0.778 | 0.24% | Yes |
| low_volatility | 7.67% | 13.81% | 0.556 | 0.26% |  |
| cost_focus | 11.76% | 13.81% | 0.852 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18222105
- Current loan ratio: 0.549
- Buffer to 70%: 21.60% drop
- Buffer to 85%: 35.44% drop
- Max drawdown (history): -27.36%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,399,894 | 0.610 | No | No |
| -20% | ¥14,577,684 | 0.686 | No | No |
| -30% | ¥12,755,474 | 0.784 | Yes | No |
| -40% | ¥10,933,263 | 0.915 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 499
- Forced liquidation events: 42

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
