# CrewTrade — 一次データ駆動の金融調査ワークスペース

[公開ダッシュボード](https://kafka2306.github.io/CrewTrade/) · [データ基盤状態](https://kafka2306.github.io/CrewTrade/data-status/) · [GitHub Actions](https://github.com/KAFKA2306/CrewTrade/actions) · [データ基盤設計](docs/data-platform.md)

CrewTradeは、一次データの取得、定量計算、評価、文章による解釈を分離し、再検証可能な分析スナップショットとして公開する研究プロジェクトです。

数値が取得できない場合は推測しません。利用権、比較可能性、秘密性、機械取得経路のいずれかが不足するときは、理由付きで分析を停止し、その状態をPagesへ公開します。

## 現在の運用状態

10テーマを次の2群に分けています。

### 正準データへ接続済み

| テーマ | 正準入力 | 廃止した入力 |
| --- | --- | --- |
| クレジット・スプレッド | FRED / ICE BofA OAS | 債券ETF価格比 |
| 金利・イールドスプレッド | FRED金利系列 / 米国財務省カーブ | HY実効利回り−10年国債、固定資産配分 |
| Oracle実績・予測監査 | SEC提出履歴 / XBRL Company Facts | 静的な基準四半期・未検証予測 |
| 著名投資家リサーチ | SEC 13F information table | 固定ティッカー配列・現在保有という表現 |

### 統制された停止・一部利用

| テーマ | 状態 | 再開条件 |
| --- | --- | --- |
| ファンド・指数比較 | 契約待ち | fundnote公式機械可読NAV |
| 7指数ポートフォリオ | 契約待ち | JPX商品マスターと長期指数代替系列 |
| 指数ETF比較 | 契約待ち | ISIN・正式指数・通貨・費用を含む商品契約 |
| 貴金属スプレッド | ライセンス待ち | LBMA履歴保存・再配布権 |
| 証券担保ローン | 非公開入力待ち | 契約版・時価・銘柄別担保掛目 |
| 半導体サイクル | 一部利用可能 | WSTS詳細表・EDINET企業XBRL |

停止中のテーマも異常ではありません。根拠が不足した数値を生成しないことを正常動作とします。

## 正準データ基盤

```text
公式API・統制された非公開入力
  → immutable raw response + SHA-256
  → normalized Parquet bronze layer
  → DuckDB catalogue / quality / lineage
  → deterministic gold views
  → use-case analysis / report / Pages
```

`data/platform/` が実行環境内の正準保存先です。

```text
data/platform/
├── raw/               取得した原文レスポンス
├── bronze/            正規化Parquet
├── manifests/         実行単位の来歴
└── catalog.duckdb     実行・ファイル・品質・gold view
```

GitHub Actionsのartifactは30日保持の検証スナップショットです。長期の正準履歴はDagu、WSL、コンテナなどの永続ボリュームで保持します。

## 一次データ源

- FRED APIを利用できる場合は`realtime_start`・`realtime_end`を含む改訂ビンテージを保存
- APIキーがない場合もFRED公式CSVを取得時点スナップショットとして保存
- 米国財務省の公式XMLから日次パー・イールド・カーブを取得
- SEC EDGARから提出履歴、Company Facts、13F information table XMLを取得
- JPX、EDINET、fundnote、LBMA、WSTS、非公開担保契約は`config/data_platform.yaml`で利用権と停止条件を管理

## 自動運用

`main`への基盤変更時、手動実行時、毎日05:17 JSTに次を実行します。

1. 正準一次データを取得
2. raw・SHA-256・Parquet・DuckDBへ保存
3. 共通品質検査を実行
4. 接続済み4テーマのレポートを生成
5. 公開可能な状態だけを`web/generated/data-platform-status.json`へ出力
6. GitHub Pagesを再生成・監査・公開

必要な秘密情報は任意の`FRED_API_KEY`だけです。SECのUser-Agentは公開リポジトリの連絡先をworkflowで宣言します。FRED APIキーがなくても公式CSVスナップショットで稼働します。

## 実行

```bash
uv sync

task data:validate
task data:test
task data:sync          # 全正準ソース
task data:status
task data:export-status

task process:all        # 正準取得 → 4分析 → Pages状態
```

個別実行:

```bash
task fetch:credit && task analyze:credit
task fetch:yield && task analyze:yield
task fetch:oracle && task analyze:oracle
task fetch:legendary_investors && task analyze:legendary_investors
```

正準カタログをSQLで監査できます。

```bash
uv run crew-data query "select * from gold_credit_oas_latest"
uv run crew-data query "select * from gold_treasury_curve_latest"
uv run crew-data query "select * from gold_sec_13f_holdings_latest"
```

静的サイトの生成と監査:

```bash
uv run python web/build_static.py
uv run python web/audit_static.py
uv run python web/build_data_status.py
uv run python web/audit_data_status.py
```

## 主要ディレクトリ

```text
config/data_platform.yaml          一次データ源・利用権・更新契約
config/use_case_data_status.yaml   10テーマの正準移行・停止状態
config/use_cases/                  分析条件
crew/data_platform/                取得・raw・Parquet・DuckDB・品質
crew/credit/                       正準OAS分析
crew/yields/                       正準金利・カーブ分析
crew/oracle/                       SEC XBRL分析
crew/legendary_investors/          SEC 13F差分分析
data/platform/                     正準データ。Git管理外
output/use_cases/                  公開レポートの正本
web/                               GitHub Pages生成・監査
web/generated/                     公開可能な基盤状態
web/templates/data_status.html     データ状態ページ
docs/                              生成済みPages
tests/data_platform/               ネットワーク非依存の契約試験
```

## 品質契約

- 対象期間、観測日、取得日時、公開日時、改訂ビンテージを保存
- 原文レスポンスとSHA-256を保存
- 主キーNULL、重複、非有限値、空データを拒否
- 通貨、単位、配当、分割、市場休業日、利用権を明示
- 異なる時点・定義・単位を無条件に結合しない
- 会社実績、会社予想、独自導出値、モデル予測を分離
- インサンプルとアウト・オブ・サンプルを分離
- 取得失敗や利用権未確認を推測で補完しない
- 非公開契約・口座状態をPagesへ出力しない

## 完了判定

Pages上のデータ基盤状態を`OK`とする条件は次です。

- 正準接続済み4テーマの必要データセットが存在する
- 最新バッチの品質検査が成功している
- 残る6テーマが理由付きの統制状態にある
- 公開状態に秘密情報が含まれない
- 調査カタログとデータ状態の静的監査が成功する

## 注意

- 掲載値は各レポート生成日時点のスナップショットです
- 13Fは四半期末時点の限定的な開示で、現在保有を示しません
- 過去の成績は将来の収益を保証しません
- 本プロジェクトは投資助言、売買推奨、運用実績の保証ではありません

**最終構造監査:** 2026-08-04
