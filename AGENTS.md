# リポジトリガイドライン

## プロジェクト構造
- `crew/`: メインパッケージ（ユースケース、クライアント、ユーティリティ）
- `Kronos/`: 金融基盤モデル（変更禁止・外部依存）
- `config/`: YAML設定ファイル
- `resources/data/`: キャッシュデータ（Parquet）
- `output/`: 生成レポート（Markdown）

## コマンド
- `task run`: データ取得・分析・レポート生成を一括実行（PYTHONPATH=Kronos自動設定）

## コーディングスタイル
- Python 3.11+、型ヒント必須
- ファイル/関数: `snake_case`、クラス: `PascalCase`
- Parquetでデータ保存、Markdownでレポート出力
- BaseUseCaseでKronos予測を利用
- No comments, handling, temporal files on Root, tests. Always detele and minimize codes.

 
