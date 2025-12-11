# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 43
- ETFs with sufficient data: 28
- Candidate universe after filtering: 12
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 12
- Excluded 15 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 10.51%
- Portfolio annual volatility: 11.95%
- Portfolio Sharpe ratio: 0.879
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.51% | 11.95% | 0.879 | 0.27% | Yes |
| low_volatility | 10.51% | 11.95% | 0.879 | 0.27% |  |
| cost_focus | 10.22% | 11.41% | 0.896 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18929137
- Current loan ratio: 0.528
- Buffer to 70%: 24.53% drop
- Buffer to 85%: 37.85% drop
- Max drawdown (history): -17.21%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥17,036,223 | 0.587 | No | No |
| -20% | ¥15,143,310 | 0.660 | No | No |
| -30% | ¥13,250,396 | 0.755 | Yes | No |
| -40% | ¥11,357,482 | 0.880 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 378
- Forced liquidation events: 74

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
