# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 17
- Candidate universe after filtering: 8
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 8
- Excluded 17 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: -2.53%
- Portfolio annual volatility: 13.21%
- Portfolio Sharpe ratio: -0.192
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | -2.53% | 13.21% | -0.192 | 0.27% | Yes |
| low_volatility | -2.53% | 13.21% | -0.192 | 0.27% |  |
| cost_focus | -2.53% | 13.21% | -0.192 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18936125
- Current loan ratio: 0.528
- Buffer to 70%: 24.56% drop
- Buffer to 85%: 37.87% drop
- Max drawdown (history): -18.21%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥17,042,513 | 0.587 | No | No |
| -20% | ¥15,148,900 | 0.660 | No | No |
| -30% | ¥13,255,288 | 0.754 | Yes | No |
| -40% | ¥11,361,675 | 0.880 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 49
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
