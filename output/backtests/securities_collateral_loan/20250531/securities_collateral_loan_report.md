# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18317522
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.01% drop from current value
- Buffer to forced liquidation: 35.77% drop from current value
- Historical max drawdown (portfolio): -17.95%

## Optimization Summary
- Total ETFs evaluated: 109
- ETFs with sufficient data: 82
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 2514.T(ＮＥＸＴ　ＦＵＮＤＳ　外国株式), 2512.T(ＮＥＸＴ　ＦＵＮＤＳ　外国債券), 2554.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 2521.T(上場インデックスファンド米国株), 2562.T(上場インデックスファンド米国株), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1545.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤ), 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1489.T(ＮＥＸＴ　ＦＵＮＤＳ　日経平均), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1364.T(ｉシェアーズ　ＪＰＸ日経４００), 1655.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 1475.T(ｉシェアーズ・コア　ＴＯＰＩＸ), 1656.T(ｉシェアーズ・コア　米国債７－), 2530.T(ＭＡＸＩＳ　ＨｕａＡｎ中国株式), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1629.T(ＮＥＸＴ　ＦＵＮＤＳ　商社・卸), 1485.T(ＭＡＸＩＳ　ＪＡＰＡＮ　設備・), 1660.T(ＭＡＸＩＳ高利回りＪリート上場)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 11.41%, volatility 13.33%, Sharpe 0.856, expense 0.19%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2020-06-01 to 2025-05-30 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 11.41% | - | - |
| Annual Volatility | 13.33% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.856 | - | - |
| Weighted Expense Ratio | 0.19% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.41% | 13.33% | 0.856 | 0.19% | Yes |
| low_volatility | 12.64% | 9.61% | 1.316 | 0.18% |  |
| cost_focus | 9.96% | 10.84% | 0.919 | 0.22% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 1.75% | 19.66% | 0.089 | 0.32% | 0.774 |
| 2 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 6.77% | 22.40% | 0.302 | 0.32% | 0.767 |
| 3 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 6.41% | 21.53% | 0.298 | 0.32% | 0.765 |
| 4 | 1586.T | 上場インデックスファンドＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌ | 12.90% | 22.90% | 0.564 | 0.09% | 0.717 |
| 5 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数 | 12.05% | 21.04% | 0.573 | 0.17% | 0.675 |
| 6 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 14.23% | 22.77% | 0.625 | 0.12% | 0.670 |
| 7 | 1659.T | ｉシェアーズ　米国リート　ＥＴＦ | 14.44% | 22.32% | 0.647 | 0.20% | 0.642 |
| 8 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 16.28% | 24.75% | 0.658 | 0.32% | 0.640 |
| 9 | 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ | 13.64% | 21.20% | 0.644 | 0.04% | 0.633 |
| 10 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 6.04% | 18.66% | 0.324 | 0.32% | 0.629 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| その他 | 2 | ¥8,792,180 | 48.0% |
| 海外株式 | 1 | ¥3,143,805 | 17.2% |
| 国内セクター | 1 | ¥2,557,170 | 14.0% |
| 債券 | 1 | ¥2,303,595 | 12.6% |
| 国内株式 | 1 | ¥1,520,772 | 8.3% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 154 | ¥36210.00 | ¥5576340 | 30.4% | 0.12% | 14.23% | 22.77% | 0.625 |
| 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 1990 | ¥1616.00 | ¥3215840 | 17.6% | 0.15% | 13.25% | 18.29% | 0.725 |
| 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | 1137 | ¥2765.00 | ¥3143805 | 17.2% | 0.23% | 12.66% | 19.90% | 0.636 |
| 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 41 | ¥62370.00 | ¥2557170 | 14.0% | 0.32% | 16.95% | 24.41% | 0.695 |
| 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 103 | ¥22365.00 | ¥2303595 | 12.6% | 0.16% | 0.23% | 9.02% | 0.025 |
| 2555.T | 東証ＲＥＩＴ　ＥＴＦ | 843 | ¥1804.00 | ¥1520772 | 8.3% | 0.24% | 2.23% | 14.44% | 0.154 |

