# Backtests Debug

バックテスト実行時の詳細デバッグ情報。

## 概要

最適化プロセスの中間データ・エラーログ・パフォーマンスメトリクスを保存。トラブルシューティング用。

## 出力内容

```
backtests_debug/
└── securities_collateral_loan/
    └── {YYYYMMDD}/
        ├── optimization_log.txt           # 最適化ログ
        ├── sample_portfolios.parquet      # 全サンプルポートフォリオ
        ├── constraint_violations.csv      # 制約違反リスト
        ├── performance_distribution.csv   # パフォーマンス分布
        └── error_log.txt                  # エラーログ
```

## ログファイル詳細

### optimization_log.txt
最適化プロセスの逐次ログ：
- サンプル生成回数
- 制約チェック結果
- 目的関数評価値
- 最良ソリューション更新

### sample_portfolios.parquet
生成された全ランダムポートフォリオ（20,000サンプル）：
- 各銘柄のウェイト
- リターン・ボラティリティ・シャープ比
- 制約違反フラグ

### constraint_violations.csv
制約違反の詳細：
- 違反した制約種別
- 違反の程度
- 該当銘柄

### performance_distribution.csv
スコア分布統計：
- 平均・中央値・標準偏差
- パーセンタイル（10, 25, 50, 75, 90）
- 最小・最大値

### error_log.txt
実行時エラー・警告：
- データ取得エラー
- 価格データ欠損
- API制限超過
