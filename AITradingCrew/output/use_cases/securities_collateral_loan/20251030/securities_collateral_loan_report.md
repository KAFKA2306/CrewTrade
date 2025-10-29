# Securities Collateral Loan Risk Report

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18172884
- Current loan ratio: 0.550
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.39% drop from current value
- Buffer to forced liquidation: 35.26% drop from current value
- Historical max drawdown (portfolio): -2.83%

## Collateral Breakdown
| Ticker | Description | Quantity | Price | Market Value |
| --- | --- | --- | --- | --- |
| 1489.T | Nikkei High Dividend Yield 50 ETF | 194 | ¥2565.00 | ¥497610 |
| 1306.T | TOPIX ETF | 202 | ¥3438.00 | ¥694476 |
| 2568.T | GX US Treasury 7-10 ETF | 45 | ¥6832.00 | ¥307440 |
| 2510.T | JGB 3-10Y ETF | 18469 | ¥858.00 | ¥15846402 |
| 2622.T | J-REIT ETF | 48 | ¥1777.00 | ¥85296 |
| 348A.T | Yomiuri 333 ETF | 3156 | ¥235.00 | ¥741660 |

## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16355596 | 0.611 | No | No |
| -20% | ¥14538307 | 0.688 | No | No |
| -30% | ¥12721019 | 0.786 | Yes | No |
| -40% | ¥10903730 | 0.917 | Yes | Yes |

## Historical Breaches
No historical instances exceeded Rakuten Securities thresholds within the observation window.
## Notes
- Loan ratio is calculated as outstanding balance divided by collateral market value.
- Rakuten Securities/Rakuten Bank requires top-up within 2 business days once the ratio reaches 70%, and may liquidate collateral immediately at 85%+.
- Borrowing limit is capped at approximately 60% of collateral value; ensure new acquisitions keep the loan ratio below 0.60 after execution.
- Interest is estimated on a simple basis and excludes taxes or transaction costs.
