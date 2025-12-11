# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18301637
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.94% drop from current value
- Buffer to forced liquidation: 35.72% drop from current value
- Historical max drawdown (portfolio): -29.65%

## Optimization Summary
- Total ETFs evaluated: 32
- ETFs with sufficient data: 22
- Candidate universe after correlation filter: 7 (threshold 0.90)
- Excluded ETFs: 0 hedged, 0 high-volatility, 10 deep-drawdown
- Selected profile: max_sharpe

### Portfolio Variants
| Variant | Optimization Strategy | Annual Return | Annual Volatility | Sharpe | Kelly (r/σ²) |
| --- | --- | --- | --- | --- | --- |
| Max Sharpe Portfolio | max_sharpe | 3.26% | 15.20% | 0.215 | 1.413 |
| Minimum-Variance Portfolio | min_variance | 3.26% | 15.20% | 0.215 | 1.413 |
| Max Kelly Criterion Portfolio | max_kelly | 3.26% | 15.20% | 0.215 | 1.413 |

**Max Sharpe Portfolio Holdings (max_sharpe)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1628.T | 14.29% | 14.28% | 404 | ¥6,470 | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 |
| 1329.T | 14.29% | 14.30% | 357 | ¥7,331 | ｉシェアーズ・コア　日経２２５　ＥＴＦ |
| 1617.T | 14.29% | 14.26% | 260 | ¥10,036 | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 |
| 1619.T | 14.29% | 14.27% | 343 | ¥7,615 | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 |
| 1621.T | 14.29% | 14.28% | 341 | ¥7,665 | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 |
| 1343.T | 14.29% | 14.31% | 3686 | ¥710 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1328.T | 14.29% | 14.30% | 716 | ¥3,655 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |

**Minimum-Variance Portfolio Holdings (min_variance)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1628.T | 14.29% | 14.28% | 404 | ¥6,470 | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 |
| 1329.T | 14.29% | 14.30% | 357 | ¥7,331 | ｉシェアーズ・コア　日経２２５　ＥＴＦ |
| 1617.T | 14.29% | 14.26% | 260 | ¥10,036 | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 |
| 1619.T | 14.29% | 14.27% | 343 | ¥7,615 | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 |
| 1621.T | 14.29% | 14.28% | 341 | ¥7,665 | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 |
| 1343.T | 14.29% | 14.31% | 3686 | ¥710 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1328.T | 14.29% | 14.30% | 716 | ¥3,655 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |

**Max Kelly Criterion Portfolio Holdings (max_kelly)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1628.T | 14.29% | 14.28% | 404 | ¥6,470 | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 |
| 1329.T | 14.29% | 14.30% | 357 | ¥7,331 | ｉシェアーズ・コア　日経２２５　ＥＴＦ |
| 1617.T | 14.29% | 14.26% | 260 | ¥10,036 | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 |
| 1619.T | 14.29% | 14.27% | 343 | ¥7,615 | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 |
| 1621.T | 14.29% | 14.28% | 341 | ¥7,665 | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 |
| 1343.T | 14.29% | 14.31% | 3686 | ¥710 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1328.T | 14.29% | 14.30% | 716 | ¥3,655 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |

### Filter Diagnostics
- Applied Asset Filters: max drawdown ≥ -30.0%

