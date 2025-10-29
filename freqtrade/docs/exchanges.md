# Exchange 固有のメモ

このページには、取引所固有であり、他の取引所には当てはまらない可能性が高い一般的な注意事項と情報がまとめられています。

## サポートされている交換機能の概要

--8<-- "includes/exchange-features.md"

## Exchange 構成

Freqtrade は、100 を超える暗号通貨をサポートする [CCXT ライブラリ](https://github.com/ccxt/ccxt) に基づいています。
為替市場と取引API。完全な最新リストは、次の場所にあります。
[CCXT リポジトリのホームページ](https://github.com/ccxt/ccxt/tree/master/python)。
ただし、開発チームによるボットのテストは数回の交換のみで行われました。
これらの最新のリストは、このドキュメントの「ホーム」セクションにあります。

他の交換を自由にテストし、フィードバックや PR を送信して、ボットを改善したり、完璧に機能する交換を確認したりしてください。

一部の取引所では、以下に示す特別な構成が必要です。

### サンプル交換構成

「binance」の取引所構成は次のようになります。
```json
"exchange": {
    "name": "binance",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {},
    "ccxt_async_config": {},
    // ... 
```
### レート制限の設定

通常、CCXT によって設定されたレート制限は信頼性が高く、適切に機能します。
レート制限に関連する問題 (通常はログ内の DDOS 例外) が発生した場合、rateLimit 設定を他の値に変更するのは簡単です。
```json
"exchange": {
    "name": "kraken",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {"enableRateLimit": true},
    "ccxt_async_config": {
        "enableRateLimit": true,
        "rateLimit": 3100
    },
```
この構成により、クラーケンが有効になるだけでなく、取引所からの禁止を回避するためのレート制限も有効になります。
`"rateLimit": 3100` は、各呼び出し間の 3.1 秒の待機イベントを定義します。これは、`"enableRateLimit"` を false に設定することで完全に無効にすることもできます。

!!! 注記
    レート制限の最適な設定は交換とホワイトリストのサイズによって異なるため、理想的なパラメーターは他の多くの設定によって異なります。
    可能な限り、取引所ごとに賢明なデフォルトを提供するよう努めます。禁止に遭遇した場合は、`"enableRateLimit"` が有効になっていることを確認し、`"rateLimit"` パラメーターを段階的に増やしてください。

## バイナンス

!!! 警告「サーバーの場所と地理的 IP 制限」
    Binance はサーバーの国に応じて API アクセスを制限していることに注意してください。現在ブロックされている国はすべてではありませんが、カナダ、マレーシア、オランダ、米国です。 [バイナンス規約 > b.] に進んでください。資格](https://www.binance.com/en/terms) で最新のリストを確認してください。

Binance は [time_in_force](configuration.md#question-order_time_in_force) をサポートしています。

!!! ヒント「取引所でのストップロス」
    Binance は「stoploss_on_exchange」をサポートし、「stop-loss-limit」注文を使用します。これには大きなメリットがあるため、取引所でストップロスを有効にしてその恩恵を受けることをお勧めします。
    先物に関しては、Binance は「ストップリミット」注文と「ストップマーケット」注文の両方をサポートしています。 `order_types.stoploss` 構成設定で `"limit"` または `"market"` を使用して、どちらのタイプを使用するかを決定できます。

### Binance ブラックリストの推奨事項

Binance の場合、アカウントに十分な追加の「BNB」を維持する意思がある場合、または手数料として「BNB」の使用を無効にする意思がない場合を除き、問題を回避するためにブラックリストに「BNB/<STAKE>」を追加することをお勧めします。
バイナンスアカウントは手数料に「BNB」を使用する場合があり、取引がたまたま「BNB」で行われた場合、さらなる取引によりこのポジションが消費され、期待額がもう存在しないため最初のBNB取引が販売できなくなる可能性があります。

取引手数料をカバーするのに十分な「BNB」が利用できない場合、手数料は「BNB」によってカバーされず、手数料の減額は行われません。 Freqtradeが手数料を賄うためにBNBを購入することは決してありません。このためには、BNB を購入して手動で監視する必要があります。

### バイナンス サイト

Binance は 2 つに分割されており、ユーザーは取引所に正しい ccxt 取引所 ID を使用する必要があります。そうしないと、API キーが認識されません。

* [binance.com](https://www.binance.com/) - 海外ユーザー。取引所 ID:「binance」を使用します。
* [binance.us](https://www.binance.us/) - 米国を拠点とするユーザー。取引所 ID: `binanceus` を使用してください。

### Binance RSA キー

Freqtrade はバイナンス RSA API キーをサポートしています。

これらを環境変数として使用することをお勧めします。
``` bash
export FREQTRADE__EXCHANGE__SECRET="$(cat ./rsa_binance.private)"
```
ただし、構成ファイルを介して構成することもできます。 json は複数行の文字列をサポートしていないため、有効な json ファイルを作成するには、すべての改行を `\n` に置き換える必要があります。
``` json
// ...
 "key": "<someapikey>",
 "secret": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBABACAFQA<...>s8KX8=\n-----END PRIVATE KEY-----"
// ...
```
### バイナンス先物

Binance には特定の (残念なことに複雑な) [先物取引定量ルール](https://www.binance.com/en/support/faq/4f462ebe6ff445d4a170be7d9e897272) があり、これに従う必要があり、多すぎる注文に対して低すぎるステーク額を禁止しています。
これらのルールに違反すると、取引が制限されます。

Binance Futures マーケットで取引する場合、先物には価格ティッカー データがないため、オーダーブックを使用する必要があります。
``` jsonc
  "entry_pricing": {
      "use_order_book": true,
      "order_book_top": 1,
      "check_depth_of_market": {
          "enabled": false,
          "bids_to_ask_delta": 1
      }
  },
  "exit_pricing": {
      "use_order_book": true,
      "order_book_top": 1
  },
```
#### Binance の分離先物設定

ユーザーはまた、先物設定の「ポジション モード」を「一方向モード」に設定し、「資産モード」を「単一資産モード」に設定する必要があります。
これらの設定は起動時にチェックされ、この設定が間違っている場合、freqtrade はエラーを表示します。

![Binance先物設定](assets/binance_futures_settings.png)

Freqtrade はこれらの設定を変更しようとはしません。

#### バイナンス BNFCR 先物

BNFCR モードは、ヨーロッパの規制問題を回避するための Binance の特別なタイプの先物モードです。  
BNFCR 先物を使用するには、次の設定の組み合わせが必要です。
``` jsonc
{
    // ...
    "trading_mode": "futures",
    "margin_mode": "cross",
    "proxy_coin": "BNFCR",
    "stake_currency": "USDT" // or "USDC"
    // ...
}
```
「stake_currency」設定は、ボットが動作する市場を定義します。この選択は実際には任意です。

取引所では、「マルチアセット モード」と「ポジション モード」を「一方向モード」に設定して使用する必要があります。  
Freqtrade は起動時にこれらの設定を確認しますが、変更しようとはしません。

## ビングクス

BingX は、「GTC」 (キャンセルされるまで有効)、「IOC」 (即時またはキャンセル)、および「PO」 (投稿のみ) 設定で [time_in_force](configuration.md# Understand-order_time_in_force) をサポートします。

!!! ヒント「取引所でのストップロス」
    Bingx は「stoploss_on_exchange」をサポートしており、逆指値注文と逆指値注文の両方を使用できます。これには大きなメリットがあるため、取引所でストップロスを有効にしてその恩恵を受けることをお勧めします。

## クラーケン

Kraken は、「GTC」（キャンセルされるまで有効）、「IOC」（即時またはキャンセル）および「PO」（投稿のみ）設定で [time_in_force](configuration.md# Understand-order_time_in_force) をサポートします。

!!! ヒント「取引所でのストップロス」
    Kraken は「stoploss_on_exchange」をサポートしており、ストップロスマーケット注文とストップロスリミット注文の両方を使用できます。大きなメリットがあるので、ぜひ活用することをおすすめします。
    `order_types.stoploss` 構成設定で `"limit"` または `"market"` を使用して、どちらのタイプを使用するかを決定できます。

### クラーケンの歴史的なデータ

Kraken API は 720 個の履歴キャンドルのみを提供します。これは、Freqtrade のドライランおよびライブ取引モードには十分ですが、バックテストには問題があります。
Kraken 取引所のデータをダウンロードするには、「--dl-trades」の使用が必須です。そうしないと、ボットが同じ 720 のローソク足を何度もダウンロードすることになり、十分なバックテスト データが得られなくなります。

ダウンロードを高速化するには、kraken が提供する [trades zip ファイル](https://support.kraken.com/hc/en-us/articles/360047543791-Downloadable-historyal-market-data-time-and-sales-) をダウンロードできます。
これらは通常、四半期に 1 回更新されます。 Freqtrade は、これらのファイルが「user_data/data/kraken/trades_csv」に配置されることを想定しています。

1 つのディレクトリに「完全な」履歴があり、別のディレクトリに増分ファイルがある増分ファイルを使用する場合、次のような構造が合理的です。
このモードの前提条件は、データがダウンロードされ、ファイル名がそのままの状態で解凍されることです。
重複したコンテンツは (タイムスタンプに基づいて) 無視されますが、データにギャップがないことが前提となります。

つまり、「完全な」履歴が 2022 年第 4 四半期に終了する場合、2023 年第 1 四半期と 2023 年第 2 四半期の両方の増分更新が利用可能になります。
これがないとデータが不完全になり、データ使用時の結果が無効になります。
```
└── trades_csv
    ├── Kraken_full_history
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    ├── Kraken_Trading_History_Q1_2023
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    └── Kraken_Trading_History_Q2_2023
        ├── BCHEUR.csv
        └── XBTEUR.csv
```
これらのファイルを freqtrade ファイルに変換できます。
``` bash
freqtrade convert-trade-data --exchange kraken --format-from kraken_csv --format-to feather
# Convert trade data to different ohlcv timeframes
freqtrade trades-to-ohlcv -p BTC/EUR BCH/EUR --exchange kraken -t 1m 5m 15m 1h
```
変換されたデータはデータのダウンロードも可能であり、最後にロードされた取引の後にダウンロードが開始されます。
``` bash
freqtrade download-data --exchange kraken --dl-trades -p BTC/EUR BCH/EUR 
```
!!! 警告「krakenからデータをダウンロードしています」
    クラーケン データをダウンロードするには、取引データをマシン上でキャンドルに変換する必要があるため、他の取引所よりも大幅に多くのメモリ (RAM) が必要になります。
    また、freqtrade はペアと時間範囲の組み合わせに関して取引所で発生したすべての取引をダウンロードする必要があるため、長い時間がかかります。したがって、しばらくお待ちください。

!!! 警告「rateLimit チューニング」
    rateLimit 設定エントリは、リクエスト/秒のレートではなく、リクエスト間の遅延をミリ秒単位で保持することに注意してください。
    したがって、Kraken API の「レート制限を超えました」例外を軽減するには、この設定を減らすのではなく増やす必要があります。

## クコイン

Kucoin では API キーごとにパスフレーズが必要なので、このキーを構成に追加して、交換セクションが次のようになるようにする必要があります。
```json
"exchange": {
    "name": "kucoin",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```
Kucoin は、「GTC」（キャンセルされるまで有効）、「FOK」（完全またはキャンセル）および「IOC」（即時またはキャンセル）設定で [time_in_force](configuration.md# Understand-order_time_in_force) をサポートしています。

!!! ヒント「取引所でのストップロス」
    Kucoin は「stoploss_on_exchange」をサポートしており、ストップロスマーケット注文とストップロスリミット注文の両方を使用できます。大きなメリットがあるので、ぜひ活用することをおすすめします。
    `order_types.stoploss` 構成設定で `"limit"` または `"market"` を使用して、使用するストップロスのタイプを決定できます。

### Kucoin ブラックリスト

Kucoin の場合、アカウントに十分な追加の `KCS` を維持する意思がある場合、または手数料のために `KCS` の使用を無効にする意志がない限り、問題を回避するためにブラックリストに `"KCS/<STAKE>" を追加することをお勧めします。 
Kucoin アカウントは手数料に「KCS」を使用する場合があり、取引がたまたま「KCS」上で行われた場合、さらなる取引によってこのポジションが消費され、期待額がもう存在しないため最初の「KCS」取引が販売できなくなる可能性があります。

## HTX

!!! ヒント「取引所でのストップロス」
    HTX は「stoploss_on_exchange」をサポートし、「stop-limit」注文を使用します。これには大きなメリットがあるため、取引所でストップロスを有効にしてその恩恵を受けることをお勧めします。

## OKX

OKX では API キーごとにパスフレーズが必要なので、このキーを構成に追加して、交換セクションが次のようになるようにする必要があります。
```json
"exchange": {
    "name": "okx",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```
ホスト my.okx.com (OKX EAA) 上の OKX に登録している場合は、交換名として「myokx」` を使用する必要があります。
間違った交換を使用すると、2 つは別個のエンティティであるため、「OKX エラー 50119: API キーが存在しません」というエラーが発生します。

!!! 警告
    OKX は、API 呼び出しごとに 100 個のキャンドルのみを提供します。したがって、この戦略では、バックテスト モードで使用できるデータはかなり少量のみになります。

!!! 警告「先物」
    OKX Futures には「ポジション モード」という概念があり、これは「買い/売り」またはロング/ショート (ヘッジ モード) になります。
    Freqtrade は両方のモードをサポートしています (買い/売りモードを使用することをお勧めします)。ただし、取引中のモード変更はサポートされていないため、例外が発生し、取引が失敗します。
    また、OKX は過去 3 か月以内の MARK キャンドルのみを提供しています。したがって、このデータがなければファンディング手数料を正しく計算できないため、その日より前の先物バックテストではわずかな誤差が生じる可能性があります。

## Gate.io

!!! ヒント「取引所でのストップロス」
    Gate.io は「stoploss_on_exchange」をサポートし、「stop-loss-limit」注文を使用します。これには大きなメリットがあるため、取引所でストップロスを有効にしてその恩恵を受けることをお勧めします。

Gate.io は、「GTC」(キャンセルされるまで有効) 設定および「IOC」(即時またはキャンセル) 設定で [time_in_force](configuration.md# Understand-order_time_in_force) をサポートします。

Gate.ioでは料金の支払いに「POINT」を利用することができます。これは取引可能な通貨ではない (利用可能な通常の市場がない) ため、手数料の自動計算は失敗します (デフォルトの手数料は 0 になります)。
構成パラメータ `exchange.unknown_fee_rate` を使用して、ポイントとステーク通貨の間の為替レートを指定できます。明らかに、ステーク通貨を変更するには、この値も変更する必要があります。

ゲート API キーには、取引する市場タイプに加えて次の権限が必要です。

* 「スポット取引」 _または_ 「無期限先物」 (読み取りおよび書き込み) (両方を選択するか、取引したい市場に一致する方を選択してください)
* 「ウォレット」(読み取り専用)
* 「アカウント」(読み取り専用)

これらの権限がないと、ボットは正しく起動せず、「権限がありません」などのエラーが表示されます。

## バイビット

!!! ヒント「取引所でのストップロス」
    Bybit (先物のみ) は「stoploss_on_exchange」をサポートし、「stop-loss-limit」注文を使用します。これには大きなメリットがあるため、取引所でストップロスを有効にしてその恩恵を受けることをお勧めします。
    先物に関しては、Bybit は「ストップリミット」注文と「ストップマーケット」注文の両方をサポートしています。 `order_types.stoploss` 構成設定で `"limit"` または `"market"` を使用して、どちらのタイプを使用するかを決定できます。

Bybit は、「GTC」（キャンセルされるまで有効）、「FOK」（完全またはキャンセル）、「IOC」（即時またはキャンセル）および「PO」（投稿のみ）設定で [time_in_force](configuration.md#question-order_time_in_force) をサポートしています。

!!! 警告「アカウントの統合」
Freqtrade はアカウントがボット専用であることを前提としています。
    したがって、ボットごとに 1 つのサブアカウントを使用することをお勧めします。これは、統合アカウントを使用する場合に特に重要です。  
    他の構成 (1 つのアカウントでの複数のボット、ボット アカウントでの手動の非ボット取引) はサポートされておらず、予期しない動作が発生する可能性があります。

### Bybit先物

bybit での先物取引は、分離先物モードでサポートされています。

起動時に、freqtrade は (サブ) アカウント全体のポジション モードを「一方向モード」に設定します。これにより、この呼び出しを何度も繰り返す (ボットの動作が遅くなる) ことは避けられますが、この設定を手動で変更すると例外やエラーが発生する可能性があります。

bybit は資金調達率の履歴を提供しないため、予行計算はライブ取引にも使用されます。

ライブ先物取引の API キーには次の権限が必要です。

* 読み書き可能
* 契約 - 注文
* 契約 - ポジション

すべての API キーを、使用する IP に制限することを強くお勧めします。


## ビットマート

Bitmart では、交換キーとシークレットに加えて API キー メモ (API キーに付ける名前) が必要です。
したがって、UID も渡す必要があります。
```json
"exchange": {
    "name": "bitmart",
    "uid": "your_bitmart_api_key_memo",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```
!!! 警告「要確認」
    Bitmart では、UI 経由の取引はレベル 1 の検証だけで問題なく機能しますが、API を介してスポット市場で正常に取引するには検証レベル 2 が必要です。

## ビゲット

Bitget では API キーごとにパスフレーズが必要なので、このキーを構成に追加して、交換セクションが次のようになるようにする必要があります。
```json
"exchange": {
    "name": "bitget",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```
Bitget は、「GTC」（キャンセルされるまで有効）、「FOK」（完全またはキャンセル）、「IOC」（即時またはキャンセル）、および「PO」（投稿のみ）設定で [time_in_force](configuration.md# Understand-order_time_in_force) をサポートします。

!!! ヒント「取引所でのストップロス」
    Bitget は「stoploss_on_exchange」をサポートしており、ストップロスマーケット注文とストップロスリミット注文の両方を使用できます。大きなメリットがあるので、ぜひ活用することをおすすめします。
    `order_types.stoploss` 構成設定で `"limit"` または `"market"` を使用して、使用するストップロスのタイプを決定できます。

### ビゲット先物

bitget での先物取引は、分離先物モードでサポートされています。

起動時に、freqtrade は (サブ) アカウント全体のポジション モードを「一方向モード」に設定します。これにより、この呼び出しを何度も繰り返す (ボットの動作が遅くなる) ことは避けられますが、この設定を手動で変更すると例外やエラーが発生する可能性があります。

## ハイパーリキッド

!!! ヒント「取引所でのストップロス」
    Hyperliquid は「stoploss_on_exchange」をサポートし、「stop-loss-limit」注文を使用します。大きなメリットがあるので、ぜひ活用することをおすすめします。

Hyperliquid は分散型取引所 (DEX) です。分散型取引所は、通常の取引所と比較して動作が少し異なります。 API キーを使用してプライベート API 呼び出しを認証する代わりに、プライベート API 呼び出しはウォレットの秘密キーで署名する必要があります (これには、Hyperliquid または選択したウォレットで生成された API ウォレットを使用することをお勧めします)。
これは次のように構成する必要があります。
```json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_eth_wallet_address",  // This should NOT be your API Wallet Address!
    "privateKey": "your_api_private_key",
    // ...
}
```
* 16 進形式のウォレットアドレス: `0x<40 の 16 進文字>` - ウォレットから簡単にコピーできます。API ウォレット アドレスではなく、メインのウォレット アドレスにする必要があります。
* 16 進数形式の privateKey: `0x<64 の 16 進数文字>` - API ウォレットの作成時に表示されるキーを使用します。

Hyperliquid は、イーサリアム上に構築されたレイヤー 2 スケーリング ソリューションである Arbitrum One チェーンでの入金と出金を処理します。 Hyperliquid は見積/担保として USDC を使用します。 Hyperliquid に USDC を入金するプロセスにはいくつかの手順が必要です。必要な手順の詳細については、[取引を開始する方法](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/how-to-start-trading) を参照してください。

!!! 注「Hyperliquid の一般的な使用上の注意」
    Hyperliquid は成行注文をサポートしていませんが、ccxt は最大 5% のスリッページで指値注文を発注することで成行注文をシミュレートします。  
    残念ながら、Hyperliquid は 5000 個の履歴ローソク足しか提供しないため、バックテストでは (時間をかけて段階的にデータをダウンロードして待機してダウンロードすることにより) 履歴的にローソク足を構築するか、最後の 5000 個のローソク足に制限する必要があります。

!!! 情報「いくつかの一般的なベスト プラクティス (すべてを網羅しているわけではありません)」
    * pip パッケージ ポイズニングなどのサプライ チェーン攻撃に注意してください。秘密キーを使用するときは常に、環境が安全であることを確認してください。
    * 実際のウォレットの秘密キーを取引に使用しないでください。 Hyperliquid [API ジェネレーター](https://app.hyperliquid.xyz/API) を使用して、別の API ウォレットを作成します。
    * freqtrade に使用するサーバーに実際のウォレットの秘密キーを保存しないでください。代わりに API ウォレットの秘密キーを使用してください。このキーでは出金はできず、取引のみが可能です。
    * ニーモニックフレーズと秘密鍵は常に秘密にしておいてください。
    * ハードウェアウォレットを初期化するときにバックアップする必要があったニーモニックと同じニーモニックを使用しないでください。同じニーモニックを使用すると、基本的にハードウェアウォレットのセキュリティが削除されます。
    * 別のソフトウェア ウォレットを作成し、取引したい資金のみをそのウォレットに転送し、そのウォレットを使用して Hyperliquid で取引します。
    * 取引に使用したくない資金がある場合（利益を得た後など）、ハードウェア ウォレットに戻してください。

### Hyperliquid Vault / サブアカウント

Hyperliquid を使用すると、ボールトまたはサブアカウントを作成できます。  
これらを Freqtrade で使用するには、次の構成パターンを使用する必要があります。
``` json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_vault_address",  // Vault or subaccount address
    "privateKey": "your_api_private_key",
    "ccxt_config": {
        "options": {
            "vaultAddress": "your_vault_address" // Optional, only if you want to use a vault or subaccount
        }
    },
    // ...
}
```
あなたの残高と取引は、メインアカウントからではなく、ボールト/サブアカウントから使用されるようになります。

### 過去の Hyperliquid データ

Hyperliquid API は、現在のデータを取得するための 1 回の呼び出しを超える履歴データを提供しないため、ダウンロードされたデータは適切な履歴データを構成しないため、データをダウンロードすることはできません。

## ビトバボ

アカウントで OperatorId を使用する必要がある場合は、次のように構成ファイルでそれを設定できます。
``` json
"exchange": {
        "name": "bitvavo",
        "key": "",
        "secret": "",
        "ccxt_config": {
            "options": {
                "operatorId": "123567"
            }
        },
   }
```
Bitvavo は、「operatorId」が整数であることを期待します。

## すべての交換

Nonce でエラー (「InvalidNonce」など) が継続的に発生する場合は、API キーを再生成することをお勧めします。 Nonce のリセットは困難ですが、通常は API キーを再生成する方が簡単です。

## 他の交換用のランダムなメモ

* Ocean (取引所 ID: `theocean`) 取引所は Web3 機能を使用しており、`web3` Python パッケージがインストールされている必要があります。
```shell
pip3 install web3
```
### 最新価格の取得 / 不完全なキャンドル

ほとんどの取引所は、OHLCV/kline API インターフェイスを介して、現在の不完全なローソク足を返します。
デフォルトでは、Freqtrade は不完全なローソク足が取引所から取得されたものとみなし、最後のローソク足を不完全なローソク足であるとみなして削除します。

交換が不完全なキャンドルを返したかどうかは、Contributor ドキュメントの [ヘルパー スクリプト](developer.md#incomplete-candles) を使用して確認できます。

再塗装の危険性があるため、Freqtrade ではこの不完全なキャンドルの使用を許可していません。

ただし、戦略の最新価格の必要性に基づいている場合、この要件は、戦略内から [データ プロバイダー](strategy-customization.md#possible-options-for-dataprovider) を使用して取得できます。

### 高度な Freqtrade Exchange 構成

詳細オプションは、「_ft_has_params」設定を使用して構成できます。これにより、デフォルトと Exchange 固有の動作がオーバーライドされます。

利用可能なオプションは、exchange クラスに `_ft_has_default` としてリストされます。

たとえば、Kraken で注文タイプ「FOK」をテストし、キャンドル制限を 200 に変更します (つまり、API 呼び出しごとに 200 キャンドルのみを取得します)。
```json
"exchange": {
    "name": "kraken",
    "_ft_has_params": {
        "order_time_in_force": ["GTC", "FOK"],
        "ohlcv_candle_limit": 200
        }
    //...
}
```
!!! 警告
    これらの設定を変更する前に、その影響を十分に理解してください。
    `_ft_has_params` オーバーライドを使用すると、予期しない動作が発生したり、ボットが壊れたりする可能性があります。 
    `_ft_has_params` のカスタム設定によって引き起こされる問題についてはサポートを提供できません。
