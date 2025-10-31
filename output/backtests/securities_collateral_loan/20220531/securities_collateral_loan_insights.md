# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 28
- Candidate universe after filtering: 21
- Selected ETFs (max_sharpe): 6
- Excluded 2 ETF(s) with volatility > 35.0%
- Excluded 40 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 10.21%
- Portfolio annual volatility: 10.95%
- Portfolio Sharpe ratio: 0.932
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.21% | 10.95% | 0.932 | 0.22% | Yes |
| low_volatility | 10.74% | 10.97% | 0.979 | 0.23% |  |
| cost_focus | 11.44% | 13.16% | 0.869 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18274560
- Current loan ratio: 0.547
- Buffer to 70%: 21.83% drop
- Buffer to 85%: 35.62% drop
- Max drawdown (history): -17.06%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,447,104 | 0.608 | No | No |
| -20% | ¥14,619,648 | 0.684 | No | No |
| -30% | ¥12,792,192 | 0.782 | Yes | No |
| -40% | ¥10,964,736 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 649
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
