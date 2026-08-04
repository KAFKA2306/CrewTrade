# CrewTrade — 金融調査ワークスペース

[公開ダッシュボード](https://kafka2306.github.io/CrewTrade/) · [GitHub Actions](https://github.com/KAFKA2306/CrewTrade/actions) · [データ基盤設計](docs/data-platform.md)

CrewTradeは、一次データの取得、定量計算、時系列予測、文章による解釈を分離し、分析スナップショットとして公開する研究プロジェクトです。

公開画面は、レポート名の一覧ではなく、**何を検証する分析なのか**を起点に設計しています。対象・期間・計算条件・予測・解釈を同じ証拠として扱いません。

## 正準データ基盤

ユースケース別のダウンロードファイルを正本とする方式から、次の共通基盤へ移行しています。

```text
一次API・統制された非公開入力
  → immutable raw response + SHA-256
  → normalized Parquet
  → DuckDB catalogue / quality / lineage
  → use-case analysis / reports
```

自動取得対象はFRED、米財務省、SEC EDGARです。JPX、EDINET、fundnote、LBMA、WSTS、証券担保契約は、利用権・機械取得可否・秘密性を `config/data_platform.yaml` に明示し、取得不能を推測で補完しません。

```bash
uv sync
uv run crew-data validate-config
uv run pytest tests/data_platform -q

export FRED_API_KEY=...
export SEC_USER_AGENT='CrewTrade contact@example.com'
uv run crew-data sync
uv run crew-data status
```

`data/platform/` にはraw、bronze Parquet、run manifest、`catalog.duckdb` が保存されます。GitHub Actions artifactは検証用スナップショットであり、正準保存先ではありません。運用時はDagu、WSL、コンテナなどの永続ボリュームで実行します。

## 公開画面

- 調査テーマを検証目的で整理
- テーマ、問い、対象、期間、警告を横断検索
- 最新スナップショット、評価状態、レポート数を表示
- 日付別レポートから前提や結論の変化を追跡
- 数値、モデル予測、LLM解釈を別の証拠として表示
- 掲載値がリアルタイムではないこと、投資助言ではないことを明示

## 調査テーマ

| 公開スラッグ | 表示名 | 主な検証軸 |
| --- | --- | --- |
| `credit` | クレジット・スプレッド | 信用リスクへの追加補償は悪化余地に見合うか |
| `imura` | ファンド・指数比較 | 条件とリスクをそろえても超過収益が残るか |
| `index_7_portfolio` | 7指数ポートフォリオ | 分散が実際の下落局面で機能するか |
| `index_etf_comparison` | 指数ETF比較 | 同じ指数名でも投資結果を分ける条件は何か |
| `legendary_investors` | 著名投資家リサーチ | 公開情報から再現可能な判断原則を抽出できるか |
| `oracle` | Oracle実績・予測監査 | 受注残が売上とキャッシュへ転換するか |
| `precious_metals_spread` | 貴金属スプレッド | 価格差が平均回帰か構造変化か |
| `securities_collateral_loan` | 証券担保ローン | どの下落率から意思決定の自由が失われるか |
| `semiconductors` | 半導体サイクル | 利益成長が数量・価格・能力のどこから生じるか |
| `yield_spread` | 金利・イールドスプレッド | 金利差がどの期待とリスクプレミアムを反映するか |

## ディレクトリ構造

```text
config/data_platform.yaml   一次データ源・利用権・更新契約
config/use_cases/           ユースケース設定
crew/data_platform/         取得・raw保存・Parquet・DuckDB・品質検査
                               sources/  FRED / Treasury / SEC / governed manual
                               cli.py    crew-data CLI
                               storage.py immutable lake + catalogue
                               quality.py common quality gates
data/platform/              正準データ（Git管理外）
output/use_cases/           公開分析結果の正本
web/                        GitHub Pages生成器・静的監査
docs/                       生成された公開サイトと設計文書
tests/data_platform/        ネットワーク非依存の契約試験
```

## 実行

```bash
task data:validate
task data:test
task data:sync:registry   # 外部認証不要
task data:sync:public     # FRED_API_KEY / SEC_USER_AGENT 必須
task data:status

task process:all          # 移行期間中の既存パイプラインと分析
task serve                # ローカルWeb画面
```

静的サイトのみを生成・監査する場合:

```bash
uv run python web/build_static.py
uv run python web/audit_static.py
```

## 分析品質の確認項目

- データ対象期間、取得日時、公開日時、改訂ビンテージを残す
- 原文レスポンスとSHA-256を保存する
- 通貨、単位、配当、分割、市場休業日、ライセンスを明示する
- 比較指数と計算条件をそろえる
- インサンプルとアウト・オブ・サンプルを分離する
- 手数料、税、スリッページを含まない結果を実績と呼ばない
- 予測入力期間、予測期間、評価指標を保存する
- LLMによる文章と定量計算結果を区別する
- 取得失敗、欠損、利用権未確認を推測で補完しない

## 注意

- 掲載値は各レポート作成日時点のスナップショットです
- 過去の成績は将来の収益を保証しません
- 予測値は確定的な将来価格ではありません
- 本プロジェクトは投資助言、売買推奨、運用実績の保証ではありません

**最終構造監査:** 2026-08-04
