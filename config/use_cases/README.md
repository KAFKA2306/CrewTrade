# Use Case Configurations

ユースケースごとのYAML設定ファイル。

## 主要セクション
- `period`: データ取得期間（例: `1y`, `max`）
- `indices`: ティッカー、名称、カテゴリ
- `loan_amount` / `ltv_limit`: LTV設定
- `optimization`: 制約、サンプルサイズ

## 実行方法
```bash
task run:imura
uv run -m crew.use_case_runner <use_case_name> --config config/use_cases/<config>.yaml
```

## 新規追加
1. YAMLファイルを追加
2. `indices`にティッカーを設定
3. 実行コマンドで確認
