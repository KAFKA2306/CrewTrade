# イールドスプレッド分析

イールドカーブのスプレッド（10Y-2Y等）を監視し、景気循環ステージ・リセッション予測シグナルを検出。

## ユースケース概要

イールドスプレッド（長期金利 - 短期金利）は景気先行指標。逆イールド（スプレッド < 0）はリセッション前兆として知られる。このユースケースは複数のスプレッドペアを監視し、経済サイクルの転換点を検出。

## モジュール構成

- `config.py`: スプレッドペア・閾値設定
- `asset_client.py`: FRED APIラッパー
- `data_pipeline.py`: トレジャリー利回りデータ取得
- `analysis.py`: スプレッド計算・Z-score・パーセンタイル
- `allocation.py`: スプレッドシグナルに基づくアロケーション推奨
- `reporting.py`: レポート生成
- `insights.py`: AI解説生成
- `use_case.py`: BaseUseCase実装

## 実行方法

```bash
uv run -m ai_trading_crew.use_case_runner yield_spread --config config/use_cases/yield_spread.yaml
```

## 設定例

```yaml
fred_series:
  - symbol: "DGS2"
    name: "2-Year Treasury"
  - symbol: "DGS5"
    name: "5-Year Treasury"
  - symbol: "DGS10"
    name: "10-Year Treasury"
  - symbol: "DGS30"
    name: "30-Year Treasury"

spread_pairs:
  - name: "10Y-2Y"
    long: "DGS10"
    short: "DGS2"
  - name: "10Y-3M"
    long: "DGS10"
    short: "DGS3MO"
  - name: "30Y-5Y"
    long: "DGS30"
    short: "DGS5"

lookback_period: "10y"
inversion_threshold: 0.0
```

## 出力

`output/use_cases/yield_spread/{YYYYMMDD}/`:
- `yield_spread_report.md`: イールドスプレッド分析レポート
- `yield_spread_insights.md`: 景気サイクル・アロケーション推奨

## 分析指標

- **Yield Spread**: 長期金利 - 短期金利（bp単位）
- **Inversion Status**: スプレッド < 0 → 逆イールド（リセッション警告）
- **Z-score**: (現在値 - 平均) / 標準偏差
- **Percentile Rank**: 過去10年間の分位点

## アロケーション推奨

| スプレッドステータス | 株式 | 債券 | 現金 |
|---|---|---|---|
| 逆イールド（< 0） | 20% | 60% | 20% |
| フラット（0-50bp） | 40% | 40% | 20% |
| スティープ（> 50bp） | 60% | 30% | 10% |
