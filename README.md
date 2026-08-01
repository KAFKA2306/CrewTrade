# CrewTrade — 金融調査ワークスペース

[公開ダッシュボード](https://kafka2306.github.io/CrewTrade/) · [GitHub Actions](https://github.com/KAFKA2306/CrewTrade/actions)

CrewTradeは、市場データの取得、定量計算、時系列予測、文章による解釈をユースケース単位で実行し、分析スナップショットとして公開する研究プロジェクトです。

公開画面は、レポート名の一覧ではなく、**何を検証する分析なのか**を起点に設計しています。対象・期間・計算条件・予測・解釈を同じ証拠として扱わず、レポート本文でそれぞれ確認できる状態を目指します。

## 公開画面

- 調査テーマを「運用評価」「資産配分」「リスク管理」「産業分析」などの検証目的で整理
- テーマ、問い、説明文を横断検索
- 各テーマの最新スナップショットと公開レポート数を表示
- 日付別レポートを切り替えて、前提や結論の変化を追跡
- レポート画像・添付物を日付別アセットへ分離し、同名ファイルの上書きを防止
- 掲載値がリアルタイムではないこと、投資助言ではないことを画面内に明示

デザインは、背景 `#fbfaf7`、本文 `#243653`、青 `#8fb5ec`、ラベンダー `#b9a8e6`、ローズ `#efb4c1`、ミント `#b7dbc8`、アプリコット `#f3cfaa` を基調としています。

## 調査テーマ

| 公開スラッグ | 表示名 | 主な検証軸 |
| --- | --- | --- |
| `imura` | ファンド・指数比較 | 比較条件とリスクをそろえても超過収益が残るか |
| `index_7_portfolio` | 7指数ポートフォリオ | 分散が実際の下落局面で機能したか |
| `index_etf_comparison` | 指数ETF比較 | 同じ指数名でも投資結果を分ける条件は何か |
| `legendary_investors` | 著名投資家リサーチ | 公開情報から再現可能な判断原則を抽出できるか |
| `oracle` | 個別企業・時系列予測 | 予測がアウト・オブ・サンプルでも情報を持つか |
| `precious_metals_spread` | 貴金属スプレッド | 価格差が平均回帰か構造変化か |
| `securities_collateral_loan` | 証券担保ローン | どの下落率から意思決定の自由が失われるか |
| `semiconductors` | 半導体サイクル | 利益成長が数量・価格・能力のどこから生じたか |
| `yield_spread` | 金利・イールドスプレッド | 金利差の変化がどの期待を反映しているか |

未登録の出力ディレクトリは削除せず、「未分類」として表示します。名称や説明を推測で補完しません。

## ディレクトリ構造

```text
config/use_cases/           ユースケース設定
output/use_cases/           分析結果の正本
  <use_case>/<YYYYMMDD>/
    report.md               公開対象Markdown
    *.png / *.csv / ...     レポート添付物
web/
  catalog.py                表示名・分類・検証軸の定義
  build_static.py           GitHub Pages生成器
  audit_static.py           生成物監査
  static/                   共通CSS・JavaScript
  templates/                Jinjaテンプレート
docs/                       生成された静的サイト
```

分析結果の正本は `output/use_cases/` です。`docs/` は `web/build_static.py` から再生成されます。

## 公開ロジック

1. `output/use_cases/<use_case>/<date>/` を列挙
2. 公開対象Markdownを決定
3. テーマ情報を `web/catalog.py` から付与
4. MarkdownをHTMLへ変換
5. 添付物を `docs/<use_case>/assets/<date>/` へコピー
6. `docs/site-manifest.json` に公開テーマと日付を記録
7. `web/audit_static.py` で言語設定、テンプレート残存、旧UI残存を検査
8. GitHub Pagesへデプロイ

同一日付ディレクトリに複数のMarkdownがあり、`report.md` または `analysis_report.md` で公開対象を一意に決められない場合、ビルドは失敗します。曖昧なファイルを任意に選んで成功扱いしません。

## セットアップ

```bash
uv sync
```

Python要件は `>=3.11,<3.12` です。依存関係の正本は `pyproject.toml` です。

APIキーや外部サービスの認証情報は環境変数または非公開設定で管理し、リポジトリへコミットしないでください。

## 実行

```bash
task process:all   # データ取得から分析まで実行
task fetch:all     # データ取得
task run           # 分析実行
task serve         # ローカルWeb画面
```

静的サイトのみを生成・監査する場合:

```bash
uv run python web/build_static.py
uv run python web/audit_static.py
```

CLIエントリポイント:

```bash
uv run crew
uv run run_crew
uv run train
uv run replay
uv run test
```

## 分析品質の確認項目

- データの対象期間と取得日時を残す
- 配当、分割、通貨、市場休業日の扱いを明示する
- インサンプルとアウト・オブ・サンプルを分離する
- 比較指数と計算条件をそろえる
- 手数料、税、スリッページを含まない結果を実績と呼ばない
- 予測モデルの入力期間、予測期間、評価指標を保存する
- LLMによる文章と定量計算結果を区別する
- 取得失敗や欠損を推測で補完しない

## 注意

- 掲載値は各レポート作成日時点のスナップショットです
- 過去の成績は将来の収益を保証しません
- Chronosなどの予測値は確定的な将来価格ではありません
- 本プロジェクトは投資助言、売買推奨、運用実績の保証ではありません

**最終構造監査:** 2026-08-02
