# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 20
- ETFs with sufficient data: 12
- Candidate universe after filtering: 12
- Selected ETFs (max_sharpe): 12
- Excluded 5 ETF(s) with volatility > 25.0%
- Portfolio annual return: -5.33%
- Portfolio annual volatility: 11.47%
- Portfolio Sharpe ratio: -0.464
- Weighted expense ratio: 0.20%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | -5.33% | 11.47% | -0.464 | 0.20% | Yes |
| low_volatility | -8.57% | 13.09% | -0.655 | 0.22% |  |
| cost_focus | -6.66% | 11.80% | -0.564 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18328405
- Current loan ratio: 0.546
- Buffer to 70%: 22.06% drop
- Buffer to 85%: 35.81% drop
- Max drawdown (history): -11.38%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,495,565 | 0.606 | No | No |
| -20% | ¥14,662,724 | 0.682 | No | No |
| -30% | ¥12,829,884 | 0.779 | Yes | No |
| -40% | ¥10,997,043 | 0.909 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 19
- Forced liquidation events: 17

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
