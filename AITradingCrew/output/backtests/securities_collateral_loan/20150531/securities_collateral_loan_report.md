# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18304855
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.96% drop from current value
- Buffer to forced liquidation: 35.73% drop from current value
- Historical max drawdown (portfolio): -14.07%

## Optimization Summary
- Total ETFs evaluated: 44
- ETFs with sufficient data: 40
- Candidate universe after correlation filter: 32 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1329.T(ｉシェアーズ・コア　日経２２５), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 17.35%, volatility 10.00%, Sharpe 1.735, expense 0.24%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2012-05-31 to 2015-05-29 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 17.35% | - | - |
| Annual Volatility | 10.00% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.735 | - | - |
| Weighted Expense Ratio | 0.24% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 17.35% | 10.00% | 1.735 | 0.24% | Yes |
| low_volatility | 16.86% | 9.54% | 1.768 | 0.22% |  |
| cost_focus | 22.05% | 11.31% | 1.950 | 0.21% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 23.30% | 12.68% | 1.837 | 0.15% | 14.488 |
| 2 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳ | 22.62% | 13.56% | 1.668 | 0.24% | 12.297 |
| 3 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 22.47% | 14.14% | 1.588 | 0.28% | 11.230 |
| 4 | 1577.T | ＮＥＸＴ　ＦＵＮＤＳ　野村日本株高配当７０連動型上場投信 | 20.79% | 14.06% | 1.479 | 0.32% | 10.514 |
| 5 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 27.99% | 16.33% | 1.714 | 0.15% | 10.492 |
| 6 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 24.49% | 15.31% | 1.600 | 0.30% | 10.454 |
| 7 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日 | 21.51% | 14.56% | 1.477 | 0.24% | 10.146 |
| 8 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配 | 17.15% | 13.08% | 1.311 | 0.30% | 10.021 |
| 9 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 36.76% | 19.32% | 1.903 | 0.20% | 9.853 |
| 10 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 16.80% | 13.39% | 1.255 | 0.15% | 9.373 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 海外株式 | 2 | ¥6,049,910 | 33.1% |
| 国内株式 | 1 | ¥5,613,275 | 30.7% |
| 国内セクター | 2 | ¥3,724,980 | 20.3% |
| コモディティ | 1 | ¥2,916,690 | 15.9% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 2825 | ¥1987.00 | ¥5613275 | 30.7% | 0.15% | 16.80% | 13.39% | 1.255 |
| 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 2101 | ¥2270.00 | ¥4769270 | 26.1% | 0.24% | 22.62% | 13.56% | 1.668 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 731 | ¥3990.00 | ¥2916690 | 15.9% | N/A | 2.37% | 12.08% | 0.196 |
| 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 230 | ¥9140.00 | ¥2102200 | 11.5% | 0.32% | 16.71% | 19.81% | 0.844 |
| 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 82 | ¥19790.00 | ¥1622780 | 8.9% | 0.32% | 25.86% | 17.63% | 1.466 |
| 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 58 | ¥22080.00 | ¥1280640 | 7.0% | 0.30% | 24.49% | 15.31% | 1.600 |

*Total: 6 ETFs, Portfolio value: ¥18,304,855*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2012 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 15.42% | 14.39% | 1.071 |
| 2012 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 22.00% | 10.70% | 2.057 |
| 2012 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 9.15% | 17.19% | 0.533 |
| 2012 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 12.68% | 17.96% | 0.706 |
| 2012 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | -4.37% | 33.13% | -0.132 |
| 2012 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 25.39% | 14.54% | 1.746 |
| 2013 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -14.80% | 20.92% | -0.708 |
| 2013 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 36.83% | 28.27% | 1.303 |
| 2013 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 56.13% | 18.85% | 2.978 |
| 2013 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 40.54% | 22.73% | 1.784 |
| 2013 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 35.81% | 33.06% | 1.083 |
| 2013 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 50.50% | 16.92% | 2.985 |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.62% | 10.54% | 0.818 |
| 2014 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 24.63% | 11.53% | 2.136 |
| 2014 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 26.15% | 16.17% | 1.617 |
| 2014 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 21.90% | 19.01% | 1.152 |
| 2014 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 7.01% | 21.39% | 0.328 |
| 2014 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 20.93% | 14.25% | 1.468 |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 3.77% | 9.82% | 0.384 |
| 2015 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -1.34% | 15.33% | -0.087 |
| 2015 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 3.32% | 13.71% | 0.242 |
| 2015 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 15.06% | 14.65% | 1.028 |
| 2015 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 19.79% | 17.17% | 1.153 |
| 2015 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 3.94% | 12.07% | 0.326 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2012 | 16.17% | 9.98% | 1.620 |
| 2013 | 27.45% | 15.84% | 1.733 |
| 2014 | 18.79% | 9.91% | 1.896 |
| 2015 | 4.64% | 8.99% | 0.516 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2015-06-01 to 2016-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | -8.98% |
| Annualized Return | -9.26% |
| Annualized Volatility | 15.24% ⚠️ (Exceeds constraint) |
| Max Drawdown | -16.18% |
| Sharpe Ratio | -0.608 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 17.35% | -9.26% | -26.62% | ⚠️ |
| Annual Volatility | 10.00% | 15.24% | +5.24% | ⚠️ BREACH |
| Sharpe Ratio | 1.735 | -0.608 | -2.343 | ⚠️ |
| Max Drawdown | 0.00% | -16.18% | -16.18% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (15.24%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +52.4% relative to backtest period.

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
| -10% | ¥16474370 | 0.607 | No | No |
| -20% | ¥14643884 | 0.683 | No | No |
| -30% | ¥12813398 | 0.780 | Yes | No |
| -40% | ¥10982913 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 396 days
- First breach: 2012-05-31
- Last breach: 2014-05-19
- Max ratio: 1.022

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2012-05-31 | 1.005 |
| 2012-06-01 | 1.018 |
| 2012-06-04 | 1.022 |
| 2012-06-05 | 1.016 |
| 2012-06-06 | 1.009 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-04-28 | 0.702 |
| 2014-05-07 | 0.704 |
| 2014-05-08 | 0.701 |
| 2014-05-09 | 0.701 |
| 2014-05-19 | 0.700 |

### Forced Liquidation Summary (>= 85%)
- Total events: 147 days
