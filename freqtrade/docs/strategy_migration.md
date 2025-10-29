# V2 と V3 間の戦略の移行

新しい市場と取引タイプ (つまりショート取引/レバレッジを利用した取引) をサポートするには、インターフェイスでいくつかの変更が必要でした。
スポット市場以外の市場を使用する場合は、戦略を新しいフォーマットに移行してください。

私たちは既存の戦略との互換性を維持することに多大な努力を払ってきたため、__スポット市場__で freqtrade を使い続けたいだけであれば、今のところ変更は必要ありません。

簡単な概要をチェックリストとして使用できます。完全な移行の詳細については、以下の詳細セクションを参照してください。

## 簡単な概要/移行チェックリスト

注: `forcesell`、`forcebuy`、`emergencysell` は、それぞれ `force_exit`、`force_enter`、`emergency_exit` に変更されます。

* 戦略方法:
  * [`populate_buy_trend()` -> `populate_entry_trend()`](#populate_buy_trend)
  * [`populate_sell_trend()` -> `populate_exit_trend()`](#populate_sell_trend)
  * [`custom_sell()` -> `custom_exit()`](#custom_sell)
  * [`check_buy_timeout()` -> `check_entry_timeout()`](#custom_entry_timeout)
  * [`check_sell_timeout()` -> `check_exit_timeout()`](#custom_entry_timeout)
  * 取引オブジェクトのないコールバックへの新しい `side` 引数
    * [`カスタムステーク額`](#カスタムステーク額)
    * [`confirm_trade_entry`](#confirm_trade_entry)
    * [`custom_entry_price`](#custom_entry_price)
  * [`confirm_trade_exit`の引数名を変更](#confirm_trade_exit)
* データフレーム列:
  * [`購入` -> `enter_long`](#populate_buy_trend)
  * [`sell` -> `exit_long`](#populate_sell_trend)
  * [`buy_tag` -> `enter_tag` (ロングトレードとショートトレードの両方に使用)](#populate_buy_trend)
  * [新しい列 `enter_short` と対応する新しい列 `exit_short`](#populate_sell_trend)
* trade-object には次の新しいプロパティが追加されました。
  * `is_short`
  * `entry_side`
  * `出口側`
  * `貿易方向`
  * 名前変更: `sell_reason` -> `exit_reason`
* [`trade.nr_of_successive_buys` を `trade.nr_of_successive_entries` に名前変更しました (主に `adjust_trade_position()` に関連します)](#adjust-trade-position-changes)
* 新しい [`leverage` コールバック](strategy-callbacks.md#leverage-callback) を導入しました。
* 情報ペアはタプルの 3 番目の要素を渡して、ローソクのタイプを定義できるようになりました。
* `@informative` デコレーターはオプションの `candle_type` 引数を受け取るようになりました。
* [ヘルパー メソッド](#helper-methods) `stoploss_from_open` と `stoploss_from_absolute` は追加の引数として `is_short` を取るようになりました。
* `INTERFACE_VERSION` は 3 に設定する必要があります。
* [戦略/構成設定](#strategyconfiguration-settings)。
  * `order_time_in_force` は買い -> エントリー、売り -> エグジットです。
  * `order_types` は買い -> エントリー、売り -> エグジットです。
  * `unfilledtimeout` 買い -> エントリー、売り -> エグジット。
  * `ignore_buying_expired_candle_after` -> 「ask_strategy/exit_pricing」の代わりにルートレベルに移動
※用語の変更
  * 売りの理由は、売りではなく「出口」という新しい名前を反映するように変更されました。 「exit_reason」チェックを使用している場合は戦略に注意し、最終的には戦略を更新してください。
    * `sell_signal` -> `exit_signal`
    * `custom_sell` -> `custom_exit`
    * `force_sell` -> `force_exit`
    * `emergency_sell` -> `emergency_exit`
  * 注文価格
    * `bid_strategy` -> `entry_pricing`
    * `ask_strategy` -> `exit_pricing`
    * `ask_last_balance` -> `price_last_balance`
    * `bid_last_balance` -> `price_last_balance`
  * Webhook の用語が「売り」から「エグジット」に、「買い」から「エントリー」に変更されました
    * `webhookbuy` -> `entry`
    * `webhookbuyfill` -> `entry_fill`
    * `webhookbuycancel` -> `entry_cancel`
    * `webhooksell` -> `exit`
    * `webhooksellfill` -> `exit_fill`
    * `webhooksellcancel` -> `exit_cancel`
  * 電報通知設定
    * `購入` -> `エントリー`
    * `buy_fill` -> `entry_fill`
    * `購入_キャンセル` -> `エントリー_キャンセル`
    * `売り` -> `撤退`
    * `sell_fill` -> `exit_fill`
    * `sell_cancel` -> `exit_cancel`
  * 戦略/構成設定:
    * `use_sell_signal` -> `use_exit_signal`
    * `sell_profit_only` -> `exit_profit_only`
    * `sell_profit_offset` -> `exit_profit_offset`
    * `ignore_roi_if_buy_signal` -> `ignore_roi_if_entry_signal`
    * `forcebuy_enable` -> `force_entry_enable`

## 詳しい説明

### `populate_buy_trend`

`populate_buy_trend()` では、割り当てる列を `'buy`' から 'enter_long'` に変更し、メソッド名を `populate_buy_trend` から `populate_entry_trend` に変更します。
```python hl_lines="1 9"
def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
            (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['buy', 'buy_tag']] = (1, 'rsi_cross')

    return dataframe
```
後：
```python hl_lines="1 9"
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
            (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

    return dataframe
```
ショートトレードのエントリーおよびエグジット方法については、[Strategy ドキュメント](strategy-customization.md#entry-signal-rules) を参照してください。

### `populate_sell_trend`

`populate_buy_trend` と同様に、`populate_sell_trend()` は `populate_exit_trend()` に名前が変更されます。
また、列を「sell」から「exit_long」に変更します。
``` python hl_lines="1 9"
def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['sell', 'exit_tag']] = (1, 'some_exit_tag')
    return dataframe
```
後
``` python hl_lines="1 9"
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['exit_long', 'exit_tag']] = (1, 'some_exit_tag')
    return dataframe
```
ショートトレードのエントリーおよびエグジット方法については、[Strategy ドキュメント](strategy-customization.md#exit-signal-rules) を参照してください。

### `カスタム販売`

「custom_sell」は「custom_exit」に名前が変更されました。
また、現在の利益や「exit_profit_only」設定とは関係なく、反復ごとに呼び出されるようになりました。
``` python hl_lines="2"
class AwesomeStrategy(IStrategy):
    def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        # ...
```

``` python hl_lines="2"
class AwesomeStrategy(IStrategy):
    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        # ...
```
### `custom_entry_timeout`

`check_buy_timeout()` は `check_entry_timeout()` に名前が変更され、`check_sell_timeout()` は `check_exit_timeout()` に名前が変更されました。
``` python hl_lines="2 6"
class AwesomeStrategy(IStrategy):
    def check_buy_timeout(self, pair: str, trade: 'Trade', order: dict, 
                            current_time: datetime, **kwargs) -> bool:
        return False

    def check_sell_timeout(self, pair: str, trade: 'Trade', order: dict, 
                            current_time: datetime, **kwargs) -> bool:
        return False 
```

``` python hl_lines="2 6"
class AwesomeStrategy(IStrategy):
    def check_entry_timeout(self, pair: str, trade: 'Trade', order: 'Order', 
                            current_time: datetime, **kwargs) -> bool:
        return False

    def check_exit_timeout(self, pair: str, trade: 'Trade', order: 'Order', 
                            current_time: datetime, **kwargs) -> bool:
        return False 
```
### `custom_stake_amount`

新しい文字列引数 `side` - `"long"` または `"short"` のいずれかになります。
``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: Optional[float], max_stake: float,
                            entry_tag: Optional[str], **kwargs) -> float:
        # ... 
        return proposed_stake
```

``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            entry_tag: str | None, side: str, **kwargs) -> float:
        # ... 
        return proposed_stake
```
### `confirm_trade_entry`

新しい文字列引数 `side` - `"long"` または `"short"` のいずれかになります。
``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: Optional[str], 
                            **kwargs) -> bool:
      return True
```
後：
``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: str | None, 
                            side: str, **kwargs) -> bool:
      return True
```
### `confirm_trade_exit`

引数「sell_reason」を「exit_reason」に変更しました。
互換性のため、`sell_reason` は引き続き期間限定で提供されます。
``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, sell_reason: str,
                           current_time: datetime, **kwargs) -> bool:
    return True
```
後：
``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
    return True
```
### `custom_entry_price`

新しい文字列引数 `side` - `"long"` または `"short"` のいずれかになります。
``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def custom_entry_price(self, pair: str, current_time: datetime, proposed_rate: float,
                           entry_tag: Optional[str], **kwargs) -> float:
      return proposed_rate
```
後：
``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def custom_entry_price(self, pair: str, trade: Trade | None, current_time: datetime, proposed_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:
      return proposed_rate
```
### トレードポジションの変更を調整する

Adjust-trade-position自体は変更されませんでしたが、`trade.nr_of_successful_buys`を使用するのではなく、代わりにショートエントリーも含まれる`trade.nr_of_successful_entries`を使用する必要があります。

### ヘルパー メソッド

引数「is_short」を「stoploss_from_open」と「stoploss_from_absolute」に追加しました。
これには「trade.is_short」の値を指定する必要があります。
``` python hl_lines="5 7"
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        # once the profit has risen above 10%, keep the stoploss at 7% above the open price
        if current_profit > 0.10:
            return stoploss_from_open(0.07, current_profit)

        return stoploss_from_absolute(current_rate - (candle['atr'] * 2), current_rate)

        return 1

```
後：
``` python hl_lines="5 7"
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:
        # once the profit has risen above 10%, keep the stoploss at 7% above the open price
        if current_profit > 0.10:
            return stoploss_from_open(0.07, current_profit, is_short=trade.is_short)

        return stoploss_from_absolute(current_rate - (candle['atr'] * 2), current_rate, is_short=trade.is_short, leverage=trade.leverage)


```
### 戦略/構成設定

#### `order_time_in_force`

`order_time_in_force` 属性が `"buy"` から `"entry"` に、および `"sell"` から `"exit"` に変更されました。
``` python
    order_time_in_force: dict = {
        "buy": "gtc",
        "sell": "gtc",
    }
```
後：
``` python hl_lines="2 3"
    order_time_in_force: dict = {
        "entry": "GTC",
        "exit": "GTC",
    }
```
#### `order_types`

`order_types` はすべての文言を `buy` から `entry` に、そして `sell` から `exit` に変更しました。
そして2つの単語は「_」で結ばれます。
``` python hl_lines="2-6"
    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "forcesell": "market",
        "forcebuy": "market",
        "stoploss": "market",
        "stoploss_on_exchange": false,
        "stoploss_on_exchange_interval": 60
    }
```
後：
``` python hl_lines="2-6"
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "emergency_exit": "market",
        "force_exit": "market",
        "force_entry": "market",
        "stoploss": "market",
        "stoploss_on_exchange": false,
        "stoploss_on_exchange_interval": 60
    }
```
#### 戦略レベルの設定

* `use_sell_signal` -> `use_exit_signal`
* `sell_profit_only` -> `exit_profit_only`
* `sell_profit_offset` -> `exit_profit_offset`
* `ignore_roi_if_buy_signal` -> `ignore_roi_if_entry_signal`
``` python hl_lines="2-5"
    # These values can be overridden in the config.
    use_sell_signal = True
    sell_profit_only = True
    sell_profit_offset: 0.01
    ignore_roi_if_buy_signal = False
```
後：
``` python hl_lines="2-5"
    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = True
    exit_profit_offset: 0.01
    ignore_roi_if_entry_signal = False
```
#### `unfilledtimeout`

「unfilledtimeout」はすべての文言を「買い」から「エントリー」に、「売り」から「退出」に変更しました。
``` python hl_lines="2-3"
unfilledtimeout = {
        "buy": 10,
        "sell": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    }
```
後：
``` python hl_lines="2-3"
unfilledtimeout = {
        "entry": 10,
        "exit": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    }
```
#### 「注文価格」

注文価格は 2 つの方法で変更されました。 「bid_strategy」は「entry_pricing」に、「ask_strategy」は「exit_pricing」に名前が変更されました。
属性 `ask_last_balance` -> `price_last_balance` および `bid_last_balance` -> `price_last_balance` も同様に名前変更されました。
また、価格側を「ask」、「bid」、「same」、または「other」として定義できるようになりました。
詳細については、[価格設定ドキュメント](configuration.md#prices-used-for-orders) を参照してください。
``` json hl_lines="2-3 6 12-13 16"
{
    "bid_strategy": {
        "price_side": "bid",
        "use_order_book": true,
        "order_book_top": 1,
        "ask_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "ask_strategy":{
        "price_side": "ask",
        "use_order_book": true,
        "order_book_top": 1,
        "bid_last_balance": 0.0
        "ignore_buying_expired_candle_after": 120
    }
}
```
後：
``` json  hl_lines="2-3 6 12-13 16"
{
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "exit_pricing":{
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0
    },
    "ignore_buying_expired_candle_after": 120
}
```
## FreqAI 戦略

`populate_any_indicators()` メソッドは、`feature_engineering_expand_all()`、`feature_engineering_expand_basic()`、`feature_engineering_standard()`、`set_freqai_targets()` に分割されました。

新しい関数ごとに、ペア (および必要に応じて時間枠) が列に自動的に追加されます。
そのため、新しいロジックを使用すると、機能の定義がはるかに簡単になります。

各メソッドの完全な説明については、対応する [freqAI ドキュメント ページ](freqai-feature-engineering.md#defining-the-features) にアクセスしてください。
``` python linenums="1" hl_lines="12-37 39-42 63-65 67-75"

def populate_any_indicators(
        self, pair, df, tf, informative=None, set_generalized_indicators=False
    ):

        if informative is None:
            informative = self.dp.get_pair_dataframe(pair, tf)

        # first loop is automatically duplicating indicators for time periods
        for t in self.freqai_info["feature_parameters"]["indicator_periods_candles"]:

            t = int(t)
            informative[f"%-{pair}rsi-period_{t}"] = ta.RSI(informative, timeperiod=t)
            informative[f"%-{pair}mfi-period_{t}"] = ta.MFI(informative, timeperiod=t)
            informative[f"%-{pair}adx-period_{t}"] = ta.ADX(informative, timeperiod=t)
            informative[f"%-{pair}sma-period_{t}"] = ta.SMA(informative, timeperiod=t)
            informative[f"%-{pair}ema-period_{t}"] = ta.EMA(informative, timeperiod=t)

            bollinger = qtpylib.bollinger_bands(
                qtpylib.typical_price(informative), window=t, stds=2.2
            )
            informative[f"{pair}bb_lowerband-period_{t}"] = bollinger["lower"]
            informative[f"{pair}bb_middleband-period_{t}"] = bollinger["mid"]
            informative[f"{pair}bb_upperband-period_{t}"] = bollinger["upper"]

            informative[f"%-{pair}bb_width-period_{t}"] = (
                informative[f"{pair}bb_upperband-period_{t}"]
                - informative[f"{pair}bb_lowerband-period_{t}"]
            ) / informative[f"{pair}bb_middleband-period_{t}"]
            informative[f"%-{pair}close-bb_lower-period_{t}"] = (
                informative["close"] / informative[f"{pair}bb_lowerband-period_{t}"]
            )

            informative[f"%-{pair}roc-period_{t}"] = ta.ROC(informative, timeperiod=t)

            informative[f"%-{pair}relative_volume-period_{t}"] = (
                informative["volume"] / informative["volume"].rolling(t).mean()
            ) # (1)

        informative[f"%-{pair}pct-change"] = informative["close"].pct_change()
        informative[f"%-{pair}raw_volume"] = informative["volume"]
        informative[f"%-{pair}raw_price"] = informative["close"]
        # (2)

        indicators = [col for col in informative if col.startswith("%")]
        # This loop duplicates and shifts all indicators to add a sense of recency to data
        for n in range(self.freqai_info["feature_parameters"]["include_shifted_candles"] + 1):
            if n == 0:
                continue
            informative_shift = informative[indicators].shift(n)
            informative_shift = informative_shift.add_suffix("_shift-" + str(n))
            informative = pd.concat((informative, informative_shift), axis=1)

        df = merge_informative_pair(df, informative, self.config["timeframe"], tf, ffill=True)
        skip_columns = [
            (s + "_" + tf) for s in ["date", "open", "high", "low", "close", "volume"]
        ]
        df = df.drop(columns=skip_columns)

        # Add generalized indicators here (because in live, it will call this
        # function to populate indicators during training). Notice how we ensure not to
        # add them multiple times
        if set_generalized_indicators:
            df["%-day_of_week"] = (df["date"].dt.dayofweek + 1) / 7
            df["%-hour_of_day"] = (df["date"].dt.hour + 1) / 25
            # (3)

            # user adds targets here by prepending them with &- (see convention below)
            df["&-s_close"] = (
                df["close"]
                .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
                .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
                .mean()
                / df["close"]
                - 1
            )  # (4)

        return df
```
1. 機能 - `feature_engineering_expand_all` に移動します
2. 基本機能。「indicator_periods_candles」全体では拡張されていません - 「feature_engineering_expand_basic()」に移動します。
3. 拡張すべきではない標準機能 - `feature_engineering_standard()` に移動します。
4. ターゲット - この部分を `set_freqai_targets()` に移動します。

### freqai - 特徴エンジニアリング すべて展開

機能は自動的に拡張されるようになりました。そのため、拡張ループと `{pair}` / `{timeframe}` 部分を削除する必要があります。
``` python linenums="1"
    def feature_engineering_expand_all(self, dataframe, period, **kwargs) -> DataFrame::
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details on how these config defined parameters accelerate feature engineering
        in the documentation at:

        https://www.freqtrade.io/en/latest/freqai-parameter-table/#feature-parameters

        https://www.freqtrade.io/en/latest/freqai-feature-engineering/#defining-the-features

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """

        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=period, stds=2.2
        )
        dataframe["bb_lowerband-period"] = bollinger["lower"]
        dataframe["bb_middleband-period"] = bollinger["mid"]
        dataframe["bb_upperband-period"] = bollinger["upper"]

        dataframe["%-bb_width-period"] = (
            dataframe["bb_upperband-period"]
            - dataframe["bb_lowerband-period"]
        ) / dataframe["bb_middleband-period"]
        dataframe["%-close-bb_lower-period"] = (
            dataframe["close"] / dataframe["bb_lowerband-period"]
        )

        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)

        dataframe["%-relative_volume-period"] = (
            dataframe["volume"] / dataframe["volume"].rolling(period).mean()
        )

        return dataframe

```
### Freqai - 特徴量エンジニアリングの基礎

基本的な機能。機能から `{pair}` 部分を必ず削除してください。
``` python linenums="1"
    def feature_engineering_expand_basic(self, dataframe: DataFrame, **kwargs) -> DataFrame::
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `include_timeframes`, `include_shifted_candles`, and `include_corr_pairs`.
        In other words, a single feature defined in this function
        will automatically expand to a total of
        `include_timeframes` * `include_shifted_candles` * `include_corr_pairs`
        numbers of features added to the model.

        Features defined here will *not* be automatically duplicated on user defined
        `indicator_periods_candles`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details on how these config defined parameters accelerate feature engineering
        in the documentation at:

        https://www.freqtrade.io/en/latest/freqai-parameter-table/#feature-parameters

        https://www.freqtrade.io/en/latest/freqai-feature-engineering/#defining-the-features

        :param df: strategy dataframe which will receive the features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe
```
### FreqAI - 特徴エンジニアリング標準
``` python linenums="1"
    def feature_engineering_standard(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This optional function will be called once with the dataframe of the base timeframe.
        This is the final function to be called, which means that the dataframe entering this
        function will contain all the features and columns created by all other
        freqai_feature_engineering_* functions.

        This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
        This function is a good place for any feature that should not be auto-expanded upon
        (e.g. day of the week).

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/latest/freqai-feature-engineering

        :param df: strategy dataframe which will receive the features
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
        dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
        return dataframe
```
### FreqAI - ターゲットの設定

ターゲットは独自の専用メソッドを取得できるようになりました。
``` python linenums="1"
    def set_freqai_targets(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/latest/freqai-feature-engineering

        :param df: strategy dataframe which will receive the targets
        usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
        """
        dataframe["&-s_close"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["close"]
            - 1
            )

        return dataframe
```
### FreqAI - 新しいデータ パイプライン

カスタム `train()`/`predict()` 関数を使用して独自のカスタム `IFreqaiModel` を作成し、*かつ* まだ `data_cleaning_train/predict()` に依存している場合は、新しいパイプラインに移行する必要があります。モデルが `data_cleaning_train/predict()` に依存していない場合は、この移行について心配する必要はありません。つまり、この移行ガイドが関係するのはごく一部のパワー ユーザーです。誤ってこのガイドに遭遇した場合は、Freqtrade discord サーバーで問題について詳しく問い合わせてください。

変換では、まず「data_cleaning_train/predict()」を削除し、「IFreqaiModel」クラスの「define_data_pipeline()」および「define_label_pipeline()」関数に置き換えます。
```python  linenums="1" hl_lines="11-14 47-49 55-57"
class MyCoolFreqaiModel(BaseRegressionModel):
    """
    Some cool custom IFreqaiModel you made before Freqtrade version 2023.6
    """
    def train(
        self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs
    ) -> Any:

        # ... your custom stuff

        # Remove these lines
        # data_dictionary = dk.make_train_test_datasets(features_filtered, labels_filtered)
        # self.data_cleaning_train(dk)
        # data_dictionary = dk.normalize_data(data_dictionary)
        # (1)

        # Add these lines. Now we control the pipeline fit/transform ourselves
        dd = dk.make_train_test_datasets(features_filtered, labels_filtered)
        dk.feature_pipeline = self.define_data_pipeline(threads=dk.thread_count)
        dk.label_pipeline = self.define_label_pipeline(threads=dk.thread_count)

        (dd["train_features"],
         dd["train_labels"],
         dd["train_weights"]) = dk.feature_pipeline.fit_transform(dd["train_features"],
                                                                  dd["train_labels"],
                                                                  dd["train_weights"])

        (dd["test_features"],
         dd["test_labels"],
         dd["test_weights"]) = dk.feature_pipeline.transform(dd["test_features"],
                                                             dd["test_labels"],
                                                             dd["test_weights"])

        dd["train_labels"], _, _ = dk.label_pipeline.fit_transform(dd["train_labels"])
        dd["test_labels"], _, _ = dk.label_pipeline.transform(dd["test_labels"])

        # ... your custom code

        return model

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> tuple[DataFrame, npt.NDArray[np.int_]]:

        # ... your custom stuff

        # Remove these lines:
        # self.data_cleaning_predict(dk)
        # (2)

        # Add these lines:
        dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
            dk.data_dictionary["prediction_features"], outlier_check=True)

        # Remove this line
        # pred_df = dk.denormalize_labels_from_metadata(pred_df)
        # (3)

        # Replace with these lines
        pred_df, _, _ = dk.label_pipeline.inverse_transform(pred_df)
        if self.freqai_info.get("DI_threshold", 0) > 0:
            dk.DI_values = dk.feature_pipeline["di"].di_values
        else:
            dk.DI_values = np.zeros(outliers.shape[0])
        dk.do_predict = outliers

        # ... your custom code
        return (pred_df, dk.do_predict)
```
1. データの正規化とクリーニングが新しいパイプライン定義で均一化されました。これは、新しい `define_data_pipeline()` 関数と `define_label_pipeline()` 関数で作成されます。 `data_cleaning_train()` 関数と `data_cleaning_predict()` 関数は使用されなくなりました。必要に応じて、「define_data_pipeline()」をオーバーライドして独自のカスタム パイプラインを作成できます。
2. データの正規化とクリーニングが新しいパイプライン定義で均一化されました。これは、新しい `define_data_pipeline()` 関数と `define_label_pipeline()` 関数で作成されます。 `data_cleaning_train()` 関数と `data_cleaning_predict()` 関数は使用されなくなりました。必要に応じて、「define_data_pipeline()」をオーバーライドして独自のカスタム パイプラインを作成できます。
3. データの非正規化は新しいパイプラインで行われます。これを以下の行に置き換えます。
