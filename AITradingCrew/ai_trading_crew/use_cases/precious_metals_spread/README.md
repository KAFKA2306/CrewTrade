# Precious Metals Spread

ETF（1540, 1541, 1542, 1543）とスポット価格の乖離を監視し、裁定取引機会を検出。

## 概要

貴金属ETFは現物（金・銀・プラチナ・パラジウム）に裏付けされているが、需給要因で乖離が発生。このユースケースは乖離率・Z-scoreを計算し、統計的異常値を検出。

## モジュール構成

- `config.py`: 対象銘柄・ルックバック期間・閾値設定
- `data_pipeline.py`: スポット価格とETF価格の取得・同期
- `analysis.py`: 乖離率計算・Z-score・異常値検出
- `reporting.py`: レポート生成
- `insights.py`: AI解説生成
- `use_case.py`: BaseUseCase実装

## 実行方法

```bash
uv run -m ai_trading_crew.use_case_runner precious_metals_spread --config config/use_cases/precious_metals_spread.yaml
```

## 設定例

```yaml
tickers:
  - ticker: "1540.T"
    name: "純金上場信託"
    spot_symbol: "XAU/USD"
  - ticker: "1541.T"
    name: "純プラチナ信託"
    spot_symbol: "XPT/USD"
  - ticker: "1542.T"
    name: "純銀信託"
    spot_symbol: "XAG/USD"
  - ticker: "1543.T"
    name: "純パラジウム信託"
    spot_symbol: "XPD/USD"

lookback_period: "2y"
zscore_threshold: 2.0
```

## 出力

`output/use_cases/precious_metals_spread/{YYYYMMDD}/`:
- `precious_metals_spread_report.md`: 乖離分析レポート
- `precious_metals_spread_insights.md`: 裁定取引シグナル解説

## 分析指標

- **乖離率**: (ETF価格 - スポット価格) / スポット価格 × 100
- **Z-score**: (乖離率 - 平均乖離率) / 標準偏差
- **異常値検出**: |Z-score| > 閾値（デフォルト: 2.0σ）
