# リポジトリガイドライン

## プロジェクト構造
- `crew/`: メインパッケージ（ユースケース、クライアント、ユーティリティ）
- `config/`: YAML設定ファイル
- `resources/data/`: キャッシュデータ（Parquet）
- `output/`: 生成レポート（Markdown）

## コマンド
- `task run`

## コーディングスタイル
- Python 3.11+、型ヒント必須
- ファイル/関数: `snake_case`、クラス: `PascalCase`
- Parquetでデータ保存、Markdownでレポート出力
- No comments, handling, temporal files on Root, tests. Always detele and minimize codes.
 
