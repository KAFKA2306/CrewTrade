# REST API

## 頻度UI

FreqUI には専用の [ドキュメント セクション](freq-ui.md) が追加されました。FreqUI に関するすべての情報については、そのセクションを参照してください。

## 構成

api_server セクションを構成に追加し、「api_server.enabled」を「true」に設定して、REST API を有効にします。

サンプル構成:
``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "somethingrandom",
        "CORS_origins": [],
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        "ws_token": "sercet_Ws_t0ken"
    },
```
!!! Danger "セキュリティ警告"
    デフォルトでは、構成はローカルホストのみをリッスンします (そのため、他のシステムからはアクセスできません)。他の人がボットを制御できる可能性があるため、この API をインターネットに公開せず、強力で一意のパスワードを選択することを強くお勧めします。

??? 「リモートサーバー上のAPI/UIアクセス」に注意してください。
    VPS 上で実行している場合は、ボットに接続するために ssh トンネルを使用するか、VPN (openVPN、ワイヤーガード) をセットアップすることを検討する必要があります。
    これにより、freqUI がインターネットに直接公開されなくなりますが、これはセキュリティ上の理由から推奨されません (freqUI はそのままでは https をサポートしません)。
    これらのツールのセットアップはこのチュートリアルの一部ではありませんが、インターネット上で多くの優れたチュートリアルが見つかります。

その後、ブラウザで「http://127.0.0.1:8080/api/v1/ping」にアクセスして API にアクセスし、API が正しく実行されているかどうかを確認します。
これにより、次の応答が返されるはずです。
``` output
{"status":"pong"}
```
他のすべてのエンドポイントは機密情報を返し、認証が必要なため、Web ブラウザーからは利用できません。

### セキュリティ

安全なパスワードを生成するには、パスワード マネージャーを使用するか、以下のコードを使用するのが最適です。
``` python
import secrets
secrets.token_hex()
```
!!! Hint "JWTトークン"
    同じメソッドを使用して、JWT 秘密鍵 (`jwt_secret_key`) も生成します。

!!! Danger "パスワードの選択"
    ボットを不正アクセスから保護するために、非常に強力で固有のパスワードを選択してください。
    また、`jwt_secret_key` をランダムなものに変更します (これを覚えておく必要はありませんが、セッションを暗号化するために使用されるため、一意のものにしたほうがよいでしょう)。

### docker を使用した構成

Docker を使用してボットを実行する場合は、ボットに受信接続をリッスンさせる必要があります。その後、セキュリティは docker によって処理されます。
``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    },
```
docker-compose ファイル内で次の 2 行が利用可能であることを確認してください。
```yml
    ports:
      - "127.0.0.1:8080:8080"
```
!!! Danger "セキュリティ警告"
    Docker ポート マッピングで `"8080:8080"` (または `"0.0.0.0:8080:8080"`) を使用すると、正しいポートでサーバーに接続しているすべてのユーザーが API を利用できるようになり、他のユーザーがボットを制御できる可能性があります。
    これは、安全な環境 (ホーム ネットワークなど) でボットを実行している場合には安全である可能性がありますが、API をインターネットに公開することはお勧めできません。

## 残りの API

### API の使用

サポートされている `freqtrade-client` パッケージ (`scripts/rest_client.py` としても入手可能) を使用して API を使用することをお勧めします。

このコマンドは、`pip install freqtrade-client` を使用して、実行中の freqtrade ボットとは独立してインストールできます。

このモジュールは軽量になるように設計されており、「requests」モジュールと「python-rapidjson」モジュールのみに依存し、freqtrade が必要とする重い依存関係はすべてスキップします。
``` bash
freqtrade-client <command> [optional parameters]
```
デフォルトでは、スクリプトは `127.0.0.1` (localhost) およびポート `8080` が使用されることを想定していますが、設定ファイルを指定してこの動作をオーバーライドすることができます。

#### 最小限のクライアント構成
``` json
{
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    }
}
```

``` bash
freqtrade-client --config rest_config.json <command> [optional parameters]
```
多くの引数を持つコマンドには、(わかりやすくするために) キーワード引数が必要になる場合があります。キーワード引数は次のように指定できます。
``` bash
freqtrade-client --config rest_config.json forceenter BTC/USDT long enter_tag=GutFeeling
```
このメソッドはすべての引数に対して機能します。使用可能なパラメータのリストについては、「show」コマンドを確認してください。

