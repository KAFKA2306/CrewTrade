# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18277365
- Current loan ratio: 0.547
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.84% drop from current value
- Buffer to forced liquidation: 35.63% drop from current value
- Historical max drawdown (portfolio): -8.09%

## Optimization Summary
- Total ETFs evaluated: 156
- ETFs with sufficient data: 122
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 2845.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤ), 2634.T(ＮＥＸＴ　ＦＵＮＤＳ　Ｓ＆Ｐ　), 2514.T(ＮＥＸＴ　ＦＵＮＤＳ　外国株式), 2512.T(ＮＥＸＴ　ＦＵＮＤＳ　外国債券), 2846.T(ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジ), 2860.T(ＮＥＸＴ　ＦＵＮＤＳ　ドイツ株), 2648.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 2554.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 2859.T(ＮＥＸＴ　ＦＵＮＤＳ　ユーロ・), 2841.T(ｉＦｒｅｅＥＴＦ　ＮＡＳＤＡＱ), 2563.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 2853.T(ｉシェアーズ　気候リスク調整世), 2857.T(ｉシェアーズ　ドイツ国債　ＥＴ), 2621.T(ｉシェアーズ　米国債２０年超　), 2856.T(ｉシェアーズ　米国債３－７年　), 2649.T(ｉシェアーズ　米国政府系機関ジ), 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 2632.T(ＭＡＸＩＳナスダック１００上場), 2630.T(ＭＡＸＩＳ米国株式（Ｓ＆Ｐ５０), 2839.T(ＭＡＸＩＳ米国国債７－１０年上), 2623.T(ｉシェアーズ　ユーロ建て投資適), 2843.T(上場インデックスファンド豪州国), 2862.T(上場インデックスファンドフラン), 2569.T(上場インデックスファンド米国株), 2521.T(上場インデックスファンド米国株), 2562.T(上場インデックスファンド米国株), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 2633.T(ＮＥＸＴ　ＦＵＮＤＳ　Ｓ＆Ｐ　), 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1489.T(ＮＥＸＴ　ＦＵＮＤＳ　日経平均), 2620.T(ｉシェアーズ　米国債１－３年　), 1656.T(ｉシェアーズ・コア　米国債７－), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 22.06%, volatility 9.13%, Sharpe 2.417, expense 0.18%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2021-05-31 to 2024-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 22.06% | - | - |
| Annual Volatility | 9.13% | ≤ 15% | ✅ |
| Sharpe Ratio | 2.417 | - | - |
| Weighted Expense Ratio | 0.18% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 22.06% | 9.13% | 2.417 | 0.18% | Yes |
| low_volatility | 23.96% | 9.31% | 2.574 | 0.23% |  |
| cost_focus | 21.19% | 9.31% | 2.276 | 0.19% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 26.79% | 12.70% | 2.110 | N/A | 16.621 |
| 2 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 29.37% | 13.41% | 2.190 | 0.28% | 16.331 |
| 3 | 2559.T | ＭＡＸＩＳ全世界株式（オール・カントリー）上場投信 | 24.91% | 12.92% | 1.928 | 0.08% | 14.928 |
| 4 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 21.74% | 12.21% | 1.781 | 0.11% | 14.585 |
| 5 | 1478.T | ｉシェアーズ　ＭＳＣＩ　ジャパン高配当利回り　ＥＴＦ | 30.62% | 14.49% | 2.113 | 0.19% | 14.585 |
| 6 | 1494.T | Ｏｎｅ　ＥＴＦ　高配当日本株 | 28.29% | 14.15% | 1.999 | 0.28% | 14.130 |
| 7 | 1651.T | ｉＦｒｅｅＥＴＦ　ＴＯＰＩＸ高配当４０指数 | 35.27% | 15.82% | 2.229 | 0.19% | 14.086 |
| 8 | 1593.T | ＭＡＸＩＳ　ＪＰＸ日経インデックス４００上場投信 | 26.75% | 14.17% | 1.888 | 0.08% | 13.330 |
| 9 | 1577.T | ＮＥＸＴ　ＦＵＮＤＳ　野村日本株高配当７０連動型上場投信 | 30.41% | 15.20% | 2.001 | 0.32% | 13.167 |
| 10 | 2529.T | ＮＥＸＴ　ＦＵＮＤＳ　野村株主還元７０連動型上場投信 | 24.30% | 13.84% | 1.756 | 0.28% | 12.686 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| その他 | 2 | ¥5,670,407 | 31.0% |
| コモディティ | 2 | ¥4,857,210 | 26.6% |
| 国内株式 | 1 | ¥3,724,435 | 20.4% |
| 海外株式 | 1 | ¥2,170,305 | 11.9% |
| 債券 | 1 | ¥1,855,008 | 10.1% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1480.T | ＮＥＸＴ　ＦＵＮＤＳ　野村企業価値分配指数連動型上場投信 | 150 | ¥27925.00 | ¥4188750 | 22.9% | 0.23% | 25.58% | 16.32% | 1.567 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 420 | ¥9012.00 | ¥3785040 | 20.7% | N/A | 26.79% | 12.70% | 2.110 |
| 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | 143 | ¥26045.00 | ¥3724435 | 20.4% | 0.04% | 26.96% | 15.20% | 1.774 |
| 2564.T | グローバルＸ　ＭＳＣＩスーパーディビィデンド－日本株式　ＥＴＦ | 765 | ¥2837.00 | ¥2170305 | 11.9% | 0.39% | 23.21% | 15.93% | 1.456 |
| 2861.T | 上場インデックスファンドフランス国債（為替ヘッジなし） | 339 | ¥5472.00 | ¥1855008 | 10.1% | 0.11% | 10.47% | 11.23% | 0.932 |
| 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 653 | ¥2269.00 | ¥1481657 | 8.1% | 0.11% | 21.74% | 12.21% | 1.781 |
| 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | 2970 | ¥361.00 | ¥1072170 | 5.9% | 0.19% | 51.73% | 23.90% | 2.164 |

