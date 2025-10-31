# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18314338
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.00% drop from current value
- Buffer to forced liquidation: 35.76% drop from current value
- Historical max drawdown (portfolio): -14.83%

## Optimization Summary
- Total ETFs evaluated: 70
- ETFs with sufficient data: 63
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 1482.T(ｉシェアーズ・コア　米国債７－), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1596.T(ＮＺＡＭ　上場投信　ＴＯＰＩＸ), 1671.T(ＷＴＩ原油価格連動型上場投信), 1481.T(上場インデックスファンド日本経)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 15.30%, volatility 9.11%, Sharpe 1.679, expense 0.21%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2015-06-01 to 2018-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 15.30% | - | - |
| Annual Volatility | 9.11% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.679 | - | - |
| Weighted Expense Ratio | 0.21% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.30% | 9.11% | 1.679 | 0.21% | Yes |
| low_volatility | 10.17% | 6.95% | 1.462 | 0.26% |  |
| cost_focus | 14.21% | 8.92% | 1.593 | 0.22% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 25.52% | 16.04% | 1.591 | 0.32% | 9.924 |
| 2 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 13.18% | 11.62% | 1.134 | 0.28% | 9.765 |
| 3 | 1308.T | 上場インデックスファンドＴＯＰＩＸ | 17.03% | 13.48% | 1.263 | 0.05% | 9.368 |
| 4 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 22.15% | 15.47% | 1.432 | 0.32% | 9.256 |
| 5 | 1475.T | ｉシェアーズ・コア　ＴＯＰＩＸ　ＥＴＦ | 16.67% | 13.43% | 1.241 | 0.04% | 9.242 |
| 6 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 17.81% | 13.89% | 1.283 | 0.32% | 9.236 |
| 7 | 1305.T | ｉＦｒｅｅＥＴＦ　ＴＯＰＩＸ（年１回決算型） | 17.07% | 13.60% | 1.255 | 0.06% | 9.224 |
| 8 | 1306.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ連動型上場投信 | 17.08% | 13.63% | 1.253 | 0.05% | 9.191 |
| 9 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 15.81% | 13.19% | 1.198 | 0.10% | 9.081 |
| 10 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 19.85% | 14.80% | 1.341 | 0.32% | 9.063 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| コモディティ | 1 | ¥5,705,080 | 31.2% |
| 国内セクター | 2 | ¥4,094,550 | 22.4% |
| 国内株式 | 1 | ¥3,565,920 | 19.5% |
| 海外株式 | 1 | ¥3,238,500 | 17.7% |
| その他 | 1 | ¥1,710,288 | 9.3% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1544 | ¥3695.00 | ¥5705080 | 31.2% | N/A | 1.97% | 6.18% | 0.318 |
| 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | 228 | ¥15640.00 | ¥3565920 | 19.5% | 0.17% | 15.96% | 16.18% | 0.987 |
| 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 1020 | ¥3175.00 | ¥3238500 | 17.7% | 0.15% | 18.30% | 16.96% | 1.079 |
| 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 69 | ¥35950.00 | ¥2480550 | 13.5% | 0.32% | 18.99% | 20.99% | 0.905 |
| 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 963 | ¥1776.00 | ¥1710288 | 9.3% | 0.04% | 16.87% | 14.70% | 1.148 |
| 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 60 | ¥26900.00 | ¥1614000 | 8.8% | 0.32% | 25.52% | 16.04% | 1.591 |

*Total: 6 ETFs, Portfolio value: ¥18,314,338*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -10.11% | 11.59% | -0.872 |
| 2015 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 5.81% | 22.77% | 0.255 |
| 2015 | 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | 8.50% | 21.10% | 0.403 |
| 2015 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -3.74% | 20.46% | -0.183 |
| 2015 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | -1.91% | 22.95% | -0.083 |
| 2015 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | -18.88% | 27.26% | -0.693 |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.00% | 10.82% | 0.000 |
| 2016 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | -1.92% | 26.96% | -0.071 |
| 2016 | 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | -2.71% | 26.51% | -0.102 |
| 2016 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 4.95% | 22.82% | 0.217 |
| 2016 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 3.57% | 27.93% | 0.128 |
| 2016 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 5.50% | 32.46% | 0.170 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 6.94% | 5.29% | 1.312 |
| 2017 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 20.14% | 10.91% | 1.846 |
| 2017 | 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | 19.43% | 11.69% | 1.662 |
| 2017 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 14.00% | 11.33% | 1.236 |
| 2017 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 33.65% | 13.03% | 2.582 |
| 2017 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 32.48% | 15.61% | 2.081 |
| 2018 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -4.03% | 8.50% | -0.473 |
| 2018 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | -3.43% | 17.44% | -0.196 |
| 2018 | 1474.T | Ｏｎｅ　ＥＴＦ　ＪＰＸ日経４００ | -4.34% | 23.47% | -0.185 |
| 2018 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -2.76% | 21.68% | -0.127 |
| 2018 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | -0.44% | 20.85% | -0.021 |
| 2018 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | -8.76% | 26.72% | -0.328 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2015 | 27.65% | 53.58% | 0.516 |
| 2016 | 1.06% | 14.05% | 0.075 |
| 2017 | 16.97% | 6.40% | 2.653 |
| 2018 | -4.18% | 10.70% | -0.391 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2018-06-01 to 2019-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | -6.30% |
| Annualized Return | -6.40% |
| Annualized Volatility | 10.66% |
| Max Drawdown | -15.97% |
| Sharpe Ratio | -0.600 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 15.30% | -6.40% | -21.70% | ⚠️ |
| Annual Volatility | 9.11% | 10.66% | +1.55% | ✓ |
| Sharpe Ratio | 1.679 | -0.600 | -2.279 | ⚠️ |
| Max Drawdown | 0.00% | -15.97% | -15.97% | ⚠️ |


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16482904 | 0.607 | No | No |
| -20% | ¥14651470 | 0.682 | No | No |
| -30% | ¥12820037 | 0.780 | Yes | No |
| -40% | ¥10988603 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 69 days
- First breach: 2015-06-01
- Last breach: 2016-06-24
- Max ratio: 0.893

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2015-06-01 | 0.789 |
| 2015-06-02 | 0.788 |
| 2015-06-03 | 0.787 |
| 2015-06-04 | 0.786 |
| 2015-06-05 | 0.788 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2015-08-31 | 0.866 |
| 2015-09-01 | 0.879 |
| 2015-09-02 | 0.884 |
| 2016-02-12 | 0.701 |
| 2016-06-24 | 0.705 |

### Forced Liquidation Summary (>= 85%)
- Total events: 8 days