??? 「プログラムによる使用」に関する注意
    `freqtrade-client` パッケージ (freqtrade とは独立してインストール可能) を独自のスクリプトで使用して、freqtrade API と対話できます。
    これを行うには、以下を使用してください。
    ``` python
    from freqtrade_client import FtRestClient
    

    client = FtRestClient(server_url, username, password)

    # Get the status of the bot
    ping = client.ping()
    print(ping)

    # Add pairs to blacklist
    client.blacklist("BTC/USDT", "ETH/USDT")
    # Add pairs to blacklist by supplying a list
    client.blacklist(*listPairs)
    # ... 
    ```
使用可能なコマンドの完全なリストについては、以下のリストを参照してください。

`help` コマンドを使用すると、Rest-client スクリプトから使用可能なコマンドをリストできます。
``` bash
freqtrade-client help
```

``` output
Possible commands:

available_pairs
    Return available pair (backtest data) based on timeframe / stake_currency selection

        :param timeframe: Only pairs with this timeframe available.
        :param stake_currency: Only pairs that include this timeframe

balance
    Get the account balance.

blacklist
    Show the current blacklist.

        :param add: List of coins to add (example: "BNB/BTC")

cancel_open_order
    Cancel open order for trade.

        :param trade_id: Cancels open orders for this trade.

count
    Return the amount of open trades.

daily
    Return the profits for each day, and amount of trades.

delete_lock
    Delete (disable) lock from the database.

        :param lock_id: ID for the lock to delete

delete_trade
    Delete trade from the database.
        Tries to close open orders. Requires manual handling of this asset on the exchange.

        :param trade_id: Deletes the trade with this ID from the database.

forcebuy
    Buy an asset.

        :param pair: Pair to buy (ETH/BTC)
        :param price: Optional - price to buy

forceenter
    Force entering a trade

        :param pair: Pair to buy (ETH/BTC)
        :param side: 'long' or 'short'
        :param price: Optional - price to buy

forceexit
    Force-exit a trade.

        :param tradeid: Id of the trade (can be received via status command)
        :param ordertype: Order type to use (must be market or limit)
        :param amount: Amount to sell. Full sell if not given

health
    Provides a quick health check of the running bot.

lock_add
    Manually lock a specific pair

        :param pair: Pair to lock
        :param until: Lock until this date (format "2024-03-30 16:00:00Z")
        :param side: Side to lock (long, short, *)
        :param reason: Reason for the lock        

locks
    Return current locks

logs
    Show latest logs.

        :param limit: Limits log messages to the last <limit> logs. No limit to get the entire log.

pair_candles
    Return live dataframe for <pair><timeframe>.

        :param pair: Pair to get data for
        :param timeframe: Only pairs with this timeframe available.
        :param limit: Limit result to the last n candles.

pair_history
    Return historic, analyzed dataframe

        :param pair: Pair to get data for
        :param timeframe: Only pairs with this timeframe available.
        :param strategy: Strategy to analyze and get values for
        :param timerange: Timerange to get data for (same format than --timerange endpoints)

performance
    Return the performance of the different coins.

ping
    simple ping

plot_config
    Return plot configuration if the strategy defines one.

profit
    Return the profit summary.

reload_config
    Reload configuration.

show_config
    Returns part of the configuration, relevant for trading operations.

start
    Start the bot if it's in the stopped state.

pause
    Pause the bot if it's in the running state. If triggered on stopped state will handle open positions.

stats
    Return the stats report (durations, sell-reasons).

status
    Get the status of open trades.

stop
    Stop the bot. Use `start` to restart.

stopbuy
    Stop buying (but handle sells gracefully). Use `reload_config` to reset.

strategies
    Lists available strategies

strategy
    Get strategy details

        :param strategy: Strategy class name

sysinfo
    Provides system information (CPU, RAM usage)

trade
    Return specific trade

        :param trade_id: Specify which trade to get.

trades
    Return trades history, sorted by id

        :param limit: Limits trades to the X last trades. Max 500 trades.
        :param offset: Offset by this amount of trades.

list_open_trades_custom_data
    Return a dict containing open trades custom-datas

        :param key: str, optional - Key of the custom-data
        :param limit: Limits trades to X trades.
        :param offset: Offset by this amount of trades.

list_custom_data
    Return a dict containing custom-datas of a specified trade

        :param trade_id: int - ID of the trade
        :param key: str, optional - Key of the custom-data

version
    Return the version of the bot.

whitelist
    Show the current whitelist.


```
### 利用可能なエンドポイント

