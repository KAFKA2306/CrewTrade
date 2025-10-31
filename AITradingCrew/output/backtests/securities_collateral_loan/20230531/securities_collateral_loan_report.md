# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18285151
- Current loan ratio: 0.547
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.87% drop from current value
- Buffer to forced liquidation: 35.66% drop from current value
- Historical max drawdown (portfolio): -4.88%

## Optimization Summary
- Total ETFs evaluated: 132
- ETFs with sufficient data: 106
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 2634.T(ＮＥＸＴ　ＦＵＮＤＳ　Ｓ＆Ｐ　), 2514.T(ＮＥＸＴ　ＦＵＮＤＳ　外国株式), 2512.T(ＮＥＸＴ　ＦＵＮＤＳ　外国債券), 2648.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 2554.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 2563.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 2621.T(ｉシェアーズ　米国債２０年超　), 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 2632.T(ＭＡＸＩＳナスダック１００上場), 2630.T(ＭＡＸＩＳ米国株式（Ｓ＆Ｐ５０), 2623.T(ｉシェアーズ　ユーロ建て投資適), 2569.T(上場インデックスファンド米国株), 2521.T(上場インデックスファンド米国株), 2562.T(上場インデックスファンド米国株), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1545.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤ), 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1655.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 2620.T(ｉシェアーズ　米国債１－３年　), 1656.T(ｉシェアーズ・コア　米国債７－), 2530.T(ＭＡＸＩＳ　ＨｕａＡｎ中国株式), 2631.T(ＭＡＸＩＳナスダック１００上場), 1671.T(ＷＴＩ原油価格連動型上場投信), 2568.T(上場インデックスファンド米国株)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 12.46%, volatility 9.23%, Sharpe 1.350, expense 0.24%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2020-06-01 to 2023-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 12.46% | - | - |
| Annual Volatility | 9.23% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.350 | - | - |
| Weighted Expense Ratio | 0.24% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.46% | 9.23% | 1.350 | 0.24% | Yes |
| low_volatility | 9.03% | 7.35% | 1.229 | 0.19% |  |
| cost_focus | 11.33% | 9.17% | 1.235 | 0.24% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 18.28% | 13.85% | 1.319 | N/A | 9.524 |
| 2 | 1478.T | ｉシェアーズ　ＭＳＣＩ　ジャパン高配当利回り　ＥＴＦ | 13.81% | 14.23% | 0.970 | 0.19% | 6.815 |
| 3 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 16.35% | 15.57% | 1.050 | 0.28% | 6.740 |
| 4 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 13.66% | 14.56% | 0.938 | 0.28% | 6.441 |
| 5 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 28.83% | 21.21% | 1.360 | 0.32% | 6.411 |
| 6 | 1651.T | ｉＦｒｅｅＥＴＦ　ＴＯＰＩＸ高配当４０指数 | 15.98% | 15.86% | 1.008 | 0.19% | 6.353 |
| 7 | 1494.T | Ｏｎｅ　ＥＴＦ　高配当日本株 | 11.69% | 15.12% | 0.773 | 0.28% | 5.111 |
| 8 | 1631.T | ＮＥＸＴ　ＦＵＮＤＳ　銀行（ＴＯＰＩＸ－１７）上場投信 | 24.14% | 22.57% | 1.070 | 0.32% | 4.739 |
| 9 | 2647.T | ＮＥＸＴ　ＦＵＮＤＳ　ブルームバーグ米国国債（７－１０年）イ | 4.59% | 9.87% | 0.465 | 0.13% | 4.712 |
| 10 | 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | 24.44% | 22.82% | 1.071 | 0.19% | 4.693 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| その他 | 3 | ¥6,770,760 | 37.0% |
| コモディティ | 1 | ¥4,836,616 | 26.5% |
| 国内株式 | 1 | ¥3,227,092 | 17.6% |
| 国内セクター | 2 | ¥2,230,800 | 12.2% |
| 債券 | 1 | ¥1,219,883 | 6.7% |

### Top Holdings (out of 8 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 712 | ¥6793.00 | ¥4836616 | 26.5% | N/A | 18.28% | 13.85% | 1.319 |
| 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 2066 | ¥1562.00 | ¥3227092 | 17.6% | 0.28% | 16.35% | 15.57% | 1.050 |
| 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 2378 | ¥1325.00 | ¥3150850 | 17.2% | 0.28% | 10.70% | 15.75% | 0.680 |
| 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 70 | ¥33650.00 | ¥2355500 | 12.9% | 0.22% | 5.69% | 16.24% | 0.351 |
| 1481.T | 上場インデックスファンド日本経済貢献株 | 567 | ¥2230.00 | ¥1264410 | 6.9% | 0.15% | 7.43% | 16.61% | 0.447 |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 37 | ¥33000.00 | ¥1221000 | 6.7% | 0.32% | 9.92% | 14.54% | 0.682 |
| 2647.T | ＮＥＸＴ　ＦＵＮＤＳ　ブルームバーグ米国国債（７－１０年）インデックス（為替ヘッ | 229 | ¥5327.00 | ¥1219883 | 6.7% | 0.13% | 4.59% | 9.87% | 0.465 |
| 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 | 51 | ¥19800.00 | ¥1009800 | 5.5% | 0.32% | 12.54% | 23.06% | 0.544 |

