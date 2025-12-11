# リポジトリガイドライン

## プロジェクト構造とモジュール構成
- `ai_trading_crew/`: クルーのオーケストレーション、アナリスト、ユーティリティ、および各ユースケース（`imura`, `securities_collateral_loan`など）のパッケージ。
- `config/`: 各ユースケースやプロジェクト全体設定用のYAMLファイル。
- `resources/data/`: キャッシュされた生および処理済みデータセット（Parquet）。生成されたアーティファクトとして扱います。
- `output/`: 実行ごとの人間が読めるレポート（Markdown）。
- `README.md`, `AGENTS.md`: コントリビューター向けドキュメント。

## ビルド、テスト、開発コマンド
- `uv sync` / `poetry install` / `pip install -e .`: Pythonの依存関係をインストールします。
- `uv run -m ai_trading_crew.use_case_runner imura --config config/use_cases/imura.yaml`: Imuraファンドユースケースを実行します。
- `python3 -m compileall ai_trading_crew`: すべてのモジュールを対象とする軽量な構文チェック。

## コーディングスタイルと命名規則
- Python 3.10以降、標準ライブラリの `typing` とPydanticモデルを使用します。
- 明示的で説明的な名前を優先します（例： `PreciousMetalsSpreadAnalyzer`）。不可欠でない限り、インラインコメントは使用しません。
- ファイルとディレクトリは `snake_case` を使用し、クラスは `PascalCase` を使用し、関数は `snake_case` を使用します。
- 生成されたテーブルはParquetとして、レポートはMarkdownとして永続化します。

## テストガイドライン
- 組み込みの `unittest` または `pytest` を使用します（ `tests/` の下に追加します）。
- テストファイルには `test_<module>.py` という名前を付け、関数には `test_<behavior>()` という名前を付けます。
- 新しいコードは最低でも `python3 -m compileall ai_trading_crew` で検証し、数値ロジックには対象を絞ったテストを追加します。

## コミットとプルリクエストのガイドライン
- コミットは小さく、命令形で、スコープを限定する必要があります（例： `Add cached metals data client`）。
- 該当する場合は、コミット本文で関連するイシューを参照します。
- プルリクエストでは、スコープ、実行したテスト、および新しい設定手順を説明する必要があります。関連する場合は、サンプル出力パスを含めます。

## セキュリティと設定のヒント
- APIキーは、 `config.py` で定義された名前を使用して `.env` に保存します（例： `TWELVE_API_KEY`）。
- `resources/data` または `output` の下のアーティファクトはコミットしないでください。ランタイムプロダクトとして扱います。
- 統合する前に、サードパーティのデータソースの可用性とライセンスを検証します。