# ![freqtrade](https://raw.githubusercontent.com/freqtrade/freqtrade/develop/docs/assets/freqtrade_poweredby.svg)

[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04864/status.svg)](https://doi.org/10.21105/joss.04864)
[![Coverage Status](https://coveralls.io/repos/github/freqtrade/freqtrade/badge.svg?branch=develop&service=github)](https://coveralls.io/github/freqtrade/freqtrade?branch=develop)
[![Documentation](https://readthedocs.org/projects/freqtrade/badge/)](https://www.freqtrade.io)

FreqtradeはPythonで書かれた無料のオープンソース暗号通貨トレーディングボットです。すべての主要取引所をサポートし、TelegramまたはWebUIを介して制御できるように設計されています。バックテスト、プロット、資金管理ツール、さらに機械学習による戦略最適化が含まれています。

![freqtrade](https://raw.githubusercontent.com/freqtrade/freqtrade/develop/docs/assets/freqtrade-screenshot.png)

## 免責事項

このソフトウェアは教育目的のみです。失うことを恐れているお金でリスクを取らないでください。ソフトウェアは自己責任で使用してください。著者およびすべての関連会社は、あなたのトレード結果について責任を負いません。

常にドライランでトレーディングボットを実行することから始め、それがどのように機能するか、どのような利益/損失を期待すべきかを理解する前に資金を投入しないでください。

コーディングとPythonの知識を持つことを強く推奨します。ソースコードを読み、このボットのメカニズムを理解することをためらわないでください。

## サポートされている取引所

各取引所に必要な特別な設定については、[取引所固有の注意事項](docs/exchanges.md)をお読みください。

- [X] [Binance](https://www.binance.com/)
- [X] [BingX](https://bingx.com/invite/0EM9RX)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bitmart](https://bitmart.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [HTX](https://www.htx.com/)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (分散型取引所、またはDEX)
- [X] [Kraken](https://kraken.com/)
- [X] [OKX](https://okx.com/)
- [X] [MyOKX](https://okx.com/) (OKX EEA)
- [ ] [その他多数の可能性](https://github.com/ccxt/ccxt/) _(動作を保証できません)_

### サポートされている先物取引所（実験的）

- [X] [Binance](https://www.binance.com/)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (分散型取引所、またはDEX)
- [X] [OKX](https://okx.com/)
- [X] [Bybit](https://bybit.com/)

始める前に、[取引所固有の注意事項](docs/exchanges.md)および[レバレッジ取引](docs/leverage.md)のドキュメントを必ずお読みください。

### コミュニティでテスト済み

コミュニティによって動作が確認された取引所:

- [X] [Bitvavo](https://bitvavo.com/)
- [X] [Kucoin](https://www.kucoin.com/)

## ドキュメント

ボットがどのように機能するかを理解するために、ボットのドキュメントを読むことをお勧めします。

完全なドキュメントは[freqtradeウェブサイト](https://www.freqtrade.io)でご覧いただけます。

## 機能

- [x] **Python 3.11+ベース**: Windows、macOS、Linuxなど、あらゆるオペレーティングシステムでボットを実行できます。
- [x] **永続性**: sqliteによる永続性を実現しています。
- [x] **ドライラン**: お金を使わずにボットを実行できます。
- [x] **バックテスト**: 売買戦略のシミュレーションを実行します。
- [x] **機械学習による戦略最適化**: 機械学習を使用して、実際の取引所データで売買戦略パラメーターを最適化します。
- [X] **適応型予測モデリング**: 適応型機械学習手法を通じて市場に自己学習するFreqAIでスマートな戦略を構築します。[詳細はこちら](https://www.freqtrade.io/en/stable/freqai/)
- [x] **暗号通貨のホワイトリスト**: トレードしたい暗号通貨を選択するか、動的ホワイトリストを使用します。
- [x] **暗号通貨のブラックリスト**: 避けたい暗号通貨を選択します。
- [x] **組み込みWebUI**: ボットを管理するための組み込みWebUI。
- [x] **Telegram経由で管理可能**: Telegramでボットを管理します。
- [x] **法定通貨で損益を表示**: 法定通貨で損益を表示します。
- [x] **パフォーマンスステータスレポート**: 現在のトレードのパフォーマンスステータスを提供します。

## クイックスタート

すぐに始める方法については、[Dockerクイックスタートドキュメント](https://www.freqtrade.io/en/stable/docker_quickstart/)を参照してください。

さらなる（ネイティブ）インストール方法については、[インストールドキュメントページ](https://www.freqtrade.io/en/stable/installation/)を参照してください。

## 基本的な使い方

### ボットコマンド

```
使用法: freqtrade [-h] [-V]
                 {trade,create-userdir,new-config,show-config,new-strategy,download-data,convert-data,convert-trade-data,trades-to-ohlcv,list-data,backtesting,backtesting-show,backtesting-analysis,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-markets,list-pairs,list-strategies,list-hyperoptloss,list-freqaimodels,list-timeframes,show-trades,test-pairlist,convert-db,install-ui,plot-dataframe,plot-profit,webserver,strategy-updater,lookahead-analysis,recursive-analysis}
                 ...

無料のオープンソース暗号通貨トレーディングボット

位置引数:
  {trade,create-userdir,new-config,show-config,new-strategy,download-data,convert-data,convert-trade-data,trades-to-ohlcv,list-data,backtesting,backtesting-show,backtesting-analysis,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-markets,list-pairs,list-strategies,list-hyperoptloss,list-freqaimodels,list-timeframes,show-trades,test-pairlist,convert-db,install-ui,plot-dataframe,plot-profit,webserver,strategy-updater,lookahead-analysis,recursive-analysis}
    trade               トレードモジュール。
    create-userdir      user-dataディレクトリを作成します。
    new-config          新しい設定を作成します
    show-config         解決済み設定を表示します
    new-strategy        新しい戦略を作成します
    download-data       バックテスト用データをダウンロードします。
    convert-data        ローソク足(OHLCV)データをある形式から
                        別の形式に変換します。
    convert-trade-data  トレードデータをある形式から別の形式に変換します。
    trades-to-ohlcv     トレードデータをOHLCVデータに変換します。
    list-data           ダウンロード済みデータを一覧表示します。
    backtesting         バックテストモジュール。
    backtesting-show    過去のバックテスト結果を表示します
    backtesting-analysis
                        バックテスト分析モジュール。
    hyperopt            Hyperoptモジュール。
    hyperopt-list       Hyperopt結果を一覧表示します
    hyperopt-show       Hyperopt結果の詳細を表示します
    list-exchanges      利用可能な取引所を表示します。
    list-markets        取引所の市場を表示します。
    list-pairs          取引所のペアを表示します。
    list-strategies     利用可能な戦略を表示します。
    list-hyperoptloss   利用可能なhyperopt損失関数を表示します。
    list-freqaimodels   利用可能なfreqAIモデルを表示します。
    list-timeframes     取引所の利用可能な時間枠を表示します。
    show-trades         トレードを表示します。
    test-pairlist       ペアリスト設定をテストします。
    convert-db          データベースを別のシステムに移行します
    install-ui          FreqUIをインストールします
    plot-dataframe      インジケーター付きローソク足をプロットします。
    plot-profit         利益を示すプロットを生成します。
    webserver           Webサーバーモジュール。
    strategy-updater    古い戦略ファイルを現在のバージョンに更新します
    lookahead-analysis  潜在的な先読みバイアスをチェックします。
    recursive-analysis  潜在的な再帰的な式の問題をチェックします。

オプション:
  -h, --help            ヘルプメッセージを表示して終了します
  -V, --version         プログラムのバージョン番号を表示して終了します
```

### Telegram RPCコマンド

Telegramは必須ではありません。ただし、これはボットを制御する優れた方法です。詳細とコマンドの完全なリストについては、[ドキュメント](https://www.freqtrade.io/en/latest/telegram-usage/)を参照してください

- `/start`: トレーダーを起動します。
- `/stop`: トレーダーを停止します。
- `/stopentry`: 新しいトレードへのエントリーを停止します。
- `/status <trade_id>|[table]`: すべてまたは特定のオープントレードを一覧表示します。
- `/profit [<n>]`: 過去n日間のすべての完了したトレードからの累積利益を一覧表示します。
- `/profit_long [<n>]`: 過去n日間のすべての完了したロングトレードからの累積利益を一覧表示します。
- `/profit_short [<n>]`: 過去n日間のすべての完了したショートトレードからの累積利益を一覧表示します。
- `/forceexit <trade_id>|all`: 指定されたトレードを即座に終了します（`minimum_roi`を無視）。
- `/fx <trade_id>|all`: `/forceexit`のエイリアス
- `/performance`: ペアでグループ化された完了した各トレードのパフォーマンスを表示します
- `/balance`: 通貨ごとのアカウント残高を表示します。
- `/daily <n>`: 過去n日間の1日あたりの利益または損失を表示します。
- `/help`: ヘルプメッセージを表示します。
- `/version`: バージョンを表示します。


## 開発ブランチ

プロジェクトは現在、2つの主要なブランチでセットアップされています:

- `develop` - このブランチには新しい機能がよくありますが、破壊的な変更も含まれる場合があります。このブランチをできるだけ安定させるよう努めています。
- `stable` - このブランチには最新の安定リリースが含まれています。このブランチは一般的によくテストされています。
- `feat/*` - これらは機能ブランチで、積極的に作業中です。特定の機能をテストしたい場合を除き、これらを使用しないでください。

## サポート

### ヘルプ / Discord

ドキュメントでカバーされていない質問や、ボットに関する詳細情報、または単に同じ考えを持つ人々と交流したい場合は、Freqtradeの[discordサーバー](https://discord.gg/p7nuUNVfP7)に参加することをお勧めします。

### [バグ / 問題](https://github.com/freqtrade/freqtrade/issues?q=is%3Aissue)

ボットにバグを発見した場合は、まず[issue tracker](https://github.com/freqtrade/freqtrade/issues?q=is%3Aissue)を検索してください。報告されていない場合は、[新しいissueを作成](https://github.com/freqtrade/freqtrade/issues/new/choose)し、チームができるだけ早くサポートできるようにテンプレートガイドに従ってください。

作成されたすべての[issue](https://github.com/freqtrade/freqtrade/issues/new/choose)について、満足度をマークするか、均衡点に達したときにissueをクローズするためのリマインダーを行ってください。

--GitHubの[コミュニティポリシー](https://docs.github.com/en/site-policy/github-terms/github-community-code-of-conduct)を維持してください--

### [機能リクエスト](https://github.com/freqtrade/freqtrade/labels/enhancement)

ボットを改善するための素晴らしいアイデアをお持ちですか？まず、この機能が[既に議論されていない](https://github.com/freqtrade/freqtrade/labels/enhancement)か検索してください。リクエストされていない場合は、[新しいリクエストを作成](https://github.com/freqtrade/freqtrade/issues/new/choose)し、バグレポートに埋もれないようにテンプレートガイドに従ってください。

### [プルリクエスト](https://github.com/freqtrade/freqtrade/pulls)

ボットに機能が欠けていると感じますか？プルリクエストを歓迎します！

プルリクエストを送信する前に、要件を理解するために[貢献ドキュメント](https://github.com/freqtrade/freqtrade/blob/develop/CONTRIBUTING.md)をお読みください。

貢献するためにコーディングは必要ありません - ドキュメントの改善から始めてみませんか？
[good first issue](https://github.com/freqtrade/freqtrade/labels/good%20first%20issue)とラベル付けされたissueは、良い最初の貢献になり、コードベースに慣れるのに役立ちます。

**注意** 主要な新機能作業を開始する前に、*計画していることを説明するissueを開くか*、[discord](https://discord.gg/p7nuUNVfP7)で話し合ってください（このためには#devチャンネルを使用してください）。これにより、関係者が機能について貴重なフィードバックを提供し、あなたがそれに取り組んでいることを他の人に知らせることができます。

**重要:** 常に`stable`ブランチではなく、`develop`ブランチに対してPRを作成してください。

## 要件

### 最新の時計

時計は正確でなければならず、取引所との通信の問題を回避するために、非常に頻繁にNTPサーバーと同期する必要があります。

### 最小ハードウェア要件

このボットを実行するには、以下の最小限のクラウドインスタンスをお勧めします:

- 最小（推奨）システム要件: 2GB RAM、1GBディスクスペース、2vCPU

### ソフトウェア要件

- [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [TA-Lib](https://ta-lib.github.io/ta-lib-python/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (推奨)
- [Docker](https://www.docker.com/products/docker) (推奨)
