# 戦略のカスタマイズ

このページでは、戦略をカスタマイズする方法、新しいインジケーターを追加する方法、取引ルールを設定する方法について説明します。

まだ理解していない場合は、以下についてよく理解してください。

- [Freqtrade Strategy 101](strategy-101.md)。戦略開発を簡単に開始できます。
- [Freqtrade ボットの基本](bot-basics.md)。ボットの動作方法に関する全体的な情報が提供されます。

## 独自の戦略を立てる

ボットにはデフォルトの戦略ファイルが含まれています。

また、他のいくつかの戦略は [戦略リポジトリ](https://github.com/freqtrade/freqtrade-strategies) で入手できます。

ただし、おそらくあなたは独自の戦略のアイデアを持っているでしょう。

この文書は、あなたのアイデアを実用的な戦略に変換するのに役立つことを目的としています。

### 戦略テンプレートの生成

開始するには、次のコマンドを使用できます。
```bash
freqtrade new-strategy --strategy AwesomeStrategy
```
これにより、テンプレートから「AwesomeStrategy」という新しい戦略が作成されます。この戦略は、ファイル名「user_data/strategies/AwesomeStrategy.py」を使用して配置されます。

!!! Note
    ストラテジの *name* とファイル名には違いがあります。ほとんどのコマンドでは、Freqtrade は *ファイル名* ではなく、ストラテジーの *名前* を使用します。

!!! Note
    「new-strategy」コマンドは、そのままでは利益を生まない開始例を生成します。

???ヒント「異なるテンプレートレベル」
    `freqtrade new-strategy` には追加パラメータ `--template` があり、作成された戦略で取得する事前構築情報の量を制御します。インジケーターの例のない空の戦略を取得するには「--template minimum」を使用し、より複雑な機能が定義されたテンプレートを取得するには「--template Advanced」を使用します。

### 戦略の構造

戦略ファイルには、戦略ロジックの構築に必要なすべての情報が含まれています。

- OHLCV形式のキャンドルデータ
- インジケーター
- エントリーロジック
  - 信号
- 終了ロジック
  - 信号
  - 最小限のROI
  - コールバック (「カスタム関数」)
- ストップロス
  - 固定/絶対
  - トレーリング
  - コールバック (「カスタム関数」)
- 価格設定 [オプション]
- 位置調整[オプション]

ボットには、ベースとして使用できる「SampleStrategy」というサンプル戦略が含まれています:「user_data/strategies/sample_strategy.py」。
パラメータ「--strategy SampleStrategy」を使用してテストできます。ファイル名ではなく、ストラテジー クラス名を使用することに注意してください。

さらに、ボットが使用する戦略インターフェイスのバージョンを定義する「INTERFACE_VERSION」という属性があります。
現在のバージョンは 3 です。これは、戦略で明示的に設定されていない場合のデフォルトでもあります。

古い戦略がインターフェイス バージョン 2 に設定されている場合がありますが、将来のバージョンではこれを設定する必要があるため、これらを v3 用語に更新する必要があります。

ボットをドライ モードまたはライブ モードで起動するには、「trade」コマンドを使用します。
```bash
freqtrade trade --strategy AwesomeStrategy
```
### ボットモード

Freqtrade 戦略は、Freqtrade ボットによって 5 つの主要なモードで処理できます。

- バックテスト
- ハイパーオプティング
- ドライ (「フォワードテスト」)
- ライブ
- FreqAI (ここでは取り上げません)

ボットをドライ モードまたはライブ モードに設定する方法については、[構成ドキュメント](configuration.md) を確認してください。

**テストするときは常にドライ モードを使用してください。これにより、資本を危険にさらさずに戦略が実際にどのように機能するかを把握できるようになります。**

## さらに深く掘り下げる

**次のセクションでは、[user_data/strategies/sample_strategy.py](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_strategy.py) を使用します。
参照用ファイル。**

!!! Note "戦略とバックテスト"
    バックテストとドライ/ライブ モード間の問題や予期せぬ違いを避けるために、次の点に注意してください。
    バックテスト中に、全時間範囲が一度に `populate_*()` メソッドに渡されるということです。
    したがって、ベクトル化された操作 (ループではなくデータフレーム全体にわたって) を使用するのが最善です。
    インデックス参照 (`df.iloc[-1]`) を避け、代わりに `df.shift()` を使用して前のローソク足にアクセスします。

!!! Warning "警告: 将来のデータの使用"
    バックテストでは全時間範囲が `populate_*()` メソッドに渡されるため、戦略作成者は
    将来のデータを戦略に利用しないように注意する必要があります。
    この一般的なパターンのいくつかは、このドキュメントの [よくある間違い](#common-missing-when-developing-strategies) セクションにリストされています。

???ヒント「先読みと再帰分析」
    Freqtrade には、一般的な先読み (将来のデータを使用) を評価するのに役立つ 2 つの便利なコマンドが含まれています。
    再帰的バイアス (指標値の分散) の問題。ドライやライブモアで戦略を実行する前に、
    常にこれらのコマンドを最初に使用する必要があります。関連ドキュメントを確認してください。
    [先読み](lookahead-analysis.md) および [再帰](recursive-analysis.md) 分析。

### データフレーム

Freqtrade は [pandas](https://pandas.pydata.org/) を使用してローソク足 (OHLCV) データを保存/提供します。
Pandas は、表形式で大量のデータを処理するために開発された優れたライブラリです。

データフレームの各行はチャート上の 1 つのローソク足に対応し、最新の完全なローソク足が常にデータフレームの最後になります (日付順にソート)。

pandas `head()` 関数を使用してメイン データフレームの最初の数行を見ると、次のようになります。
```output
> dataframe.head()
                       date      open      high       low     close     volume
0 2021-11-09 23:25:00+00:00  67279.67  67321.84  67255.01  67300.97   44.62253
1 2021-11-09 23:30:00+00:00  67300.97  67301.34  67183.03  67187.01   61.38076
2 2021-11-09 23:35:00+00:00  67187.02  67187.02  67031.93  67123.81  113.42728
3 2021-11-09 23:40:00+00:00  67123.80  67222.40  67080.33  67160.48   78.96008
4 2021-11-09 23:45:00+00:00  67160.48  67160.48  66901.26  66943.37  111.39292
```
データフレームは、列が単一の値ではなく、一連のデータ値であるテーブルです。そのため、次のような単純な Python 比較は機能しません。
``` python
    if dataframe['rsi'] > 30:
        dataframe['enter_long'] = 1
```
上記のセクションは、「系列の真理値があいまいです [...]」 というエラーで失敗します。

これは、パンダと互換性のある方法で記述する必要があるため、操作はデータフレーム全体にわたって実行されます (つまり、「ベクトル化」)。
``` python
    dataframe.loc[
        (dataframe['rsi'] > 30)
    , 'enter_long'] = 1
```
このセクションでは、データフレームに新しい列があり、RSI が 30 を超えるたびに「1」が割り当てられます。

Freqtrade は、この新しい列をエントリーシグナルとして使用し、その後、次のオープンローソク足で取引が開始されると想定します。

Pandas は、メトリクスを高速に計算する方法、つまり「ベクトル化」を提供します。この速度を活用するには、ループを使用せず、代わりにベクトル化されたメソッドを使用することをお勧めします。

ベクトル化された操作は、データの全範囲にわたって計算を実行するため、各行をループする場合と比較して、インジケーターを計算する際にはるかに高速になります。

???ヒント「シグナル vs トレード」
    - シグナルはローソク足の終値でインジケーターから生成され、取引に参加する意図を示します。
    - 取引は、(ライブ モードの取引所で) 実行される注文であり、次のローソク足のオープンにできるだけ近いところで取引が開始されます。

!!! Warning "取引注文の前提条件"
    バックテストでは、ローソク足の終値でシグナルが生成されます。その後、次のローソク足が開くとすぐに取引が開始されます。

    ドライおよびライブでは、すべてのペアのデータフレームを最初に分析してから取引処理を行う必要があるため、遅延する可能性があります。 
    それらのペアごとに発生します。これは、ドライ/ライブでは、計算量をできるだけ低くすることに注意する必要があることを意味します。 
    通常は少数のペアを実行し、適切なクロック速度の CPU を使用することで、可能な限り遅延を抑えます。

#### 「リアルタイム」ローソク足データを表示できないのはなぜですか?

Freqtrade は、不完全/未完成のローソク足をデータフレームに保存しません。

戦略決定を行うために不完全なデータを使用することは「再描画」と呼ばれ、他のプラットフォームでもこれが許可されている場合があります。

Freqtrade はそうではありません。データフレームでは、完全/完成したローソク足データのみが利用可能です。

### インジケーターをカスタマイズする

入口信号と出口信号にはインジケーターが必要です。戦略ファイルのメソッド `populate_indicators()` に含まれるリストを拡張することで、さらにインジケーターを追加できます。

`populate_entry_trend()` または `populate_exit_trend()` で使用されるインジケーターのみを追加するか、別のインジケーターを設定するために追加する必要があります。そうしないと、パフォーマンスが低下する可能性があります。

列 `"open"、"high"、"low"、"close"、"volume"` を削除/変更せずに、常にこれら 3 つの関数からデータフレームを返すことが重要です。そうしないと、これらのフィールドに予期しないものが含まれることになります。

サンプル：
```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Adds several different TA indicators to the given DataFrame

    Performance Note: For the best performance be frugal on the number of indicators
    you are using. Let uncomment only the indicator you are using in your strategies
    or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
    :param dataframe: Dataframe with data from the exchange
    :param metadata: Additional information, like the currently traded pair
    :return: a Dataframe with all mandatory indicators for the strategies
    """
    dataframe['sar'] = ta.SAR(dataframe)
    dataframe['adx'] = ta.ADX(dataframe)
    stoch = ta.STOCHF(dataframe)
    dataframe['fastd'] = stoch['fastd']
    dataframe['fastk'] = stoch['fastk']
    dataframe['bb_lower'] = ta.BBANDS(dataframe, nbdevup=2, nbdevdn=2)['lowerband']
    dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)
    dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)
    dataframe['mfi'] = ta.MFI(dataframe)
    dataframe['rsi'] = ta.RSI(dataframe)
    dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
    dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
    dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
    dataframe['ao'] = awesome_oscillator(dataframe)
    macd = ta.MACD(dataframe)
    dataframe['macd'] = macd['macd']
    dataframe['macdsignal'] = macd['macdsignal']
    dataframe['macdhist'] = macd['macdhist']
    hilbert = ta.HT_SINE(dataframe)
    dataframe['htsine'] = hilbert['sine']
    dataframe['htleadsine'] = hilbert['leadsine']
    dataframe['plus_dm'] = ta.PLUS_DM(dataframe)
    dataframe['plus_di'] = ta.PLUS_DI(dataframe)
    dataframe['minus_dm'] = ta.MINUS_DM(dataframe)
    dataframe['minus_di'] = ta.MINUS_DI(dataframe)

    # remember to always return the dataframe
    return dataframe
```
!!! Note "もっとインジケーターの例が必要ですか?"
    [user_data/strategies/sample_strategy.py](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_strategy.py) を調べてください。
    次に、必要なインジケーターのコメントを解除します。

#### インジケーター ライブラリ

freqtrade は、すぐに使用できる次の技術ライブラリをインストールします。

- [ta-lib](https://ta-lib.github.io/ta-lib-python/)
- [パンダスタ](https://twopirllc.github.io/pandas-ta/)
- [テクニカル](https://technical.freqtrade.io)

必要に応じて追加のテクニカル ライブラリをインストールしたり、戦略作成者がカスタム インジケーターを作成/発明したりすることができます。

### 戦略立ち上げ期間

一部のインジケーターには、値を計算するのに十分なローソク足データがない (NaN) か、計算が正しくないため、不安定な起動期間があります。 Freqtrade はこの不安定な期間の長さを知らず、データフレーム内のインジケーター値を使用するため、不一致が発生する可能性があります。

これを考慮して、戦略に「startup_candle_count」属性を割り当てることができます。

これは、戦略が安定したインジケーターを計算するために必要なローソクの最大数に設定する必要があります。ユーザーが情報ペアを含むより高いタイムフレームを含む場合、「startup_candle_count」は必ずしも変化するわけではありません。この値は、インフォマティブ タイムフレームのいずれかが安定したインジケーターを計算するために必要な最大期間 (ローソク足) です。

使用する正しい `startup_candle_count` を確認して見つけるには、[recursive-analysis](recursive-analysis.md) を使用できます。再帰分析で分散が 0% であることが示された場合は、十分な開始ローソク足データがあると確信できます。

この戦略例では、値が正しいことを確認するために ema100 の計算に必要な最小履歴は 400 キャンドルであるため、これを 400 (「startup_candle_count = 400」) に設定する必要があります。
``` python
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
```
どれだけの履歴が必要かをボットに知らせることで、バックテストとハイパーオプト中に指定された時間範囲でバックテスト取引を開始できます。

!!! Warning "x 呼び出しを使用して OHLCV を取得する"
    「警告 - OHLCV を取得するために 3 回の呼び出しを使用しています」のような警告が表示された場合。これにより、ボットの動作が遅くなる可能性があります。戦略に本当に 1500 本のローソクが必要かどうかを確認してください。シグナルにこれだけの履歴データが本当に必要かどうかを検討する必要があります。
    これを行うと、Freqtrade が同じペアに対して複数の呼び出しを行うことになり、明らかに 1 回のネットワーク リクエストよりも遅くなります。
    結果として、Freqtrade はキャンドルを更新するのに時間がかかるため、可能であれば避けるべきです。
    取引所の過負荷やfreqtradeの速度低下を避けるため、コール数は合計5回に制限されています。

!!! Warning
    `startup_candle_count` は、`ohlcv_candle_limit * 5` (ほとんどの取引所では 500 * 5) 未満である必要があります。これは、ドライラン/ライブトレード操作中にこの量のキャンドルしか利用できないためです。

#### 例

上記のように、EMA100 を使用した戦略例を使用して、500 万ローソク足の 1 か月 (2019 年 1 月) のバックテストを試してみましょう。
``` bash
freqtrade backtesting --timerange 20190101-20190201 --timeframe 5m
```
「startup_candle_count」が 400 に設定されていると仮定すると、有効なエントリーシグナルを生成するには 400 個のキャンドルが必要であることがバックテストでわかります。 「20190101 - (400 * 5m)」、つまり ~2018-12-30 11:40:00 からデータがロードされます。

このデータが利用可能な場合、インジケーターはこの拡張された時間範囲で計算されます。その後、バックテストが実行される前に、不安定な起動期間 (2019-01-01 00:00:00 まで) が削除されます。

!!! Note "利用できない起動キャンドル データ"
    起動期間のデータが利用できない場合は、この起動期間を考慮して時間範囲が調整されます。この例では、バックテストは 2019-01-02 09:20:00 から開始されます。

### エントリーシグナルルール

戦略ファイル内のメソッド `populate_entry_trend()` を編集して、エントリー戦略を更新します。

列 `"open"、"high"、"low"、"close"、"volume"` を削除/変更せずに常にデータフレームを返すことが重要です。そうしないと、これらのフィールドに予期しないものが含まれることになります。その後、戦略が無効な値を生成したり、完全に機能しなくなる可能性があります。

このメソッドは、新しい列 `"enter_long"` (short の場合は `"enter_short"`) も定義します。これには、エントリの場合は `1`、「アクションなし」の場合は `0` を含める必要があります。 `enter_long` は、ストラテジーがショートのみの場合でも設定する必要がある必須の列です。

「enter_tag」列を使用してエントリ シグナルに名前を付けることができます。これは、後で戦略をデバッグおよび評価するのに役立ちます。

「user_data/strategies/sample_strategy.py」のサンプル:
```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Based on TA indicators, populates the buy signal for the given dataframe
    :param dataframe: DataFrame populated with indicators
    :param metadata: Additional information, like the currently traded pair
    :return: DataFrame with buy column
    """
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
??? 「ショートトレードを入力する」ことに注意してください
    ショートエントリーは `enter_short` を設定することで作成できます (ロングトレードの `enter_long` に対応します)。
    「enter_tag」列は同じままです。
    空売りは取引所と市場の構成によってサポートされる必要があります。
    また、ショートする場合は、[`can_short`](#can-short) を戦略に適切に設定してください。
    ```python
    # allow both long and short trades
    can_short = True

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 70)) &  # Signal: RSI crosses below 70
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['enter_short', 'enter_tag']] = (1, 'rsi_cross')

        return dataframe
    ```
!!! Note
    購入するには、販売者が購入する必要があります。したがって、ボットがアクティビティのない期間に売買を行わないようにするには、ボリュームを > 0 (`dataframe['volume'] > 0`) にする必要があります。

### 出口信号ルール

メソッド `populate_exit_trend()` を戦略ファイルに編集して、出口戦略を更新します。

exit-signal は、設定または戦略で `use_exit_signal` を false に設定することで抑制できます。

`use_exit_signal` は [シグナル衝突ルール](#colliding-signals) には影響しません。これは引き続き適用され、エントリを防ぐことができます。

列 `"open"、"high"、"low"、"close"、"volume"` を削除/変更せずに常にデータフレームを返すことが重要です。そうしないと、これらのフィールドに予期しないものが含まれることになります。その後、戦略が無効な値を生成したり、完全に機能しなくなる可能性があります。

このメソッドは、新しい列 `"exit_long"` (short の場合は `"exit_short"`) も定義します。これには、終了の場合は 1 を、「アクションなし」の場合は 0 を含める必要があります。

「exit_tag」列を使用して終了シグナルに名前を付けることができます。これは、後で戦略をデバッグおよび評価するのに役立ちます。

「user_data/strategies/sample_strategy.py」のサンプル:
```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Based on TA indicators, populates the exit signal for the given dataframe
    :param dataframe: DataFrame populated with indicators
    :param metadata: Additional information, like the currently traded pair
    :return: DataFrame with buy column
    """
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['exit_long', 'exit_tag']] = (1, 'rsi_too_high')
    return dataframe
```
??? 「ショートトレードを終了する」ことに注意してください
    短い出口は、`exit_short` (`exit_long` に対応) を設定することで作成できます。
    「exit_tag」列は同じままです。
    空売りは取引所と市場の構成によってサポートされる必要があります。
    また、ショートする場合は、[`can_short`](#can-short) を戦略に適切に設定してください。
    ```python
    # allow both long and short trades
    can_short = True

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['exit_long', 'exit_tag']] = (1, 'rsi_too_high')
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 30)) &  # Signal: RSI crosses below 30
                (dataframe['tema'] < dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['exit_short', 'exit_tag']] = (1, 'rsi_too_low')
        return dataframe
    ```
### 最小限の ROI

「minimal_roi」戦略変数は、エグジットシグナルとは別に、取引がエグジットする前に到達すべき最小投資収益率 (ROI) を定義します。

これは次の形式、つまり Python の「dict」で、dict キー (コロンの左側) は取引が開始されてからの経過分、値 (コロンの右側) はパーセンテージです。
```python
minimal_roi = {
    "40": 0.0,
    "30": 0.01,
    "20": 0.02,
    "0": 0.04
}
```
したがって、上記の構成は次のことを意味します。

- 利益が 4% に達するたびに終了
- 利益が 2% に達したら終了 (20 分後に有効)
- 利益が 1% に達したら終了 (30 分後に有効)
- 取引に損失がなくなった場合に終了 (40 分後に有効)

計算には手数料も含まれます。

#### 最小限の ROI を無効にする

ROI を完全に無効にするには、ROI を空の辞書に設定します。
```python
minimal_roi = {}
```
#### 最小限の ROI で計算を使用する

ローソク足の期間 (タイムフレーム) に基づいて時間を使用するには、次のスニペットが便利です。

これにより、戦略の時間枠を変更できますが、最小 ROI 時間は引き続きローソク足として設定されます。 3本のキャンドルの後。
``` python
from freqtrade.exchange import timeframe_to_minutes

class AwesomeStrategy(IStrategy):

    timeframe = "1d"
    timeframe_mins = timeframe_to_minutes(timeframe)
    minimal_roi = {
        "0": 0.05,                      # 5% for the first 3 candles
        str(timeframe_mins * 3): 0.02,  # 2% after 3 candles
        str(timeframe_mins * 6): 0.01,  # 1% After 6 candles
    }
```
??? info「すぐに満たされない注文」
    `minimal_roi` は、取引が初期化された時間、つまりこの取引の最初の注文が行われた時間である `trade.open_date` を参照として受け取ります。
    これは、すぐには約定しない指値注文 (通常、`custom_entry_price()` を介して「オフスポット」価格と組み合わせて) や、最初の注文価格が `adjust_entry_price()` を介して置き換えられる場合にも当てはまります。
    使用される時間は、新規発注または調整された注文の日付ではなく、最初の `trade.open_date` (最初の注文が最初に発注されたとき) からのものになります。

### ストップロス

あなたに対する強い動きから資本を保護するために、ストップロスを設定することを強くお勧めします。

10% ストップロスの設定例:
``` python
stoploss = -0.10
```
ストップロス機能に関する完全なドキュメントについては、専用の [ストップロス ページ](stoploss.md) をご覧ください。

### 期間

これは、ボットが戦略で使用するキャンドルの周期性です。

一般的な値は `"1m"`、`"5m"`、`"15m"`、`"1h"` ですが、取引所でサポートされているすべての値が機能するはずです。

同じエントリー/エグジットシグナルは、ある時間枠ではうまく機能する可能性がありますが、他の時間枠では機能しない場合があることに注意してください。

この設定は、戦略メソッド内で `self.timeframe` 属性としてアクセスできます。

### ショートできる

先物市場でショートシグナルを使用するには、「can_short = True」を設定する必要があります。

これを可能にする戦略はスポット市場では機能しません。

ショートシグナルを生成するために「enter_short」列に「1」の値がある場合、「can_short = False」(デフォルト) を設定すると、設定で先物市場を指定していても、これらのショートシグナルは無視されます。

### メタデータ辞書

`metadata` dict (`populate_entry_trend`、`populate_exit_trend`、`populate_indicators` で利用可能) には追加情報が含まれています。
現在、これは「pair」で、「metadata['pair']」を使用してアクセスでき、「XRP/BTC」（先物市場の場合は「XRP/BTC:BTC」）形式でペアを返します。

メタデータ辞書は変更しないでください。また、戦略内の複数の機能にわたって情報を保持しません。

代わりに、[情報の保存](strategy-advanced.md#storing-information-persistent) セクションを確認してください。

--8<-- "includes/strategy-imports.md"

## 戦略ファイルの読み込み

デフォルトでは、freqtrade は `userdir` 内のすべての `.py` ファイル (デフォルトは `user_data/strategies`) からストラテジーをロードしようとします。

あなたの戦略が `AwesomeStrategy` という名前で、ファイル `user_data/strategies/AwesomeStrategy.py` に保存されていると仮定すると、次のようにして freqtrade をドライ (または設定に応じてライブ) モードで開始できます。
```bash
freqtrade trade --strategy AwesomeStrategy
```
ファイル名ではなくクラス名を使用していることに注意してください。

「freqtrade list-strategies」を使用すると、Freqtrade がロードできるすべての戦略 (正しいフォルダー内のすべての戦略) のリストを表示できます。
また、潜在的な問題を強調する「ステータス」フィールドも含まれます。

???ヒント「戦略ディレクトリをカスタマイズする」
    「--strategy-path user_data/otherPath」を使用すると、別のディレクトリを使用できます。このパラメータは、戦略を必要とするすべてのコマンドで使用できます。

## 有益なペア

### 取引不可能なペアのデータを取得する

追加の有益なペア (参照ペア) のデータは、より広い時間枠でデータを確認するための一部の戦略にとって有益です。

これらのペアの OHLCV データは、通常のホワイトリスト更新プロセスの一部としてダウンロードされ、他のペアと同様に「DataProvider」経由で利用できます (以下を参照)。

これらのペアは、ペアのホワイトリストでも指定されているか、動的ホワイトリストによって選択されていない限り、**取引されません**。 「ボリュームペアリスト」。

ペアは、最初の引数としてペア、2 番目の引数としてタイムフレームを使用して、`("pair", "timeframe")` 形式のタプルとして指定する必要があります。

サンプル：
``` python
def informative_pairs(self):
    return [("ETH/USDT", "5m"),
            ("BTC/TUSD", "15m"),
            ]
```
完全なサンプルは [DataProvider セクション](#complete-dataprovider-sample) にあります。

!!! Warning
    これらのペアは定期的なホワイトリスト更新の一部として更新されるため、このリストは短くしておくことをお勧めします。
    使用されている取引所で利用可能 (かつアクティブ) である限り、すべてのタイムフレームとすべてのペアを指定できます。
    ただし、可能な限り長い時間枠でリサンプリングを使用することをお勧めします。
    リクエストが多すぎて取引所が混乱し、ブロックされるリスクを避けるためです。

??? 「代替キャンドルの種類」に注意してください。
    Informative_pairs は、ローソク足のタイプを明示的に定義する 3 番目のタプル要素を提供することもできます。
    代替のローソク式が利用できるかどうかは、取引モードと取引所によって異なります。
    一般に、スポット ペアは先物市場では使用できません。また、先物ローソク足はスポット ボットの情報ペアとして使用できません。
    これに関する詳細は変更される可能性がありますが、変更される場合は交換ドキュメントに記載されています。
    ``` python
    def informative_pairs(self):
        return [
            ("ETH/USDT", "5m", ""),   # Uses default candletype, depends on trading_mode (recommended)
            ("ETH/USDT", "5m", "spot"),   # Forces usage of spot candles (only valid for bots running on spot markets).
            ("BTC/TUSD", "15m", "futures"),  # Uses futures candles (only bots with `trading_mode=futures`)
            ("BTC/TUSD", "15m", "mark"),  # Uses mark candles (only bots with `trading_mode=futures`)
        ]
    ```
***

### 情報ペアのデコレータ (`@informative()`)

情報ペアを簡単に定義するには、「@informative」デコレータを使用します。修飾されたすべての `populate_indicators_*` メソッドは個別に実行されます。
また、他の情報ペアからのデータにはアクセスできません。ただし、各ペアのすべての情報データフレームはマージされ、メインの `populate_indicators()` メソッドに渡されます。

!!! Note
    別の情報ペアを生成するときに、ある情報ペアのデータを使用する必要がある場合は、`@informative` デコレータを使用しないでください。代わりに、[DataProvider セクション](#complete-dataprovider-sample) の説明に従って、情報ペアを手動で定義します。

ハイパーオプト化する場合、ハイパーオプタブル パラメーター `.value` 属性の使用はサポートされません。 `.range` 属性を使用してください。詳細については、[インジケーター パラメーターの最適化](hyperopt.md#optimizing-an-indicator-parameter) を参照してください。

??? info「完全なドキュメント」
    ``` python
    def informative(
        timeframe: str,
        asset: str = "",
        fmt: str | Callable[[Any], str] | None = None,
        *,
        candle_type: CandleType | str | None = None,
        ffill: bool = True,
    ) -> Callable[[PopulateIndicators], PopulateIndicators]:
        """
        A decorator for populate_indicators_Nn(self, dataframe, metadata), allowing these functions to
        define informative indicators.

        Example usage:

            @informative('1h')
            def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
                dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
                return dataframe

        :param timeframe: Informative timeframe. Must always be equal or higher than strategy timeframe.
        :param asset: Informative asset, for example BTC, BTC/USDT, ETH/BTC. Do not specify to use
                    current pair. Also supports limited pair format strings (see below)
        :param fmt: Column format (str) or column formatter (callable(name, asset, timeframe)). When not
        specified, defaults to:
        * {base}_{quote}_{column}_{timeframe} if asset is specified.
        * {column}_{timeframe} if asset is not specified.
        Pair format supports these format variables:
        * {base} - base currency in lower case, for example 'eth'.
        * {BASE} - same as {base}, except in upper case.
        * {quote} - quote currency in lower case, for example 'usdt'.
        * {QUOTE} - same as {quote}, except in upper case.
        Format string additionally supports this variables.
        * {asset} - full name of the asset, for example 'BTC/USDT'.
        * {column} - name of dataframe column.
        * {timeframe} - timeframe of informative dataframe.
        :param ffill: ffill dataframe after merging informative pair.
        :param candle_type: '', mark, index, premiumIndex, or funding_rate
        """
    ```
???例「有益なペアを定義する迅速かつ簡単な方法」

    ほとんどの場合、`merge_informative_pair()` によって提供される機能と柔軟性は必要ないため、デコレータを使用して情報ペアをすばやく定義できます。
    ``` python

    from datetime import datetime
    from freqtrade.persistence import Trade
    from freqtrade.strategy import IStrategy, informative

    class AwesomeStrategy(IStrategy):
        
        # This method is not required. 
        # def informative_pairs(self): ...

        # Define informative upper timeframe for each pair. Decorators can be stacked on same 
        # method. Available in populate_indicators as 'rsi_30m' and 'rsi_1h'.
        @informative('30m')
        @informative('1h')
        def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe

        # Define BTC/STAKE informative pair. Available in populate_indicators and other methods as
        # 'btc_rsi_1h'. Current stake currency should be specified as {stake} format variable 
        # instead of hard-coding actual stake currency. Available in populate_indicators and other 
        # methods as 'btc_usdt_rsi_1h' (when stake currency is USDT).
        @informative('1h', 'BTC/{stake}')
        def populate_indicators_btc_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe

        # Define BTC/ETH informative pair. You must specify quote currency if it is different from
        # stake currency. Available in populate_indicators and other methods as 'eth_btc_rsi_1h'.
        @informative('1h', 'ETH/BTC')
        def populate_indicators_eth_btc_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe
    
        # Define BTC/STAKE informative pair. A custom formatter may be specified for formatting
        # column names. A callable `fmt(**kwargs) -> str` may be specified, to implement custom
        # formatting. Available in populate_indicators and other methods as 'rsi_upper_1h'.
        @informative('1h', 'BTC/{stake}', '{column}_{timeframe}')
        def populate_indicators_btc_1h_2(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi_upper'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe
    
        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            # Strategy timeframe indicators for current pair.
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            # Informative pairs are available in this method.
            dataframe['rsi_less'] = dataframe['rsi'] < dataframe['rsi_1h']
            return dataframe

    ```
!!! Note
    他のペアの有益なデータフレームにアクセスする場合は、文字列フォーマットを使用します。これにより、戦略コードを調整することなく、構成内のステーク通貨を簡単に変更できるようになります。
    ``` python
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        stake = self.config['stake_currency']
        dataframe.loc[
            (
                (dataframe[f'btc_{stake}_rsi_1h'] < 35)
                &
                (dataframe['volume'] > 0)
            ),
            ['enter_long', 'enter_tag']] = (1, 'buy_signal_rsi')
    
        return dataframe
    ```
あるいは、列の名前変更を使用して列名からステーク通貨を削除することもできます: `@informative('1h', 'BTC/{stake}', fmt='{base}_{column}_{timeframe}')`。

!!! Warning "メソッド名が重複しています"
    `@informative()` デコレータでタグ付けされたメソッドは、常に一意の名前を持つ必要があります。同じ名前を再利用すると (たとえば、すでに定義されている情報メソッドをコピーして貼り付ける場合)、以前に定義されたメソッドは上書きされ、Python プログラミング言語の制限によりエラーは発生しません。このような場合、ストラテジー ファイルの上位のメソッドで作成されたインジケーターがデータフレームでは使用できないことがわかります。メソッド名を注意深く確認し、一意であることを確認してください。

### *merge_informative_pair()*

この方法は、先読みバイアスなしで、情報ペアを通常のメイン データフレームに安全かつ一貫してマージするのに役立ちます。

オプション:

- 列の名前を変更して一意の列を作成します
- 先読みバイアスなしでデータフレームをマージします
- フォワードフィル（オプション）

完全なサンプルについては、以下の [完全なデータ プロバイダーの例](#complete-dataprovider-sample) を参照してください。

有益なデータフレームのすべての列は、名前が変更された方法で返されるデータフレームで利用できるようになります。

!!! Example "列の名前変更"
    `inf_tf = '1d'` と仮定すると、結果の列は次のようになります。
    ``` python
    'date', 'open', 'high', 'low', 'close', 'rsi'                     # from the original dataframe
    'date_1d', 'open_1d', 'high_1d', 'low_1d', 'close_1d', 'rsi_1d'   # from the informative dataframe
    ```
???例「列の名前変更 - 1h」
    `inf_tf = '1h'` と仮定すると、結果の列は次のようになります。
    ``` python
    'date', 'open', 'high', 'low', 'close', 'rsi'                     # from the original dataframe
    'date_1h', 'open_1h', 'high_1h', 'low_1h', 'close_1h', 'rsi_1h'   # from the informative dataframe
    ```
???例「カスタム実装」
    このためのカスタム実装が可能であり、次のように実行できます。
    ``` python

    # Shift date by 1 candle
    # This is necessary since the data is always the "open date"
    # and a 15m candle starting at 12:15 should not know the close of the 1h candle from 12:00 to 13:00
    minutes = timeframe_to_minutes(inf_tf)
    # Only do this if the timeframes are different:
    informative['date_merge'] = informative["date"] + pd.to_timedelta(minutes, 'm')

    # Rename columns to be unique
    informative.columns = [f"{col}_{inf_tf}" for col in informative.columns]
    # Assuming inf_tf = '1d' - then the columns will now be:
    # date_1d, open_1d, high_1d, low_1d, close_1d, rsi_1d

    # Combine the 2 dataframes
    # all indicators on the informative sample MUST be calculated before this point
    dataframe = pd.merge(dataframe, informative, left_on='date', right_on=f'date_merge_{inf_tf}', how='left')
    # FFill to have the 1d value available in every row throughout the day.
    # Without this, comparisons would only work once per day.
    dataframe = dataframe.ffill()

    ```
!!! Warning "有益な時間枠 < 時間枠"
    この方法では、提供される追加情報が使用されないため、メイン データフレームのタイムフレームよりも小さい情報タイムフレームを使用することはお勧めできません。
    より詳細な情報を適切に使用するには、より高度な方法を適用する必要があります (このドキュメントの範囲外です)。

## 追加データ (DataProvider)

この戦略により、「DataProvider」へのアクセスが提供されます。これにより、戦略で使用する追加のデータを取得できるようになります。

失敗した場合、すべてのメソッドは「None」を返します。つまり、失敗しても例外は発生しません。

常に動作モードを確認して、データを取得するための正しい方法を選択してください (例については以下を参照)。

!!! Warning "Hyperopt の制限事項"
    DataProvider は hyperopt 中に使用できますが、**ストラテジ**内の `populate_indicators()` でのみ使用でき、hyperopt クラス ファイル内では使用できません。
    また、`populate_entry_trend()` および `populate_exit_trend()` メソッドでも使用できません。

### データプロバイダーの可能なオプション

- [`available_pairs`](#available_pairs) - キャッシュされたペアとそのタイムフレーム (ペア、タイムフレーム) をリストするタプルを含むプロパティ。
- [`current_whitelist()`](#current_whitelist) - ホワイトリストに登録されたペアの現在のリストを返します。動的ホワイトリスト (つまり、 VolumePairlist) にアクセスするのに役立ちます。
- [`get_pair_dataframe(pair, timeframe)`](#get_pair_dataframepair-timeframe) - これは汎用メソッドであり、履歴データ (バックテスト用) またはキャッシュされたライブ データ (ドライラン モードおよびライブラン モード用) を返します。
- [`get_analyzed_dataframe(pair, timeframe)`](#get_analyzed_dataframepair-timeframe) - 分析されたデータフレーム (`populate_indicators()`、`populate_buy()`、`populate_sell()` の呼び出し後) と最新の分析の時間を返します。
- `history_ohlcv(pair, timeframe)` - ディスクに保存されている履歴データを返します。
- `market(pair)` - ペアの市場データを返します: 手数料、限度額、精度、アクティビティ フラグなど。市場データ構造の詳細については、[ccxt ドキュメント](https://github.com/ccxt/ccxt/wiki/Manual#markets) を参照してください。
- `ohlcv(pair, timeframe)` - ペアの現在キャッシュされているローソク足 (OHLCV) データ。DataFrame または空の DataFrame を返します。
- [`orderbook(pair, minimum)`](#orderbookpair-maximum) - ペアの最新のオーダーブック データ、合計 `maximum` エントリを持つ買い/売りの辞書を返します。
- [`ticker(pair)`](#tickerpair) - ペアの現在のティッカー データを返します。 Ticker データ構造の詳細については、[ccxt ドキュメント](https://github.com/ccxt/ccxt/wiki/Manual#price-tickers) を参照してください。
- [`check_delisting(pair)`](#check_delistingpair) - ペア上場廃止スケジュールがあればその日時を返し、それ以外の場合は None を返します
- [`funding_rate(pair)`](#funding_ratepair) - ペアの現在の資金調達率データを返します。
- `runmode` - 現在の実行モードを含むプロパティ。

### 使用例

### *利用可能なペア*
``` python
for pair, timeframe in self.dp.available_pairs:
    print(f"available {pair}, {timeframe}")
```
### *current_whitelist()*

出来高上位 10 の取引ペアの「1d」タイムフレームから生成されたシグナルを使用して「5m」タイムフレームを取引する戦略を開発したと想像してください。

戦略ロジックは次のようになります。

*「ボリュームペアリスト」を使用して 5 分ごとにボリュームの上位 10 ペアをスキャンし、14 日間の RSI を使用して出入りします。*

利用可能なデータが限られているため、「5m」ローソク足を 14 日 RSI で使用する日足ローソク足にリサンプリングすることは非常に困難です。ほとんどの取引所はユーザーをわずか 500 ～ 1000 キャンドルに制限しており、実質的に 1 日あたり約 1.74 キャンドルが得られます。少なくとも14日は必要です！

データをリサンプリングできないため、情報のペアを使用する必要がありますが、ホワイトリストは動的であるため、どのペアを使用すればよいかわかりません。問題があります!

ここで、`self.dp.current_whitelist()` を呼び出して、ホワイトリスト内のペアのみを取得すると便利です。
```python
    def informative_pairs(self):

        # get access to all pairs available in whitelist.
        pairs = self.dp.current_whitelist()
        # Assign timeframe to each pair so they can be downloaded and cached for strategy.
        informative_pairs = [(pair, '1d') for pair in pairs]
        return informative_pairs
```
??? 「current_whitelist を使用したプロット」に注意してください
    現在のホワイトリストは「plot-dataframe」ではサポートされていません。このコマンドは通常、明示的なペアリストを提供することによって使用されるため、このメソッドの戻り値が誤解を招く可能性があるためです。
    また、Web サーバー モードの構成ではペアリストを設定する必要がないため、[Web サーバー モード](utils.md#webserver-mode) での FreqUI 視覚化でもサポートされていません。

### *get_pair_dataframe(ペア, タイムフレーム)*
``` python
# fetch live / historical candle (OHLCV) data for the first informative pair
inf_pair, inf_timeframe = self.informative_pairs()[0]
informative = self.dp.get_pair_dataframe(pair=inf_pair,
                                         timeframe=inf_timeframe)
```
!!! Warning "バックテストに関する警告"
    バックテストでは、`dp.get_pair_dataframe()` の動作は呼び出される場所によって異なります。
    `populate_*()` メソッド内で、`dp.get_pair_dataframe()` は完全な時間範囲を返します。ドライ/ライブ モードで実行するときに予期せぬ事態を避けるために、「将来を見据える」ことはしないようにしてください。
    [callbacks](strategy-callbacks.md) 内で、現在の (シミュレートされた) ローソク足までの全時間範囲を取得します。

### *get_analyzed_dataframe(ペア, タイムフレーム)*

このメソッドは、freqtrade が内部的に最後のシグナルを決定するために使用します。
また、特定のコールバックで使用して、アクションを引き起こしたシグナルを取得することもできます (利用可能なコールバックの詳細については、[高度な戦略ドキュメント](strategy-advanced.md) を参照してください)。
``` python
# fetch current dataframe
dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=metadata['pair'],
                                                         timeframe=self.timeframe)
```
!!! Note "利用可能なデータがありません"
    要求されたペアがキャッシュされていない場合は、空のデータフレームを返します。
    「if dataframe.empty:」を使用してこれを確認し、それに応じてこのケースを処理できます。
    ホワイトリストに登録されたペアを使用する場合、これは発生しないはずです。

### *オーダーブック(ペア、最大)*

ペアの現在のオーダーブックを取得します。
``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    ob = self.dp.orderbook(metadata['pair'], 1)
    dataframe['best_bid'] = ob['bids'][0][0]
    dataframe['best_ask'] = ob['asks'][0][0]
```
オーダーブックの構造は、[ccxt](https://github.com/ccxt/ccxt/wiki/Manual#order-book- Structure) のオーダー構造と一致しているため、結果は次のような形式になります。
``` js
{
    'bids': [
        [ price, amount ], // [ float, float ]
        [ price, amount ],
        ...
    ],
    'asks': [
        [ price, amount ],
        [ price, amount ],
        //...
    ],
    //...
}
```
したがって、上で示したように `ob['bids'][0][0]` を使用すると、最良の入札価格が使用されます。 `ob['bids'][0][1]` は、このオーダーブックのポジションの金額を調べます。

!!! Warning "バックテストに関する警告"
    オーダーブックは履歴データの一部ではないため、このメソッドを使用すると最新の値が返されるため、バックテストと hyperopt が正しく機能しません。

### *ティッカー(ペア)*
``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    ticker = self.dp.ticker(metadata['pair'])
    dataframe['last_price'] = ticker['last']
    dataframe['volume24h'] = ticker['quoteVolume']
    dataframe['vwap'] = ticker['vwap']
```
!!! Warning
    ティッカー データ構造は ccxt 統一インターフェイスの一部ですが、このメソッドによって返される値は次のとおりです。
    取引所ごとに異なります。たとえば、多くの取引所は「vwap」値を返しません。
    「last」フィールドは常に入力するとは限りません（None になる可能性もあります）。そのため、ティッカーを注意深く確認する必要があります。
    交換から返されたデータを収集し、適切なエラー処理/デフォルトを追加します。

!!! Warning "バックテストに関する警告"
    このメソッドは常に最新のリアルタイム値を返します。そのため、ランモードチェックを行わずにバックテスト/ハイパーオプト中に使用すると、誤った結果が生じます。データフレーム全体には、すべての行に同じ単一の値が含まれます。

### *check_delisting(ペア)*
```python
def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs):
    if self.dp.runmode.value in ('live', 'dry_run'):
        delisting_dt = self.dp.check_delisting(pair)
        if delisting_dt is not None:
            return "delist"
```
!!! Note "上場廃止情報の入手可能性"
    このメソッドは特定の取引所でのみ使用でき、これが使用できない場合、またはペアの上場廃止が予定されていない場合は「None」を返します。

!!! Warning "バックテストに関する警告"
    このメソッドは常に最新のリアルタイム値を返します。そのため、ランモードチェックを行わずにバックテスト/ハイパーオプト中に使用すると、誤った結果が生じます。データフレーム全体には、すべての行に同じ単一の値が含まれます。

### *資金レート(ペア)*

ペアの現在の資金調達レートを取得します。「base/quote:settle」形式の先物ペアに対してのみ機能します (例: 「ETH/USDT:USDT」)。
``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    funding_rate = self.dp.funding_rate(metadata['pair'])
    dataframe['current_funding_rate'] = funding_rate['fundingRate']
    dataframe['next_funding_timestamp'] = funding_rate['fundingTimestamp']
    dataframe['next_funding_datetime'] = funding_rate['fundingDatetime']
```
資金調達レート構造は、[ccxt](https://github.com/ccxt/ccxt/wiki/Manual#funding-rate-structural) の資金調達レート構造と一致しているため、結果は次のような形式になります。
``` python
{
    "info": {
        # ... 
    },
    "symbol": "BTC/USDT:USDT",
    "markPrice": 110730.7,
    "indexPrice": 110782.52,
    "interestRate": 0.0001,
    "estimatedSettlePrice": 110822.67200153,
    "timestamp": 1757146321001,
    "datetime": "2025-09-06T08:12:01.001Z",
    "fundingRate": 5.609e-05,
    "fundingTimestamp": 1757174400000,
    "fundingDatetime": "2025-09-06T16:00:00.000Z",
    "nextFundingRate": None,
    "nextFundingTimestamp": None,
    "nextFundingDatetime": None,
    "previousFundingRate": None,
    "previousFundingTimestamp": None,
    "previousFundingDatetime": None,
    "interval": None,
}
```
したがって、上で示したように `funding_rate['fundingRate']` を使用すると、現在の資金調達率が使用されます。
実際に利用可能なデータは取引所によって異なるため、このコードは取引所間では期待どおりに機能しない可能性があります。

!!! Warning "バックテストに関する警告"
    現在の資金調達率は履歴データの一部ではないため、このメソッドを使用すると最新の値が返されるため、バックテストと hyperopt が正しく機能しません。
    バックテストには過去に利用可能な資金調達レートを使用することをお勧めします (これは自動的にダウンロードされ、取引所が提供する頻度、通常は 4 時間または 8 時間です)。
    `self.dp.get_pair_dataframe(pair=metadata['pair']、timeframe='8h'、candle_type="funding_rate")`

### 通知を送信

データプロバイダーの `.send_msg()` 関数を使用すると、戦略からカスタム通知を送信できます。
2 番目の引数 (`always_send`) が True に設定されていない限り、同じ通知はキャンドルごとに 1 回だけ送信されます。
``` python
    self.dp.send_msg(f"{metadata['pair']} just got hot!")

    # Force send this notification, avoid caching (Please read warning below!)
    self.dp.send_msg(f"{metadata['pair']} just got hot!", always_send=True)
```
通知は取引モード (ライブ/ドライラン) でのみ送信されるため、このメソッドはバックテストの条件なしで呼び出すことができます。

!!! Warning "スパム行為"
    このメソッドで `always_send=True` を設定すると、かなりうまくスパムを送信できます。 5 秒ごとのメッセージを避けるために、これは細心の注意を払って使用し、キャンドルが点灯している間は起こらないとわかっている条件でのみ使用してください。

### 完全なデータプロバイダーのサンプル
```python
from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame

class SampleStrategy(IStrategy):
    # strategy init stuff...

    timeframe = '5m'

    # more strategy init stuff..

    def informative_pairs(self):

        # get access to all pairs available in whitelist.
        pairs = self.dp.current_whitelist()
        # Assign tf to each pair so they can be downloaded and cached for strategy.
        informative_pairs = [(pair, '1d') for pair in pairs]
        # Optionally Add additional "static" pairs
        informative_pairs += [("ETH/USDT", "5m"),
                              ("BTC/TUSD", "15m"),
                            ]
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if not self.dp:
            # Don't do anything if DataProvider is not available.
            return dataframe

        inf_tf = '1d'
        # Get the informative pair
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=inf_tf)
        # Get the 14 day rsi
        informative['rsi'] = ta.RSI(informative, timeperiod=14)

        # Use the helper function merge_informative_pair to safely merge the pair
        # Automatically renames the columns and merges a shorter timeframe dataframe and a longer timeframe informative pair
        # use ffill to have the 1d value available in every row throughout the day.
        # Without this, comparisons between columns of the original and the informative pair would only work once per day.
        # Full documentation of this method, see below
        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, inf_tf, ffill=True)

        # Calculate rsi of the original dataframe (5m timeframe)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Do other stuff
        # ...

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                (dataframe['rsi_1d'] < 30) &                     # Ensure daily RSI is < 30
                (dataframe['volume'] > 0)                        # Ensure this candle had volume (important for backtesting)
            ),
            ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

```
***

## 追加データ (ウォレット)

この戦略により、「wallets」オブジェクトへのアクセスが提供されます。これには、取引所のウォレット/アカウントの現在の残高が含まれます。

!!! Note "バックテスト / Hyperopt"
    ウォレットの動作は、呼び出された関数に応じて異なります。
    `populate_*()` メソッド内では、設定された完全なウォレットが返されます。
    [callbacks](strategy-callbacks.md) 内で、シミュレーション プロセスのその時点で実際にシミュレートされたウォレットに対応するウォレットの状態を取得します。

バックテスト中の失敗を避けるために、「ウォレット」が利用可能かどうかを常に確認してください。
``` python
if self.wallets:
    free_eth = self.wallets.get_free('ETH')
    used_eth = self.wallets.get_used('ETH')
    total_eth = self.wallets.get_total('ETH')
```
### ウォレットの可能なオプション

- `get_free(asset)` - 現在取引可能な残高
- `get_used(asset)` - 現在拘束されている残高 (オープンオーダー)
- `get_total(asset)` - 利用可能残高の合計 - 上記 2 つの合計

***

## 追加データ (取引)

取引履歴は、データベースにクエリを実行することで戦略内で取得できます。

ファイルの先頭で、必要なオブジェクトをインポートします。
```python
from freqtrade.persistence import Trade
```
次の例では、現在のペア (`metadata['pair']`) について今日からの取引をクエリします。他のフィルターも簡単に追加できます。
``` python
trades = Trade.get_trades_proxy(pair=metadata['pair'],
                                open_date=datetime.now(timezone.utc) - timedelta(days=1),
                                is_open=False,
            ]).order_by(Trade.close_date).all()
# Summarize profit for this pair.
curdayprofit = sum(trade.close_profit for trade in trades)
```
利用可能なメソッドの完全なリストについては、[Trade object](trade-object.md) ドキュメントを参照してください。

!!! Warning
    バックテストまたはハイパーオプト中は `populate_*` メソッドでは取引履歴を利用できず、結果は空になります。

## 特定のペアの取引が行われないようにする

Freqtrade は、ペアが終了すると、現在のローソク足のペアを (そのローソク足が終了するまで) 自動的にロックし、そのペアの即時の再エントリーを防ぎます。

これは、1 つのローソク内で多数の頻繁な取引の「ウォーターフォール」を防ぐためです。

ロックされたペアには、「ペア <ペア> は現在ロックされています。」というメッセージが表示されます。

### 戦略内からペアをロックする

場合によっては、特定のイベントが発生した後にペアをロックすることが望ましい場合があります (例: 連続して複数の取引で負けた場合など)。

Freqtrade には、`self.lock_pair(pair, until, [reason])` を呼び出すことで、戦略内からこれを行う簡単な方法があります。
「until」は将来の日時オブジェクトでなければならず、その後、そのペアの取引は再び有効になります。「reason」はペアがロックされた理由を詳細に示すオプションの文字列です。

ロックは、ペアがロック解除された理由を指定して `self.unlock_pair(pair)` または `self.unlock_reason(<reason>)` を呼び出して手動で解除することもできます。
`self.unlock_reason(<reason>)` は、指定された理由で現在ロックされているすべてのペアのロックを解除します。

ペアが現在ロックされているかどうかを確認するには、`self.is_pair_locked(pair)` を使用します。

!!! Note
    ロックされたペアは常に次のローソク足に切り上げられます。したがって、「5m」の時間枠を仮定すると、「until」を 10:18 に設定したロックは、10:15 から 10:20 までのローソク足が終了するまでペアをロックします。

!!! Warning
    バックテスト中はペアを手動でロックすることはできません。保護によるロックのみが許可されます。

#### ペアロックの例
``` python
from freqtrade.persistence import Trade
from datetime import timedelta, datetime, timezone
# Put the above lines at the top of the strategy file, next to all the other imports
# --------

# Within populate indicators (or populate_entry_trend):
if self.config['runmode'].value in ('live', 'dry_run'):
    # fetch closed trades for the last 2 days
    trades = Trade.get_trades_proxy(
        pair=metadata['pair'], is_open=False, 
        open_date=datetime.now(timezone.utc) - timedelta(days=2))
    # Analyze the conditions you'd like to lock the pair .... will probably be different for every strategy
    sumprofit = sum(trade.close_profit for trade in trades)
    if sumprofit < 0:
        # Lock pair for 12 hours
        self.lock_pair(metadata['pair'], until=datetime.now(timezone.utc) + timedelta(hours=12))
```
## メインのデータフレームを出力します

現在のメイン データフレームを検査するには、`populate_entry_trend()` または `populate_exit_trend()` のいずれかで print ステートメントを発行できます。
現在どのデータが表示されているかを明確にするために、ペアを印刷することもできます。
``` python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            #>> whatever condition<<<
        ),
        ['enter_long', 'enter_tag']] = (1, 'somestring')

    # Print the Analyzed pair
    print(f"result for {metadata['pair']}")

    # Inspect the last 5 rows
    print(dataframe.tail())

    return dataframe
```
`print(dataframe.tail())` の代わりに `print(dataframe)` を使用すると、数行以上を印刷することもできます。ただし、これは大量の出力 (5 秒ごとに 1 ペアあたり約 500 行) が発生する可能性があるため、お勧めできません。

## 戦略を立てるときによくある間違い

### バックテストをしながら将来を見据える

バックテストでは、パフォーマンス上の理由から、データフレームの時間範囲全体を一度に分析します。このため、戦略作成者は、戦略が将来を先読みしていないこと、つまりドライ モードやライブ モードでは利用できないデータを使用していないことを確認する必要があります。

これは一般的な問題点であり、バックテストとドライ/ライブラン方法の間に大きな違いを引き起こす可能性があります。将来を見据えた戦略は、バックテストでは優れたパフォーマンスを示し、多くの場合、信じられないほどの利益や勝率をもたらしますが、実際の状況では失敗するか、パフォーマンスが低下します。

次のリストには、フラストレーションを防ぐために避けるべき一般的なパターンがいくつか含まれています。

- `shift(-1)` やその他の負の値を使用しないでください。これはバックテストで将来のデータを使用しますが、ドライ モードやライブ モードでは利用できません。
- `.iloc[-1]` やデータフレーム内の他の絶対位置を `populate_` 関数内で使用しないでください。これはドライランとバックテストでは異なるためです。ただし、絶対 `iloc` インデックスはコールバックで安全に使用できます。[Strategy Callbacks](strategy-callbacks.md) を参照してください。
- すべてのデータフレームまたは列の値を使用する関数は使用しないでください。 `dataframe['mean_volume'] = dataframe['volume'].mean()`。バックテストでは完全なデータフレームが使用されるため、データフレーム内のどの時点でも、「mean_volume」シリーズには将来のデータが含まれることになります。代わりに、rolling() 計算を使用してください。 `dataframe['volume'].rolling(<window>).mean()`。
- `.resample('1h')` は使用しないでください。これは期間間隔の左側の境界を使用するため、データを時間の境界から時間の先頭に移動します。代わりに `.resample('1h', label='right')` を使用してください。
- 長いタイムフレームを短いタイムフレームに結合するために `.merge()` を使用しないでください。代わりに、[情報ペア](#informative-pairs) ヘルパーを使用してください。 (日付は終了日ではなく開始日を参照するため、単純なマージでは暗黙的に先読みバイアスが発生する可能性があります)。

!!! Tip "問題の特定"
    常に 2 つのヘルパー コマンド [lookhead-analysis](lookahead-analysis.md) と [recursive-analysis](recursive-analysis.md) を使用する必要があります。これらはそれぞれ、さまざまな方法で戦略の問題を解決するのに役立ちます。
    それらをありのまま、つまり最も一般的な問題を特定するためのヘルパーとして扱ってください。それぞれの結果が否定的であっても、上記のエラーがまったく含まれていないことは保証されません。

### 信号の衝突
矛盾するシグナルが衝突する場合 (例: 「enter_long」 と 「exit_long」 の両方が「1」 に設定されている場合)、 freqtrade は何もせず、エントリーシグナルを無視します。これにより、エントリーしてすぐに終了する取引が回避されます。明らかに、これによりエントリが失われる可能性があります。

次のルールが適用され、3 つのシグナルのうち複数が設定されている場合、エントリーシグナルは無視されます。

- `enter_long` -> `exit_long`、`enter_short`
- `enter_short` -> `exit_short`、`enter_long`

## さらなる戦略のアイデア

戦略に関する追加のアイデアを入手するには、[戦略リポジトリ](https://github.com/freqtrade/freqtrade-strategies) にアクセスしてください。例として自由に使用できますが、結果は現在の市場状況、使用するペアなどによって異なります。したがって、これらの戦略は学習目的のみに考慮されるべきであり、現実世界の取引ではありません。まず交換/希望のペアの戦略をバックテストし、次に予行演習を行って慎重に評価し、ご自身の責任で使用してください。

独自の戦略のインスピレーションとして自由に使用してください。リポジトリへの新しい戦略を含むプル リクエストを喜んで受け入れます。

## 次のステップ

これで完璧な戦略が完成したので、それをバックテストしてみましょう。
次のステップは、[バックテストの使用方法](backtesting.md) を学習することです。