別のルート経由で REST API を手動で呼び出したい場合は、 「curl」を介して直接実行する場合、以下の表に、関連する URL エンドポイントとパラメータを示します。
以下の表のすべてのエンドポイントには、API のベース URL をプレフィックスとして付ける必要があります。 `http://127.0.0.1:8080/api/v1/` - したがって、コマンドは `http://127.0.0.1:8080/api/v1/<command>` になります。

|  エンドポイント |方法 |説明/パラメータ |
|----------|----------|---------------|
| `/ping` |入手 | API Readiness をテストする単純なコマンド - 認証は必要ありません。
| `/スタート` |投稿 |トレーダーを開始します。
| `/一時停止` |投稿 |トレーダーを一時停止します。ルールに従って公開取引を適切に処理します。新しいポジションには入らないでください。
| `/停止` |投稿 |トレーダーを止めます。
| `/ストップバイ` |投稿 |トレーダーが新しい取引を開始するのを阻止します。ルールに従ってオープンな取引を正常に終了します。
| `/reload_config` |投稿 |設定ファイルをリロードします。
| `/トレード` |入手 |最後の取引をリストします。コールあたりの取引は 500 件に制限されています。
| `/trade/<tradeid>` |入手 |特定の取引を取得します。<br/>*Params:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>` |削除 |データベースから取引を削除します。オープン注文をクローズしようとします。取引所でこの取引を手動で処理する必要があります。<br/>*Params:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/open-order` |削除 |この取引のオープン注文をキャンセルします。<br/>*Params:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/reload` |投稿 |取引所から取引をリロードします。ライブでのみ機能し、取引所で手動で売却された取引の回収に役立つ可能性があります。<br/>*Params:*<br/>- `tradeid` (`int`)
| `/show_config` |入手 |現在の構成の一部と、動作に関連する設定を表示します。
| `/ログ` |入手 |最新のログメッセージを表示します。
| `/ステータス` |入手 |オープンな取引をすべてリストします。
| `/カウント` |入手 |使用された取引と利用可能な取引の数を表示します。
| `/エントリ` |入手 |指定されたペア (ペアが指定されていない場合はすべてのペア) の各入力タグの利益統計を表示します。ペアはオプションです。<br/>*Params:*<br/>- `pair` (`str`)
| `/終了` |入手 |指定されたペア (ペアが指定されていない場合はすべてのペア) の各終了理由の利益統計を表示します。ペアはオプションです。<br/>*Params:*<br/>- `pair` (`str`)
| `/mix_tags` |入手 |指定されたペア (ペアが指定されていない場合はすべてのペア) の入力タグ + 終了理由の各組み合わせの収益統計を表示します。ペアはオプションです。<br/>*Params:*<br/>- `pair` (`str`)
| `/ロック` |入手 |現在ロックされているペアを表示します。
| `/ロック` |投稿 | 「まで」までペアをロックします。 (期限は最も近い時間枠に切り上げられます)。サイドはオプションで、「ロング」または「ショート」のいずれかです（デフォルトは「ロング」です）。理由はオプションです。<br/>*Params:*<br/>- `<pair>` (`str`)<br/>- `<until>` (`datetime`)<br/>- `[side]` (`str`)<br/>- `[reason]` (`str`)
| `/locks/<ロックID>` |削除 | ID によってロックを削除 (無効化) します。<br/>*Params:*<br/>- `lockid` (`int`)
| `/利益` |入手 |クローズ取引からの利益/損失の概要とパフォーマンスに関するいくつかの統計を表示します。
| `/強制終了` |投稿 |指定された注文タイプ (「マーケット」または「リミット」、指定されていない場合は構成設定を使用)、および選択された金額 (指定されていない場合は全額売り) を使用して、指定された取引 (「minimum_roi」を無視) を即座に終了します。 `all` を `tradeid` として指定すると、現在開いているすべての取引が強制終了されます。<br/>*Params:*<br/>- `<tradeid>` (`int` または `str`)<br/>- `<ordertype>` (`str`)<br/>- `[amount]` (`float`)
| `/forceenter` |投稿 |指定されたペアを即座に入力します。サイドはオプションで、「ロング」または「ショート」のいずれかです（デフォルトは「ロング」です）。料金はオプションです。 (`force_entry_enable` は True に設定する必要があります)<br/>*Params:*<br/>- `<pair>` (`str`)<br/>- `<side>` (`str`)<br/>- `[rate]` (`float`)
| `/パフォーマンス` |入手 |完了した各取引のパフォーマンスをペアごとにグループ化して表示します。
| `/バランス` |入手 |通貨ごとの口座残高を表示します。
| `/毎日` |入手 |過去 n 日間の 1 日あたりの損益を表示します (n のデフォルトは 7)。<br/>*Params:*<br/>- `timescale` (`int`)
| `/毎週` |入手 |過去 n 日間の週ごとの損益を表示します (n のデフォルトは 4)。<br/>*Params:*<br/>- `timescale` (`int`)
| `/毎月` |入手 |過去 n 日間の月ごとの損益を表示します (n のデフォルトは 3)。<br/>*Params:*<br/>- `timescale` (`int`)
| `/統計` |入手 |利益/損失の理由と平均保有時間の概要を表示します。
| `/ホワイトリスト` |入手 |現在のホワイトリストを表示します。
| `/ブラックリスト` |入手 |現在のブラックリストを表示します。
| `/ブラックリスト` |投稿 |指定されたペアをブラックリストに追加します。<br/>*Params:*<br/>- `blacklist` (`str`)
| `/ブラックリスト` |削除 |指定されたペアのリストをブラックリストから削除します。<br/>*Params:*<br/>- `[pair,pair]` (`list[str]`)
| `/ペアキャンドル` |入手 |ボットの実行中に、ペアとタイムフレームの組み合わせのデータフレームを返します。 **アルファ**
| `/ペアキャンドル` |投稿 |ボットの実行中に、指定された列のリストでフィルター処理された、ペアとタイムフレームの組み合わせのデータフレームを返します。 **アルファ**<br/>*Params:*<br/>- `<column_list>` (`list[str]`)
| `/pair_history` |入手 |指定された戦略によって分析された、指定された時間範囲の分析されたデータフレームを返します。 **アルファ**
| `/pair_history` |投稿 |指定された戦略によって分析され、返される列の指定されたリストによってフィルター処理された、指定された時間範囲の分析されたデータフレームを返します。 **アルファ**<br/>*Params:*<br/>- `<column_list>` (`list[str]`)
| `/plot_config` |入手 |戦略からプロット構成を取得します (構成されていない場合は何も取得しません)。 **アルファ**
| `/戦略` |入手 |戦略ディレクトリ内の戦略をリストします。 **アルファ**
| `/strategy/<strategy>` |入手 |戦略クラス名によって特定の戦略コンテンツを取得します。 **アルファ**<br/>*Params:*<br/>- `<戦略>` (`str`)
| `/available_pairs` |入手 |利用可能なバックテスト データをリストします。 **アルファ**
| `/バージョン` |入手 |バージョンを表示します。
| `/sysinfo` |入手 |システム負荷に関する情報を表示します。
| `/健康` |入手 |ボットの健全性 (最後のボット ループ) を表示します。

!!! Warning "アルファステータス"
    上記の *アルファ ステータス* のラベルが付いたエンドポイントは、予告なくいつでも変更される可能性があります。

### メッセージ WebSocket

API サーバーには、freqtrade ボットからの RPC メッセージをサブスクライブするための WebSocket エンドポイントが含まれています。
これを使用して、エントリ/イグジットフィルメッセージ、ホワイトリストの変更、ペアの入力されたインジケーターなど、ボットからのリアルタイムデータを消費できます。

これは、Freqtrade で [Producer/Consumer モード](Producer-consumer.md) を設定するためにも使用されます。

REST API がポート `8080` の `127.0.0.1` に設定されていると仮定すると、エンドポイントは `http://localhost:8080/api/v1/message/ws` で利用できます。

