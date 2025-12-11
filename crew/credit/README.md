# クレジットスプレッド分析

ジャンク債（HYG, JNK）とトレジャリー（TLT）のスプレッドを監視し、リスクオン/オフシグナルを検出。

## ユースケース概要

クレジットスプレッドは景気サイクル・リスク選好度の先行指標。拡大時はリスクオフ（株式売り・債券買い）、縮小時はリスクオン（株式買い）を示唆。

## モジュール構成

- `config.py`: 対象債券ETF・ルックバック期間設定
- `data_pipeline.py`: 債券ETF価格取得
- `analysis.py`: スプレッド計算・パーセンタイル分析
- `reporting.py`: レポート生成
- `insights.py`: AI解説生成
- `use_case.py`: BaseUseCase実装

## 実行方法

```bash
uv run -m ai_trading_crew.use_case_runner credit_spread --config config/use_cases/credit_spread.yaml
```

## 設定例

```yaml
tickers:
  high_yield:
    - "HYG"  # iShares iBoxx High Yield Corporate Bond
    - "JNK"  # SPDR Bloomberg High Yield Bond
  treasury:
    - "TLT"  # iShares 20+ Year Treasury Bond
  benchmark:
    - "AGG"  # iShares Core U.S. Aggregate Bond

lookback_period: "5y"
percentile_thresholds:
  extreme_low: 10
  low: 25
  high: 75
  extreme_high: 90
```

## 出力

`output/use_cases/credit_spread/{YYYYMMDD}/`:
- `credit_spread_report.md`: スプレッド分析レポート
- `credit_spread_insights.md`: リスクオン/オフシグナル解説

## 分析指標

- **Credit Spread**: HYG/JNK利回り - TLT利回り（代理指標として価格比率を使用）
- **Percentile Rank**: 過去5年間の分位点
- **トレンド**: 7日/30日移動平均
- **シグナル**:
  - スプレッド > 90%ile → リスクオフ（株式売り）
  - スプレッド < 10%ile → リスクオン（株式買い）
