# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18296520
- Current loan ratio: 0.547
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.92% drop from current value
- Buffer to forced liquidation: 35.70% drop from current value
- Historical max drawdown (portfolio): -23.11%

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 25
- Candidate universe after correlation filter: 16 (threshold 0.90)
- Excluded hedged ETFs: 1482.T(ｉシェアーズ・コア　米国債７－)
- Excluded high-volatility ETFs (> 35.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1596.T(ＮＺＡＭ　上場投信　ＴＯＰＩＸ), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -35.0%): 1473.T(Ｏｎｅ　ＥＴＦ　トピックス), 1305.T(ｉＦｒｅｅＥＴＦ　ＴＯＰＩＸ（), 1306.T(ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩ), 1628.T(ＮＥＸＴ　ＦＵＮＤＳ　運輸・物), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1619.T(ＮＥＸＴ　ＦＵＮＤＳ　建設・資), 1630.T(ＮＥＸＴ　ＦＵＮＤＳ　小売（Ｔ), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1617.T(ＮＥＸＴ　ＦＵＮＤＳ　食品（Ｔ), 1620.T(ＮＥＸＴ　ＦＵＮＤＳ　素材・化), 1546.T(ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジ), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1343.T(ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1577.T(ＮＥＸＴ　ＦＵＮＤＳ　野村日本), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1398.T(ＳＭＤＡＭ　東証ＲＥＩＴ指数上), 1478.T(ｉシェアーズ　ＭＳＣＩ　ジャパ), 1476.T(ｉシェアーズ・コア　Ｊリート　), 1475.T(ｉシェアーズ・コア　ＴＯＰＩＸ), 1595.T(ＮＺＡＭ　上場投信　東証ＲＥＩ), 1597.T(ＭＡＸＩＳ　Ｊリート上場投信), 1550.T(ＭＡＸＩＳ　海外株式（ＭＳＣＩ), 1348.T(ＭＡＸＩＳ　トピックス上場投信), 1345.T(上場インデックスファンドＪリー), 1399.T(上場インデックスファンドＭＳＣ), 1308.T(上場インデックスファンドＴＯＰ), 1681.T(上場インデックスファンド海外新), 1680.T(上場インデックスファンド海外先), 1554.T(上場インデックスファンド世界株), 1698.T(上場インデックスファンド日本高), 1547.T(上場インデックスファンド米国株)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 14.76%, volatility 13.73%, Sharpe 1.075, expense 0.20%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2016-05-31 to 2021-05-31 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 14.76% | - | - |
| Annual Volatility | 13.73% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.075 | - | - |
| Weighted Expense Ratio | 0.20% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.76% | 13.73% | 1.075 | 0.20% | Yes |
| low_volatility | 12.70% | 12.17% | 1.043 | 0.23% |  |
| cost_focus | 13.94% | 13.81% | 1.010 | 0.22% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1586.T | 上場インデックスファンドＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌ | 10.43% | 27.16% | 0.384 | 0.09% | 0.729 |
| 2 | 1481.T | 上場インデックスファンド日本経済貢献株 | 11.24% | 24.65% | 0.456 | 0.15% | 0.680 |
| 3 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 4.34% | 19.18% | 0.226 | 0.32% | 0.658 |
| 4 | 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | 8.97% | 18.58% | 0.483 | 0.17% | 0.452 |
| 5 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 11.63% | 20.23% | 0.575 | 0.32% | 0.446 |
| 6 | 1477.T | ｉシェアーズ　ＭＳＣＩ　日本株最小分散　ＥＴＦ | 3.89% | 15.85% | 0.245 | 0.19% | 0.443 |
| 7 | 1311.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ　Ｃｏｒｅ　３０連動型上場投 | 7.85% | 17.55% | 0.447 | 0.19% | 0.425 |
| 8 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 8.53% | 17.67% | 0.483 | 0.18% | 0.400 |
| 9 | 1320.T | ｉＦｒｅｅＥＴＦ　日経２２５（年１回決算型） | 12.45% | 19.57% | 0.636 | 0.12% | 0.397 |
| 10 | 1364.T | ｉシェアーズ　ＪＰＸ日経４００　ＥＴＦ | 8.61% | 17.55% | 0.491 | 0.04% | 0.366 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内株式 | 2 | ¥6,254,760 | 34.2% |
| 国内セクター | 2 | ¥4,334,040 | 23.7% |
| コモディティ | 1 | ¥4,309,200 | 23.6% |
| その他 | 1 | ¥3,398,520 | 18.6% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 157 | ¥29100.00 | ¥4568700 | 25.0% | 0.14% | 12.42% | 18.94% | 0.655 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 810 | ¥5320.00 | ¥4309200 | 23.6% | N/A | 8.72% | 13.64% | 0.639 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 223 | ¥15240.00 | ¥3398520 | 18.6% | 0.20% | 25.13% | 24.01% | 1.047 |
| 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 116 | ¥27990.00 | ¥3246840 | 17.7% | 0.32% | 17.01% | 21.33% | 0.797 |
| 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 58 | ¥29070.00 | ¥1686060 | 9.2% | 0.04% | 12.28% | 19.11% | 0.642 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 36 | ¥30200.00 | ¥1087200 | 5.9% | 0.32% | 13.18% | 19.80% | 0.666 |

*Total: 6 ETFs, Portfolio value: ¥18,296,520*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -0.69% | 8.50% | -0.081 |
| 2016 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 10.82% | 23.16% | 0.467 |
| 2016 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 11.46% | 25.62% | 0.447 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.53% | 24.79% | 0.546 |
| 2016 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 13.62% | 27.36% | 0.498 |
| 2016 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 3.18% | 20.48% | 0.155 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 6.94% | 5.29% | 1.312 |
| 2017 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 18.22% | 11.83% | 1.541 |
| 2017 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 19.73% | 13.14% | 1.502 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 26.77% | 14.21% | 1.884 |
| 2017 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 31.69% | 16.23% | 1.952 |
| 2017 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 21.24% | 12.40% | 1.713 |
| 2018 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -5.06% | 6.96% | -0.728 |
| 2018 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | -11.46% | 18.86% | -0.608 |
| 2018 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | -13.12% | 17.32% | -0.758 |
| 2018 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | -3.81% | 25.86% | -0.148 |
| 2018 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | -22.04% | 21.20% | -1.039 |
| 2018 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -13.10% | 20.22% | -0.648 |
| 2019 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 15.73% | 11.59% | 1.358 |
| 2019 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 18.55% | 14.65% | 1.266 |
| 2019 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 19.30% | 12.06% | 1.601 |
| 2019 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 37.25% | 19.15% | 1.945 |
| 2019 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 35.10% | 17.84% | 1.968 |
| 2019 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 27.94% | 13.31% | 2.099 |
| 2020 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 18.09% | 25.12% | 0.720 |
| 2020 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 15.77% | 25.53% | 0.618 |
| 2020 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 15.93% | 24.82% | 0.642 |
| 2020 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 39.01% | 33.02% | 1.181 |
| 2020 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 23.22% | 25.15% | 0.923 |
| 2020 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 19.35% | 29.07% | 0.666 |
| 2021 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 6.51% | 12.78% | 0.509 |
| 2021 | 1369.T | Ｏｎｅ　ＥＴＦ　日経２２５ | 5.06% | 19.89% | 0.254 |
| 2021 | 1397.T | ＳＭＤＡＭ　日経２２５上場投信 | 5.21% | 21.40% | 0.243 |
| 2021 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.14% | 22.59% | 0.582 |
| 2021 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 6.34% | 20.74% | 0.306 |
| 2021 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 4.64% | 18.56% | 0.250 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2016 | 7.88% | 14.67% | 0.537 |
| 2017 | 19.03% | 8.04% | 2.368 |
| 2018 | -11.44% | 12.07% | -0.948 |
| 2019 | 23.85% | 8.97% | 2.658 |
| 2020 | 21.48% | 19.03% | 1.129 |
| 2021 | 7.06% | 15.14% | 0.467 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2021-05-31 to 2022-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 2.27% |
| Annualized Return | 2.27% |
| Annualized Volatility | 15.93% ⚠️ (Exceeds constraint) |
| Max Drawdown | -13.21% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 14.76% | 2.27% | -12.49% | ⚠️ |
| Annual Volatility | 13.73% | 15.93% | +2.20% | ⚠️ BREACH |
| Max Drawdown | 0.00% | -13.21% | -13.21% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (15.93%) **EXCEEDED** the backtest constraint (15%).

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
| -10% | ¥16466868 | 0.607 | No | No |
| -20% | ¥14637216 | 0.683 | No | No |
| -30% | ¥12807564 | 0.781 | Yes | No |
| -40% | ¥10977912 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 979 days
- First breach: 2016-05-31
- Last breach: 2020-06-15
- Max ratio: 1.093

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2016-05-31 | 1.001 |
| 2016-06-01 | 1.008 |
| 2016-06-02 | 1.018 |
| 2016-06-03 | 1.028 |
| 2016-06-06 | 1.027 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-05-27 | 0.717 |
| 2020-05-28 | 0.707 |
| 2020-05-29 | 0.710 |
| 2020-06-01 | 0.703 |
| 2020-06-15 | 0.716 |

### Forced Liquidation Summary (>= 85%)
- Total events: 357 days
