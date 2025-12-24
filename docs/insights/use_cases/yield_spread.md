# Yield Spread (イールドスプレッド) 分析レポート

## エグゼクティブサマリー (Executive Summary)
米国ハイイールド債と10年国債の利回り差（イールドスプレッド）を用いた市場レジーム分析結果です。
現在のレジームは**「Neutral（中立）」**と判定されており、スプレッドは239.0bpで推移しています。この環境下では、極端なリスクテイクを避け、株式（SPY）と国債（IEF）をバランス良く保有する配分が推奨されています。

## 現状のステータス (Latest Snapshot)
- **Regime**: **Neutral**
- **Date**: 2025-10-28
- **Spread**: 239.00 bp (Z-score: -0.26)
- **Market Rates**:
    - High Yield: 6.40%
    - 10Y Treasury: 4.01%

## 推奨ポートフォリオ (Allocation Guidance)
現在のNeutralレジームにおける最適化ポートフォリオは、株式と債券の分散を重視しています。

| Asset | Ticker | Weight |
|---|---|---|
| 米国株 (S&P 500) | SPY | **55.13%** |
| 米国中期国債 (7-10Y) | IEF | **44.83%** |
| ハイイールド債 | HYG | 0.04% |

**予測パフォーマンス**:
- **Sharpe Ratio**: 0.89
- **Annual Return**: 12.0%
- **Max Drawdown**: -11.0%

## 参照データ
`output/use_cases/yield_spread/`
