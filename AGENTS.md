# リポジトリガイドライン

## プロジェクト構造
- `crew/`: メインパッケージ（ユースケース、クライアント、ユーティリティ）
- `config/`: YAML設定ファイル
- `resources/data/`: キャッシュデータ（Parquet）
- `output/`: 生成レポート（Markdown）

## コマンド
- `uv sync`: 依存関係インストール
- `task run:imura`: Imura分析実行
- `uv run -m crew.use_case_runner imura --config config/use_cases/imura.yaml`

## コーディングスタイル
- Python 3.11+、型ヒント必須
- ファイル/関数: `snake_case`、クラス: `PascalCase`
- Parquetでデータ保存、Markdownでレポート出力

## セキュリティ
- APIキーは`.env`に保存
- `resources/data`と`output`はコミット不可