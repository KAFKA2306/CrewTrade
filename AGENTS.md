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

## Outcome-first task interpretation (Altitude / Depth / Range / Speed)

- **Altitude:** Interpret a task as a verifiable user outcome, not only the named intermediate step. Infer the smallest justified acceptance criteria from the request and current repository state; do not silently expand scope or override explicit instructions.
- **Depth:** Use primary/current evidence and real domain tools and methods. Verify the actual postcondition independently of agent self-report, preferably on the exact changed revision or target runtime.
- **Range:** Combine code, data, tests, runtime/UI, and domain expertise when that materially improves the outcome, while respecting canonical owners and avoiding duplicate systems.
- **Speed:** Complete authorized read-only and reversible work through implementation, focused checks, and read-back without unnecessary approval loops. Bound retries and stop at the proven outcome.
- These principles never bypass repository-specific security, privacy, permission, publication, spending, destructive-action, or release boundaries. State verified results and any remaining `UNVERIFIED` layers.