**Removed for deep drawdown**
| Ticker | Name |
| --- | --- |
| 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 |
| 1631.T | ＮＥＸＴ　ＦＵＮＤＳ　銀行（ＴＯＰＩＸ－１７）上場投信 |
| 1632.T | ＮＥＸＴ　ＦＵＮＤＳ　金融（除く銀行）（ＴＯＰＩＸ－１７）上場投信 |
| 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 |
| 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 |
| 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 |
| 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 |
| 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 |
| 1633.T | ＮＥＸＴ　ＦＵＮＤＳ　不動産（ＴＯＰＩＸ－１７）上場投信 |
| 1671.T | ＷＴＩ原油価格連動型上場投信 |

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2008-04-04 to 2011-05-31 (3.2 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 3.26% | - | - |
| Annual Volatility | 15.20% | ≤ 12% | ❌ |
| Sharpe Ratio | 0.215 | - | - |
| Weighted Expense Ratio | 0.25% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 3.26% | 15.20% | 0.215 | 0.25% | Yes |
| low_volatility | 3.26% | 15.20% | 0.215 | 0.25% |  |
| cost_focus | 3.26% | 15.20% | 0.215 | 0.25% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1311.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ　Ｃｏｒｅ　３０連動型上場投 | -5.78% | 21.01% | -0.275 | 0.19% | 0.637 |
| 2 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -11.28% | 18.51% | -0.610 | 0.32% | 0.619 |
| 3 | 1305.T | ｉＦｒｅｅＥＴＦ　ＴＯＰＩＸ（年１回決算型） | -3.22% | 19.75% | -0.163 | 0.06% | 0.569 |
| 4 | 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | 0.29% | 23.20% | 0.013 | 0.04% | 0.562 |
| 5 | 1348.T | ＭＡＸＩＳ　トピックス上場投信 | -3.28% | 20.20% | -0.163 | 0.06% | 0.562 |
| 6 | 1308.T | 上場インデックスファンドＴＯＰＩＸ | -3.00% | 20.29% | -0.148 | 0.05% | 0.556 |
| 7 | 1306.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ連動型上場投信 | -2.88% | 20.36% | -0.141 | 0.05% | 0.550 |
| 8 | 1622.T | ＮＥＸＴ　ＦＵＮＤＳ　自動車・輸送機（ＴＯＰＩＸ－１７）上場 | 1.52% | 26.14% | 0.058 | 0.32% | 0.488 |
| 9 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -0.82% | 19.40% | -0.042 | 0.32% | 0.463 |
| 10 | 1330.T | 上場インデックスファンド２２５ | 0.55% | 22.14% | 0.025 | 0.09% | 0.456 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 3 | ¥7,837,085 | 42.8% |
| 国内株式 | 2 | ¥5,235,680 | 28.6% |
| コモディティ | 1 | ¥2,616,980 | 14.3% |
| その他 | 1 | ¥2,611,892 | 14.3% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 3686 | ¥710.43 | ¥2618639 | 14.3% | 0.15% | 6.41% | 18.46% | 0.347 |
| 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | 357 | ¥7330.65 | ¥2617041 | 14.3% | 0.04% | 0.29% | 23.20% | 0.013 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 716 | ¥3655.00 | ¥2616980 | 14.3% | N/A | 20.58% | 17.10% | 1.203 |
| 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 404 | ¥6470.47 | ¥2614071 | 14.3% | 0.32% | -11.28% | 18.51% | -0.610 |
| 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 341 | ¥7664.83 | ¥2613706 | 14.3% | 0.32% | -0.49% | 15.02% | -0.033 |
| 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 343 | ¥7614.85 | ¥2611892 | 14.3% | 0.32% | 2.53% | 22.88% | 0.110 |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 260 | ¥10035.80 | ¥2609307 | 14.3% | 0.32% | -0.82% | 19.40% | -0.042 |

*Total: 7 ETFs, Portfolio value: ¥18,301,637*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2008 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -21.62% | 75.34% | -0.287 |
| 2008 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -23.68% | 35.93% | -0.659 |
| 2008 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | -26.25% | 48.47% | -0.542 |
| 2008 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -9.87% | 40.94% | -0.241 |
| 2008 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -19.65% | 30.80% | -0.638 |
| 2009 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 19.80% | 22.78% | 0.869 |
| 2009 | 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | 16.32% | 27.24% | 0.599 |
| 2009 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 0.18% | 26.34% | 0.007 |
| 2009 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 2.64% | 20.34% | 0.130 |
| 2009 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 8.61% | 26.47% | 0.325 |
| 2009 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -9.84% | 20.27% | -0.485 |
| 2009 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -17.70% | 19.43% | -0.911 |
| 2010 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 11.35% | 16.22% | 0.700 |
| 2010 | 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | -2.65% | 19.53% | -0.136 |
| 2010 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 27.24% | 15.50% | 1.757 |
| 2010 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -11.30% | 17.14% | -0.659 |
| 2010 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | -0.53% | 20.63% | -0.025 |
| 2010 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -5.03% | 14.46% | -0.348 |
| 2010 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -3.74% | 15.78% | -0.237 |
| 2011 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 9.60% | 16.95% | 0.566 |
| 2011 | 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | -4.58% | 29.96% | -0.153 |
| 2011 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -5.78% | 22.66% | -0.255 |
| 2011 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 0.62% | 25.85% | 0.024 |
| 2011 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 4.61% | 28.55% | 0.162 |
| 2011 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -0.67% | 16.67% | -0.040 |
| 2011 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -10.71% | 24.90% | -0.430 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2008 | -5.15% | 39.95% | -0.129 |
| 2009 | 30.36% | 34.11% | 0.890 |
| 2010 | 0.91% | 12.79% | 0.071 |
| 2011 | -1.39% | 19.42% | -0.071 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2011-05-31 to 2012-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | -6.81% |
| Annualized Return | -6.79% |
| Annualized Volatility | 10.80% |
| Max Drawdown | -11.92% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 3.26% | -6.79% | -10.06% | ⚠️ |
| Annual Volatility | 15.20% | 10.80% | -4.40% | ✓ |
| Max Drawdown | 0.00% | -11.92% | -11.92% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

Forward volatility changed by -28.9% relative to backtest period.

This demonstrates that **historical constraints do NOT guarantee future compliance**.
Market regime changes can significantly alter risk characteristics.


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16471473 | 0.607 | No | No |
| -20% | ¥14641309 | 0.683 | No | No |
| -30% | ¥12811146 | 0.781 | Yes | No |
| -40% | ¥10980982 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 59 days
- First breach: 2008-07-15
- Last breach: 2008-12-30
- Max ratio: 0.840

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2008-07-15 | 0.703 |
| 2008-07-18 | 0.701 |
| 2008-09-11 | 0.706 |
| 2008-09-12 | 0.700 |
| 2008-10-08 | 0.719 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2008-12-24 | 0.727 |
| 2008-12-25 | 0.721 |
| 2008-12-26 | 0.716 |
| 2008-12-29 | 0.713 |
| 2008-12-30 | 0.709 |