WebSocket エンドポイントにアクセスするには、エンドポイント URL のクエリ パラメーターとして「ws_token」が必要です。

安全な「ws_token」を生成するには、次のコードを実行できます。
``` python
>>> import secrets
>>> secrets.token_urlsafe(25)
'hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q'
```
次に、そのトークンを「api_server」設定の「ws_token」の下に追加します。同様に:
``` json
"api_server": {
    "enabled": true,
    "listen_ip_address": "127.0.0.1",
    "listen_port": 8080,
    "verbosity": "error",
    "enable_openapi": false,
    "jwt_secret_key": "somethingrandom",
    "CORS_origins": [],
    "username": "Freqtrader",
    "password": "SuperSecret1!",
    "ws_token": "hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q" // <-----
},
```
これで、`http://localhost:8080/api/v1/message/ws?token=hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q` のエンドポイントに接続できるようになります。

!!! Danger "サンプルトークンの再利用"
    上記のサンプル トークンは使用しないでください。安全を確保するには、完全に新しいトークンを生成します。

#### WebSocket の使用

WebSocket に接続すると、ボットは RPC メッセージを購読しているすべての人に RPC メッセージをブロードキャストします。メッセージのリストを購読するには、以下のような JSON リクエストを WebSocket 経由で送信する必要があります。 `data` キーはメッセージ タイプ文字列のリストでなければなりません。
``` json
{
  "type": "subscribe",
  "data": ["whitelist", "analyzed_df"] // A list of string message types
}
```
メッセージ タイプのリストについては、「freqtrade/enums/rpcmessagetype.py」の RPCMessageType enum を参照してください。

