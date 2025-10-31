# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 103
- ETFs with sufficient data: 32
- Candidate universe after filtering: 25
- Selected ETFs (max_sharpe): 7
- Excluded 32 ETF(s) with volatility > 25.0%
- Excluded 32 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 9.37%
- Portfolio annual volatility: 9.06%
- Portfolio Sharpe ratio: 1.034
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.37% | 9.06% | 1.034 | 0.17% | Yes |
| low_volatility | 7.77% | 7.80% | 0.996 | 0.17% |  |
| cost_focus | 7.09% | 7.85% | 0.904 | 0.18% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18291850
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -10.71%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,462,665 | 0.607 | No | No |
| -20% | ¥14,633,480 | 0.683 | No | No |
| -30% | ¥12,804,295 | 0.781 | Yes | No |
| -40% | ¥10,975,110 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
