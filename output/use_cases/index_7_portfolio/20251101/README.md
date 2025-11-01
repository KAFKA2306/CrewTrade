# index_7_portfolio（オリジナル指数）実行メモ

- 検証コマンド  
  `PYTHONPATH=AITradingCrew python3 -m ai_trading_crew.use_case_runner index_7_portfolio --config AITradingCrew/config/use_cases/index_7_portfolio_original.yaml`
- 出力ディレクトリ  
  `output/use_cases/index_7_portfolio/20251101/`
- データ取得期間  
  2015-10-16 〜 2025-10-31（取得した7指数の共通期間）

## 生成ファイル
- `index_7_portfolio_report.md`：8種類のグラフを埋め込んだMarkdownレポート
- `graphs/*.png`：資産配分〜相関ヒートマップまで8枚のPNG
- `optimized_portfolio.parquet`：最適化後ポートフォリオの構成

## 備考
- 設定ファイルは `AITradingCrew/config/use_cases/index_7_portfolio_original.yaml` を使用。国内ETFとは別ユニバースのため、検証目的でのみ利用。
- `validation.py` 内のウォークフォワード処理で `FutureWarning: 'M' is deprecated` が発生するため、将来的には `ME`（月末）頻度への変更を検討。
