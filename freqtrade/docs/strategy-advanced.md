# 高度な戦略

このページでは、戦略に使用できるいくつかの高度な概念について説明します。
始めたばかりの場合は、まず [Freqtrade の基本](bot-basics.md) と [戦略のカスタマイズ](strategy-customization.md) で説明されている方法に慣れてください。

ここで説明するメソッドの呼び出しシーケンスは、[ボット実行ロジック](bot-basics.md#bot-execution-logic) で説明されています。これらのドキュメントは、カスタマイズのニーズにどの方法が最適かを判断するのにも役立ちます。

!!! Note
    コールバック メソッドは、戦略で使用される場合にのみ実装する必要があります。

!!! Tip
    「freqtrade new-strategy --strategy MyAwesomeStrategy --template Advanced」を実行して、利用可能なすべてのコールバック メソッドを含む戦略テンプレートから始めます。

## 情報の保存 (永続的)

Freqtrade を使用すると、特定の取引に関連付けられたユーザーのカスタム情報をデータベースに保存/取得できます。

取引オブジェクトを使用すると、`trade.set_custom_data(key='my_key', value=my_value)` を使用して情報を保存し、`trade.get_custom_data(key='my_key')` を使用して取得できます。各データエントリは、取引およびユーザーが指定したキー (「文字列」タイプ) に関連付けられます。これは、トレード オブジェクトも提供するコールバックでのみ使用できることを意味します。

データをデータベース内に保存できるようにするには、freqtrade がデータをシリアル化する必要があります。これは、データを JSON 形式の文字列に変換することによって行われます。
Freqtrade は取得時にこのアクションを元に戻そうとするため、戦略の観点からはこれは関係ありません。
```python
from freqtrade.persistence import Trade
from datetime import timedelta

class AwesomeStrategy(IStrategy):

    def bot_loop_start(self, **kwargs) -> None:
        for trade in Trade.get_open_order_trades():
            fills = trade.select_filled_orders(trade.entry_side)
            if trade.pair == 'ETH/USDT':
                trade_entry_type = trade.get_custom_data(key='entry_type')
                if trade_entry_type is None:
                    trade_entry_type = 'breakout' if 'entry_1' in trade.enter_tag else 'dip'
                elif fills > 1:
                    trade_entry_type = 'buy_up'
                trade.set_custom_data(key='entry_type', value=trade_entry_type)
        return super().bot_loop_start(**kwargs)

    def adjust_entry_price(self, trade: Trade, order: Order | None, pair: str,
                           current_time: datetime, proposed_rate: float, current_order_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:
        # Limit orders to use and follow SMA200 as price target for the first 10 minutes since entry trigger for BTC/USDT pair.
        if (
            pair == 'BTC/USDT' 
            and entry_tag == 'long_sma200' 
            and side == 'long' 
            and (current_time - timedelta(minutes=10)) > trade.open_date_utc 
            and order.filled == 0.0
        ):
            dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
            current_candle = dataframe.iloc[-1].squeeze()
            # store information about entry adjustment
            existing_count = trade.get_custom_data('num_entry_adjustments', default=0)
            if not existing_count:
                existing_count = 1
            else:
                existing_count += 1
            trade.set_custom_data(key='num_entry_adjustments', value=existing_count)

            # adjust order price
            return current_candle['sma_200']

        # default: maintain existing order
        return current_order_rate

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs):

        entry_adjustment_count = trade.get_custom_data(key='num_entry_adjustments')
        trade_entry_type = trade.get_custom_data(key='entry_type')
        if entry_adjustment_count is None:
            if current_profit > 0.01 and (current_time - timedelta(minutes=100) > trade.open_date_utc):
                return True, 'exit_1'
        else
            if entry_adjustment_count > 0 and if current_profit > 0.05:
                return True, 'exit_2'
            if trade_entry_type == 'breakout' and current_profit > 0.1:
                return True, 'exit_3

        return False, None
```
上記は単純な例です。エントリー調整などの取引データを取得するより簡単な方法があります。

!!! Note
    保存する必要があるデータをシリアル化するときに問題が発生しないように、単純なデータ型「[bool, int, float, str]」を使用することをお勧めします。
    大量のデータを保存すると、データベースが大きくなる (その結果、速度も低下する) など、予期しない副作用が発生する可能性があります。

!!! Warning "シリアル化できないデータ"
    提供されたデータをシリアル化できない場合は、警告がログに記録され、指定された `key` のエントリにはデータとして `None` が含まれます。

??? 「すべての属性」に注意してください
    custom-data には、Trade オブジェクト (以下では「trade」とします) を介した次のアクセサーがあります。

    * `trade.get_custom_data(key='something',default=0)` - 指定された型で指定された実際の値を返します。
    * `trade.get_custom_data_entry(key='something')` - メタデータを含むエントリを返します。値には `.value` プロパティ経由でアクセスできます。
    * `trade.set_custom_data(key='something', value={'some': 'value'})` - この取引に対応するキーを設定または更新します。値はシリアル化可能である必要があり、保存されるデータは比較的小さくしておくことをお勧めします。

    「値」は任意のタイプ (設定時と受信時の両方) にすることができますが、json シリアル化可能である必要があります。

## 情報の保存 (非永続)

!!! Warning "廃止されました"
    この情報保存方法は非推奨であるため、非永続ストレージを使用しないことをお勧めします。  
    代わりに [永続ストレージ](#storing-information-persistent) を使用してください。

    したがって、その内容は折りたたまれています。

???要約「情報の保存」
    情報の保存は、戦略クラス内に新しい辞書を作成することで実現できます。

    変数の名前は自由に選択できますが、事前定義された戦略変数との名前の衝突を避けるために「custom_」を接頭辞として付ける必要があります。
    ```python
    class AwesomeStrategy(IStrategy):
        # Create custom dictionary
        custom_info = {}

        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            # Check if the entry already exists
            if not metadata["pair"] in self.custom_info:
                # Create empty entry for this pair
                self.custom_info[metadata["pair"]] = {}

            if "crosstime" in self.custom_info[metadata["pair"]]:
                self.custom_info[metadata["pair"]]["crosstime"] += 1
            else:
                self.custom_info[metadata["pair"]]["crosstime"] = 1
    ```
    !!! Warning
        データは、ボットの再起動 (または構成の再ロード) 後は保持されません。また、データ量は少なく保つ必要があります (DataFrame などは使用しない)。そうしないと、ボットが大量のメモリを消費し始め、最終的にはメモリが不足してクラッシュします。

    !!! Note
        データがペア固有である場合は、必ずペアをディクショナリ内のキーの 1 つとして使用してください。

## データフレームへのアクセス

データプロバイダーからクエリを実行することで、さまざまな戦略関数のデータフレームにアクセスできます。
``` python
from freqtrade.exchange import timeframe_to_prev_date

class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: 'Trade', order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: 'datetime', **kwargs) -> bool:
        # Obtain pair dataframe.
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

        # Obtain last available candle. Do not use current_time to look up latest candle, because 
        # current_time points to current incomplete candle whose data is not available.
        last_candle = dataframe.iloc[-1].squeeze()
        # <...>

        # In dry/live runs trade open date will not match candle open date therefore it must be 
        # rounded.
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        # Look up trade candle.
        trade_candle = dataframe.loc[dataframe['date'] == trade_date]
        # trade_candle may be empty for trades that just opened as it is still incomplete.
        if not trade_candle.empty:
            trade_candle = trade_candle.squeeze()
            # <...>
```
!!! Warning ".iloc[-1]の使用"
    `get_analyzed_dataframe()` はバックテストで確認できるキャンドルのみを返すため、ここで `.iloc[-1]` を使用できます。
    これは `populate_*` メソッドでは機能しないため、その領域では `.iloc[]` を使用しないようにしてください。
    また、これはバージョン 2021.5 以降でのみ機能します。

***

## タグを入力してください

戦略に複数のエントリーシグナルがある場合、トリガーしたシグナルに名前を付けることができます。
その後、`custom_exit` でエントリーシグナルにアクセスできます。
```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["enter_tag"] = ""
    signal_rsi = (qtpylib.crossed_above(dataframe["rsi"], 35))
    signal_bblower = (dataframe["bb_lowerband"] < dataframe["close"])
    # Additional conditions
    dataframe.loc[
        (
            signal_rsi
            | signal_bblower
            # ... additional signals to enter a long position
        )
        & (dataframe["volume"] > 0)
            , "enter_long"
        ] = 1
    # Concatenate the tags so all signals are kept
    dataframe.loc[signal_rsi, "enter_tag"] += "long_signal_rsi "
    dataframe.loc[signal_bblower, "enter_tag"] += "long_signal_bblower "

    return dataframe

def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                current_profit: float, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    last_candle = dataframe.iloc[-1].squeeze()
    if "long_signal_rsi" in trade.enter_tag and last_candle["rsi"] > 80:
        return "exit_signal_rsi"
    if "long_signal_bblower" in trade.enter_tag and last_candle["high"] > last_candle["bb_upperband"]:
        return "exit_signal_bblower"
    # ...
    return None

```
!!! Note
    「enter_tag」は 255 文字に制限されており、残りのデータは切り捨てられます。

!!! Warning
    `enter_tag` 列は 1 つだけあり、ロングトレードとショートトレードの両方に使用されます。
    結果として、この列は「最後の書き込みが優先」として扱われる必要があります (結局のところ、これは単なるデータフレーム列です)。
    複数の信号が衝突するような複雑な状況では (または、異なる条件に基づいて信号が再び非アクティブ化された場合)、エントリ信号に間違ったタグが適用され、奇妙な結果が生じる可能性があります。
    これらの結果は、前のタグを上書きする戦略の結果であり、最後のタグが「固定」され、freqtrade が使用するタグになります。

## 終了タグ

[エントリのタグ付け](#enter-tag)と同様に、終了タグも指定できます。
``` python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["exit_tag"] = ""
    rsi_exit_signal = (dataframe["rsi"] > 70)
    ema_exit_signal  = (dataframe["ema20"] < dataframe["ema50"])
    # Additional conditions
    dataframe.loc[
        (
            rsi_exit_signal
            | ema_exit_signal
            # ... additional signals to exit a long position
        ) &
        (dataframe["volume"] > 0)
        ,
    "exit_long"] = 1
    # Concatenate the tags so all signals are kept
    dataframe.loc[rsi_exit_signal, "exit_tag"] += "exit_signal_rsi "
    dataframe.loc[rsi_exit_signal2, "exit_tag"] += "exit_signal_rsi "

    return dataframe
```
提供された exit-tag は exit-reason として使用され、バックテスト結果にそのように表示されます。

!!! Note
    「exit_reason」は 100 文字に制限されており、残りのデータは切り捨てられます。

## 戦略バージョン

「version」メソッドを使用し、この戦略に必要なバージョンを返すことで、カスタム戦略のバージョン管理を実装できます。
``` python
def version(self) -> str:
    """
    Returns version of the strategy.
    """
    return "1.1"
```
!!! Note
    これに加えて、適切なバージョン管理 (git リポジトリなど) を必ず実装する必要があります。freqtrade は戦略の履歴バージョンを保持しないため、最終的に戦略を以前のバージョンにロールバックできるかどうかはユーザー次第です。

## 派生戦略

戦略は他の戦略から派生させることができます。これにより、カスタム戦略コードの重複が回避されます。このテクニックを使用すると、メイン戦略の小さな部分をオーバーライドし、残りの部分はそのままにすることができます。
``` python title="user_data/strategies/myawesomestrategy.py"
class MyAwesomeStrategy(IStrategy):
    ...
    stoploss = 0.13
    trailing_stop = False
    # All other attributes and methods are here as they
    # should be in any custom strategy...
    ...

```

``` python title="user_data/strategies/MyAwesomeStrategy2.py"
from myawesomestrategy import MyAwesomeStrategy
class MyAwesomeStrategy2(MyAwesomeStrategy):
    # Override something
    stoploss = 0.08
    trailing_stop = True
```
属性とメソッドの両方をオーバーライドして、必要な方法で元のストラテジの動作を変更することができます。

サブクラスを同じファイル内に保持することは技術的には可能ですが、hyperopt パラメーター ファイルでいくつかの問題が発生する可能性があるため、別のストラテジー ファイルを使用し、上記のように親ストラテジーをインポートすることをお勧めします。

## 埋め込み戦略

Freqtrade は、設定ファイルに戦略を埋め込む簡単な方法を提供します。
これは、BASE64 エンコーディングを利用し、この文字列を戦略構成フィールドに指定することによって行われます。
選択した構成ファイル内にあります。

### 文字列を BASE64 としてエンコードする

これは、Python で BASE64 文字列を生成する方法の簡単な例です。
```python
from base64 import urlsafe_b64encode

with open(file, 'r') as f:
    content = f.read()
content = urlsafe_b64encode(content.encode('utf-8'))
```
変数「content」には、BASE64 でエンコードされた形式の戦略ファイルが含まれます。これを構成ファイルで次のように設定できるようになりました
```json
"strategy": "NameOfStrategy:BASE64String"
```
「NameOfStrategy」が戦略名と同じであることを確認してください。

## パフォーマンスに関する警告

戦略を実行すると、ログに次のようなメッセージが表示されることがあります。

> パフォーマンス警告: データフレームは非常に断片化されています。

これは [`pandas`](https://github.com/pandas-dev/pandas) からの警告であり、警告には次のように続きます。
`pd.concat(axis=1)`を使用します。
これはパフォーマンスにわずかな影響を与える可能性がありますが、通常は hyperopt 時 (インジケーターの最適化時) にのみ表示されます。

例えば：
```python
for val in self.buy_ema_short.range:
    dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod=val)
```
に書き換える必要があります
```python
frames = [dataframe]
for val in self.buy_ema_short.range:
    frames.append(DataFrame({
        f'ema_short_{val}': ta.EMA(dataframe, timeperiod=val)
    }))

# Combine all dataframes, and reassign the original dataframe column
dataframe = pd.concat(frames, axis=1)
```
ただし、Freqtrade は、`populate_indicators()` メソッドの直後にデータフレームに対して `dataframe.copy()` を実行することでこれに対抗します。そのため、これによるパフォーマンスへの影響は低いか、まったくないはずです。
