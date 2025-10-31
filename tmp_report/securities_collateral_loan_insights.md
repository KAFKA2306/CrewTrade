# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 6
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 4 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 16.08%
- Portfolio annual volatility: 14.15%
- Portfolio Sharpe ratio: 1.136
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 16.08% | 14.15% | 1.136 | 0.24% | Yes |
| low_volatility | 12.76% | 12.49% | 1.021 | 0.27% |  |
| cost_focus | 17.14% | 14.90% | 1.150 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18291545
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -16.98%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,462,390 | 0.607 | No | No |
| -20% | ¥14,633,236 | 0.683 | No | No |
| -30% | ¥12,804,082 | 0.781 | Yes | No |
| -40% | ¥10,974,927 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 672
- Forced liquidation events: 422

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
