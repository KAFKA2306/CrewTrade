# Webhookの使用法

## 設定

設定ファイルにwebhookセクションを追加し、`webhook.enabled`を`true`に設定してwebhookを有効にします。

サンプル設定（IFTTTを使用してテスト済み）。

```json
  "webhook": {
        "enabled": true,
        "url": "https://maker.ifttt.com/trigger/<YOUREVENT>/with/key/<YOURKEY>/",
        "entry": {
            "value1": "{pair}の購入",
            "value2": "指値{limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
        "entry_cancel": {
            "value1": "{pair}のオープン買い注文のキャンセル",
            "value2": "指値{limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
         "entry_fill": {
            "value1": "{pair}の買い注文が約定しました",
            "value2": "@{open_rate:8f}",
            "value3": ""
        },
        "exit": {
            "value1": "{pair}の決済",
            "value2": "指値{limit:8f}",
            "value3": "利益：{profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_cancel": {
            "value1": "{pair}のオープン決済注文のキャンセル",
            "value2": "指値{limit:8f}",
            "value3": "利益：{profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_fill": {
            "value1": "{pair}の決済注文が約定しました",
            "value2": "@{close_rate:8f}",
            "value3": ""
        },
        "status": {
            "value1": "ステータス：{status}",
            "value2": "",
            "value3": ""
        }
    },
```

`webhook.url`のURLは、webhookの正しいURLを指している必要があります。[IFTTT](https://ifttt.com)を使用している場合（上記のサンプルで示されているように）、イベントとキーをURLに挿入してください。

POSTボディの形式をフォームエンコード（デフォルト）、JSONエンコード、または生データに設定できます。それぞれ`"format": "form"`、`"format": "json"`、または`"format": "raw"`を使用します。Mattermost Cloud統合のサンプル設定：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURSUBDOMAIN>.cloud.mattermost.com/hooks/<YOURHOOK>",
        "format": "json",
        "status": {
            "text": "ステータス：{status}"
        }
    },
```

結果は、たとえば`{"text":"ステータス：実行中"}`ボディと`Content-Type: application/json`ヘッダーを持つPOSTリクエストになり、Mattermostチャネルに`ステータス：実行中`メッセージが表示されます。

フォームエンコードまたはJSONエンコード設定を使用する場合、任意の数のペイロード値を設定でき、キーと値の両方がPOSTリクエストに出力されます。ただし、生データ形式を使用する場合、1つの値しか設定できず、**必ず**`"data"`という名前を付ける必要があります。この場合、データキーはPOSTリクエストに出力されず、値のみが出力されます。例：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "format": "raw",
        "webhookstatus": {
            "data": "ステータス：{status}"
        }
    },
```

結果は、たとえば`ステータス：実行中`ボディと`Content-Type: text/plain`ヘッダーを持つPOSTリクエストになります。

### ネストされたWebhook設定

一部のWebhookターゲットでは、ネストされた構造が必要です。
これは、コンテンツをテキストとして直接ではなく、辞書またはリストとして設定することで実現できます。

これはJSON形式でのみサポートされています。

```json
"webhook": {
    "enabled": true,
    "url": "https://<yourhookurl>",
    "format": "json",
    "status": {
        "msgtype": "text",
        "text": {
            "content": "ステータス更新：{status}"
        }
    }
}
```

結果は、たとえば`{"msgtype":"text","text":{"content":"ステータス更新：実行中"}}`ボディと`Content-Type: application/json`ヘッダーを持つPOSTリクエストになります。

## 追加設定

`webhook.retries`パラメータは、webhookリクエストが失敗した場合（つまり、HTTP応答ステータスが200でない場合）に試行する最大再試行回数に設定できます。デフォルトでは、これは無効になっている`0`に設定されています。追加の`webhook.retry_delay`パラメータを設定して、再試行間の時間を秒単位で指定できます。デフォルトでは、これは`0.1`（つまり100ミリ秒）に設定されています。再試行回数または再試行遅延を増やすと、webhookとの接続に問題がある場合にトレーダーが遅くなる可能性があることに注意してください。
`webhook.timeout`を指定することもできます。これは、ボットが他のホストを応答しないと見なすまで待機する時間を定義します（デフォルトは10秒）。

