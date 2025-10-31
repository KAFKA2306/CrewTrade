# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 37
- Candidate universe after filtering: 24
- Selected ETFs (max_sharpe): 7
- Excluded 3 ETF(s) with volatility > 35.0%
- Excluded 11 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 10.60%
- Portfolio annual volatility: 13.75%
- Portfolio Sharpe ratio: 0.771
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.60% | 13.75% | 0.771 | 0.23% | Yes |
| low_volatility | 7.16% | 10.01% | 0.715 | 0.21% |  |
| cost_focus | 8.18% | 11.25% | 0.727 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18292737
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.69% drop
- Max drawdown (history): -17.75%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,463,463 | 0.607 | No | No |
| -20% | ¥14,634,190 | 0.683 | No | No |
| -30% | ¥12,804,916 | 0.781 | Yes | No |
| -40% | ¥10,975,642 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 262
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
