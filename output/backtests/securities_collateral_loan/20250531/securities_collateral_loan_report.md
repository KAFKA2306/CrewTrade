# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18256828
- Current loan ratio: 0.548
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.75% drop from current value
- Buffer to forced liquidation: 35.56% drop from current value
- Historical max drawdown (portfolio): -18.66%

## Optimization Summary
- Total ETFs evaluated: 109
- ETFs with sufficient data: 93
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 2514.T(ＮＥＸＴ　ＦＵＮＤＳ　外国株式), 2512.T(ＮＥＸＴ　ＦＵＮＤＳ　外国債券), 2554.T(ＮＥＸＴ　ＦＵＮＤＳ　ブルーム), 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 2521.T(上場インデックスファンド米国株), 2562.T(上場インデックスファンド米国株), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 35.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1489.T(ＮＥＸＴ　ＦＵＮＤＳ　日経平均), 1364.T(ｉシェアーズ　ＪＰＸ日経４００), 1655.T(ｉシェアーズ　Ｓ＆Ｐ　５００　), 1475.T(ｉシェアーズ・コア　ＴＯＰＩＸ), 1656.T(ｉシェアーズ・コア　米国債７－), 2530.T(ＭＡＸＩＳ　ＨｕａＡｎ中国株式), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 13.71%, volatility 14.10%, Sharpe 0.972, expense 0.21%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2020-06-01 to 2025-05-30 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 13.71% | - | - |
| Annual Volatility | 14.10% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.972 | - | - |
| Weighted Expense Ratio | 0.21% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 13.71% | 14.10% | 0.972 | 0.21% | Yes |
| low_volatility | 11.69% | 11.07% | 1.056 | 0.17% |  |
| cost_focus | 14.39% | 14.67% | 0.981 | 0.23% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 1.75% | 19.66% | 0.089 | 0.32% | 0.774 |
| 2 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 6.77% | 22.40% | 0.302 | 0.32% | 0.767 |
| 3 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 6.41% | 21.53% | 0.298 | 0.32% | 0.765 |
| 4 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 11.34% | 24.83% | 0.457 | 0.22% | 0.760 |
| 5 | 1633.T | ＮＥＸＴ　ＦＵＮＤＳ　不動産（ＴＯＰＩＸ－１７）上場投信 | 14.09% | 26.79% | 0.526 | 0.32% | 0.754 |
| 6 | 1622.T | ＮＥＸＴ　ＦＵＮＤＳ　自動車・輸送機（ＴＯＰＩＸ－１７）上場 | 15.22% | 26.06% | 0.584 | 0.32% | 0.725 |
| 7 | 1586.T | 上場インデックスファンドＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌ | 12.90% | 22.90% | 0.564 | 0.09% | 0.717 |
| 8 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数 | 12.05% | 21.04% | 0.573 | 0.17% | 0.675 |
| 9 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 14.23% | 22.77% | 0.625 | 0.12% | 0.670 |
| 10 | 1659.T | ｉシェアーズ　米国リート　ＥＴＦ | 14.44% | 22.32% | 0.647 | 0.20% | 0.642 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| その他 | 2 | ¥8,453,280 | 46.3% |
| 国内セクター | 1 | ¥4,305,080 | 23.6% |
| 海外株式 | 1 | ¥3,300,363 | 18.1% |
| REIT | 1 | ¥1,255,625 | 6.9% |
| 国内株式 | 1 | ¥942,480 | 5.2% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 140 | ¥37620.00 | ¥5266800 | 28.8% | 0.22% | 11.34% | 24.83% | 0.457 |
| 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | 221 | ¥19480.00 | ¥4305080 | 23.6% | 0.32% | 20.15% | 28.58% | 0.705 |
| 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 2442 | ¥1351.50 | ¥3300363 | 18.1% | 0.17% | 12.05% | 21.04% | 0.573 |
| 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 88 | ¥36210.00 | ¥3186480 | 17.5% | 0.12% | 14.23% | 22.77% | 0.625 |
| 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | 125 | ¥10045.00 | ¥1255625 | 6.9% | 0.14% | 3.78% | 14.32% | 0.264 |
| 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 36 | ¥26180.00 | ¥942480 | 5.2% | 0.18% | 14.80% | 22.48% | 0.659 |

