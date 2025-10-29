# 頻度UI

Freqtrade は、freqtrade フロントエンドである [FreqUI](https://github.com/freqtrade/frequi) を提供できる組み込み Web サーバーを提供します。

デフォルトでは、UI はインストール (スクリプト、Docker) の一部として自動的にインストールされます。
freqUI は、「freqtrade install-ui」コマンドを使用して手動でインストールすることもできます。
これと同じコマンドを使用して、freqUI を新しいリリースに更新することもできます。

ボットがトレード / ドライラン モード (`freqtrade trade` を使用) で開始されると、設定された API ポート (デフォルトでは `http://127.0.0.1:8080`) で UI が利用可能になります。

??? 「freqUI に貢献したいですか?」に注意してください。
    開発者はこのメソッドを使用せず、[freqUI リポジトリ](https://github.com/freqtrade/frequi) で説明されているメソッドを使用して対応するクローンを作成し、freqUI のソースコードを取得する必要があります。フロントエンドを構築するには、動作するノードのインストールが必要です。

!!! ヒント「freqtrade を実行するのに freqUI は必要ありません」
    freqUI は freqtrade のオプションのコンポーネントであり、ボットの実行には必須ではありません。
    これはボットを監視し、ボットと対話するために使用できるフロントエンドです。しかし、freqtrade 自体はそれなしでも完全に正常に動作します。

## 構成

FreqUI には独自の構成ファイルがありませんが、[rest-api](rest-api.md) の動作セットアップが利用可能であることを前提としています。
freqUI を使用してセットアップするには、対応するドキュメント ページを参照してください。

## UI

FreqUI は、ボットの監視と対話に使用できる最新の応答性の高い Web アプリケーションです。

FreqUI は、明るいテーマと暗いテーマを提供します。
テーマは、ページ上部の目立つボタンから簡単に切り替えることができます。
このページのスクリーンショットのテーマは、選択したドキュメントのテーマに適応するため、ダーク (またはライト) バージョンを表示するには、ドキュメントのテーマを切り替えてください。

### ログイン

以下のスクリーンショットは、freqUI のログイン画面を示しています。

![FreqUI - ログイン](assets/frequi-login-CORS.png#only-dark)
![FreqUI - ログイン](assets/frequi-login-CORS-light.png#only-light)

!!! ヒント「CORS」
    このスクリーンショットに示されている Cors エラーは、UI が API とは異なるポートで実行されており、[CORS](#cors) がまだ正しくセットアップされていないことが原因です。

### 取引ビュー

取引ビューを使用すると、ボットが行っている取引を視覚化し、ボットと対話することができます。
このページでは、ボットを開始および停止して対話することもできます。また、設定されている場合は、強制的にトレードのエントリーとエグジットを行うこともできます。

![FreqUI - トレードビュー](assets/freqUI-trade-pane-dark.png#only-dark)
![FreqUI - トレードビュー](assets/freqUI-trade-pane-light.png#only-light)

### プロットコンフィギュレーター

FreqUI プロットは、戦略内の `plot_config` 設定オブジェクト (「戦略から」ボタンでロード可能) または UI 経由で設定できます。
複数のプロット構成を作成し、自由に切り替えることができるため、チャートに柔軟でさまざまなビューを表示できます。

プロット設定には、取引ビューの右上隅にある「プロット コンフィギュレーター」(歯車アイコン) ボタンからアクセスできます。

![FreqUI - プロット構成](assets/freqUI-plot-configurator-dark.png#only-dark)
![FreqUI - プロット構成](assets/freqUI-plot-configurator-light.png#only-light)

### 設定

設定ページにアクセスすると、いくつかの UI 関連の設定を変更できます。

変更できるもの (特に):

* UIのタイムゾーン
* ファビコン (ブラウザ タブ) の一部としてオープン取引を視覚化
※キャンドルの色（上/下→赤/緑）
* アプリ内通知タイプを有効/無効にします

![FreqUI - 設定ビュー](assets/frequi-settings-dark.png#only-dark)
![FreqUI - 設定ビュー](assets/frequi-settings-light.png#only-light)

## Webサーバーモード

freqtrade が [ウェブサーバー モード](utils.md#webserver-mode) で開始されると (freqtrade は `freqtrade webserver` で開始されます)、ウェブサーバーは追加機能を許可する特別なモードで開始されます。例:

※データのダウンロード中
* ペアリストのテスト
* [バックテスト戦略](#backtesting)
* ... 拡張予定

### バックテスト

freqtrade が [ウェブサーバー モード](utils.md#webserver-mode) で開始されると (freqtrade は `freqtrade webserver` で開始されます)、バックテスト ビューが利用可能になります。
このビューにより、戦略をバックテストし、結果を視覚化することができます。

以前のバックテスト結果をロードして視覚化したり、結果を相互に比較したりすることもできます。

![FreqUI - バックテスト](assets/freqUI-backtesting-dark.png#only-dark)
![FreqUI - バックテスト](assets/freqUI-backtesting-light.png#only-light)


--8<-- "includes/cors.md"