*Total: 7 ETFs, Portfolio value: ¥18,277,365*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2021 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -1.77% | 12.33% | -0.143 |
| 2021 | 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | 3.65% | 16.33% | 0.223 |
| 2021 | 1480.T | ＮＥＸＴ　ＦＵＮＤＳ　野村企業価値分配指数連動型上場投信 | 4.31% | 14.71% | 0.293 |
| 2021 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 1.91% | 15.76% | 0.121 |
| 2021 | 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | -1.10% | 19.74% | -0.056 |
| 2021 | 2564.T | グローバルＸ　ＭＳＣＩスーパーディビィデンド－日本株式　ＥＴＦ | 1.95% | 12.85% | 0.152 |
| 2022 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 15.10% | 14.71% | 1.026 |
| 2022 | 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | -4.98% | 18.76% | -0.265 |
| 2022 | 1480.T | ＮＥＸＴ　ＦＵＮＤＳ　野村企業価値分配指数連動型上場投信 | -6.69% | 19.11% | -0.350 |
| 2022 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | -7.77% | 14.32% | -0.543 |
| 2022 | 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | 33.09% | 20.72% | 1.597 |
| 2022 | 2564.T | グローバルＸ　ＭＳＣＩスーパーディビィデンド－日本株式　ＥＴＦ | 8.99% | 15.57% | 0.577 |
| 2022 | 2861.T | 上場インデックスファンドフランス国債（為替ヘッジなし） | -7.00% | 17.65% | -0.397 |
| 2023 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 19.93% | 11.19% | 1.782 |
| 2023 | 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | 26.62% | 14.75% | 1.804 |
| 2023 | 1480.T | ＮＥＸＴ　ＦＵＮＤＳ　野村企業価値分配指数連動型上場投信 | 24.55% | 14.57% | 1.685 |
| 2023 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 21.83% | 12.21% | 1.788 |
| 2023 | 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | 29.01% | 26.01% | 1.115 |
| 2023 | 2564.T | グローバルＸ　ＭＳＣＩスーパーディビィデンド－日本株式　ＥＴＦ | 24.94% | 15.75% | 1.584 |
| 2023 | 2861.T | 上場インデックスファンドフランス国債（為替ヘッジなし） | 14.75% | 9.56% | 1.544 |
| 2024 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 24.92% | 15.13% | 1.647 |
| 2024 | 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | 17.14% | 15.41% | 1.112 |
| 2024 | 1480.T | ＮＥＸＴ　ＦＵＮＤＳ　野村企業価値分配指数連動型上場投信 | 18.13% | 18.03% | 1.005 |
| 2024 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 14.54% | 12.55% | 1.159 |
| 2024 | 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 | 38.05% | 20.53% | 1.854 |
| 2024 | 2564.T | グローバルＸ　ＭＳＣＩスーパーディビィデンド－日本株式　ＥＴＦ | 10.82% | 14.15% | 0.764 |
| 2024 | 2861.T | 上場インデックスファンドフランス国債（為替ヘッジなし） | 2.55% | 8.29% | 0.307 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2021 | 2.09% | 10.90% | 0.191 |
| 2022 | 16.12% | 18.84% | 0.855 |
| 2023 | 22.86% | 8.20% | 2.788 |
| 2024 | 17.21% | 9.40% | 1.832 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2024-06-03 to 2025-05-30 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | -13.39% |
| Annualized Return | -13.90% |
| Annualized Volatility | 26.38% ⚠️ (Exceeds constraint) |
| Max Drawdown | -27.16% |
| Sharpe Ratio | -0.527 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 22.06% | -13.90% | -35.96% | ⚠️ |
| Annual Volatility | 9.13% | 26.38% | +17.25% | ⚠️ BREACH |
| Sharpe Ratio | 2.417 | -0.527 | -2.944 | ⚠️ |
| Max Drawdown | 0.00% | -27.16% | -27.16% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (26.38%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +189.0% relative to backtest period.

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
| -10% | ¥16449628 | 0.608 | No | No |
| -20% | ¥14621892 | 0.684 | No | No |
| -30% | ¥12794156 | 0.782 | Yes | No |
| -40% | ¥10966419 | 0.912 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 492 days
- First breach: 2021-05-31
- Last breach: 2023-06-01
- Max ratio: 0.967

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2021-05-31 | 0.934 |
| 2021-06-01 | 0.937 |
| 2021-06-02 | 0.933 |
| 2021-06-03 | 0.926 |
| 2021-06-04 | 0.932 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2023-05-26 | 0.708 |
| 2023-05-29 | 0.705 |
| 2023-05-30 | 0.705 |
| 2023-05-31 | 0.707 |
| 2023-06-01 | 0.706 |

### Forced Liquidation Summary (>= 85%)
- Total events: 294 days