*Total: 8 ETFs, Portfolio value: ¥18,285,151*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2020 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 2.57% | 22.04% | 0.116 |
| 2020 | 1481.T | 上場インデックスファンド日本経済貢献株 | 17.24% | 15.15% | 1.138 |
| 2020 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 16.23% | 22.05% | 0.736 |
| 2020 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 7.37% | 16.87% | 0.437 |
| 2020 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -0.77% | 17.76% | -0.043 |
| 2020 | 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 | 21.03% | 31.91% | 0.659 |
| 2020 | 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 8.75% | 18.24% | 0.480 |
| 2021 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 4.62% | 12.50% | 0.370 |
| 2021 | 1481.T | 上場インデックスファンド日本経済貢献株 | 11.06% | 15.77% | 0.701 |
| 2021 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 2.63% | 19.60% | 0.134 |
| 2021 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 22.93% | 15.48% | 1.481 |
| 2021 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 3.86% | 14.95% | 0.258 |
| 2021 | 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 | 19.86% | 27.71% | 0.717 |
| 2021 | 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 17.24% | 15.20% | 1.134 |
| 2021 | 2647.T | ＮＥＸＴ　ＦＵＮＤＳ　ブルームバーグ米国国債（７－１０年）インデックス（為替ヘッ | 2.10% | 4.12% | 0.510 |
| 2022 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 15.10% | 14.71% | 1.026 |
| 2022 | 1481.T | 上場インデックスファンド日本経済貢献株 | -1.37% | 18.01% | -0.076 |
| 2022 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 7.78% | 16.96% | 0.459 |
| 2022 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 17.81% | 15.45% | 1.153 |
| 2022 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 4.09% | 15.64% | 0.261 |
| 2022 | 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 | 11.32% | 23.62% | 0.479 |
| 2022 | 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 6.24% | 16.93% | 0.369 |
| 2022 | 2647.T | ＮＥＸＴ　ＦＵＮＤＳ　ブルームバーグ米国国債（７－１０年）インデックス（為替ヘッ | -3.06% | 10.13% | -0.302 |
| 2023 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 12.93% | 11.98% | 1.079 |
| 2023 | 1481.T | 上場インデックスファンド日本経済貢献株 | 10.89% | 12.94% | 0.842 |
| 2023 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 3.86% | 15.50% | 0.249 |
| 2023 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 7.85% | 16.79% | 0.468 |
| 2023 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 12.72% | 11.37% | 1.119 |
| 2023 | 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 | 13.11% | 22.34% | 0.587 |
| 2023 | 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 11.16% | 12.53% | 0.890 |
| 2023 | 2647.T | ＮＥＸＴ　ＦＵＮＤＳ　ブルームバーグ米国国債（７－１０年）インデックス（為替ヘッ | 7.64% | 11.00% | 0.694 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2020 | 8.22% | 11.67% | 0.704 |
| 2021 | 20.06% | 13.62% | 1.473 |
| 2022 | 9.38% | 9.67% | 0.970 |
| 2023 | 9.97% | 8.05% | 1.239 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2023-06-01 to 2024-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 563.86% |
| Annualized Return | 600.75% |
| Annualized Volatility | 520.33% ⚠️ (Exceeds constraint) |
| Max Drawdown | -17.63% |
| Sharpe Ratio | 1.155 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 12.46% | 600.75% | +588.29% | ⚠️ |
| Annual Volatility | 9.23% | 520.33% | +511.11% | ⚠️ BREACH |
| Sharpe Ratio | 1.350 | 1.155 | -0.196 | ✓ |
| Max Drawdown | 0.00% | -17.63% | -17.63% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (520.33%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +5538.5% relative to backtest period.

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
| -10% | ¥16456636 | 0.608 | No | No |
| -20% | ¥14628121 | 0.684 | No | No |
| -30% | ¥12799606 | 0.781 | Yes | No |
| -40% | ¥10971091 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 329 days
- First breach: 2020-06-01
- Last breach: 2021-10-25
- Max ratio: 0.873

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-06-01 | 0.855 |
| 2020-06-02 | 0.850 |
| 2020-06-03 | 0.845 |
| 2020-06-04 | 0.847 |
| 2020-06-05 | 0.840 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2021-10-13 | 0.707 |
| 2021-10-14 | 0.705 |
| 2021-10-21 | 0.703 |
| 2021-10-22 | 0.706 |
| 2021-10-25 | 0.706 |

### Forced Liquidation Summary (>= 85%)
- Total events: 27 days