*Total: 6 ETFs, Portfolio value: ¥18,256,828*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2020 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 16.23% | 22.05% | 0.736 |
| 2020 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 15.68% | 18.82% | 0.833 |
| 2020 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | -11.73% | 23.14% | -0.507 |
| 2020 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | 14.11% | 17.39% | 0.811 |
| 2020 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 7.51% | 24.48% | 0.307 |
| 2020 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 17.06% | 13.55% | 1.260 |
| 2021 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 2.63% | 19.60% | 0.134 |
| 2021 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 10.20% | 17.15% | 0.595 |
| 2021 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | 36.58% | 26.41% | 1.385 |
| 2021 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | 14.66% | 16.01% | 0.916 |
| 2021 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 46.34% | 15.59% | 2.973 |
| 2021 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 10.52% | 21.58% | 0.487 |
| 2022 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 7.78% | 16.96% | 0.459 |
| 2022 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | -4.46% | 19.04% | -0.234 |
| 2022 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | 18.54% | 30.69% | 0.604 |
| 2022 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | -5.91% | 15.55% | -0.380 |
| 2022 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | -15.04% | 23.25% | -0.647 |
| 2022 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | -5.28% | 17.11% | -0.309 |
| 2023 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 12.65% | 19.48% | 0.650 |
| 2023 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 24.81% | 15.03% | 1.651 |
| 2023 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | 34.95% | 24.90% | 1.404 |
| 2023 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | -3.60% | 11.19% | -0.322 |
| 2023 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 16.09% | 19.29% | 0.834 |
| 2023 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 23.02% | 23.66% | 0.973 |
| 2024 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | 11.56% | 40.37% | 0.286 |
| 2024 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 18.95% | 33.64% | 0.563 |
| 2024 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | 25.49% | 32.86% | 0.776 |
| 2024 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | -7.79% | 12.65% | -0.616 |
| 2024 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | 11.67% | 18.68% | 0.625 |
| 2024 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | 19.77% | 27.66% | 0.715 |
| 2025 | 1485.T | ＭＡＸＩＳ　ＪＡＰＡＮ　設備・人材積極投資企業２００上場投信 | -7.61% | 17.01% | -0.448 |
| 2025 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 0.48% | 27.67% | 0.017 |
| 2025 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場投信 | -10.06% | 32.79% | -0.307 |
| 2025 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | 4.45% | 12.65% | 0.352 |
| 2025 | 2515.T | ＮＥＸＴ　ＦＵＮＤＳ　外国ＲＥＩＴ・Ｓ＆Ｐ先進国ＲＥＩＴ指数（除く日本・為替ヘッ | -7.05% | 29.75% | -0.237 |
| 2025 | 2560.T | ＭＡＸＩＳカーボン・エフィシェント日本株上場投信 | -2.79% | 31.69% | -0.088 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2020 | 9.47% | 13.33% | 0.711 |
| 2021 | 18.59% | 12.05% | 1.543 |
| 2022 | 0.32% | 12.48% | 0.026 |
| 2023 | 18.33% | 11.25% | 1.629 |
| 2024 | 14.90% | 19.03% | 0.783 |
| 2025 | -6.17% | 15.78% | -0.391 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2025-06-02 to 2025-10-31 (0.4 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 21.66% |
| Annualized Return | 60.64% |
| Annualized Volatility | 15.92% ⚠️ (Exceeds constraint) |
| Max Drawdown | -7.15% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 13.71% | 60.64% | +46.93% | ⚠️ |
| Annual Volatility | 14.10% | 15.92% | +1.82% | ⚠️ BREACH |
| Max Drawdown | 0.00% | -7.15% | -7.15% | ✓ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (15.92%) **EXCEEDED** the backtest constraint (15%).

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
| -10% | ¥16431145 | 0.609 | No | No |
| -20% | ¥14605462 | 0.685 | No | No |
| -30% | ¥12779780 | 0.782 | Yes | No |
| -40% | ¥10954097 | 0.913 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 442 days
- First breach: 2020-06-01
- Last breach: 2023-03-30
- Max ratio: 0.953

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2020-06-01 | 0.910 |
| 2020-06-02 | 0.899 |
| 2020-06-03 | 0.889 |
| 2020-06-04 | 0.889 |
| 2020-06-05 | 0.887 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2023-03-24 | 0.720 |
| 2023-03-27 | 0.718 |
| 2023-03-28 | 0.716 |
| 2023-03-29 | 0.708 |
| 2023-03-30 | 0.707 |

### Forced Liquidation Summary (>= 85%)
- Total events: 122 days