*Total: 6 ETFs, Portfolio value: ¥18,317,522*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2020 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | -6.12% | 7.99% | -0.766 |
| 2020 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 22.71% | 20.10% | 1.130 |
| 2020 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | 31.31% | 18.45% | 1.697 |
| 2020 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 15.29% | 15.46% | 0.989 |
| 2020 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | 6.81% | 17.94% | 0.380 |
| 2020 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 17.06% | 13.55% | 1.260 |
| 2021 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 5.10% | 5.90% | 0.865 |
| 2021 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 6.68% | 21.46% | 0.311 |
| 2021 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | 7.76% | 18.17% | 0.427 |
| 2021 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 8.37% | 16.67% | 0.502 |
| 2021 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | 16.27% | 13.28% | 1.225 |
| 2021 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 10.52% | 21.58% | 0.487 |
| 2022 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | -4.07% | 10.53% | -0.386 |
| 2022 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | -11.93% | 24.45% | -0.488 |
| 2022 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | -9.43% | 22.76% | -0.414 |
| 2022 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | -9.55% | 17.79% | -0.537 |
| 2022 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | -7.90% | 16.67% | -0.474 |
| 2022 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | -5.28% | 17.11% | -0.309 |
| 2023 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 6.79% | 8.91% | 0.762 |
| 2023 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 31.90% | 19.64% | 1.624 |
| 2023 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | 15.39% | 15.28% | 1.007 |
| 2023 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 25.82% | 14.16% | 1.824 |
| 2023 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | -4.52% | 11.46% | -0.394 |
| 2023 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 23.02% | 23.66% | 0.973 |
| 2024 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 6.42% | 9.30% | 0.690 |
| 2024 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 20.99% | 28.83% | 0.728 |
| 2024 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | 16.74% | 20.54% | 0.815 |
| 2024 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 22.73% | 20.77% | 1.095 |
| 2024 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | -7.58% | 13.95% | -0.543 |
| 2024 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 19.77% | 27.66% | 0.715 |
| 2025 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | -7.85% | 11.90% | -0.660 |
| 2025 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 6.93% | 34.17% | 0.203 |
| 2025 | 1658.T | ｉシェアーズ・コア　ＭＳＣＩ　新興国株　ＥＴＦ | -2.81% | 26.21% | -0.107 |
| 2025 | 2518.T | ＮＥＸＴ　ＦＵＮＤＳ　ＭＳＣＩ日本株女性活躍指数（セレクト）連動型上場投信 | 0.44% | 27.66% | 0.016 |
| 2025 | 2555.T | 東証ＲＥＩＴ　ＥＴＦ | 4.94% | 13.58% | 0.364 |
| 2025 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | -2.79% | 31.69% | -0.088 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2020 | 13.90% | 9.65% | 1.441 |
| 2021 | 9.02% | 11.80% | 0.764 |
| 2022 | -7.57% | 12.18% | -0.622 |
| 2023 | 17.17% | 11.43% | 1.503 |
| 2024 | 15.26% | 15.20% | 1.004 |
| 2025 | -1.06% | 16.98% | -0.062 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2025-06-02 to 2025-10-31 (0.4 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 19.73% |
| Annualized Return | 54.55% |
| Annualized Volatility | 22.88% ⚠️ (Exceeds constraint) |
| Max Drawdown | -11.68% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 11.41% | 54.55% | +43.14% | ⚠️ |
| Annual Volatility | 13.33% | 22.88% | +9.55% | ⚠️ BREACH |
| Max Drawdown | 0.00% | -11.68% | -11.68% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (22.88%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +71.7% relative to backtest period.

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
| -10% | ¥16485770 | 0.607 | No | No |
| -20% | ¥14654018 | 0.682 | No | No |
| -30% | ¥12822265 | 0.780 | Yes | No |
| -40% | ¥10990513 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 403 days
- First breach: 2020-06-01
- Last breach: 2023-04-11
- Max ratio: 0.844

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-06-01 | 0.837 |
| 2020-06-02 | 0.827 |
| 2020-06-03 | 0.818 |
| 2020-06-04 | 0.814 |
| 2020-06-05 | 0.812 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2023-04-05 | 0.705 |
| 2023-04-06 | 0.711 |
| 2023-04-07 | 0.709 |
| 2023-04-10 | 0.707 |
| 2023-04-11 | 0.705 |
