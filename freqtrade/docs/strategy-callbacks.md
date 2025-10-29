# 戦略コールバック

メインの戦略関数 (`populate_indicators()`、`populate_entry_trend()`、`populate_exit_trend()`) はベクトル化された方法で使用する必要があり、[バックテスト中に 1 回] (bot-basics.md#backtesting-hyperopt-execution-logic) のみ呼び出されますが、コールバックは「必要なときはいつでも」呼び出されます。

したがって、操作中の遅延を避けるために、コールバックで大量の計算を実行することは避けてください。
使用されるコールバックに応じて、取引の開始時または終了時、または取引期間中に呼び出される場合があります。

現在利用可能なコールバック:

* [`bot_start()`](#bot-start)
* [`bot_loop_start()`](#ボットループスタート)
* [`custom_stake_amount()`](#ステークサイズ管理)
* [`custom_exit()`](#カスタム終了信号)
* [`custom_stoploss()`](#カスタムストップロス)
* [`custom_roi()`](#カスタムロイ)
* [`custom_entry_price()` および `custom_exit_price()`](#custom-order-price-rules)
* [`check_entry_timeout()` および `check_exit_timeout()`](#custom-order-timeout-rules)
* [`confirm_trade_entry()`](#トレードエントリー-購入注文-確認)
* [`confirm_trade_exit()`](#トレード出口売り注文確認)
* [`adjust_trade_position()`](#adjust-trade-position)
* [`adjust_entry_price()`](#adjust-entry-price)
* [`leverage()`](#leverage-callback)
* [`order_filled()`](#order-filled-callback)

!!! Tip "コールバック呼び出しシーケンス"
    コールバック呼び出しシーケンスは [bot-basics](bot-basics.md#bot-execution-logic) で見つけることができます。

--8<-- "includes/strategy-imports.md"

--8<-- "includes/strategy-exit-comparisons.md"


## ボットの開始

ストラテジーがロードされるときに 1 回呼び出される単純なコールバック。
これは、一度だけ実行する必要があり、データプロバイダーとウォレットが設定された後に実行されるアクションを実行するために使用できます。
``` python
import requests

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def bot_start(self, **kwargs) -> None:
        """
        Called only once after bot instantiation.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        if self.config["runmode"].value in ("live", "dry_run"):
            # Assign this to the class by using self.*
            # can then be used by populate_* methods
            self.custom_remote_data = requests.get("https://some_remote_source.example.com")

```
hyperopt では、これは起動時に 1 回だけ実行されます。

## ボットループの開始

ドライ/ライブ モードでの各ボット スロットル反復の開始時に (約 5 回ごとに) 1 回呼び出される単純なコールバック
別の設定でない限り、秒単位)、またはバックテスト/ハイパーオプト モードではキャンドルごとに 1 回。
これは、ペアに依存しない計算 (すべてのペアに適用)、外部データのロードなどを実行するために使用できます。
``` python
# Default imports
import requests

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def bot_loop_start(self, current_time: datetime, **kwargs) -> None:
        """
        Called at the start of the bot iteration (one loop).
        Might be used to perform pair-independent tasks
        (e.g. gather some remote resource for comparison)
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        if self.config["runmode"].value in ("live", "dry_run"):
            # Assign this to the class by using self.*
            # can then be used by populate_* methods
            self.remote_data = requests.get("https://some_remote_source.example.com")

```
## ステークサイズの管理

取引を開始する前に呼び出され、新しい取引を行うときにポジション サイズを管理できるようになります。
```python
# Default imports

class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            leverage: float, entry_tag: str | None, side: str,
                            **kwargs) -> float:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
        current_candle = dataframe.iloc[-1].squeeze()

        if current_candle["fastk_rsi_1h"] > current_candle["fastd_rsi_1h"]:
            if self.config["stake_amount"] == "unlimited":
                # Use entire available wallet during favorable conditions when in compounding mode.
                return max_stake
            else:
                # Compound profits during favorable conditions instead of using a static stake.
                return self.wallets.get_total_stake_amount() / self.config["max_open_trades"]

        # Use default stake amount.
        return proposed_stake
```
コードで例外が発生した場合、Freqtrade は `proused_stake` 値に戻ります。例外自体がログに記録されます。

!!! Tip
    「min_stake <= returns_value <= max_stake」であることを保証する必要はありません。戻り値がサポートされている範囲に固定され、このアクションがログに記録されるため、取引は成功します。

!!! Tip
    「0」または「None」を返すと、取引が行われなくなります。

## カスタム終了信号

取引が終了するまで、スロットル反復ごと (約 5 秒ごと) にオープン取引が呼び出されます。

指定された位置を閉じる必要があることを示すカスタム終了信号を定義できます (完全終了)。これは、個々の取引ごとに終了条件をカスタマイズする必要がある場合、または終了の決定を行うために取引データが必要な場合に非常に役立ちます。

たとえば、`custom_exit()` を使用して 1:2 のリスク リワード ROI を実装できます。

ストップロスの代わりに `custom_exit()` シグナルを使用することは *推奨されません*。この点では、`custom_stoploss()` を使用するより劣った方法ですが、交換時にストップロスを維持することもできます。

!!! Note
    このメソッドから (空ではない) `string` または `True` を返すことは、指定された時間にローソク足に終了シグナルを設定することと同じです。終了信号がすでに設定されている場合、または終了信号が無効になっている場合 (`use_exit_signal=False`)、このメソッドは呼び出されません。 「string」の最大長は 64 文字です。この制限を超えると、メッセージは 64 文字に切り詰められます。
    `custom_exit()` は `exit_profit_only` を無視し、新しい Enter シグナルがある場合でも、`use_exit_signal=False` でない限り常に呼び出されます。

現在の利益に応じてさまざまなインジケーターを使用し、1 日以上開いた取引を終了する方法の例:
``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Above 20% profit, sell when rsi < 80
        if current_profit > 0.2:
            if last_candle["rsi"] < 80:
                return "rsi_below_80"

        # Between 2% and 10%, sell if EMA-long above EMA-short
        if 0.02 < current_profit < 0.1:
            if last_candle["emalong"] > last_candle["emashort"]:
                return "ema_long_below_80"

        # Sell any positions at a loss if they are held for more than one day.
        if current_profit < 0.0 and (current_time - trade.open_date_utc).days >= 1:
            return "unclog"
```
ストラテジー コールバックでのデータフレームの使用の詳細については、[データフレーム アクセス](strategy-advanced.md#dataframe-access) を参照してください。

## カスタムストップロス

取引が終了するまで、反復ごと (約 5 秒ごと) にオープン取引が呼び出されます。

カスタム ストップロス メソッドの使用は、ストラテジー オブジェクトで `use_custom_stoploss=True` を設定することによって有効にする必要があります。

ストップロス価格は上方にのみ移動できます。「custom_stoploss」から返されたストップロス値が以前に設定されたストップロス価格よりも低い場合、その値は無視されます。従来の「ストップロス」値は絶対的な下位レベルとして機能し、(取引で初めてこのメソッドが呼び出される前に) 初期ストップロスとして設定され、依然として必須です。  
カスタム ストップロスは通常の変更ストップロスとして機能するため、「trailing_stop」と同様に動作します。これにより終了する取引には、「trailing_stop_loss」` の exit_reason が設定されます。

このメソッドは、ストップロス値 (浮動小数点数 / 数値) を現在の価格のパーセンテージとして返す必要があります。
例えば。 「current_rate」が 200 USD の場合、「0.02」を返すとストップロス価格が 2% 低い 196 USD に設定されます。
バックテスト中、「current_rate」（および「current_profit」）はローソク足の高値（または短期取引の場合は安値）に対して提供され、結果として得られるストップロスはローソク足の安値（または短期取引の場合は高値）に対して評価されます。

戻り値の絶対値が使用される (符号は無視される) ため、`0.05` または `-0.05` を返すと同じ結果となり、現在の価格の 5% 下のストップロスになります。
「None」を返すと「変更したくない」と解釈され、ストップロスを変更したくない場合に返す唯一の安全な方法です。
`NaN` および `inf` 値は無効とみなされ、無視されます (`None` と同じ)。

取引所のストップロスは `trailing_stop` と同様に機能し、取引所のストップロスは `stoploss_on_exchange_interval` で設定されたように更新されます ([取引所のストップロスの詳細](stoploss.md#stop-loss-on-exchangefreqtrade))。

先物市場を利用している場合は、[ストップロスとレバレッジ](stoploss.md#stoploss-and-leverage) セクションに注意してください。「custom_stoploss」から返されるストップロス値は、相対的な価格の動きではなく、この取引のリスクであるためです。

!!! Note "日付の使用"
    すべての時間ベースの計算は、`current_time` に基づいて実行する必要があります。`datetime.now()` または `datetime.utcnow()` の使用はバックテストのサポートを中断するため、推奨されません。

!!! Tip "トレーリングストップロス"
    カスタムのストップロス値を使用する場合は、「trailing_stop」を無効にすることをお勧めします。どちらも連携して機能しますが、カスタム関数ではこれを望まないのに、価格を引き上げるためのトレーリング ストップが発生し、競合する動作が発生する可能性があります。

### ポジション調整後にストップロスを調整する
戦略によっては、[ポジション調整](#adjust-trade-position) 後に両方向でストップロスを調整する必要が生じる場合があります。
このため、freqtrade は注文が約定した後に `after_fill=True` を指定して追加の呼び出しを行います。これにより、戦略でストップロスを任意の方向に移動できるようになります (また、ストップロスと現在の価格の間のギャップも拡大しますが、これは通常は禁止されています)。

!!! Note "下位互換性"
    この呼び出しは、「after_fill」パラメータが「custom_stoploss」関数の関数定義の一部である場合にのみ行われます。
    したがって、これは既存の実行中の戦略に影響を与えることはありません（そして、驚くべきことに）。

### カスタムストップロスの例

次のセクションでは、カスタム ストップロス関数で何ができるかについての例をいくつか示します。
もちろん、さらに多くのことが可能であり、すべての例を自由に組み合わせることができます。

#### カスタム ストップロスによるトレーリング ストップ

通常の 4% のトレーリング ストップロス (最大到達価格から 4% 遅れたトレーリング) をシミュレートするには、次の非常に簡単な方法を使用します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:
        """
        Custom stoploss logic, returning the new distance relative to current_rate (as ratio).
        e.g. returning -0.05 would create a stoploss 5% below current_rate.
        The custom stoploss can never be below self.stoploss, which serves as a hard maximum loss.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/

        When not implemented by a strategy, returns the initial stoploss value.
        Only called when use_custom_stoploss is set to True.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param after_fill: True if the stoploss is called after the order was filled.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: New stoploss value, relative to the current_rate
        """
        return -0.04 * trade.leverage
```
#### 時間ベースのトレーリングストップ

最初の 60 分間は最初のストップロスを使用し、その後 10% のトレーリング ストップロスに変更し、2 時間 (120 分) 後に 5% のトレーリング ストップロスを使用します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:

        # Make sure you have the longest interval first - these conditions are evaluated from top to bottom.
        if current_time - timedelta(minutes=120) > trade.open_date_utc:
            return -0.05 * trade.leverage
        elif current_time - timedelta(minutes=60) > trade.open_date_utc:
            return -0.10 * trade.leverage
        return None
```
#### アフターフィル調整を備えた時間ベースのトレーリングストップ

最初の 60 分間は最初のストップロスを使用し、その後 10% のトレーリング ストップロスに変更し、2 時間 (120 分) 後に 5% のトレーリング ストップロスを使用します。
追加の注文が約定した場合は、ストップロスを新しい `open_rate` ([すべてのエントリの平均](#position-adjust-calculations)) よりも -10% 低く設定します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:

        if after_fill: 
            # After an additional order, start with a stoploss of 10% below the new open rate
            return stoploss_from_open(0.10, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        # Make sure you have the longest interval first - these conditions are evaluated from top to bottom.
        if current_time - timedelta(minutes=120) > trade.open_date_utc:
            return -0.05 * trade.leverage
        elif current_time - timedelta(minutes=60) > trade.open_date_utc:
            return -0.10 * trade.leverage
        return None
```
#### ペアごとに異なるストップロス

ペアに応じて異なるストップロスを使用します。
この例では、「ETH/BTC」と「XRP/BTC」のトレーリングストップロスを10％、「LTC/BTC」のトレーリングストップロスを5％、その他すべてのペアのトレーリングストップロスを15％として最高価格を追跡します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        if pair in ("ETH/BTC", "XRP/BTC"):
            return -0.10 * trade.leverage
        elif pair in ("LTC/BTC"):
            return -0.05 * trade.leverage
        return -0.15 * trade.leverage
```
#### 正のオフセットを持つトレーリング ストップロス

利益が 4% を超えるまでは最初のストップロスを使用し、その後は現在の利益の 50% (最小 2.5%、最大 5%) のトレーリング ストップロスを使用します。

ストップロスは増加のみ可能であり、現在のストップロスよりも低い値は無視されることに注意してください。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        if current_profit < 0.04:
            return None # return None to keep using the initial stoploss

        # After reaching the desired offset, allow the stoploss to trail by half the profit
        desired_stoploss = current_profit / 2

        # Use a minimum of 2.5% and a maximum of 5%
        return max(min(desired_stoploss, 0.05), 0.025) * trade.leverage
```
#### ステップストップロス

この例では、現在の価格を継続的に追跡するのではなく、現在の利益に基づいて固定のストップロス価格レベルを設定します。

* 利益が 20% に達するまでは通常のストップロスを使用します
* 利益が 20% を超えたら、ストップロスを始値の 7% に設定します。
* 利益が 25% を超えたら、ストップロスを始値より 15% 上に設定します。
* 利益が 40% を超えたら、ストップロスを始値より 25% 上に設定します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        # evaluate highest to lowest, so that highest possible stop is used
        if current_profit > 0.40:
            return stoploss_from_open(0.25, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        elif current_profit > 0.25:
            return stoploss_from_open(0.15, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        elif current_profit > 0.20:
            return stoploss_from_open(0.07, current_profit, is_short=trade.is_short, leverage=trade.leverage)

        # return maximum stoploss value, keeping current stoploss price unchanged
        return None
```
#### データフレームの例のインジケーターを使用したカスタム ストップロス

ストップロスの絶対値は、データフレームに保存されているインジケーターから取得できます。例では、価格を下回る放物線状の SAR をストップロスとして使用します。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # <...>
        dataframe["sar"] = ta.SAR(dataframe)

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Use parabolic sar as absolute stoploss price
        stoploss_price = last_candle["sar"]

        # Convert absolute price to percentage relative to current_rate
        if stoploss_price < current_rate:
            return stoploss_from_absolute(stoploss_price, current_rate, is_short=trade.is_short)

        # return maximum stoploss value, keeping current stoploss price unchanged
        return None
```
ストラテジー コールバックでのデータフレームの使用の詳細については、[データフレーム アクセス](strategy-advanced.md#dataframe-access) を参照してください。

### ストップロス計算の一般的なヘルパー

#### 始値に対するストップロス

`custom_stoploss()` から返されるストップロス値は、`current_rate` に相対的なパーセンテージを指定する必要がありますが、代わりに _entry_ 価格に相対的なストップロスを指定したい場合もあります。
`stoploss_from_open()` は、`custom_stoploss` から返されるストップロス値を計算するヘルパー関数です。このストップロス値は、エントリー ポイントを超える望ましい取引利益に相当します。

???例「カスタムストップロス関数から始値を基準としたストップロスを返す」

    始値が 100 ドルで、`current_price` が 121 ドルであるとします (`current_profit` は `0.21` になります)。  

    始値の 7% 上のストップ価格が必要な場合は、`stoploss_from_open(0.07, current_profit, False)` を呼び出すと、`0.1157024793` が返されます。  121ドル以下の11.57%は107ドルで、これは100ドル以上の7%と同じです。

    この関数はレバレッジを考慮します。つまり、10 倍のレバレッジでは、実際のストップロスは 100 ドルを超える 0.7% になります (0.7% * 10x = 7%)。
    ``` python
    # Default imports

    class AwesomeStrategy(IStrategy):

        # ... populate_* methods

        use_custom_stoploss = True

        def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                            current_rate: float, current_profit: float, after_fill: bool,
                            **kwargs) -> float | None:

            # once the profit has risen above 10%, keep the stoploss at 7% above the open price
            if current_profit > 0.10:
                return stoploss_from_open(0.07, current_profit, is_short=trade.is_short, leverage=trade.leverage)

            return 1

    ```
完全な例は、ドキュメントの [カスタム ストップロス](strategy-callbacks.md#custom-stoploss) セクションにあります。

!!! Note
    「stoploss_from_open()」に無効な入力を指定すると、「CustomStoploss 関数が有効なストップロスを返しませんでした」という警告が生成される場合があります。
    これは、「current_profit」パラメータが指定された「open_relative_stop」を下回っている場合に発生する可能性があります。取引を終了するときにこのような状況が発生する可能性があります
    `confirm_trade_exit()` メソッドによってブロックされます。警告は、「exit_reason」をチェックしてストップロスの売りを決してブロックしないことで解決できます。
    「confirm_trade_exit()」、または「return stoploss_from_open(...) または 1」イディオムを使用して、次の場合にストップロスを変更しないように要求します。
    `current_profit < open_relative_stop`。

#### 絶対価格からのストップロス率

`custom_stoploss()` から返されるストップロス値は、常に `current_rate` を基準としたパーセンテージを指定します。指定された絶対価格レベルでストップロスを設定するには、`stop_rate` を使用して、`current_rate` に対して相対的に何パーセントが始値から指定された場合と同じ結果が得られるかを計算する必要があります。

ヘルパー関数 `stoploss_from_absolute()` を使用すると、絶対価格から `custom_stoploss()` から返される現在の価格の相対ストップに変換できます。

???例「カスタムストップロス関数からの絶対価格を使用してストップロスを返す」

    現在価格より 2xATR 下のストップ価格を追跡したい場合は、`stoploss_from_absolute(current_rate + (side *candle["atr"] * 2), current_rate=current_rate, is_short=trade.is_short, leverage=trade.leverage)` を呼び出すことができます。
    先物の場合、[`custom_stoploss`](strategy-callbacks.md#custom-stoploss) コールバックは相対的な価格の動きではなく、["risk for this trade"](stoploss.md#stoploss-and-leverage) を返すため、レバレッジを調整するだけでなく、方向 (上または下) を調整する必要があります。
    ``` python
    # Default imports

    class AwesomeStrategy(IStrategy):

        use_custom_stoploss = True

        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
            return dataframe

        def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                            current_rate: float, current_profit: float, after_fill: bool,
                            **kwargs) -> float | None:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
            candle = dataframe.iloc[-1].squeeze()
            side = 1 if trade.is_short else -1
            return stoploss_from_absolute(current_rate + (side * candle["atr"] * 2), 
                                          current_rate=current_rate, 
                                          is_short=trade.is_short,
                                          leverage=trade.leverage)

    ```
---

## カスタム ROI

取引が終了するまで、反復ごと (約 5 秒ごと) にオープン取引が呼び出されます。

カスタム ROI メソッドの使用は、戦略オブジェクトで `use_custom_roi=True` を設定することによって有効にする必要があります。

この方法では、取引を終了するためのカスタムの最小 ROI しきい値を比率で表して定義できます (例: 5% の利益の場合は「0.05」)。 「minimal_roi」と「custom_roi」の両方が定義されている場合、2 つのしきい値のうち低い方が終了をトリガーします。たとえば、`minimal_roi` が `{"0": 0.10}` (0 分で 10%) に設定され、`custom_roi` が `0.05` を返す場合、利益が 5% に達すると取引は終了します。また、`custom_roi` が `0.10` を返し、`minimal_roi` が `{"0": 0.05}` (0 分で 5%) に設定されている場合、利益が 5% に達したときに取引は終了します。

このメソッドは、新しい ROI しきい値を比率として表す浮動小数点数を返すか、「minimal_roi」ロジックにフォールバックするには「None」を返す必要があります。 `NaN` または `inf` 値を返すと無効とみなされ、`None` として扱われるため、ボットは `minimal_roi` 構成を使用します。

### カスタム ROI の例

次の例は、「custom_roi」関数を使用してさまざまな ROI ロジックを実装する方法を示しています。

#### 側面ごとのカスタム ROI

「側」に応じて異なる ROI しきい値を使用します。この例では、長いエントリの場合は 5%、短いエントリの場合は 2% です。
```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:
        """
        Custom ROI logic, returns a new minimum ROI threshold (as a ratio, e.g., 0.05 for +5%).
        Only called when use_custom_roi is set to True.

        If used at the same time as minimal_roi, an exit will be triggered when the lower
        threshold is reached. Example: If minimal_roi = {"0": 0.01} and custom_roi returns 0.05,
        an exit will be triggered if profit reaches 5%.

        :param pair: Pair that's currently analyzed.
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime.
        :param trade_duration: Current trade duration in minutes.
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the current trade.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: New ROI value as a ratio, or None to fall back to minimal_roi logic.
        """
        return 0.05 if side == "long" else 0.02
```
#### ペアごとのカスタム ROI

「ペア」に応じて異なる ROI しきい値を使用します。
```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        stake = trade.stake_currency
        roi_map = {
            f"BTC/{stake}": 0.02, # 2% for BTC
            f"ETH/{stake}": 0.03, # 3% for ETH
            f"XRP/{stake}": 0.04, # 4% for XRP
        }

        return roi_map.get(pair, 0.01) # 1% for any other pair
```
#### エントリ タグごとのカスタム ROI

購入シグナルで提供される「entry_tag」に応じて、異なる ROI しきい値を使用します。
```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        roi_by_tag = {
            "breakout": 0.08,       # 8% if tag is "breakout"
            "rsi_overbought": 0.05, # 5% if tag is "rsi_overbought"
            "mean_reversion": 0.03, # 3% if tag is "mean_reversion"
        }

        return roi_by_tag.get(entry_tag, 0.01)  # 1% if tag is unknown
```
#### ATR に基づくカスタム ROI

ROI 値は、データフレームに格納されているインジケーターから取得できます。この例では、ATR 比を ROI として使用します。
``` python
# Default imports
# <...>
import talib.abstract as ta

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # <...>
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=10)

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        atr_ratio = last_candle["atr"] / last_candle["close"]

        return atr_ratio # Returns the ATR value as ratio
```
---

## カスタムオーダーの価格ルール

デフォルトでは、freqtrade はオーダーブックを使用して注文価格を自動的に設定します ([関連ドキュメント](configuration.md#prices-used-for-orders))。戦略に基づいてカスタム注文価格を作成するオプションもあります。

この機能を使用するには、戦略ファイル内に「custom_entry_price()」関数を作成してエントリー価格をカスタマイズし、エグジットの「custom_exit_price()」関数を作成します。

これらの各メソッドは、取引所で注文を行う直前に呼び出されます。

!!! Note
    カスタム価格設定関数が None または無効な値を返した場合、価格は通常の価格設定設定に基づく `proposit_rate` に戻ります。

!!! Note
    Custom_entry_price を使用すると、取引に関連付けられた最初のエントリー注文が作成されるとすぐに取引オブジェクトが利用可能になります。最初のエントリーでは、「trade」パラメーター値は「None」になります。

### カスタム注文のエントリー価格とエグジット価格の例
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def custom_entry_price(self, pair: str, trade: Trade | None, current_time: datetime, proposed_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:

        dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                timeframe=self.timeframe)
        new_entryprice = dataframe["bollinger_10_lowerband"].iat[-1]

        return new_entryprice

    def custom_exit_price(self, pair: str, trade: Trade,
                          current_time: datetime, proposed_rate: float,
                          current_profit: float, exit_tag: str | None, **kwargs) -> float:

        dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                timeframe=self.timeframe)
        new_exitprice = dataframe["bollinger_10_upperband"].iat[-1]

        return new_exitprice

```
!!! Warning
    エントリー価格とエグジット価格の変更は、指値注文の場合にのみ機能します。選択した価格によっては、多数の注文が約定されない可能性があります。デフォルトでは、現在の価格とカスタム価格の間の最大許容距離は 2% ですが、この値は設定で `custom_price_max_ distance_ratio` パラメータを使用して変更できます。
    **例**:
    new_entryprice が 97、projected_rate が 100、`custom_price_max_ distance_ratio` が 2% に設定されている場合、保持される有効なカスタム エントリ価格は 98 となり、現在の (提案された) レートより 2% 低くなります。

!!! Warning "バックテスト"
    カスタム価格はバックテスト (2021.12 以降) でサポートされており、価格がローソク足の安値/高値範囲内にある場合、注文は約定します。
    すぐに約定しない注文は定期的なタイムアウト処理の対象となり、これは (詳細) キャンドルごとに 1 回発生します。
    `custom_exit_price()` は、タイプ exit_signal、カスタム exit、および部分的 exit の売りの場合にのみ呼び出されます。他のすべてのエグジット タイプでは、通常のバックテスト価格が使用されます。

## カスタムオーダーのタイムアウトルール

シンプルな時間ベースのオーダータイムアウトは、戦略を介して、または「unfilledtimeout」セクションの設定で設定できます。

ただし、freqtrade は両方の注文タイプにカスタム コールバックも提供しており、注文がタイムアウトしたかどうかをカスタム基準に基づいて決定できます。

!!! Note
    バックテストでは、価格がローソク足の安値/高値範囲内にある場合に注文が約定されます。
    以下のコールバックは、すぐに約定しない注文 (カスタム価格設定を使用する) の (詳細) キャンドルごとに 1 回呼び出されます。

### カスタムオーダーのタイムアウトの例

注文が約定されるかキャンセルされるまで、開いている注文ごとに呼び出されます。
「check_entry_timeout()」は取引エントリーの場合に呼び出され、「check_exit_timeout()」は取引終了注文の場合に呼び出されます。

資産の価格に応じて異なる未フィルタイムアウトを適用する簡単な例を以下に示します。
高価な資産には厳しいタイムアウトを適用する一方で、安価なコインのフィルにはより多くの時間を与えます。

この関数は、`True` (注文をキャンセル) または `False` (注文を維持) を返す必要があります。
``` python
    # Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    # Set unfilledtimeout to 25 hours, since the maximum timeout from below is 24 hours.
    unfilledtimeout = {
        "entry": 60 * 25,
        "exit": 60 * 25
    }

    def check_entry_timeout(self, pair: str, trade: Trade, order: Order,
                            current_time: datetime, **kwargs) -> bool:
        if trade.open_rate > 100 and trade.open_date_utc < current_time - timedelta(minutes=5):
            return True
        elif trade.open_rate > 10 and trade.open_date_utc < current_time - timedelta(minutes=3):
            return True
        elif trade.open_rate < 1 and trade.open_date_utc < current_time - timedelta(hours=24):
           return True
        return False


    def check_exit_timeout(self, pair: str, trade: Trade, order: Order,
                           current_time: datetime, **kwargs) -> bool:
        if trade.open_rate > 100 and trade.open_date_utc < current_time - timedelta(minutes=5):
            return True
        elif trade.open_rate > 10 and trade.open_date_utc < current_time - timedelta(minutes=3):
            return True
        elif trade.open_rate < 1 and trade.open_date_utc < current_time - timedelta(hours=24):
           return True
        return False
```
!!! Note
    上の例では、「unfilledtimeout」を 24 時間より大きい値に設定する必要があります。それ以外の場合は、そのタイプのタイムアウトが最初に適用されます。

### カスタムオーダーのタイムアウト例 (追加データを使用)
``` python
    # Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    # Set unfilledtimeout to 25 hours, since the maximum timeout from below is 24 hours.
    unfilledtimeout = {
        "entry": 60 * 25,
        "exit": 60 * 25
    }

    def check_entry_timeout(self, pair: str, trade: Trade, order: Order,
                            current_time: datetime, **kwargs) -> bool:
        ob = self.dp.orderbook(pair, 1)
        current_price = ob["bids"][0][0]
        # Cancel buy order if price is more than 2% above the order.
        if current_price > order.price * 1.02:
            return True
        return False


    def check_exit_timeout(self, pair: str, trade: Trade, order: Order,
                           current_time: datetime, **kwargs) -> bool:
        ob = self.dp.orderbook(pair, 1)
        current_price = ob["asks"][0][0]
        # Cancel sell order if price is more than 2% below the order.
        if current_price < order.price * 0.98:
            return True
        return False
```
---

## ボットの注文確認

トレードのエントリー/エグジットを確認します。
これは、注文が行われる前に呼び出される最後のメソッドです。

### トレードエントリー（買い注文）の確認

`confirm_trade_entry()` を使用すると、取引エントリーを最新の 1 秒で中止することができます (おそらく価格が期待したものではないため)。
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: str | None,
                            side: str, **kwargs) -> bool:
        """
        Called right before placing a entry order.
        Timing for this function is critical, so avoid doing heavy computations or
        network requests in this method.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/

        When not implemented by a strategy, returns True (always confirming).

        :param pair: Pair that's about to be bought/shorted.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in target (base) currency that's going to be traded.
        :param rate: Rate that's going to be used when using limit orders 
                     or current rate for market orders.
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param current_time: datetime object, containing the current datetime
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: "long" or "short" - indicating the direction of the proposed trade
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return bool: When True is returned, then the buy-order is placed on the exchange.
            False aborts the process
        """
        return True

```
### 取引終了（売り注文）の確認

`confirm_trade_exit()` を使用すると、取引終了 (売り) を最新の 1 秒で中止できます (おそらく価格が期待したものではないため)。

異なる終了理由が適用される場合、`confirm_trade_exit()` は同じ取引の 1 回の反復内で複数回呼び出される可能性があります。
終了理由 (該当する場合) は次の順序になります。

* `exit_signal` / `custom_exit`
* `ストップロス`
*「ロイ」
* `trailing_stop_loss`
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
        """
        Called right before placing a regular exit order.
        Timing for this function is critical, so avoid doing heavy computations or
        network requests in this method.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/

        When not implemented by a strategy, returns True (always confirming).

        :param pair: Pair for trade that's about to be exited.
        :param trade: trade object.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in base currency.
        :param rate: Rate that's going to be used when using limit orders
                     or current rate for market orders.
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param exit_reason: Exit reason.
            Can be any of ["roi", "stop_loss", "stoploss_on_exchange", "trailing_stop_loss",
                           "exit_signal", "force_exit", "emergency_exit"]
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return bool: When True, then the exit-order is placed on the exchange.
            False aborts the process
        """
        if exit_reason == "force_exit" and trade.calc_profit_ratio(rate) < 0:
            # Reject force-sells with negative profit
            # This is just a sample, please adjust to your needs
            # (this does not necessarily make sense, assuming you know when you're force-selling)
            return False
        return True

```
!!! Warning
    `confirm_trade_exit()` はストップロスの出口を防ぐことができ、これはストップロスの出口を無視するため、重大な損失を引き起こします。
    `confirm_trade_exit()` は清算の場合には呼び出されません。清算は取引所によって強制されるため、拒否することはできません。

## トレードポジションを調整する

`position_adjustment_enable` 戦略プロパティは、戦略での `adjust_trade_position()` コールバックの使用を有効にします。
パフォーマンス上の理由から、デフォルトでは無効になっており、有効になっている場合、freqtrade は起動時に警告メッセージを表示します。
「adjust_trade_position()」を使用すると、DCA (ドルコスト平均法) でリスクを管理したり、ポジションを増減したりするなど、追加の注文を実行できます。

追加の注文にも追加料金がかかり、それらの注文は「max_open_trades」にはカウントされません。

このコールバックは、約定を待っているオープン注文 (買いまたは売り) がある場合にも呼び出されます。金額、価格、または方向が異なる場合は、既存のオープン注文をキャンセルして新しい注文を出します。また、部分的に約定された注文はキャンセルされ、コールバックによって返された新しい金額に置き換えられます。

「adjust_trade_position()」は取引中に非常に頻繁に呼び出されるため、実装のパフォーマンスを可能な限り維持する必要があります。

ポジション調整は常に取引の方向に適用されるため、ロングトレードかショートトレードかに関係なく、正の値は常にポジションを増加させます（負の値はポジションを減少させます）。
調整オーダーは、2 要素のタプルを返すことによってタグを割り当てることができます。最初の要素は調整額、2 番目の要素はタグです (例: `return 250, "increase_favorable_conditions"`)。

レバレッジの変更は不可能であり、返される賭け金額はレバレッジを適用する前の額とみなされます。

現在ポジションに割り当てられている合計ステークは「trade.stake_amount」に保持されます。したがって、`trade.stake_amount` は、`adjust_trade_position()` を通じて行われる追加エントリーおよび部分的なエグジットのたびに常に更新されます。

!!! Danger "ルーズなロジック"
    ドライ実行およびライブ実行では、この関数は「throttle_process_secs」ごとに呼び出されます (デフォルトは 5 秒)。緩いロジックの場合 (例: 最後のローソク足の RSI が 30 未満の場合にポジションを増やす)、ボットは資金がなくなるか、「max_position_adjustment」制限に達するか、RSI が 30 を超える新しいローソク足が到着するまで、5 秒ごとに追加の再エントリーを行います。

    部分的な終了でも同じことが発生する可能性があります。  
    したがって、厳密なロジックを用意し、最後に約定した注文や注文がすでにオープンしているかどうかを確認するようにしてください。

!!! Warning "多くの位置調整によるパフォーマンス"
ポジション調整は戦略の成果を上げるための良いアプローチですが、この機能を広範囲に使用すると欠点が生じる可能性もあります。  
    各注文は取引期間中取引オブジェクトに添付されるため、メモリ使用量が増加します。
    したがって、長期間にわたる取引や数十秒、さらには数百秒にわたるポジション調整は推奨されず、パフォーマンスに影響を与えないように定期的に取引を終了する必要があります。

!!! Warning "バックテスト"
    バックテスト中、このコールバックは「timeframe」または「timeframe_detail」のキャンドルごとに呼び出されるため、実行時のパフォーマンスに影響します。
    また、バックテストではローソク当たり 1 回しか取引を調整できないのに対し、ライブではローソク当たり複数回取引を調整できるため、ライブとバックテストの間で結果が異なる可能性もあります。

### 位置を増やす

この戦略は、追加のエントリー注文を作成する必要がある場合 (ポジションが増加する -> ロング取引の場合は買い注文、ショート取引の場合は売り注文)、「min_stake」と「max_stake」の間で正の **stake_amount** (ステーク通貨で) を返すことが期待されます。

ウォレットに十分な資金がない場合 (戻り値が `max_stake` を超えている場合)、シグナルは無視されます。
`max_entry_position_adjustment` プロパティは、ボットが実行できる (最初のエントリー注文に加えて) 取引ごとの追加エントリーの数を制限するために使用されます。デフォルトでは、値は -1 で、ボットの調整エントリ数に制限がないことを意味します。

`max_entry_position_adjustment` で設定した追加エントリの最大量に達すると、追加のエントリは無視されますが、それでも部分的な終了を探してコールバックが呼び出されます。

!!! Note "ステークサイズについて"
    固定ステークサイズを使用すると、ポジション調整なしと同様に、最初の注文に使用される金額になります。
    DCA で追加の注文を購入したい場合は、そのための十分な資金をウォレットに残してください。
    DCA 注文で「無制限」のステーク量を使用するには、最初の注文にすべての資金が割り当てられることを避けるために、「custom_stake_amount()」コールバックも実装する必要があります。

### 位置を下げる

この戦略は、部分的なエグジットに対して負の stake_amount (ステーク通貨で) を返すと予想されます。
その時点で完全に所有されている株式を返す (`-trade.stake_amount`) と、完全な終了になります。  
上記を超える値を返すと (残りの stake_amount が負になるため)、ボットはシグナルを無視します。
部分的エグジットの場合、部分的エグジット注文のコインの量を計算するために使用される式が「部分的にエグジットされる金額 = negative_stake_amount * trade.amount / trade.stake_amount」であることを知っておくことが重要です。ここで、「negative_stake_amount」は「adjust_trade_position」関数から返される値です。式に見られるように、この式ではポジションの現在の損益は考慮されません。価格変動の影響をまったく受けない「trade.amount」と「trade.stake_amount」のみを考慮します。

たとえば、オープンレート 50 で 2 SHITCOIN/USDT を購入するとします。これは、取引の賭け金が 100 USDT であることを意味します。価格が 200 に上がったので、その半分を売りたいとします。その場合、「trade.stake_amount」の -50% (0.5 * 100 USDT) (-50 に相当) を返さなければなりません。ボットは販売に必要な金額を計算します。これは「50 * 2 / 100」で、1 SHITCOIN/USDT に相当します。 -200 (2 * 200 の 50%) を返すと、「trade.stake_amount」は 100 USDT のみですが、200 USDT の販売を要求しているため、ボットはそれを無視します。これは、4 SHITCOIN/USDT の販売を要求していることを意味します。

上の例に戻ると、現在のレートが 200 であるため、取引の現在の USDT 値は 400 USDT になります。 100 USDT を部分的に売却して初期投資を取り除き、価格が上昇し続けることを期待して取引での利益を残しておきたいとします。その場合は、別のアプローチを行う必要があります。まず、販売に必要な正確な金額を計算する必要があります。この場合、現在のレートに基づいて 100 USDT 相当を売却したいため、部分的に売却するために必要な正確な金額は「100 * 2 / 400」で、これは 0.5 SHITCOIN/USDT に相当します。売りたい正確な金額 (0.5) がわかったので、`adjust_trade_position` 関数で返す必要がある値は、`-部分的に決済される金額 * trade.stake_amount / trade.amount` となり、-25 に等しくなります。ボットは 0.5 SHITCOIN/USDT を販売し、1.5 を取引に維持します。部分的な出口からは 100 USDT を受け取ります。

!!! Warning "ストップロスの計算"
    ストップロスは、平均価格ではなく、最初の始値から計算されます。
    通常のストップロス ルールが引き続き適用されます (下に移動することはできません)。

    「/stopentry」コマンドはボットによる新しい取引の入力を停止しますが、ポジション調整機能は既存の取引で新しい注文を買い続けます。
``` python
# Default imports

class DigDeeperStrategy(IStrategy):

    position_adjustment_enable = True

    # Attempts to handle large drops with DCA. High stoploss is required.
    stoploss = -0.30

    # ... populate_* methods

    # Example specific variables
    max_entry_position_adjustment = 3
    # This number is explained a bit further down
    max_dca_multiplier = 5.5

    # This is called when placing the initial order (opening trade)
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            leverage: float, entry_tag: str | None, side: str,
                            **kwargs) -> float:

        # We need to leave most of the funds for possible further DCA orders
        # This also applies to fixed stakes
        return proposed_stake / self.max_dca_multiplier

    def adjust_trade_position(self, trade: Trade, current_time: datetime,
                              current_rate: float, current_profit: float,
                              min_stake: float | None, max_stake: float,
                              current_entry_rate: float, current_exit_rate: float,
                              current_entry_profit: float, current_exit_profit: float,
                              **kwargs
                              ) -> float | None | tuple[float | None, str | None]:
        """
        Custom trade adjustment logic, returning the stake amount that a trade should be
        increased or decreased.
        This means extra entry or exit orders with additional fees.
        Only called when `position_adjustment_enable` is set to True.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/

        When not implemented by a strategy, returns None

        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Current entry rate (same as current_entry_profit)
        :param current_profit: Current profit (as ratio), calculated based on current_rate 
                               (same as current_entry_profit).
        :param min_stake: Minimal stake size allowed by exchange (for both entries and exits)
        :param max_stake: Maximum stake allowed (either through balance, or by exchange limits).
        :param current_entry_rate: Current rate using entry pricing.
        :param current_exit_rate: Current rate using exit pricing.
        :param current_entry_profit: Current profit using entry pricing.
        :param current_exit_profit: Current profit using exit pricing.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: Stake amount to adjust your trade,
                       Positive values to increase position, Negative values to decrease position.
                       Return None for no action.
                       Optionally, return a tuple with a 2nd element with an order reason
        """
        if trade.has_open_orders:
            # Only act if no orders are open
            return

        if current_profit > 0.05 and trade.nr_of_successful_exits == 0:
            # Take half of the profit at +5%
            return -(trade.stake_amount / 2), "half_profit_5%"

        if current_profit > -0.05:
            return None

        # Obtain pair dataframe (just to show how to access it)
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        # Only buy when not actively falling price.
        last_candle = dataframe.iloc[-1].squeeze()
        previous_candle = dataframe.iloc[-2].squeeze()
        if last_candle["close"] < previous_candle["close"]:
            return None

        filled_entries = trade.select_filled_orders(trade.entry_side)
        count_of_entries = trade.nr_of_successful_entries
        # Allow up to 3 additional increasingly larger buys (4 in total)
        # Initial buy is 1x
        # If that falls to -5% profit, we buy 1.25x more, average profit should increase to roughly -2.2%
        # If that falls down to -5% again, we buy 1.5x more
        # If that falls once again down to -5%, we buy 1.75x more
        # Total stake for this trade would be 1 + 1.25 + 1.5 + 1.75 = 5.5x of the initial allowed stake.
        # That is why max_dca_multiplier is 5.5
        # Hope you have a deep wallet!
        try:
            # This returns first order stake size
            stake_amount = filled_entries[0].stake_amount_filled
            # This then calculates current safety order size
            stake_amount = stake_amount * (1 + (count_of_entries * 0.25))
            return stake_amount, "1/3rd_increase"
        except Exception as exception:
            return None

        return None

```
### 位置調整の計算

※エントリー率は加重平均により算出しております。
※退場は平均入場率には影響しません。
* 部分エグジット相対利益は、この時点の平均エントリー価格に対する相対的なものです。
※最終エグジット相対利益は総投下資本に基づいて計算されます。 (以下の例を参照してください)

???例「計算例」
    *この例では、簡単にするために手数料が 0 であり、架空のコインのロング ポジションがあると仮定しています。*  
    
    * 100@8\$ を購入 
    * 100@9\$ を購入 -> 平均価格: 8.5\$
    * 100@10\$ を販売 -> 平均価格: 8.5\$、実現利益 150\$、17.65%
    * 150@11\$ を購入 -> 平均価格: 10\$、実現利益 150\$、17.65%
    * 100@12\$ を販売 -> 平均価格: 10\$、合計実現利益 350\$、20%
    * 150@14\$ を販売 -> 平均価格: 10\$、合計実現利益 950\$、40% <- *これが最後の「終了」メッセージになります*

    この取引の合計利益は、投資 $3350 に対して $950 (`100@8$ + 100@9$ + 150@11$`) でした。したがって、最終的な相対利益は 28.35% (`950 / 3350`) になります。

## 注文価格を調整する

「adjust_order_price()」コールバックは、戦略開発者が新しいローソク足の到着時に指値注文を更新/交換するために使用できます。  
このコールバックは、注文が現在のローソク内で (再) 配置されていない限り、反復ごとに 1 回呼び出されます。つまり、各注文の最大 (再) 配置はローソクごとに 1 回に制限されます。
これは、最初の注文が行われた後、最初のコールが次のローソク足の開始時に行われることも意味します。

`custom_entry_price()`/`custom_exit_price()` は依然として、シグナル時の最初の指値注文価格目標を決定するものであることに注意してください。

「None」を返すことで、このコールバックから注文をキャンセルできます。

`current_order_rate` を返すと、取引所の注文は「現状のまま」維持されます。
他の価格を返品すると、既存の注文がキャンセルされ、新しい注文に置き換えられます。

元の注文のキャンセルが失敗した場合、注文は交換されませんが、注文は交換時にキャンセルされる可能性が高くなります。最初のエントリーでこれが発生すると注文は削除されますが、ポジション調整注文では取引サイズはそのまま残ります。  
注文が部分的に約定された場合、注文は交換されません。ただし、必要に応じて、[`adjust_trade_position()`](#adjust-trade-position) を使用して、取引サイズを予想されるポジション サイズに調整することができます。

!!! Warning "通常のタイムアウト"
    エントリの「unfilledtimeout」メカニズム (および「check_entry_timeout()」/「check_exit_timeout()」) は、このコールバックよりも優先されます。
    上記のメソッドでキャンセルされた注文では、このコールバックは呼び出されません。期待どおりにタイムアウト値を更新してください。
```python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def adjust_order_price(
        self,
        trade: Trade,
        order: Order | None,
        pair: str,
        current_time: datetime,
        proposed_rate: float,
        current_order_rate: float,
        entry_tag: str | None,
        side: str,
        is_entry: bool,
        **kwargs,
    ) -> float | None:
        """
        Exit and entry order price re-adjustment logic, returning the user desired limit price.
        This only executes when a order was already placed, still open (unfilled fully or partially)
        and not timed out on subsequent candles after entry trigger.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-callbacks/

        When not implemented by a strategy, returns current_order_rate as default.
        If current_order_rate is returned then the existing order is maintained.
        If None is returned then order gets canceled but not replaced by a new one.

        :param pair: Pair that's currently analyzed
        :param trade: Trade object.
        :param order: Order object
        :param current_time: datetime object, containing the current datetime
        :param proposed_rate: Rate, calculated based on pricing settings in entry_pricing.
        :param current_order_rate: Rate of the existing order in place.
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :param is_entry: True if the order is an entry order, False if it's an exit order.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float or None: New entry price value if provided
        """

        # Limit entry orders to use and follow SMA200 as price target for the first 10 minutes since entry trigger for BTC/USDT pair.
        if (
            is_entry
            and pair == "BTC/USDT" 
            and entry_tag == "long_sma200" 
            and side == "long" 
            and (current_time - timedelta(minutes=10)) <= trade.open_date_utc
        ):
            # just cancel the order if it has been filled more than half of the amount
            if order.filled > order.remaining:
                return None
            else:
                dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
                current_candle = dataframe.iloc[-1].squeeze()
                # desired price
                return current_candle["sma_200"]
        # default: maintain existing order
        return current_order_rate
```
!!! danger "「adjust_*_price()」との非互換性"
    `adjust_order_price()` と `adjust_entry_price()`/`adjust_exit_price()` の両方が実装されている場合は、`adjust_order_price()` のみが使用されます。
    エントリー/エグジット価格を調整する必要がある場合は、`adjust_order_price()` でロジックを実装するか、分割された `adjust_entry_price()` / `adjust_exit_price()` コールバックを使用できますが、両方を使用することはできません。
    これらの混合はサポートされていないため、ボットの起動時にエラーが発生します。

### エントリー価格を調整する

「adjust_entry_price()」コールバックは、戦略開発者が到着時にエントリー指値注文を更新/置換するために使用できます。
これは `adjust_order_price()` のサブセットであり、エントリー注文の場合にのみ呼び出されます。
残りの動作はすべて「adjust_order_price()」と同じです。

取引開始日 (`trade.open_date_utc`) は、最初の注文の時点のままになります。
これを必ず認識してください。最終的には、これを考慮して他のコールバックのロジックを調整し、代わりに最初に約定した注文の日付を使用してください。

### エグジット価格を調整する

「adjust_exit_price()」コールバックは、戦略開発者が到着時に決済指値注文を更新/置換するために使用できます。
これは `adjust_order_price()` のサブセットであり、決済注文の場合にのみ呼び出されます。
残りの動作はすべて「adjust_order_price()」と同じです。

## コールバックを活用する

レバレッジが許可されている市場で取引する場合、このメソッドは希望のレバレッジを返す必要があります (デフォルトは 1 -> レバレッジなし)。

資本が 500USDT であると仮定すると、レバレッジ = 3 で取引すると、500 x 3 = 1500 USDT のポジションが得られます。

「max_leverage」を超える値は「max_leverage」に調整されます。
レバレッジをサポートしていない市場/取引所の場合、この方法は無視されます。
``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str | None, side: str,
                 **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: "long" or "short" - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return 1.0
```
すべての利益計算にはレバレッジが含まれます。ストップロス/ROI にはレバレッジも計算に含まれます。
10 倍のレバレッジで 10% のストップロスを定義すると、1% の下落でストップロスがトリガーされます。

## 注文完了コールバック

`order_filled()` コールバックは、注文が約定された後に現在の取引状態に基づいて特定のアクションを実行するために使用できます。
これは注文タイプ (エントリー、エグジット、ストップロス、ポジション調整) に関係なく呼び出されます。

戦略が取引エントリー時にローソクの高値を保存する必要があると仮定すると、次の例に示すように、このコールバックを使用してこれが可能です。
``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def order_filled(self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs) -> None:
        """
        Called right after an order fills. 
        Will be called for all order types (entry, exit, stoploss, position adjustment).
        :param pair: Pair for trade
        :param trade: trade object.
        :param order: Order object.
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        # Obtain pair dataframe (just to show how to access it)
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if (trade.nr_of_successful_entries == 1) and (order.ft_order_side == trade.entry_side):
            trade.set_custom_data(key="entry_candle_high", value=last_candle["high"])

        return None

```
!!! Tip "データの保存について詳しく見る"
    データの保存について詳しくは、[カスタム取引データの保存](strategy-advanced.md#storing-information-persistent) セクションをご覧ください。
    これは高度な使用法とみなされ、慎重に使用する必要があることに注意してください。

## プロット注釈コールバック

プロット注釈コールバックは、freqUI がグラフを表示するデータを要求するたびに呼び出されます。
このコールバックは取引サイクルのコンテキストでは意味がなく、チャート作成の目的でのみ使用されます。

このストラテジーは、チャートに表示される `AnnotationType` オブジェクトのリストを返すことができます。
返されたコンテンツに応じて、グラフには水平領域、垂直領域、ボックス、または線を表示できます。

### 注釈の種類

現在、「area」と「line」の 2 種類の注釈がサポートされています。

＃＃＃＃ エリア
``` json
{
    "type": "area", // Type of the annotation, currently only "area" is supported
    "start": "2024-01-01 15:00:00", // Start date of the area
    "end": "2024-01-01 16:00:00",  // End date of the area
    "y_start": 94000.2,  // Price / y axis value
    "y_end": 98000, // Price / y axis value
    "color": "",
    "z_level": 5, // z-level, higher values are drawn on top of lower values. Positions relative to the Chart elements need to be set in freqUI.
    "label": "some label"
}
```
＃＃＃＃ ライン
``` json
{
    "type": "line", // Type of the annotation, currently only "line" is supported
    "start": "2024-01-01 15:00:00", // Start date of the line
    "end": "2024-01-01 16:00:00",  // End date of the line
    "y_start": 94000.2,  // Price / y axis value
    "y_end": 98000, // Price / y axis value
    "color": "",
    "z_level": 5, // z-level, higher values are drawn on top of lower values. Positions relative to the Chart elements need to be set in freqUI.
    "label": "some label",
    "width": 2, // Optional, line width in pixels. Defaults to 1
    "line_style": "dashed", // Optional, can be "solid", "dashed" or "dotted". Defaults to "solid"

}
```
以下の例では、チャートの 8 時間目と 15 時間目のエリアを灰色でマークし、市場の開始時間と終了時間を強調表示します。
これは明らかに非常に基本的な例です。
``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def plot_annotations(
        self, pair: str, start_date: datetime, end_date: datetime, dataframe: DataFrame, **kwargs
    ) -> list[AnnotationType]:
        """
        Retrieve area annotations for a chart.
        Must be returned as array, with type, label, color, start, end, y_start, y_end.
        All settings except for type are optional - though it usually makes sense to include either
        "start and end" or "y_start and y_end" for either horizontal or vertical plots
        (or all 4 for boxes).
        :param pair: Pair that's currently analyzed
        :param start_date: Start date of the chart data being requested
        :param end_date: End date of the chart data being requested
        :param dataframe: DataFrame with the analyzed data for the chart
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return: List of AnnotationType objects
        """
        annotations = []
        while start_dt < end_date:
            start_dt += timedelta(hours=1)
            if start_dt.hour in (8, 15):
                annotations.append(
                    {
                        "type": "area",
                        "label": "Trade open and close hours",
                        "start": start_dt,
                        "end": start_dt + timedelta(hours=1),
                        # Omitting y_start and y_end will result in a vertical area spanning the whole height of the main Chart
                        "color": "rgba(133, 133, 133, 0.4)",
                    }
                )

        return annotations

```
エントリは検証され、予期されたスキーマに対応しない場合は UI に渡されず、一致しない場合はエラーがログに記録されます。

!!! Warning "多くの注釈"
    注釈を使用しすぎると、特に大量の履歴データをプロットする場合に UI がハングする可能性があります。
    注釈機能は注意して使用してください。

### プロット注釈の例

![FreqUI - プロット注釈](assets/freqUI-chart-annotations-dark.png#only-dark)
![FreqUI - プロット注釈](assets/freqUI-chart-annotations-light.png#only-light)

???情報「上記のプロットに使用されたコード」
    これはコード例であり、そのように扱う必要があります。
    ``` python
    # Default imports

    class AwesomeStrategy(IStrategy):
        def plot_annotations(
            self, pair: str, start_date: datetime, end_date: datetime, dataframe: DataFrame, **kwargs
        ) -> list[AnnotationType]:
            annotations = []
            while start_dt < end_date:
                start_dt += timedelta(hours=1)
                if (start_dt.hour % 4) == 0:
                    annotations.append(
                        {
                            "type": "area",
                            "label": "4h",
                            "start": start_dt,
                            "end": start_dt + timedelta(hours=1),
                            "color": "rgba(133, 133, 133, 0.4)",
                        }
                    )
                elif (start_dt.hour % 2) == 0:
                price = dataframe.loc[dataframe["date"] == start_dt, ["close"]].mean()
                    annotations.append(
                        {
                            "type": "area",
                            "label": "2h",
                            "start": start_dt,
                            "end": start_dt + timedelta(hours=1),
                            "y_end": price * 1.01,
                            "y_start": price * 0.99,
                            "color": "rgba(0, 255, 0, 0.4)",
                            "z_level": 5,
                        }
                    )

            return annotations

    ```
