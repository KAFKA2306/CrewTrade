# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18323797
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.04% drop from current value
- Buffer to forced liquidation: 35.80% drop from current value
- Historical max drawdown (portfolio): -15.43%

## Optimization Summary
- Total ETFs evaluated: 121
- ETFs with sufficient data: 102
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 2514.T(ＮＥＸＴ　ＦＵＮＤＳ　外国株式), 2512.T(ＮＥＸＴ　ＦＵＮＤＳ　外国債券), 2554.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 2563.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 2621.T(ｉシェアーズ　米国債２０年超　), 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 2623.T(ｉシェアーズ　ユーロ建て投資適), 2569.T(上場インデックスファンド米国株), 2521.T(上場インデックスファンド米国株), 2562.T(上場インデックスファンド米国株), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1628.T(ＮＥＸＴ　ＦＵＮＤＳ　運輸・物), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1655.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 2567.T(ＮＺＡＭ　上場投信　Ｓ＆Ｐ／Ｊ), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 8.60%, volatility 6.93%, Sharpe 1.242, expense 0.16%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2019-05-31 to 2022-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 8.60% | - | - |
| Annual Volatility | 6.93% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.242 | - | - |
| Weighted Expense Ratio | 0.16% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.60% | 6.93% | 1.242 | 0.16% | Yes |
| low_volatility | 14.32% | 8.96% | 1.598 | 0.17% |  |
| cost_focus | 11.95% | 8.16% | 1.465 | 0.18% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2620.T | ｉシェアーズ　米国債１－３年　ＥＴＦ | 10.43% | 6.17% | 1.691 | 0.14% | 27.419 |
| 2 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 23.39% | 14.98% | 1.561 | 0.28% | 10.420 |
| 3 | 1489.T | ＮＥＸＴ　ＦＵＮＤＳ　日経平均高配当株５０指数連動型上場投信 | 26.95% | 16.11% | 1.673 | 0.28% | 10.385 |
| 4 | 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | 3.30% | 5.65% | 0.584 | 0.14% | 10.328 |
| 5 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 26.92% | 16.68% | 1.614 | 0.30% | 9.672 |
| 6 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数 | 30.83% | 18.00% | 1.713 | 0.17% | 9.516 |
| 7 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 25.90% | 16.51% | 1.569 | 0.15% | 9.502 |
| 8 | 1659.T | ｉシェアーズ　米国リート　ＥＴＦ | 33.22% | 18.95% | 1.753 | 0.20% | 9.251 |
| 9 | 1478.T | ｉシェアーズ　ＭＳＣＩ　ジャパン高配当利回り　ＥＴＦ | 20.55% | 15.14% | 1.357 | 0.19% | 8.964 |
| 10 | 1657.T | ｉシェアーズ・コア　ＭＳＣＩ　先進国株（除く日本）ＥＴＦ | 26.49% | 17.23% | 1.538 | 0.19% | 8.924 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| コモディティ | 1 | ¥5,868,720 | 32.0% |
| 債券 | 1 | ¥5,672,920 | 31.0% |
| 国内株式 | 2 | ¥4,338,972 | 23.7% |
| その他 | 1 | ¥1,343,655 | 7.3% |
| 海外株式 | 1 | ¥1,099,530 | 6.0% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 988 | ¥5940.00 | ¥5868720 | 32.0% | N/A | 10.30% | 13.92% | 0.740 |
| 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | 20841 | ¥272.20 | ¥5672920 | 31.0% | 0.14% | 3.30% | 5.65% | 0.584 |
| 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 1657 | ¥1595.00 | ¥2642915 | 14.4% | 0.10% | 11.02% | 15.98% | 0.690 |
| 2528.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ　Ｃｏｒｅ指数 | 1441 | ¥1177.00 | ¥1696057 | 9.3% | 0.20% | 12.55% | 15.53% | 0.808 |
| 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 807 | ¥1665.00 | ¥1343655 | 7.3% | 0.11% | 9.72% | 15.98% | 0.608 |
| 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 855 | ¥1286.00 | ¥1099530 | 6.0% | 0.17% | 30.83% | 18.00% | 1.713 |

*Total: 6 ETFs, Portfolio value: ¥18,323,797*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2019 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 14.63% | 13.14% | 1.114 |
| 2019 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 14.33% | 11.98% | 1.197 |
| 2019 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 3.10% | 23.21% | 0.134 |
| 2019 | 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | 2.84% | 4.07% | 0.698 |
| 2019 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 6.58% | 12.23% | 0.538 |
| 2019 | 2528.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ　Ｃｏｒｅ指数 | 10.81% | 27.09% | 0.399 |
| 2020 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 18.09% | 25.12% | 0.720 |
| 2020 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 6.20% | 22.39% | 0.277 |
| 2020 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 4.84% | 31.59% | 0.153 |
| 2020 | 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | 1.26% | 8.48% | 0.149 |
| 2020 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | -15.62% | 32.97% | -0.474 |
| 2020 | 2528.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ　Ｃｏｒｅ指数 | -17.29% | 37.85% | -0.457 |
| 2021 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 4.62% | 12.50% | 0.370 |
| 2021 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 10.15% | 14.90% | 0.681 |
| 2021 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 10.05% | 15.46% | 0.650 |
| 2021 | 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | 6.15% | 4.99% | 1.233 |
| 2021 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 46.34% | 15.59% | 2.973 |
| 2021 | 2528.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ　Ｃｏｒｅ指数 | 15.39% | 15.32% | 1.004 |
| 2022 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 13.66% | 15.50% | 0.882 |
| 2022 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | -3.97% | 18.80% | -0.211 |
| 2022 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | -5.56% | 17.51% | -0.317 |
| 2022 | 1656.T | ｉシェアーズ・コア　米国債７－１０年　ＥＴＦ | -0.15% | 7.30% | -0.020 |
| 2022 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | -2.58% | 21.89% | -0.118 |
| 2022 | 2528.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ　Ｃｏｒｅ指数 | -2.20% | 17.25% | -0.128 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2019 | 8.57% | 5.85% | 1.464 |
| 2020 | 3.62% | 12.06% | 0.300 |
| 2021 | 9.35% | 6.75% | 1.385 |
| 2022 | 2.47% | 7.09% | 0.348 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2022-06-01 to 2023-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 193.04% |
| Annualized Return | 202.18% |
| Annualized Volatility | 286.72% ⚠️ (Exceeds constraint) |
| Max Drawdown | -30.59% |
| Sharpe Ratio | 0.705 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 8.60% | 202.18% | +193.58% | ⚠️ |
| Annual Volatility | 6.93% | 286.72% | +279.80% | ⚠️ BREACH |
| Sharpe Ratio | 1.242 | 0.705 | -0.536 | ⚠️ |
| Max Drawdown | 0.00% | -30.59% | -30.59% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (286.72%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +4039.3% relative to backtest period.

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
| -10% | ¥16491418 | 0.606 | No | No |
| -20% | ¥14659038 | 0.682 | No | No |
| -30% | ¥12826658 | 0.780 | Yes | No |
| -40% | ¥10994278 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 3 days
- First breach: 2020-03-17
- Last breach: 2020-03-19
- Max ratio: 0.717

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-03-17 | 0.708 |
| 2020-03-18 | 0.705 |
| 2020-03-19 | 0.717 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-03-17 | 0.708 |
| 2020-03-18 | 0.705 |
| 2020-03-19 | 0.717 |
