# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 62
- ETFs with sufficient data: 46
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 6
- Excluded 15 ETF(s) with volatility > 25.0%
- Excluded 1 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 4.62%
- Portfolio annual volatility: 10.05%
- Portfolio Sharpe ratio: 0.460
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.62% | 10.05% | 0.460 | 0.25% | Yes |
| low_volatility | 4.25% | 10.01% | 0.424 | 0.24% |  |
| cost_focus | 4.73% | 12.27% | 0.385 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18309449
- Current loan ratio: 0.546
- Buffer to 70%: 21.98% drop
- Buffer to 85%: 35.75% drop
- Max drawdown (history): -13.61%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,478,504 | 0.607 | No | No |
| -20% | ¥14,647,559 | 0.683 | No | No |
| -30% | ¥12,816,614 | 0.780 | Yes | No |
| -40% | ¥10,985,669 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
