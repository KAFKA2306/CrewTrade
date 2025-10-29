# ボットを設定する

Freqtrade には、多くの構成可能な機能と可能性があります。
デフォルトでは、これらの設定は構成ファイルを介して構成されます (下記を参照)。

## Freqtrade 設定ファイル

ボットは、動作中に一連の構成パラメーターを使用し、それらはすべてボット構成に準拠します。通常、その設定をファイル (Freqtrade 設定ファイル) から読み取ります。

デフォルトでは、ボットは現在の作業ディレクトリにある「config.json」ファイルから構成を読み込みます。

`-c/--config` コマンドライン オプションを使用して、ボットによって使用される別の構成ファイルを指定できます。

[クイックスタート](docker_quickstart.md#docker-quick-start)方法でインストールした場合
ボットの場合、インストール スクリプトによってデフォルトの構成ファイル (`config.json`) がすでに作成されているはずです。

デフォルトの設定ファイルが作成されていない場合は、「freqtrade new-config --config user_data/config.json」を使用して基本的な設定ファイルを生成することをお勧めします。

Freqtrade 設定ファイルは JSON 形式で記述されます。

標準の JSON 構文に加えて、構成ファイル内で 1 行の `// ...` および複数行の `/* ... */` コメントを使用したり、パラメータのリストの末尾にカンマを使用したりできます。

JSON 形式に詳しくなくても心配する必要はありません。選択したエディターで構成ファイルを開き、必要なパラメーターにいくつかの変更を加え、変更を保存して、最後にボットを再起動するか、以前に停止した場合は、構成に加えた変更を使用してボットを再実行します。ボットは起動時に構成ファイルの構文を検証し、編集中にエラーがあった場合は警告を発し、問題のある行を指摘します。

### 環境変数

環境変数を介して Freqtrade 設定のオプションを設定します。
これは、構成または戦略内の対応する値よりも優先されます。

環境変数を freqtrade 設定にロードするには、接頭辞として `FREQTRADE__` を付ける必要があります。

`__` はレベル区切り文字として機能するため、使用される形式は `FREQTRADE__{section}__{key}` に対応する必要があります。
そのため、環境変数を「export FREQTRADE__STAKE_AMOUNT=200」として定義すると、結果は「{stake_amount: 200}」になります。

より複雑な例としては、交換キーを秘密に保つための「export FREQTRADE__EXCHANGE__KEY=<yourExchangeKey>」などがあります。これにより、値が設定の「exchange.key」セクションに移動されます。
このスキームを使用すると、すべての構成設定を環境変数としても使用できるようになります。

環境変数は構成内の対応する設定を上書きしますが、コマンド ライン引数が常に優先されることに注意してください。

一般的な例:
``` bash
FREQTRADE__TELEGRAM__CHAT_ID=<telegramchatid>
FREQTRADE__TELEGRAM__TOKEN=<telegramToken>
FREQTRADE__EXCHANGE__KEY=<yourExchangeKey>
FREQTRADE__EXCHANGE__SECRET=<yourExchangeSecret>
```
Json リストは json として解析されるため、次を使用してペアのリストを設定できます。
``` bash
export FREQTRADE__EXCHANGE__PAIR_WHITELIST='["BTC/USDT", "ETH/USDT"]'
```
!!! 注記
    検出された環境変数は起動時にログに記録されます。そのため、値が構成に基づいて予想されるものと異なる理由が見つからない場合は、その値が環境変数から読み込まれていないことを確認してください。

!!! ヒント「結合結果を検証する」
    [show-config サブコマンド](utils.md#show-config) を使用すると、最終的に結合された構成を確認できます。

???警告「ロードシーケンス」
    環境変数は、初期構成後にロードされます。そのため、環境変数を通じて構成へのパスを指定することはできません。そのためには「--config path/to/config.json」を使用してください。
    これはある程度 `user_dir` にも当てはまります。ユーザー ディレクトリは環境変数を通じて設定できますが、設定はその場所からロードされません**。

### 複数の構成ファイル

複数の構成ファイルを指定してボットで使用することも、ボットがプロセスの標準入力ストリームから構成パラメーターを読み取ることもできます。

「add_config_files」で追加の設定ファイルを指定できます。このパラメータで指定されたファイルはロードされ、初期設定ファイルとマージされます。ファイルは、初期構成ファイルを基準にして解決されます。
これは複数の `--config` パラメータを使用するのと似ていますが、すべてのコマンドに対してすべてのファイルを指定する必要がないため、使用方法はより簡単です。

!!! ヒント「結合結果を検証する」
    [show-config サブコマンド](utils.md#show-config) を使用すると、最終的に結合された構成を確認できます。

!!! ヒント「シークレットを秘密にするために複数の構成ファイルを使用する」
    シークレットを含む 2 番目の構成ファイルを使用できます。こうすることで、API キーを自分専用に保ちながら、「プライマリ」構成ファイルを共有できます。
    2 番目のファイルでは、オーバーライドするもののみを指定する必要があります。
    キーが複数の構成に含まれている場合は、「最後に指定された構成」が優先されます (上記の例では、`config-private.json`)。

    1 回限りのコマンドの場合は、複数の「--config」パラメータを指定して以下の構文を使用することもできます。
    ``` bash
    freqtrade trade --config user_data/config1.json --config user_data/config-private.json <...>
    ```
以下は上の例と同等ですが、再利用しやすいように構成内に 2 つの構成ファイルがあります。
    ``` json title="user_data/config.json"
    "add_config_files": [
        "config1.json",
        "config-private.json"
    ]
    ```

    ``` bash
    freqtrade trade --config user_data/config.json <...>
    ```
??? 「構成衝突処理」に注意してください
    同じ構成設定が「config.json」と「config-import.json」の両方で行われる場合、親構成が優先されます。
    以下の場合、再利用可能な「インポート」設定でこのキーが上書きされるため、マージ後の「max_open_trades」は 3 になります。
    ``` json title="user_data/config.json"
    {
        "max_open_trades": 3,
        "stake_currency": "USDT",
        "add_config_files": [
            "config-import.json"
        ]
    }
    ```

    ``` json title="user_data/config-import.json"
    {
        "max_open_trades": 10,
        "stake_amount": "unlimited",
    }
    ```
結果として得られる組み合わせ構成:
    ``` json title="Result"
    {
        "max_open_trades": 3,
        "stake_currency": "USDT",
        "stake_amount": "unlimited"
    }
    ```
複数のファイルが `add_config_files` セクションにある場合、それらは同じレベルにあるとみなされ、最後に出現したファイルが以前の設定をオーバーライドします (親がすでにそのようなキーを定義している場合を除く)。

## エディターのオートコンプリートと検証

JSON スキーマをサポートするエディターを使用している場合は、構成ファイルの先頭に次の行を追加することで、Freqtrade が提供するスキーマを使用して構成ファイルのオートコンプリートと検証を行うことができます。
``` json
{
    "$schema": "https://schema.freqtrade.io/schema.json",
}
```
??? 「開発版」に注意してください
    開発スキーマは「https://schema.freqtrade.io/schema_dev.json」として入手できますが、最高のエクスペリエンスを得るには安定バージョンを使用することをお勧めします。

## 設定パラメータ

以下の表に、使用可能なすべての構成パラメータを示します。

Freqtrade は、コマンド ライン (CLI) 引数を介して多くのオプションをロードすることもできます (詳細については、コマンド `--help` の出力を確認してください)。

### 構成オプションの普及率

すべてのオプションの普及率は次のとおりです。

* CLI 引数は他のオプションをオーバーライドします
* [環境変数](#environment-variables)
* 構成ファイルは順番に使用され (最後のファイルが優先されます)、戦略構成をオーバーライドします。
* ストラテジー構成は、構成またはコマンドライン引数を介して設定されない場合にのみ使用されます。これらのオプションは、以下の表で [Strategy Override](#parameters-in-the-strategy) とマークされています。

### パラメータテーブル

必須パラメータは **必須** とマークされており、可能な方法のいずれかで設定する必要があることを意味します。

|  パラメータ |説明 |
|-----------|---------------|
| `max_open_trades` | **必須。** ボットが許可されているオープン取引の数。オープントレードはペアごとに 1 つだけ可能であるため、ペアリストの長さも適用される可能性のある制限です。 -1 の場合、無視されます (つまり、ペアリストによって制限される潜在的に無制限のオープン取引)。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 [戦略オーバーライド](#parameters-in-the-strategy)。<br> **データ型:** 正の整数または -1。
| `ステーク通貨` | **必須。** 取引に使用される暗号通貨。 <br> **データ型:** 文字列
| `賭け金` | **必須。** ボットが各取引に使用する暗号通貨の量。ボットが利用可能な残高をすべて使用できるようにするには、「無制限」に設定します。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 <br> **データ型:** 正の浮動小数点または `"unlimited"`。
| `取引可能残高比率` |ボットが取引できる合計アカウント残高の比率。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 <br>*デフォルトは `0.99` 99%)。*<br> **データ型:** `0.1` と `1.0` の間の正の浮動小数点数。
| `利用可能な資本` |ボットに利用可能な開始資金。同じ Exchange アカウントで複数のボットを実行する場合に便利です。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 <br> **データ型:** 正の浮動小数点数。
| `amend_last_stake_amount` |必要に応じて、最後の賭け金額を減らして使用します。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `last_stake_amount_min_ratio` |残して実行する必要がある最小賭け金額を定義します。最後のステーク額が減額された場合 (つまり、「amend_last_stake_amount」が「true」に設定されている場合) にのみ適用されます。 [詳細は以下をご覧ください](#cconfiguring-amount-per-trade)。 <br>*デフォルトは `0.5` です。* <br> **データ型:** Float (比率として)
| `amount_reserve_percent` |最小ペアステーク額でいくらかを予約します。ボットは、取引拒否の可能性を回避するために、ペアの最小ステーク額を計算するときに「amount_reserve_percent」+ストップロス値を予約します。 <br>*デフォルトは `0.05` (5%) です。* <br> **データ型:** 比率としての正の浮動小数点数。
| `時間枠` |使用する時間枠 (例: `1m`、`5m`、`15m`、`30m`、`1h` ...)。通常、構成には欠落しており、戦略で指定されます。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br> **データ型:** 文字列
| `法定表示通貨` |利益を示すために使用される法定通貨。 [詳細は以下をご覧ください](#what-values-can-be-used-for-fiat_display_currency)。 <br> **データ型:** 文字列
| `ドライラン` | **必須。** ボットをドライ ラン モードにする必要があるか、運用モードにする必要があるかを定義します。 <br>*デフォルトは「true」です。* <br> **データ型:** ブール値
| `ドライランウォレット` |ドライラン モードで実行されているボットによって使用されるシミュレートされたウォレットの開始金額をステーク通貨で定義します。 [詳細は以下をご覧ください](#dry-run-wallet)<br>*デフォルトは `1000` です。* <br> **データ型:** Float または Dict
| `cancel_open_orders_on_exit` | `/stop` RPC コマンドが発行されたとき、`Ctrl+C` が押されたとき、またはボットが予期せず終了したときに、オープン注文をキャンセルします。 「true」に設定すると、市場暴落の際に「/stop」を使用して未約定注文および部分約定済みの注文をキャンセルできるようになります。オープンポジションには影響しません。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `プロセスのみ_新しいキャンドル` |新しいローソクが到着した場合にのみインジケーターの処理を有効にします。 false の場合、各ループでインジケーターが設定されます。これは、同じローソク足が何度も処理されてシステム負荷が発生することを意味しますが、ローソク足だけでなくティック データに依存する戦略には役立ちます。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「true」です。* <br> **データ型:** ブール値
| `minimal_roi` | **必須。** ボットが取引を終了するために使用する比率としてしきい値を設定します。 [詳細については以下をご覧ください](#under-minimal_roi)。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br> **データ型:** 辞書
| `ストップロス` |  **必須。** ボットによって使用されるストップロスの比率としての値。詳細については、[ストップロスのドキュメント](stoploss.md)を参照してください。 [戦略オーバーライド](#parameters-in-the-strategy)。  <br> **データ型:** Float (比率として)
| `トレーリングストップ` |トレーリング ストップロスを有効にします (設定ファイルまたは戦略ファイルの「ストップロス」に基づいて)。詳細については、[ストップロスのドキュメント](stoploss.md#trailing-stop-loss)を参照してください。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br> **データ型:** ブール値
| `trailing_stop_positive` |利益に達したらストップロスを変更します。詳細については、[ストップロスのドキュメント](stoploss.md#trailing-stop-loss-Difference-positive-loss)を参照してください。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br> **データ型:** Float
| `trailing_stop_positive_offset` | 「trailing_stop_positive」を適用するタイミングのオフセット。正である必要があるパーセンテージ値。詳細については、[ストップロスのドキュメント](stoploss.md#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset)を参照してください。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは `0.0` (オフセットなし)。* <br> **データ型:** Float
| `trailing_only_offset_is_reached` |オフセットに達した場合にのみ、トレーリング ストップロスを適用します。 [ストップロスのドキュメント](stoploss.md)。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `料金` |バックテスト/ドライラン中に使用される料金。通常は設定しないでください。freqtrade は取引所のデフォルト手数料にフォールバックします。比率として設定します (例: 0.001 = 0.1%)。手数料は取引ごとに、購入時に1回、売却時に1回の2回適用されます。 <br> **データ型:** Float (比率として)
| `先物ファンディング率` |過去の資金調達レートが取引所から入手できない場合に使用されるユーザー指定の資金調達レート。これは実際の過去のレートを上書きしません。特定のコインをテストしていて、資金調達率が freqtrade の利益計算にどのような影響を与えるかを理解している場合を除き、これを 0 に設定することをお勧めします。 [詳細はこちら](leverage.md#unavailable-funding-rates) <br>*デフォルトは「None」です。*<br> **データ型:** Float
| `取引モード` |定期的に取引するか、レバレッジを利用して取引するか、一致する暗号通貨の価格から価格が導出される契約を取引するかを指定します。 [活用ドキュメント](leverage.md)。 <br>*デフォルトは `"spot"` です。* <br> **データ型:** 文字列
| `マージンモード` |レバレッジを使用して取引する場合、これにより、トレーダーが所有する担保を各取引ペアに共有するか分離するかが決まります [レバレッジに関するドキュメント](leverage.md)。 <br> **データ型:** 文字列
| `清算バッファ` |ポジションが清算価格に達するのを防ぐために、清算価格とストップロスの間にどのくらいの大きさのセーフティネットを置くかを指定する比率 [レバレッジドキュメント](leverage.md)。 <br>*デフォルトは「0.05」です。* <br> **データ型:** Float
| | **未入力のタイムアウト**
| `unfilledtimeout.entry` | **必須。** 未約定のエントリー注文が完了するまでボットが待機する時間 (分または秒)。その後、注文はキャンセルされます。 [戦略オーバーライド](#parameters-in-the-strategy).<br> **データ型:** 整数
| `unfilledtimeout.exit` | **必須。** ボットが未約定の決済注文の完了を待つ時間 (分または秒)。その後、注文はキャンセルされ、シグナルがある限り、現在の (新しい) 価格で繰り返されます。 [戦略オーバーライド](#parameters-in-the-strategy).<br> **データ型:** 整数
| `unfilledtimeout.unit` | unfilledtimeout設定で使用する単位。注: unfilledtimeout.unit を「秒」に設定する場合、「internals.process_throttle_secs」は timeout [Strategy Override](#parameters-in-the-strategy) よりも小さいか等しい必要があります。 <br> *デフォルトは「分」`。* <br> **データ型:** 文字列
| `unfilledtimeout.exit_timeout_count` |終了オーダーがタイムアウトになる回数。このタイムアウト回数に達すると、緊急終了がトリガーされます。 0 を指定すると、無制限の注文キャンセルが許可されます。 [戦略オーバーライド](#parameters-in-the-strategy).<br>*デフォルトは「0」です。* <br> **データ型:** 整数
| | **価格**
| `entry_pricing.price_side` |ボットがエントリー率を取得するために参照するスプレッドの側を選択します。 [詳細は以下をご覧ください](#entry-price)。<br> *デフォルトは `"same"` です。* <br> **データ型:** 文字列 (`ask`、`bid`、`same`、または `other`)。
| `entry_pricing.price_last_balance` | **必須。** 入札価格を補間します。詳細は[下記](#entry-price-without-orderbook-enabled)。
| `entry_pricing.use_order_book` | [Order Book Entry](#entry-price-with-orderbook-enabled) でレートを使用して入力できるようにします。 <br> *デフォルトは「true」です。*<br> **データ型:** ブール値
| `entry_pricing.order_book_top` |ボットは、オーダーブック「price_side」の上位 N レートを使用して取引を開始します。つまり、値 2 を指定すると、ボットは [Order Book Entry](#entry-price-with-orderbook-enabled) の 2 番目のエントリを選択できるようになります。 <br>*デフォルトは「1」です。* <br> **データ型:** 正の整数
| `entry_価格設定。 check_ Depth_of_market.enabled` |オーダーブックで買い注文と売り注文の差額が満たされている場合はエントリーしないでください。 [市場の深さを確認する](#check- Depth-of-market)。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `entry_価格設定。 check_ Depth_of_market.bids_to_ask_delta` |オーダーブックにある買い注文と売り注文の差額比率。 1 未満の値は売り注文のサイズが大きいことを意味し、1 より大きい値は買い注文のサイズが大きいことを意味します。 [市場の厚みを確認](#check- Depth-of-market) <br> *デフォルトは `0` です。* <br> **データ型:** Float (比率として)
| `exit_pricing.price_side` |離脱率を取得するためにボットが参照するスプレッドの側を選択します。 [詳細は以下をご覧ください](#exit-price-side)。<br> *デフォルトは `"same"` です。* <br> **データ型:** 文字列 (`ask`、`bid`、`same`、または `other`)。
| `exit_pricing.price_last_balance` |終了価格を補間します。詳細は[下記](#exit-price-without-orderbook-enabled)。
| `exit_pricing.use_order_book` | [Order Book Exit](#exit-price-with-orderbook-enabled) を使用してオープン取引の終了を有効にします。 <br> *デフォルトは「true」です。*<br> **データ型:** ブール値
| `exit_pricing.order_book_top` |ボットは注文帳「price_side」の上位 N レートを使用して終了します。つまり、値 2 を指定すると、ボットが [Order Book Exit](#exit-price-with-orderbook-enabled) で 2 番目のアスクレートを選択できるようになります。<br>*デフォルトは `1` です。* <br> **データ型:** 正の整数
| `カスタム価格の最大距離率` |現在の価格とカスタムのエントリー価格またはエグジット価格の間の最大距離比率を構成します。 <br>*デフォルトは `0.02` 2%)。*<br> **データ型:** 正の浮動小数点数
| | **注文/信号処理**
| `use_exit_signal` | 「minimal_roi」に加えて、戦略によって生成された出口シグナルを使用します。 <br>これを false に設定すると、`"exit_long"` 列と `"exit_short"` 列の使用が無効になります。他の終了メソッド (ストップロス、ROI、コールバック) には影響しません。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「true」です。* <br> **データ型:** ブール値
| `exit_profit_only` |ボットが「exit_profit_offset」に達するまで待ってから、終了の決定を下します。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `出口利益オフセット` |終了信号は、この値を超えるとのみアクティブになります。 「exit_profit_only=True」と組み合わせた場合にのみアクティブになります。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは `0.0` です。* <br> **データ型:** Float (比率として)
| `ignore_roi_if_entry_signal` |エントリー信号がまだアクティブな場合は終了しないでください。この設定は、`minimal_roi` および `use_exit_signal` よりも優先されます。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「false」です。* <br> **データ型:** ブール値
| `ignore_buying_expired_candle_after` |買いシグナルが使用されなくなるまでの秒数を指定します。 <br> **データ型:** 整数
| `order_types` |アクションに応じて注文タイプを設定します (`"entry"`、`"exit"`、`"stoploss"`、`"stoploss_on_exchange"`)。 [詳細は以下をご覧ください](#under-order_types)。 [戦略オーバーライド](#parameters-in-the-strategy).<br> **データ型:** 辞書
| `order_time_in_force` |エントリー注文とエグジット注文の有効時間を構成します。 [詳細については以下をご覧ください](#under-order_time_in_force)。 [戦略オーバーライド](#parameters-in-the-strategy)。 <br> **データ型:** 辞書
| `位置調整有効` |戦略でポジション調整 (追加の買いまたは売り) を使用できるようにします。 [詳細はこちら](strategy-callbacks.md#adjust-trade-position)。 <br> [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「false」です。*<br> **データ型:** ブール値
| `max_entry_position_adjustment` |最初のエントリー注文に加えて、オープン取引ごとに追加注文できる最大数。追加注文を無制限にするには、「-1」に設定します。 [詳細はこちら](strategy-callbacks.md#adjust-trade-position)。 <br> [戦略オーバーライド](#parameters-in-the-strategy)。 <br>*デフォルトは「-1」です。*<br> **データ型:** 正の整数または -1
| | **交換**
| `exchange.name` | **必須。** 使用する交換クラスの名前。 <br> **データ型:** 文字列
| `交換キー` |交換に使用する API キー。運用モードの場合にのみ必要です。<br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `交換.秘密` |交換に使用する API シークレット。運用モードの場合にのみ必要です。<br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `交換.パスワード` |交換に使用する API パスワード。本番モードの場合、および API リクエストにパスワードを使用する交換の場合にのみ必要です。<br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `exchange.uid` |交換に使用する API uid。本番モードの場合、および API リクエストに uid を使用する交換の場合にのみ必要です。<br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `exchange.pair_whitelist` |ボットが取引に使用し、バックテスト中に潜在的な取引を確認するために使用するペアのリスト。正規表現ペアを「.*/BTC」としてサポートします。 VolumePairList では使用されません。 [詳細](plugins.md#pairlists-and-pairlist-handlers)。 <br> **データ型:** リスト
| `exchange.pair_blacklist` |ボットが取引とバックテストのために絶対に避けなければならないペアのリスト。 [詳細](plugins.md#pairlists-and-pairlist-handlers)。 <br> **データ型:** リスト
| `exchange.ccxt_config` |両方の ccxt インスタンス (同期と非同期) に渡される追加の CCXT パラメーター。通常、これは追加の ccxt 構成の正しい場所です。パラメータは取引所ごとに異なる場合があり、[ccxt ドキュメント](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation) に記載されています。 Exchange シークレットはログに含まれる可能性があるため、ここでは追加しないでください (代わりに専用フィールドを使用してください)。 <br> **データ型:** 辞書
| `exchange.ccxt_sync_config` |通常の (同期) ccxt インスタンスに渡される追加の CCXT パラメータ。パラメータは取引所ごとに異なる場合があり、[ccxt ドキュメント](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation) に文書化されています。<br> **データ型:** 辞書
| `exchange.ccxt_async_config` |追加の CCXT パラメータが非同期 ccxt インスタンスに渡されます。パラメータは取引所ごとに異なる場合があり、[ccxt ドキュメント](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation) に文書化されています。<br> **データ型:** 辞書
| `exchange.enable_ws` |交換用の Websocket の使用を有効にします。 <br>[詳細](#consuming-exchange-websockets).<br>*デフォルトは「true」です。* <br> **データ型:** ブール値
| `exchange.markets_refresh_interval` |マーケットがリロードされる間隔（分単位）。 <br>*デフォルトは「60」分です。* <br> **データ型:** 正の整数
| `exchange.skip_open_order_update` |取引所で問題が発生した場合、起動時にオープン注文の更新をスキップします。ライブ条件でのみ関連します。<br>*デフォルトは「false」*<br> **データ型:** ブール値
| `exchange.unknown_fee_rate` |取引手数料を計算するときに使用するフォールバック値。これは、取引不可能な通貨で手数料がかかる取引所に役立ちます。ここで指定した値は「手数料コスト」と乗算されます。<br>*デフォルトは「なし」です<br> **データ型:** float
| `exchange.log_responses` |関連する交換応答をログに記録します。デバッグ モードのみ - 慎重に使用してください。<br>*デフォルトは「false」です*<br> **データ型:** ブール値
| `exchange.only_from_ccxt` | data.binance.vision からのデータのダウンロードを防止します。これを false のままにすると、ダウンロードを大幅に高速化できますが、サイトが利用できない場合は問題が発生する可能性があります。<br>*デフォルトは「false」です*<br> **データ型:** ブール値
| `experimental.block_bad_exchanges` | freqtrade では機能しないことが知られている取引所をブロックします。その交換が今すぐ機能するかどうかをテストする場合を除き、デフォルトのままにしておきます。 <br>*デフォルトは「true」です。* <br> **データ型:** ブール値
| | **プラグイン**
| `ペアリスト` |使用する 1 つ以上のペアリストを定義します。 [詳細](plugins.md#pairlists-and-pairlist-handlers)。 <br>*デフォルトは `StaticPairList` です。* <br> **データ型:** 辞書のリスト
| | **電報**
| `テレグラム.有効` |テレグラムの使用を有効にします。 <br> **データ型:** ブール値
| `テレグラム.トークン` | Telegram ボット トークン。 「telegram.enabled」が「true」の場合にのみ必要です。 <br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `telegram.chat_id` |個人の Telegram アカウント ID。 「telegram.enabled」が「true」の場合にのみ必要です。 <br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `telegram.balance_dust_level` |ダストレベル (ステーク通貨で) - これを下回る残高を持つ通貨は `/balance` によって表示されません。 <br> **データ型:** float
| `テレグラム.リロード` |電報メッセージの「リロード」ボタンを許可します。 <br>*デフォルトは「true」です。<br> **データ型:** ブール値
| `telegram.notification_settings.*` |詳細な通知設定。詳細については、[テレグラムのドキュメント](telegram-usage.md) を参照してください。<br> **データ型:** 辞書
| `telegram.allow_custom_messages` | dataprovider.send_msg() 関数を介してストラテジーからの Telegram メッセージの送信を有効にします。 <br> **データ型:** ブール値
| | **ウェブフック**
| `webhook.enabled` | Webhook 通知の使用を有効にする <br> **データ型:** Boolean
| `webhook.url` | Webhook の URL。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.entry` |エントリ時に送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.entry_cancel` |エントリーオーダーキャンセル時に送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.entry_fill` |エントリーオーダーが満たされたときに送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.exit` |終了時に送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.exit_cancel` |終了オーダーのキャンセル時に送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.exit_fill` |終了オーダーが満たされたときに送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.status` |ステータス呼び出しで送信するペイロード。 「webhook.enabled」が「true」の場合にのみ必要です。詳細については、[webhook ドキュメント](webhook-config.md) を参照してください。 <br> **データ型:** 文字列
| `webhook.allow_custom_messages` | dataprovider.send_msg() 関数を介してストラテジーから Webhook メッセージの送信を有効にします。 <br> **データ型:** ブール値
| | **Rest API / FreqUI / プロデューサー/コンシューマー**
| `api_server.enabled` | APIサーバーの使用を有効にします。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。 <br> **データ型:** ブール値
| `api_server.listen_ip_address` | IPアドレスをバインドします。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。 <br> **データタイプ:** IPv4
| `api_server.listen_port` |バインドポート。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。 <br>**データ型:** 1024 ～ 65535 の整数
| `api_server.verbosity` |ログの詳細度。 「info」はすべての RPC 呼び出しを出力しますが、「error」はエラーのみを表示します。 <br>**Datatype:** 列挙型、`info` または `error` のいずれか。デフォルトは「情報」です。
| `api_server.ユーザー名` | APIサーバーのユーザー名。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。 <br>**秘密にしておき、公開しないでください。**<br> **データ型:** 文字列
| `api_server.パスワード` | APIサーバーのパスワード。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。 <br>**秘密にしておき、公開しないでください。**<br> **データ型:** 文字列
| `api_server.ws_token` |メッセージ WebSocket の API トークン。詳細については、[API サーバーのドキュメント](rest-api.md) を参照してください。  <br>**秘密にしておき、公開しないでください。** <br> **データ型:** 文字列
| `ボット名` |ボットの名前。 API 経由でクライアントに渡されます - ボットを区別したり名前を付けるために表示できます。<br> *デフォルトは `freqtrade`*<br> **データ型:** 文字列
| `external_message_consumer` |詳細については、[Producer/Consumer モード](Producer-consumer.md) を有効にしてください。 <br> **データ型:** 辞書
| | **その他**
| `初期状態` |アプリケーションの初期状態を定義します。停止に設定されている場合、ボットは「/start」RPC コマンドを使用して明示的に開始する必要があります。 <br>*デフォルトは `stopped` です。* <br> **データ型:** 列挙型、`running`、`paused`、または `stopped` のいずれか
| `force_entry_enable` | RPC コマンドでトレードエントリーを強制できるようにします。詳細については以下をご覧ください。 <br> **データ型:** ブール値
| `disable_dataframe_checks` |ストラテジー メソッドから返された OHLCV データフレームが正しいかどうかのチェックを無効にします。データフレームを意図的に変更し、何をしているのかを理解する場合にのみ使用してください。 [戦略オーバーライド](#parameters-in-the-strategy)。<br> *デフォルトは「False」*です。 <br> **データ型:** ブール値
| `internals.process_throttle_secs` |プロセス スロットル、つまり 1 つのボット反復ループの最小ループ期間を設定します。秒単位の値。 <br>*デフォルトは「5」秒です。* <br> **データ型:** 正の整数
| `internals.heartbeat_interval` | N 秒ごとにハートビート メッセージを出力します。ハートビート メッセージを無効にするには、0 に設定します。 <br>*デフォルトは「60」秒です。* <br> **データ型:** 正の整数または 0
| `internals.sd_notify` | sd_notify プロトコルの使用を有効にして、ボットの状態の変化を systemd サービス マネージャーに通知し、キープアライブ ping を発行します。詳細については、[こちら](advanced-setup.md#configure-the-bot-running-as-a-systemd-service)を参照してください。 <br> **データ型:** ブール値
| `戦略` | **必須** 使用する Strategy クラスを定義します。 「--strategy NAME」を介して設定することをお勧めします。 <br> **データ型:** クラス名
| `戦略パス` |追加の戦略ルックアップ パスを追加します (ディレクトリである必要があります)。 <br> **データ型:** 文字列
| `recursive_strategy_search` | 「true」に設定すると、「user_data/strategies」内のサブディレクトリで戦略を再帰的に検索します。 <br> **データ型:** ブール値
| `user_data_dir` |ユーザーデータを含むディレクトリ。 <br> *デフォルトは `./user_data/`* です。 <br> **データ型:** 文字列
| `db_url` |使用するデータベースの URL を宣言します。注: これは、「dry_run」が「true」の場合は「sqlite:///tradesv3.dryrun.sqlite」にデフォルト設定され、実稼働インスタンスの場合は「sqlite:///tradesv3.sqlite」にデフォルト設定されます。 <br> **データ型:** 文字列、SQLAlchemy 接続文字列
| `ログファイル` |ログファイル名を指定します。 10 ファイルのログ ファイル ローテーションにローリング戦略を使用し、ファイルあたり 1 MB の制限を設けます。 <br> **データ型:** 文字列
| `add_config_files` |追加の構成ファイル。これらのファイルはロードされ、現在の構成ファイルとマージされます。ファイルは最初のファイルを基準にして解決されます。<br> *デフォルトは `[]`* です。 <br> **データ型:** 文字列のリスト
| `dataformat_ohlcv` |ヒストリカル ローソク足 (OHLCV) データの保存に使用するデータ形式。 <br> *デフォルトは「フェザー」*です。 <br> **データ型:** 文字列
| `データフォーマットトレード` |過去の取引データを保存するために使用するデータ形式。 <br> *デフォルトは「フェザー」*です。 <br> **データ型:** 文字列
| `reduce_df_footprint` | RAM/ディスクの使用量を削減する (およびトレーニング/推論タイミングのバックテスト/ハイパーオプトおよび FreqAI を削減する) ことを目的として、すべての数値列を float32/int32 にリキャストします。 <br> **データ型:** ブール値。 <br> デフォルト:「False」。
| `log_config` | Python ロギングのログ構成を含むディクショナリ。 [詳細](advanced-setup.md#advanced-logging) <br> **データ型:** dict。 <br> デフォルト: `FtRichHandler`

### ストラテジ内のパラメータ

次のパラメータは、構成ファイルまたはストラテジで設定できます。
構成ファイルに設定された値は、常にストラテジに設定された値を上書きします。

* `minimal_roi`
* `時間枠`
* `ストップロス`
* `max_open_trades`
* `trailing_stop`
* `trailing_stop_positive`
* `trailing_stop_positive_offset`
* `trailing_only_offset_is_reached`
* `use_custom_stoploss`
* `process_only_new_candles`
* `order_types`
* `order_time_in_force`
* `unfilledtimeout`
* `disable_dataframe_checks`
* `use_exit_signal`
* `exit_profit_only`
* `exit_profit_offset`
* `ignore_roi_if_entry_signal`
* `ignore_buying_expired_candle_after`
* `位置調整有効`
* `max_entry_position_adjustment`

### 取引ごとの金額の設定

ボットが取引に参加するために使用するステーク通貨の量を構成するには、いくつかの方法があります。以下で説明するように、すべてのメソッドは [利用可能な残高の設定](#tradable-balance) を尊重します。

#### 最小取引ステーク

最低賭け金は取引所とペアによって異なり、通常は取引所のサポートページに記載されています。
XRP/USD の最低取引可能額が 20 XRP (取引所によって与えられる) で、価格が 0.6\$ であると仮定すると、このペアを購入するための最低賭け金額は `20 * 0.6 ~= 12` となります。
この取引所には USD にも制限があり、すべての注文は 10\$ 以上である必要がありますが、この場合は適用されません。

安全な実行を保証するために、freqtrade はステーク量 10.1\$ での購入を許可せず、その代わりにペアの下にストップロスを配置するのに十分なスペースがあることを確認します (+ `amount_reserve_percent` で定義されるオフセット。デフォルトは 5%)。

5% のリザーブの場合、最小賭け金は ~12.6\$ (`12 * (1 + 0.05)`) になります。それに加えて 10% のストップロスを考慮すると、最終的には ~14\$ (`12.6 / (1 - 0.1)`) の値になります。

ストップロス値が大きい場合にこの計算を制限するため、計算された最小ステーク制限は実際の制限を 50% 以上上回ることはありません。

!!! 警告
    取引所の限度額は通常安定しており、頻繁には更新されないため、単に取引所による最後の限度額調整以降、価格が大幅に上昇したという理由だけで、一部のペアはかなり高い最低限度額を示すことがあります。 Freqtrade は、計算された/望ましいステーク量より 30% を超える場合を除き、ステーク量をこの値に調整します。その場合、取引は拒否されます。

#### ドライランウォレット

予行演習モードで実行すると、ボットはシミュレートされたウォレットを使用して取引を実行します。このウォレットの開始残高は「dry_run_wallet」によって定義されます (デフォルトは 1000)。
より複雑なシナリオの場合は、辞書を「dry_run_wallet」に割り当てて、各通貨の開始残高を定義することもできます。
```json
"dry_run_wallet": {
    "BTC": 0.01,
    "ETH": 2,
    "USDT": 1000
}
```
コマンド ライン オプション (`--dry-run-wallet`) を使用して構成値をオーバーライドできますが、それは浮動小数点値のみであり、ディクショナリは使用できません。辞書を使用したい場合は、設定ファイルを調整してください。

!!! 注記
    ステーク通貨以外の残高は取引には使用されませんが、ウォレット残高の一部として表示されます。
    クロスマージン取引所では、取引に利用可能な担保を計算するためにウォレット残高が使用される場合があります。

#### 取引可能残高

デフォルトでは、ボットは「完全な金額 - 1%」が自由に使えると想定し、[動的ステーク金額](#dynamic-stake-amount) を使用すると、完全な残高を取引ごとに「max_open_trades」バケットに分割します。
Freqtrade は取引開始時に最終的な手数料として 1% を留保するため、デフォルトではそれには触れません。

`tradable_balance_ratio` 設定を使用して、「手付かずの」金額を構成できます。

たとえば、取引所のウォレットで利用可能な 10 ETH があり、「tradable_balance_ratio=0.5」 (50%) である場合、ボットは取引に最大量の 5 ETH を使用し、これを利用可能な残高とみなします。ウォレットの残りの部分は取引によって影響を受けません。

!!! 危険
    同じアカウントで複数のボットを実行する場合、この設定は**使用しないでください**。代わりに、[ボットへの利用可能な資本](#assign-available-capital) を参照してください。

!!! 警告
    「tradable_balance_ratio」設定は、現在の残高 (自由残高 + 取引で拘束された残高) に適用されます。したがって、開始残高を 1000 と仮定すると、「tradable_balance_ratio=0.99」の設定では、取引所で常に 10 通貨単位が利用可能であることが保証されません。たとえば、合計残高が (連敗または残高の引き出しにより) 500 に減少した場合、無料金額は 5 ユニットに減少する可能性があります。

#### 利用可能な資本を割り当てる

同じ取引所アカウントで複数のボットを使用するときに複利利益を最大限に活用するには、各ボットを特定の開始残高に制限する必要があります。
これは、「available_capital」を希望の開始残高に設定することで実現できます。

アカウントに 10000 USDT があり、この取引所で 2 つの異なる戦略を実行するとします。
「available_capital=5000」を設定すると、各ボットに 5000 USDT の初期資本が付与されます。
次に、ボットはこの開始残高を「max_open_trades」バケットに均等に分割します。
利益のある取引により、他のボットのステーク サイズに影響を与えることなく、このボットのステーク サイズが増加します。
「available_capital」を調整するには、設定を再ロードして有効にする必要があります。 `available_capital` を調整すると、以前の `available_capital` と新しい `available_capital` の差が追加されます。取引が開かれているときに利用可能な資本を減らしても、取引は終了しません。取引が完了すると差額がウォレットに返されます。この結果は、調整と取引終了の間の価格の動きによって異なります。

!!! 警告「「tradable_balance_ratio」と互換性がありません」
    このオプションを設定すると、「tradable_balance_ratio」の設定が置き換えられます。

#### 最後の賭け金額を修正する

取引可能な残高が 1000 USDT、`stake_amount=400`、および `max_open_trades=3` であると仮定します。
ボットは 2 つの取引を開きますが、800 USDT がすでに他の取引で結び付けられているため、要求された 400 USDT はもう利用できないため、最後の取引スロットを満たすことができません。

これを克服するには、オプション「amend_last_stake_amount」を「True」に設定します。これにより、ボットは最後の取引スロットを満たすために利用可能な残高まで stake_amount を減らすことができます。

上の例では、これは次のことを意味します。

* Trade1: 400 USDT
* Trade2: 400 USDT
* Trade3: 200 USDT

!!! 注記
    このオプションは [静的ステーク額](#static-stake-amount) にのみ適用されます。[動的ステーク額](#dynamic-stake-amount) は残高を均等に分割するためです。

!!! 注記
    最終ステークの最小額は「last_stake_amount_min_ratio」を使用して設定できます。デフォルトは 0.5 (50%) です。これは、これまでに使用された最小ステーク額が「stake_amount * 0.5」であることを意味します。これにより、ペアの最低取引可能額に近く、取引所によって拒否される可能性のある非常に低い賭け金が回避されます。

#### 静的賭け金額

「stake_amount」設定は、ボットが各取引に使用するステーク通貨の量を静的に設定します。

最小構成値は 0.0001 ですが、問題を避けるために、使用しているステーク通貨の取引所の取引最低額を確認してください。

この設定は「max_open_trades」と組み合わせて機能します。取引に関わる最大資本は「stake_amount * max_open_trades」です。
たとえば、「max_open_trades=3」および「stake_amount=0.05」の構成を想定すると、ボットは最大で (0.05 BTC x 3) = 0.15 BTC を使用します。

!!! 注記
    この設定は、[利用可能な残高の構成](#tradable-balance) を尊重します。

#### 動的賭け金額

あるいは、取引所で利用可能な残高を使用し、それを許可された取引数 (`max_open_trades`) で等分する動的なステーク額を使用することもできます。

これを設定するには、`stake_amount="unlimited"` を設定します。また、最終的な手数料の最小残高を維持するために、「tradable_balance_ratio=0.99」 (99%) を設定することをお勧めします。

この場合、取引額は次のように計算されます。
```python
currency_balance / (max_open_trades - current_open_trades)
```
ボットがアカウント内の利用可能なすべての `stake_currency` (マイナス `tradable_balance_ratio`) セットを取引できるようにするには、
```json
"stake_amount" : "unlimited",
"tradable_balance_ratio": 0.99,
```
!!! ヒント「利益の複利」
    この構成では、ボットのパフォーマンスに応じて賭け金を増減することができ (ボットが負けている場合は賭け金が低くなり、ボットが勝利記録を持っている場合は、より高い残高が利用できるため賭け金が高くなります)、結果的に利益が複利になります。

!!! 注意「ドライランモード使用時」
    `"stake_amount" : "unlimited" をドライラン、バックテスト、または Hyperopt と組み合わせて使用すると、残高は `dry_run_wallet` のステークから開始され、進化していきます。
    したがって、「dry_run_wallet」を適切な値 (たとえば、BTC の場合は 0.05 または 0.01、USDT の場合は 1000 または 100 など) に設定することが重要です。そうしないと、一度に 100 BTC (またはそれ以上) または 0.05 USDT (またはそれ以下) での取引をシミュレートする可能性があります。これは、実際の利用可能な残高に対応していない可能性があり、または賭け金の注文金額の取引所の最小制限を下回っている可能性があります。通貨。

#### 位置調整による動的なステーク量

無制限のステークでポジション調整を使用したい場合は、戦略に応じて値を返すように `custom_stake_amount` も実装する必要があります。
一般的な値は、提案された賭け金の 25% ～ 50% の範囲になりますが、戦略と、ポジション調整バッファーとしてウォレットにどのくらい残しておきたいかによって大きく異なります。

たとえば、ポジション調整で同じ賭け金で 2 回の追加購入ができると想定している場合、バッファーは最初に提案された無制限の賭け金の 66.6667% である必要があります。

または、別の例で、ポジション調整が元のステーク額の 3 倍で 1 回の追加購入ができると想定している場合、「custom_stake_amount」は提案されたステーク額の 25% を返し、その後のポジション調整のために 75% を残しておく必要があります。

--8<-- "includes/pricing.md"

## 構成の詳細

### minimum_roi を理解する

「minimal_roi」設定パラメータは、キーが期間である JSON オブジェクトです。
単位は分で、その値は比率としての最小 ROI です。
以下の例を参照してください。
```json
"minimal_roi": {
    "40": 0.0,    # Exit after 40 minutes if the profit is not negative
    "30": 0.01,   # Exit after 30 minutes if there is at least 1% profit
    "20": 0.02,   # Exit after 20 minutes if there is at least 2% profit
    "0":  0.04    # Exit immediately if there is at least 4% profit
},
```
ほとんどの戦略ファイルには、最適な `minimal_roi` 値がすでに含まれています。
このパラメータは、戦略ファイルまたは構成ファイルで設定できます。構成ファイルで使用すると、
戦略ファイルの「minimal_roi」値。
Strategy または Configuration のどちらでも設定されていない場合、デフォルトの 1000% `{"0": 10}` が使用され、取引で 1000% の利益が得られない限り、最小 ROI は無効になります。

!!! 「特定の時間後に強制終了する特殊なケース」に注意してください。
    特殊なケースでは、ROI として `"<N>": -1` を使用します。これにより、ボットは、それがプラスかマイナスかに関係なく、N 分後に強制的に取引を終了するため、時間制限のある強制終了を表します。

### Force_entry_enable を理解する

`force_entry_enable` 設定パラメータは、Telegram および REST API 経由でのforce-enter (`/forcelong`、`/forceshort`) コマンドの使用を有効にします。
セキュリティ上の理由から、デフォルトでは無効になっており、有効になっている場合、freqtrade は起動時に警告メッセージを表示します。
たとえば、「/forceenter ETH/BTC」をボットに送信すると、freqtrade がペアを購入し、通常の終了シグナル (ROI、ストップロス、/forceexit) が表示されるまで保持されます。

これは戦略によっては危険な場合があるため、注意して使用してください。

使用法の詳細については、[テレグラムのドキュメント](telegram-usage.md)を参照してください。

### 期限切れのキャンドルを無視する

より長い時間枠 (たとえば、1 時間以上) を操作し、低い「max_open_trades」値を使用する場合、取引スロットが利用可能になるとすぐに最後のローソクを処理できます。最後のローソク足を処理するときに、そのローソク足で買いシグナルを使用することが望ましくない状況が発生する可能性があります。たとえば、戦略でクロスオーバーを使用する条件を使用している場合、そのポイントは取引を開始するにはあまりにも前に過ぎている可能性があります。

このような状況では、「ignore_buying_expired_candle_after」を正の数に設定することで、指定された期間を超えたキャンドルを無視する機能を有効にすることができます。これは、買いシグナルが期限切れになるまでの秒数を示します。

たとえば、戦略で 1 時間の時間枠を使用しており、新しいローソク足が入った最初の 5 分以内にのみ購入したい場合は、次の構成を戦略に追加できます。
``` json
  {
    //...
    "ignore_buying_expired_candle_after": 300,
    // ...
  }
```
!!! 注記
    この設定は、新しいローソク足が出現するたびにリセットされるため、アクティブな 2 番目または 3 番目のローソク足でスティックシグナルが実行されるのを妨げることはありません。 1 つのローソク足に対してのみアクティブになる買いシグナルには、「トリガー」セレクターを使用するのが最適です。

### order_types を理解する

`order_types` 設定パラメータは、アクション (`entry`、`exit`、`stoploss`、`emergency_exit`、`force_exit`、`force_entry`) を注文タイプ (`market`、`limit` など) にマッピングするだけでなく、取引所でのストップロスを設定し、取引所でのストップロスの更新間隔を秒単位で定義します。

これにより、指値注文を使用してエントリーし、指値注文を使用して終了し、成行注文を使用してストップロスを作成することができます。
また、
ストップロスは「取引所で」、つまり買い注文が履行されるとすぐにストップロス注文が出されます。

設定ファイルに設定された `order_types` は、ストラテジ全体に設定された値を上書きするため、`order_types` 辞書全体を 1 か所で設定する必要があります。

これを構成する場合、次の 4 つの値 (`entry`、`exit`、`stoploss`、`stoploss_on_exchange`) が存在する必要があります。存在しない場合、ボットは起動に失敗します。

(`emergency_exit`、`force_exit`、`force_entry`、`stoploss_on_exchange`、`stoploss_on_exchange_interval`、`stoploss_on_exchange_limit_ratio`) の詳細については、ストップロスのドキュメント [取引所のストップロス](stoploss.md) を参照してください。

戦略の構文:
```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99,
}
```
構成：
```json
"order_types": {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": false,
    "stoploss_on_exchange_interval": 60
}
```
!!! 注「成行注文サポート」
    すべての取引所が「成行」注文をサポートしているわけではありません。
    取引所が成行注文をサポートしていない場合は、次のメッセージが表示されます。
    「Exchange <yourexchange> は成行注文をサポートしていません。」とすると、ボットは起動を拒否します。

!!! 警告「成行注文の使用」
    成行注文をご利用の際は、[成行注文の価格設定](#market-order-pricing)セクションをよくお読みください。

!!! 「取引所のストップロス」に注意してください。
    「order_types.stoploss_on_exchange_interval」は必須ではありません。次の場合は値を変更しないでください。
    あなたが何をしているのかわかりません。ストップロスの仕組みについて詳しくは、
    [ストップロスのドキュメント](stoploss.md)を参照してください。

    「order_types.stoploss_on_exchange」が有効で、ストップロスが取引所で手動でキャンセルされた場合、ボットは新しいストップロス注文を作成します。

!!! 警告「警告: order_types.stoploss_on_exchange の失敗」
    何らかの理由で取引所作成時のストップロスが失敗した場合、「緊急終了」が開始されます。デフォルトでは、成行注文を使用して取引を終了します。非常口の順序タイプは、「order_types」辞書に「emergency_exit」値を設定することで変更できますが、これはお勧めできません。

### order_time_in_force を理解する

「order_time_in_force」設定パラメータは、取引所で注文が実行されるポリシーを定義します。  
一般的に使用される有効期間は次のとおりです。

**GTC (キャンセルされるまで有効):**

ほとんどの場合、これは有効なデフォルトの時間です。これは、ユーザーがキャンセルするまで注文が交換されたままになることを意味します。完全にまたは部分的に満たすことができます。部分的に履行された場合、残りはキャンセルされるまで交換に残ります。

**FOK (フィル オア キル):**

これは、注文が即座にかつ完全に実行されない場合、注文は取引所によってキャンセルされることを意味します。

**IOC (即時またはキャンセル):**

部分的に満たされることを除けば、FOK (上記) と同じです。残りの部分は交換により自動的にキャンセルされます。

これは最小取引サイズを下回る部分的な約定につながる可能性があるため、必ずしも推奨されるわけではありません。

**PO (郵便のみ):**

ポストのみ注文。メーカー発注またはキャンセルとさせていただきます。
これは、注文が少なくとも一定期間、約定されていない状態でオーダーブック上に置かれなければならないことを意味します。

取引所でサポートされている有効期間の値については、[Exchange ドキュメント](exchanges.md) を確認してください。

#### time_in_force 構成

「order_time_in_force」パラメータには、有効なポリシー値の開始時間と終了時間の辞書が含まれています。
これは構成ファイルまたは戦略で設定できます。
構成ファイルに設定された値は、通常の [優先規則](#configuration-option-prevalence) に従って、ストラテジ内の値を上書きします。

可能な値は、「GTC」 (デフォルト)、「FOK」、または「IOC」です。
``` python
"order_time_in_force": {
    "entry": "GTC",
    "exit": "GTC"
},
```
!!! 警告
    自分が何をしているのかを理解し、特定の取引所で異なる値を使用した場合の影響を調査していない限り、デフォルト値を変更しないでください。


### 法定通貨への変換

Freqtrade は、Coingecko API を使用して、コインの価値を Telegram レポートの対応する法定通貨の価値に変換します。
法定通貨は設定ファイルで「fiat_display_currency」として設定できます。

構成から `fiat_display_currency` を完全に削除すると、coingecko の初期化がスキップされ、FIAT 通貨換算が表示されなくなります。これは、ボットが正しく機能するためには重要ではありません。

#### fiat_display_currency にはどのような値を使用できますか?

`fiat_display_currency` 設定パラメータは、通貨に使用する基本通貨を設定します。
ボット Telegram レポートでのコインから法定通貨への変換。

有効な値は次のとおりです。
```json
"AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD"
```
法定通貨に加えて、さまざまな暗号通貨がサポートされています。

有効な値は次のとおりです。
```json
"BTC", "ETH", "XRP", "LTC", "BCH", "BNB"
```
#### Coingecko レート制限の問題

一部の IP 範囲では、coingecko はレートを大幅に制限します。
このような場合は、coingecko API キーを構成に追加するとよいでしょう。
``` json
{
    "fiat_display_currency": "USD",
    "coingecko": {
        "api_key": "your-api",
        "is_demo": true
    }
}
```
Freqtrade は、Demo と Pro の両方の coingecko API キーをサポートしています。

Coingecko API キーは、ボットが正しく機能するために必要ありません。
これは Telegram レポートでコインを法定通貨に変換するためにのみ使用され、通常は API キーなしでも機能します。

## Exchange WebSocket の消費

Freqtrade は、ccxt.pro を通じて WebSocket を使用できます。

Freqtrade は、データを常に利用できるようにすることを目的としています。
WebSocket 接続が失敗した (または無効になった) 場合、ボットは REST API 呼び出しに戻ります。

WebSocket が原因であると思われる問題が発生した場合は、「exchange.enable_ws」設定 (デフォルトは true) を使用して WebSocket を無効にすることができます。
```jsonc
"exchange": {
    // ...
    "enable_ws": false,
    // ...
}
```
プロキシを使用する必要がある場合、詳細については [プロキシ セクション](#using-a-proxy-with-freqtrade) を参照してください。

!!! インフォメーション「ロールアウト」
    ボットの安定性を確保するために、これをゆっくりと実装しています。
    現在、使用は ohlcv データ ストリームに限定されています。
    また、少数の取引所に限定されており、新しい取引所は継続的に追加されています。

## ドライラン モードの使用

ボットをドライラン モードで起動して、ボットがどのように動作するかを確認することをお勧めします。
行動し、戦略のパフォーマンスはどうなるか。ドライランモードでは、
ボットはあなたのお金に関与しません。ライブ シミュレーションのみを実行します。
取引所で取引を作成します。

1. 「config.json」構成ファイルを編集します。
2. 「dry-run」を「true」に切り替え、永続データベースの「db_url」を指定します。
```json
"dry_run": true,
"db_url": "sqlite:///tradesv3.dryrun.sqlite",
```
3. Exchange API キーとシークレットを削除します (空の値または偽の資格情報で変更します)。
```json
"exchange": {
    "name": "binance",
    "key": "key",
    "secret": "secret",
    ...
}
```
ドライラン モードで実行するボットのパフォーマンスに満足したら、運用モードに切り替えることができます。

!!! 注記
    シミュレートされたウォレットはドライラン モード中に使用でき、開始資本は `dry_run_wallet` (デフォルトは 1000) であると想定されます。

### 予行演習に関する考慮事項

* API キーは提供される場合と提供されない場合があります。取引所での読み取り専用操作 (つまり、アカウントの状態を変更しない操作) のみがドライラン モードで実行されます。
* ウォレット (`/balance`) は `dry_run_wallet` に基づいてシミュレートされています。
* 注文はシミュレーションされ、取引所には送信されません。
* 成行注文は、注文が出された瞬間の注文帳の出来高に基づいて約定され、最大スリッページは 5% です。
* 価格が定義されたレベルに達すると指値注文が約定します。または、「unfilledtimeout」設定に基づいてタイムアウトになります。
* 指値注文は、価格を 1% 以上超えた場合に成行注文に変換され、通常の成行注文ルールに基づいて直ちに約定されます (上記の成行注文に関するポイントを参照)。
* `stoploss_on_exchange`と組み合わせると、ストップロス価格が約定されたものとみなされます。
* 未処理の注文 (データベースに保存される取引ではない) は、オフライン中に約定されなかったものとして、ボットの再起動後も開いたままになります。

## 本番モードに切り替える

本番モードでは、ボットがあなたの資金を利用します。戦略を誤ると、すべての資金を失う可能性があるため、注意してください。
運用モードで実行するときは、何をしているのかに注意してください。

本番モードに切り替えるときは、予行演習によって為替資金が台無しになり、最終的に統計が汚染されることを避けるために、必ず別の新しいデータベースを使用してください。

### Exchange アカウントをセットアップする

Exchange Web サイトから API キー (通常は「key」と「secret」を取得しますが、一部の取引所では追加の「password」が必要です) を作成する必要があります。これを構成内の適切なフィールドに挿入するか、「freqtrade new-config」コマンドで要求された場合に挿入する必要があります。
API キーは通常、ライブ取引 (リアルマネーの取引、ボットを「本番モード」で実行、取引所で実際の注文を実行) にのみ必要であり、予行演習 (取引シミュレーション) モードで実行するボットには必要ありません。ボットを予行演習モードで設定する場合、これらのフィールドに空の値を入力できます。

### ボットを実稼働モードに切り替えるには

**「config.json」ファイルを編集します。**

**ドライランを false に切り替え、設定されている場合はデータベース URL を忘れずに調整してください。**
```json
"dry_run": false,
```
**Exchange API キーを挿入します (偽の API キーに変更します):**
```json
{
    "exchange": {
        "name": "binance",
        "key": "af8ddd35195e9dc500b9a6f799f6f5c93d89193b",
        "secret": "08a9dc6db3d7b53e1acebd9275677f4b0a04f1a5",
        //"password": "", // Optional, not needed by all exchanges)
        // ...
    }
    //...
}
```
また、ドキュメントの [Exchanges](exchanges.md) セクションを必ず読んで、Exchange に固有の潜在的な構成の詳細を認識する必要があります。

!!! ヒント「秘密は内緒にしてね」
    シークレットを秘密にするには、API キーに 2 番目の構成を使用することをお勧めします。
    新しい設定ファイル (例: `config-private.json`) で上記のスニペットを使用し、設定をこのファイルに保存するだけです。
    次に、「freqtrade trade --config user_data/config.json --config user_data/config-private.json <...>」でボットを起動し、キーをロードします。

    **決して**プライベート設定ファイルや交換キーを他人と共有しないでください。

## Freqtrade でプロキシを使用する

freqtrade でプロキシを使用するには、適切な値に設定された変数 `"HTTP_PROXY"` と `"HTTPS_PROXY"` を使用してプロキシ設定をエクスポートします。
これにより、交換リクエストを除くすべて (テレグラム、coingecko など) にプロキシ設定が適用されます。
``` bash
export HTTP_PROXY="http://addr:port"
export HTTPS_PROXY="http://addr:port"
freqtrade
```
### プロキシ交換リクエスト

Exchange 接続にプロキシを使用するには、ccxt 構成の一部としてプロキシを定義する必要があります。
``` json
{ 
  "exchange": {
    "ccxt_config": {
      "httpsProxy": "http://addr:port",
      "wsProxy": "http://addr:port",
    }
  }
}
```
利用可能なプロキシ タイプの詳細については、[ccxt プロキシ ドキュメント](https://docs.ccxt.com/#/README?id=proxy) を参照してください。

## 次のステップ

これで config.json の構成が完了しました。次のステップは、[ボットを開始](bot-usage.md)することです。
