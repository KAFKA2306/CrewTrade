# Securities Collateral Loan Risk Report

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18136749
- Current loan ratio: 0.551
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.23% drop from current value
- Buffer to forced liquidation: 35.13% drop from current value
- Historical max drawdown (portfolio): -3.00%

## Collateral Breakdown
| Ticker | Description | Quantity | Price | Market Value |
| --- | --- | --- | --- | --- |
| 1306.T | NEXT FUNDS TOPIX ETF | 73 | ¥3438.00 | ¥250974 |
| 2568.T | NASDAQ100 ETF (No Hedge) | 118 | ¥6832.00 | ¥806176 |
| 2510.T | NEXT FUNDS Domestic Bond NOMURA-BPI | 19302 | ¥858.00 | ¥16561116 |
| 2622.T | iShares USD Emerging Markets Bond Hedged | 159 | ¥1777.00 | ¥282543 |
| 348A.T | MAXIS Yomiuri 333 ETF | 1004 | ¥235.00 | ¥235940 |

## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16323074 | 0.613 | No | No |
| -20% | ¥14509399 | 0.689 | No | No |
| -30% | ¥12695724 | 0.788 | Yes | No |
| -40% | ¥10882049 | 0.919 | Yes | Yes |

## Historical Breaches
No historical instances exceeded Rakuten Securities thresholds within the observation window.
## Notes
- Loan ratio is calculated as outstanding balance divided by collateral market value.
- Rakuten Securities/Rakuten Bank requires top-up within 2 business days once the ratio reaches 70%, and may liquidate collateral immediately at 85%+.
- Borrowing limit is capped at approximately 60% of collateral value; ensure new acquisitions keep the loan ratio below 0.60 after execution.
- Interest is estimated on a simple basis and excludes taxes or transaction costs.
