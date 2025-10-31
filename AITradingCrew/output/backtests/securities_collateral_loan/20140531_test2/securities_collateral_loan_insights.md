# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 7
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 17.28%
- Portfolio annual volatility: 13.49%
- Portfolio Sharpe ratio: 1.280
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 17.28% | 13.49% | 1.280 | 0.26% | Yes |
| low_volatility | 14.71% | 12.32% | 1.194 | 0.24% |  |
| cost_focus | 16.01% | 12.97% | 1.235 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18305292
- Current loan ratio: 0.546
- Buffer to 70%: 21.96% drop
- Buffer to 85%: 35.73% drop
- Max drawdown (history): -13.69%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,474,763 | 0.607 | No | No |
| -20% | ¥14,644,234 | 0.683 | No | No |
| -30% | ¥12,813,704 | 0.780 | Yes | No |
| -40% | ¥10,983,175 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 412
- Forced liquidation events: 184

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