再試行のサンプル設定：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "timeout": 10,
        "retries": 3,
        "retry_delay": 0.2,
        "status": {
            "status": "ステータス：{status}"
        }
    },
```

カスタムメッセージは、戦略内から`self.dp.send_msg()`関数を介してWebhookエンドポイントに送信できます。これを有効にするには、`allow_custom_messages`オプションを`true`に設定します。

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "allow_custom_messages": true,
        "strategy_msg": {
            "status": "戦略メッセージ：{msg}"
        }
    },
```

さまざまなイベントに対してさまざまなペイロードを設定できます。すべてのフィールドが必要なわけではありませんが、少なくとも1つの辞書を設定する必要があります。そうしないと、webhookは呼び出されません。

## Webhookメッセージタイプ

### エントリ/エントリフィル

`webhook.entry`および`webhook.entry_fill`のフィールドは、ボットがポジションを増やすためにロング/ショート注文を出すとき、またはその注文がそれぞれ約定したときに埋められます。パラメータはstring.formatを使用して埋められます。
使用可能なパラメータは次のとおりです。

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* ~~`limit` # 非推奨 - 使用しないでください。~~
* `open_rate`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`

### エントリキャンセル

`webhook.entry_cancel`のフィールドは、ボットがロング/ショート注文をキャンセルしたときに埋められます。パラメータはstring.formatを使用して埋められます。
使用可能なパラメータは次のとおりです。

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `limit`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`

### 決済/決済フィル

`webhook.exit`および`webhook.exit_fill`のフィールドは、ボットが決済注文を出すとき、またはその決済注文がそれぞれ約定したときに埋められます。パラメータはstring.formatを使用して埋められます。
使用可能なパラメータは次のとおりです。

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `amount`
* `open_rate`
* `close_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `enter_tag`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`
* `sub_trade`
* `is_final_exit`


### 決済キャンセル

`webhook.exit_cancel`のフィールドは、ボットが決済注文をキャンセルしたときに埋められます。パラメータはstring.formatを使用して埋められます。
使用可能なパラメータは次のとおりです。

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `order_rate`
* `amount`
* `open_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`

### ステータス

`webhook.status`のフィールドは、通常のステータスメッセージ（開始/停止/...）に使用されます。パラメータはstring.formatを使用して埋められます。

ここで使用できる唯一の値は`{status}`です。

## Discord

Discordでは特別な形式のWebhookが利用できます。
これは次のように設定できます。

```json
"discord": {
    "enabled": true,
    "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
    "exit_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Close rate": "{close_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Close date": "{close_date:%Y-%m-%d %H:%M:%S}"},
        {"Profit": "{profit_amount} {stake_currency}"},
        {"Profitability": "{profit_ratio:.2%}"},
        {"Enter tag": "{enter_tag}"},
        {"Exit Reason": "{exit_reason}"},
        {"Strategy": "{strategy}"},
        {"Timeframe": "{timeframe}"},
    ],
    "entry_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Enter tag": "{enter_tag}"},
        {"Strategy": "{strategy} {timeframe}"},
    ]
}
```

上記はデフォルトを表します（`exit_fill`および`entry_fill`はオプションであり、上記の設定にデフォルト設定されます）。もちろん変更も可能です。
2つのデフォルト値（`entry_fill` / `exit_fill`）のいずれかを無効にするには、空の配列を割り当てることができます（`exit_fill: []`）。

利用可能なフィールドはWebhookのフィールドに対応しており、対応するWebhookセクションに記載されています。

通知はデフォルトで次のようになります。

![discord-notification](assets/discord_notification.png)

カスタムメッセージは、dataprovider.send_msg()関数を介して戦略からDiscordエンドポイントに送信できます。これを有効にするには、`allow_custom_messages`オプションを`true`に設定します。

```json
  "discord": {
        "enabled": true,
        "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
        "allow_custom_messages": true,
    },
```