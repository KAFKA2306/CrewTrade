# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 98
- ETFs with sufficient data: 33
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 7
- Excluded 9 ETF(s) with volatility > 25.0%
- Excluded 50 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 14.95%
- Portfolio annual volatility: 10.19%
- Portfolio Sharpe ratio: 1.466
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.95% | 10.19% | 1.466 | 0.18% | Yes |
| low_volatility | 11.81% | 8.47% | 1.395 | 0.14% |  |
| cost_focus | 14.70% | 10.63% | 1.383 | 0.15% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18221402
- Current loan ratio: 0.549
- Buffer to 70%: 21.60% drop
- Buffer to 85%: 35.43% drop
- Max drawdown (history): -14.48%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,399,262 | 0.610 | No | No |
| -20% | ¥14,577,122 | 0.686 | No | No |
| -30% | ¥12,754,981 | 0.784 | Yes | No |
| -40% | ¥10,932,841 | 0.915 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 968
- Forced liquidation events: 390

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
