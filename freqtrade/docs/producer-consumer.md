# プロデューサー / コンシューマーモード

freqtrade は、インスタンス (「コンシューマー」とも呼ばれます) が、メッセージ Web ソケットを使用して上流の freqtrade インスタンス (「プロデューサー」とも呼ばれます) からのメッセージをリッスンできるメカニズムを提供します。主に、「analyzed_df」メッセージと「whitelist」メッセージです。これにより、計算されたインジケーター (およびシグナル) を複数回計算することなく、複数のボットのペアで再利用できるようになります。

メッセージ Web ソケット (これがプロデューサーになります) の「api_server」構成のセットアップについては、Rest API ドキュメントの [メッセージ Web ソケット](rest-api.md#message-websocket) を参照してください。

!!! Note
    ボットへの不正アクセスを避けるために、`ws_token` をランダムで自分だけが知っているものに設定することを強くお勧めします。

## 構成

コンシューマーの構成ファイルに「external_message_consumer」セクションを追加して、インスタンスへのサブスクライブを有効にします。
```json
{
    //...
   "external_message_consumer": {
        "enabled": true,
        "producers": [
            {
                "name": "default", // This can be any name you'd like, default is "default"
                "host": "127.0.0.1", // The host from your producer's api_server config
                "port": 8080, // The port from your producer's api_server config
                "secure": false, // Use a secure websockets connection, default false
                "ws_token": "sercet_Ws_t0ken" // The ws_token from your producer's api_server config
            }
        ],
        // The following configurations are optional, and usually not required
        // "wait_timeout": 300,
        // "ping_timeout": 10,
        // "sleep_time": 10,
        // "remove_entry_exit_signals": false,
        // "message_size_limit": 8
    }
    //...
}
```
|  パラメータ |説明 |
|-----------|---------------|
| `有効` | **必須。** コンシューマー モードを有効にします。 false に設定すると、このセクションの他の設定はすべて無視されます。<br>*デフォルトは `false` です。*<br> **Datatype:** boolean 。
| `プロデューサー` | **必須。** プロデューサのリスト <br> **データ型:** 配列。
| `プロデューサー名` | **必須。** このプロデューサーの名前。複数のプロデューサーが使用されている場合、この名前は `get_Producer_pairs()` および `get_Producer_df()` の呼び出しで使用する必要があります。<br> **データ型:** 文字列
| `プロデューサー.ホスト` | **必須。** プロデューサからのホスト名または IP アドレス。<br> **データ型:** 文字列
| `プロデューサーズポート` | **必須。** 上記のホストに一致するポート。<br>*デフォルトは `8080`。*<br> **データ型:** 整数
| `プロデューサー.セキュア` | **オプション。** WebSocket 接続で ssl を使用します。デフォルトは False。<br> **データ型:** 文字列
| `プロデューサーズ.ws_token` | **必須。** プロデューサで構成された `ws_token`。<br> **データ型:** 文字列
| | **オプションの設定**
| `wait_timeout` |メッセージが受信されない場合は、再度 ping を実行するまでタイムアウトします。 <br>*デフォルトは「300」です。*<br> **データ型:** 整数 - 秒単位。
| `ping_timeout` | Ping タイムアウト <br>*デフォルトは「10」です。*<br> **データ型:** 整数 - 秒単位。
| `睡眠時間` |接続を再試行するまでのスリープ時間。<br>*デフォルトは「10」です。*<br> **データ型:** 整数 - 秒単位。
| `remove_entry_exit_signals` |データフレーム受信時にデータフレームから信号列を削除します (0 に設定します)。<br>*デフォルトは「false」です。*<br> **データ型:** ブール値。
| `initial_candle_limit` |プロデューサーから期待される初期キャンドル。<br>*デフォルトは `1500`。*<br> **データ型:** 整数 - キャンドルの数。
| `メッセージサイズ制限` |メッセージごとのサイズ制限<br>*デフォルトは「8」です。*<br> **データ型:** 整数 - メガバイト。

「populate_indicators()」でインジケーターを計算する代わりに (または計算するだけでなく)、フォロワー インスタンスはプロデューサー インスタンスのメッセージ (または高度な構成では複数のプロデューサー インスタンス) への接続をリッスンし、アクティブなホワイトリスト内の各ペアについて、プロデューサーの最も最近分析されたデータフレームをリクエストします。

コンシューマ インスタンスには、分析されたデータフレームの完全なコピーがあり、データフレーム自体を計算する必要はありません。

## 例

### 例 - プロデューサー戦略

複数のインジケーターを備えたシンプルな戦略。戦略自体には特別な考慮事項は必要ありません。
```py
class ProducerStrategy(IStrategy):
    #...
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate indicators in the standard freqtrade way which can then be broadcast to other instances
        """
        dataframe['rsi'] = ta.RSI(dataframe)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &
                (dataframe['tema'] <= dataframe['bb_middleband']) &
                (dataframe['tema'] > dataframe['tema'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```
!!! Tip "周波数AI"
    これを使用すると、強力なマシン上で [FreqAI](freqai.md) をセットアップすることができ、一方、ラズベリーのような単純なマシン上でコンシューマを実行し、プロデューサから生成された信号をさまざまな方法で解釈できます。


### 例 - 消費者戦略

論理的に同等の戦略で、それ自体はインジケーターを計算しませんが、プロデューサーで計算されたインジケーターに基づいて取引の決定を行うために利用できる、同じ分析済みのデータフレームが使用されます。この例では、消費者は同じエントリ基準を持っていますが、これは必須ではありません。消費者は、異なるロジックを使用して取引を開始/終了し、指定されたインジケーターのみを使用する場合があります。
```py
class ConsumerStrategy(IStrategy):
    #...
    process_only_new_candles = False # required for consumers

    _columns_to_expect = ['rsi_default', 'tema_default', 'bb_middleband_default']

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Use the websocket api to get pre-populated indicators from another freqtrade instance.
        Use `self.dp.get_producer_df(pair)` to get the dataframe
        """
        pair = metadata['pair']
        timeframe = self.timeframe

        producer_pairs = self.dp.get_producer_pairs()
        # You can specify which producer to get pairs from via:
        # self.dp.get_producer_pairs("my_other_producer")

        # This func returns the analyzed dataframe, and when it was analyzed
        producer_dataframe, _ = self.dp.get_producer_df(pair)
        # You can get other data if the producer makes it available:
        # self.dp.get_producer_df(
        #   pair,
        #   timeframe="1h",
        #   candle_type=CandleType.SPOT,
        #   producer_name="my_other_producer"
        # )

        if not producer_dataframe.empty:
            # If you plan on passing the producer's entry/exit signal directly,
            # specify ffill=False or it will have unintended results
            merged_dataframe = merge_informative_pair(dataframe, producer_dataframe,
                                                      timeframe, timeframe,
                                                      append_timeframe=False,
                                                      suffix="default")
            return merged_dataframe
        else:
            dataframe[self._columns_to_expect] = 0

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        # Use the dataframe columns as if we calculated them ourselves
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi_default'], self.buy_rsi.value)) &
                (dataframe['tema_default'] <= dataframe['bb_middleband_default']) &
                (dataframe['tema_default'] > dataframe['tema_default'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```
!!! Tip "アップストリーム信号の使用"
    `remove_entry_exit_signals=false` を設定すると、プロデューサーのシグナルを直接使用することもできます。これらは (`suffix="default"` が使用されたと仮定して) `enter_long_default` として利用可能である必要があり、シグナルとして直接使用することも、追加のインジケーターとして使用することもできます。