これで、これらのタイプの RPC メッセージがボットで送信されるたびに、接続がアクティブである限り、WebSocket 経由でメッセージを受信できるようになります。通常、リクエストはリクエストと同じ形式を取ります。
``` json
{
  "type": "analyzed_df",
  "data": {
      "key": ["NEO/BTC", "5m", "spot"],
      "df": {}, // The dataframe
      "la": "2022-09-08 22:14:41.457786+00:00"
  }
}
```
#### リバース プロキシのセットアップ

[Nginx](https://nginx.org/en/docs/) を使用する場合、WebSocket が機能するには次の構成が必要です (この構成は不完全で、一部の情報が欠落しているため、そのままでは使用できないことに注意してください)。

`<freqtrade_listen_ip>` (および後続のポート) を、構成/セットアップに一致する IP とポートに置き換えてください。
```
http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    #...

    server {
        #...

        location / {
            proxy_http_version 1.1;
            proxy_pass http://<freqtrade_listen_ip>:8080;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
        }
    }
}
```
リバース プロキシを適切に (安全に) 構成するには、WebSocket のプロキシに関するドキュメントを参照してください。

- **Traefik**: Traefik はすぐに WebSocket をサポートします。[ドキュメント](https://doc.traefik.io/traefik/) を参照してください。
- **Caddy**: Caddy v2 はすぐに WebSocket をサポートします。[ドキュメント](https://caddyserver.com/docs/v2-upgrade#proxy) を参照してください。

!!! Tip "SSL証明書"
    certbot などのツールを使用して SSL 証明書をセットアップし、上記のリバース プロキシのいずれかを使用して暗号化された接続を通じてボットの UI にアクセスできます。
    これにより転送中のデータは保護されますが、プライベート ネットワーク (VPN、SSH トンネル) の外部で freqtrade API を実行することはお勧めしません。

### OpenAPI インターフェース

組み込みの openAPI インターフェイス (Swagger UI) を有効にするには、api_server 設定で `"enable_openapi": true` を指定します。
これにより、「/docs」エンドポイントで Swagger UI が有効になります。デフォルトでは、<http://localhost:8080/docs> で実行されますが、設定によって異なります。

### JWT トークンを使用した高度な API の使用法

!!! Note
    以下はアプリケーション (API 経由で情報を取得する Freqtrade REST API クライアント) で実行する必要があり、定期的に使用することを目的としていません。

Freqtrade の REST API は、JWT (JSON Web Token) も提供します。
次のコマンドを使用してログインし、結果として得られる access_token を使用できます。
``` bash
> curl -X POST --user Freqtrader http://localhost:8080/api/v1/token/login
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g","refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiZWQ1ZWI3YjAtYjMwMy00YzAyLTg2N2MtNWViMjIxNWQ2YTMxIiwiZXhwIjoxNTkxNzExNjgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.d1AT_jYICyTAjD0fiQAr52rkRqtxCjUGEMwlNuuzgNQ"}

> access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g"
# Use access_token for authentication
> curl -X GET --header "Authorization: Bearer ${access_token}" http://localhost:8080/api/v1/count

```
アクセス トークンには短いタイムアウト (15 分) があるため、「token/refresh」リクエストを定期的に使用して新しいアクセス トークンを取得する必要があります。
``` bash
> curl -X POST --header "Authorization: Bearer ${refresh_token}"http://localhost:8080/api/v1/token/refresh
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk5NzQsIm5iZiI6MTU4OTExOTk3NCwianRpIjoiMDBjNTlhMWUtMjBmYS00ZTk0LTliZjAtNWQwNTg2MTdiZDIyIiwiZXhwIjoxNTg5MTIwODc0LCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.1seHlII3WprjjclY6DpRhen0rqdF4j6jbvxIhUFaSbs"}
```
--8<-- "includes/cors.md"
