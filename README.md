# CrewTrade — 一次データ駆動の金融調査ワークスペース

[公開ダッシュボード](https://kafka2306.github.io/CrewTrade/) · [データ基盤状態](https://kafka2306.github.io/CrewTrade/data-status/) · [GitHub Actions](https://github.com/KAFKA2306/CrewTrade/actions) · [データ基盤設計](docs/data-platform.md)

CrewTradeは、一次データの取得、定量計算、評価、文章による解釈を分離し、再検証可能な分析スナップショットとして公開する研究プロジェクトです。

取得経路、利用権、比較可能性、秘密性のいずれかが不足する場合は数値を推測せず、理由付きで停止します。Pagesの`OK`は「全テーマが数値を出している」ことではなく、到達可能な公開分析が正準稼働し、残りが明示的に統制されていることを意味します。

## 現在の運用状態

### 公開用の正準データへ接続済み

| テーマ | 正準入力 | 廃止した入力 |
| --- | --- | --- |
| 金利・イールドスプレッド | 米国財務省の名目・実質カーブ | HY実効利回り−10年国債、固定資産配分 |

### 統制された停止・一部利用

| テーマ | 状態 | 再開条件 |
| --- | --- | --- |
| Oracle実績・予測監査 | 外部実行基盤待ち | `data.sec.gov`へ到達できる検証済みrunner |
| 著名投資家リサーチ | 外部実行基盤待ち | SEC提出履歴・13F明細を取得できる検証済みrunner |
| クレジット・スプレッド | 再配布権待ち | ICE BofA OASの公開利用許諾 |
| ファンド・指数比較 | 契約待ち | fundnote公式機械可読NAV |
| 7指数ポートフォリオ | 契約待ち | JPX商品マスターと長期指数代替系列 |
| 指数ETF比較 | 契約待ち | ISIN・正式指数・通貨・費用を含む商品契約 |
| 貴金属スプレッド | ライセンス待ち | LBMA履歴保存・再配布権 |
| 証券担保ローン | 非公開入力待ち | 契約版・時価・銘柄別担保掛目 |
| 半導体サイクル | 一部利用可能 | WSTS詳細表・EDINET企業XBRL |

Oracleと著名投資家の旧固定値・固定ティッカー入力は廃止済みです。SEC公式APIへ切り替えた実装は保持していますが、GitHub-hosted runnerから`data.sec.gov`への要求が宣言済みUser-AgentでもHTTP 403となるため、Pages CIでは自動取得を停止しています。未検証の簡易XBRLパーサーへ置き換えず、到達可能なself-hosted、WSL、Dagu等の永続実行基盤が確認できてから再開します。

クレジット分析ではETF価格比を信用スプレッドとみなす旧実装を廃止しました。FREDが公開するICE BofA系列には内部利用・第三者公開に関する制約があるため、利用許諾を記録できるまでPagesへの数値更新を停止します。

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

GitHub Actionsのartifactは30日保持の検証スナップショットです。長期履歴はDagu、WSL、コンテナなどの永続ボリュームで保持します。

## 一次データ源

- 米国財務省の公式XMLから日次の名目パー・イールド・カーブを取得
- 米国財務省の公式XMLから日次の実質パー・イールド・カーブを取得
- 10年期待インフレは同日の名目10年金利から実質10年金利を引いた独自導出値として分離
- SEC EDGAR adapterは提出履歴、Company Facts、13F information table XMLに対応するが、Pages CIでは外部到達性のため停止
- ICE BofA OAS、JPX、EDINET、fundnote、LBMA、WSTS、非公開担保契約は`config/data_platform.yaml`で利用権と停止条件を管理

## 自動運用

`main`への基盤変更時、手動実行時、毎日05:17 JSTに次を実行します。

1. 米国財務省の名目・実質カーブを取得
2. raw・SHA-256・Parquet・DuckDBへ保存
3. 共通品質検査を実行
4. 金利・イールドスプレッドのレポートを生成
5. 残る9テーマの停止・一部利用・非公開入力状態を更新
6. GitHub Pagesを再生成・監査・公開

SEC取得は`sec_edgar` sourceを有効化し、連絡可能なUser-Agentと到達可能な外部runnerを設定した環境でのみ実行します。

## 実行

```bash
uv sync

task data:validate
task data:test
task data:sync
task data:status
task data:export-status

task process:all
```

公開用の個別実行:

```bash
task fetch:yield && task analyze:yield
```

SEC外部runnerで検証済みスナップショットが存在する場合のみ:

```bash
task fetch:oracle && task analyze:oracle
task fetch:legendary_investors && task analyze:legendary_investors
```

正準カタログをSQLで監査できます。

```bash
uv run crew-data query "select * from gold_treasury_curve_latest"
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
crew/yields/                       正準金利・カーブ分析
crew/oracle/                       SEC XBRL分析。外部runner用
crew/legendary_investors/          SEC 13F差分分析。外部runner用
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
- 取得失敗、利用権未確認、非公開入力不足を推測で補完しない
- 非公開契約・口座状態をPagesへ出力しない
- 外部APIの到達不能を成功扱いせず、理由付き統制状態へ移す

## 完了判定

Pages上のデータ基盤状態を`OK`とする条件は次です。

- 到達可能な正準接続済み1テーマに必要な3データセットが存在する
- 最新バッチの品質検査が成功している
- 残る9テーマが理由付きの統制状態にある
- 取得待ちが0件である
- 公開状態に秘密情報・再配布禁止データが含まれない
- 調査カタログとデータ状態の静的監査が成功する

## 注意

- 掲載値は各レポート生成日時点のスナップショットです
- 10年期待インフレは名目・実質パー・イールドの差で、FREDのブレークイーブン系列そのものではありません
- 13Fは四半期末時点の限定的な開示で、現在保有を示しません
- 過去の成績は将来の収益を保証しません
- 本プロジェクトは投資助言、売買推奨、運用実績の保証ではありません

**最終構造監査:** 2026-08-05
