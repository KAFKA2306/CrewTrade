# 設定

FreqAI は、一般的な [Freqtrade 構成ファイル](configuration.md) と標準の [Freqtrade 戦略](strategy-customization.md) を通じて構成されます。 FreqAI の設定ファイルと戦略ファイルの例は、それぞれ「config_examples/config_freqai.example.json」と「freqtrade/templates/FreqaiExampleStrategy.py」にあります。

## 設定ファイルのセットアップ

 [パラメータ テーブル](freqai-parameter-table.md#parameter-table) で強調表示されているように、選択できる追加パラメータが多数ありますが、FreqAI 設定には少なくとも次のパラメータが含まれている必要があります (パラメータ値は単なる例です)。
```json
    "freqai": {
        "enabled": true,
        "purge_old_models": 2,
        "train_period_days": 30,
        "backtest_period_days": 7,
        "identifier" : "unique-id",
        "feature_parameters" : {
            "include_timeframes": ["5m","15m","4h"],
            "include_corr_pairlist": [
                "ETH/USD",
                "LINK/USD",
                "BNB/USD"
            ],
            "label_period_candles": 24,
            "include_shifted_candles": 2,
            "indicator_periods_candles": [10, 20]
        },
        "data_split_parameters" : {
            "test_size": 0.25
        }
    }
```
完全な設定例は「config_examples/config_freqai.example.json」で入手できます。

!!!注記
    「識別子」は初心者に見落とされがちですが、この値は構成において重要な役割を果たします。この値は、実行の 1 つを説明するために選択した一意の ID です。これを同じに保つことで、クラッシュ耐性を維持できるだけでなく、バ​​ックテストを高速化することができます。新しい実行 (新しい機能、新しいモデルなど) を試したい場合は、すぐにこの値を変更する必要があります (または、`user_data/models/unique-id` フォルダーを削除する必要があります。詳細については、[パラメーター テーブル](freqai-parameter-table.md#feature-parameters) を参照してください。

## FreqAI 戦略の構築

FreqAI 戦略では、標準 [Freqtrade 戦略](strategy-customization.md) に次のコード行を含める必要があります。
```python
    # user should define the maximum startup candle count (the largest number of candles
    # passed to any single indicator)
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # the model will return all labels created by user in `set_freqai_targets()`
        # (& appended targets), an indication of whether or not the prediction should be accepted,
        # the target mean/std values for each of the labels created by user in
        # `set_freqai_targets()` for each training period.

        dataframe = self.freqai.start(dataframe, metadata, self)

        return dataframe

    def feature_engineering_expand_all(self, dataframe: DataFrame, period, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """

        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        return dataframe

    def feature_engineering_expand_basic(self, dataframe: DataFrame, **kwargs) -> DataFrame:
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

        :param df: strategy dataframe which will receive the features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe

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

        :param df: strategy dataframe which will receive the features
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

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
`feature_engineering_*()` で [features](freqai-feature-engineering.md#feature-engineering) が追加される様子に注目してください。一方、`set_freqai_targets()` はラベル/ターゲットを追加します。戦略の完全な例は「templates/FreqaiExampleStrategy.py」で入手できます。

!!!注記
    `self.freqai.start()` 関数は `populate_indicators()` の外部から呼び出すことはできません。

!!!注記
    機能は「feature_engineering_*()」で定義する必要があります**。 `populate_indicators()` で FreqAI 機能を定義する
    アルゴリズムがライブ/ドライ モードで失敗する原因となります。特定のペアまたはタイムフレームに関連付けられていない一般化された機能を追加するには、「feature_engineering_standard()」を使用する必要があります。
    (「freqtrade/templates/FreqaiExampleStrategy.py」に例示されているように)。

## 重要なデータフレームのキーパターン

以下は、一般的な戦略データフレーム (`df[]`) 内に含める/使用することが予想される値です。

|  データフレームキー |説明 |
|-----------|---------------|
| `df['&*']` | `set_freqai_targets()` の先頭に `&` が付いたデータフレーム列は、FreqAI 内のトレーニング ターゲット (ラベル) として扱われます (通常、命名規則 `&-s*` に従います)。たとえば、40 キャンドル先の終値を予測するには、設定で `"label_period_candles": 40` を使用して `df['&-s_close'] = df['close'].shift(-self.freqai_info["feature_parameters"]["label_period_candles"])` を設定します。 FreqAI は予測を作成し、`populate_entry/exit_trend()` で使用される同じキー (`df['&-s_close']`) の下で予測を返します。 <br> **データ型:** モデルの出力によって異なります。
| `df['&*_std/mean']` |トレーニング中 (または `fit_live_predictions_candles` によるライブ トラッキング) 中の、定義されたラベルの標準偏差と平均値。一般的に、予測の希少性を理解するために使用されます (`templates/FreqaiExampleStrategy.py` に示されているように Z スコアを使用し、[ここ](#creating-a-dynamic-target-threshold) で説明されているように、特定の予測がトレーニング中または `fit_live_predictions_candles` を使用して履歴的に観察された頻度を評価します)。 <br> **データ型:** 浮動小数点数。
| `df['do_predict']` |外れ値のデータ ポイントを示します。戻り値は -2 から 2 までの整数であり、これにより予測が信頼できるかどうかがわかります。 `do_predict==1` は、予測が信頼できることを意味します。入力データポイントの相違指数 (DI、詳細は [こちら](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di)) が構成で定義されたしきい値を超えている場合、FreqAI は `do_predict` から 1 を減算し、結果として `do_predict==0` になります。 「use_SVM_to_remove_outliers」がアクティブな場合、サポート ベクター マシン (SVM、詳細は [こちら](freqai-feature-engineering.md#identifying-outliers-using-a-support-vector-machine-svm)) もトレーニング データと予測データの外れ値を検出する可能性があります。この場合、SVM は「do_predict」から 1 を減算します。入力データ ポイントが SVM によって外れ値とみなされたが DI によってはみなされなかった場合、またはその逆の場合、結果は `do_predict==0` になります。 DI と SVM の両方が入力データ ポイントを外れ値とみなした場合、結果は `do_predict==-1` になります。 SVM と同様に、`use_DBSCAN_to_remove_outliers` がアクティブな場合、DBSCAN (詳細は [こちら](freqai-feature-engineering.md#identifying-outliers-with-dbscan)) も異常値を検出し、`do_predict` から 1 を減算することがあります。したがって、SVM と DBSCAN の両方がアクティブで、DI しきい値を超えたデータポイントを外れ値として識別した場合、結果は「do_predict==-2」になります。特定のケースは `do_predict == 2` の場合で、これはモデルが `expired_hours` を超えたために期限切れになったことを意味します。 <br> **データ型:** -2 ～ 2 の整数。
| `df['DI_values']` |相違指数 (DI) 値は、FreqAI が予測において持つ信頼レベルの代用です。 DI が低いほど、予測がトレーニング データに近い、つまり予測の信頼度が高いことを意味します。 DI の詳細については、[こちら](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di) をご覧ください。 <br> **データ型:** 浮動小数点数。
| `df['%*']` | 「feature_engineering_*()」内の「%」が先頭に付加されたデータフレーム列は、トレーニング特徴として扱われます。たとえば、`df['%-rsi']` を設定することで、トレーニング機能セットに RSI を含めることができます (`templates/FreqaiExampleStrategy.py` と同様)。これがどのように行われるかについての詳細は、[こちら](freqai-feature-engineering.md) を参照してください。 <br> **注意:** `%` が先頭に付加された特徴量の数は非常に急速に増加する可能性があるため ([パラメータ テーブル](freqai-parameter-table.md) で説明されているように、`include_shifted_candles` や `include_timeframes` などの乗算機能を使用して数万の特徴量を簡単に設計できます)、これらの特徴量は FreqAI から返されるデータフレームから削除されます。戦略。特定のタイプのフィーチャをプロット目的で保持するには、先頭に `%%` を付加します (詳細は以下を参照)。 <br> **データ型:** ユーザーが作成した機能によって異なります。
| `df['%%*']` | `feature_engineering_*()` の `%%` が先頭に付加されたデータフレーム列は、上記の `%` が先頭に付加された場合とまったく同様に、トレーニング特徴として扱われます。ただし、この場合、フィーチャは、Dry/Live/Backtesting での FreqUI/plot-dataframe プロットおよびモニタリングの戦略に戻されます。<br> **データタイプ:** ユーザーが作成したフィーチャによって異なります。 `feature_engineering_expand()` で作成された機能には、設定した拡張に応じて自動 FreqAI 命名スキーマが設定されることに注意してください (つまり、`include_timeframes`、`include_corr_pairlist`、`indicators_periods_candles`、`include_shifted_candles`)。したがって、`feature_engineering_expand_all()` から `%%-rsi` をプロットしたい場合、プロット設定の最終的な命名スキームは、`period=10`、`timeframe=1h`、および `pair=ETH/USDT:USDT` の `rsi` 機能の場合は `%%-rsi-period_10_ETH/USDT:USDT_1h` になります。 (先物ペアを使用している場合は、「:USDT」が追加されます)。 `self.freqai.start()` の後の `populate_indicators()` に `print(dataframe.columns)` を追加するだけで、プロット目的でストラテジーに返される利用可能な機能の完全なリストを確認できます。

## `startup_candle_count` の設定

FreqAI 戦略の「startup_candle_count」は、標準の Freqtrade 戦略と同じ方法で設定する必要があります (詳細は [こちら](strategy-customization.md#strategy-startup-period) を参照してください)。この値は、最初のトレーニングの開始時に NaN が発生しないように、「dataprovider」を呼び出すときに十分な量のデータが提供されることを保証するために Freqtrade によって使用されます。この値は、インジケーター作成関数 (TA-Lib 関数など) に渡される最長期間 (ローソク足単位) を特定することで簡単に設定できます。提示された例では、「startup_candle_count」は 20 です。これは、「indicators_periods_candles」の最大値であるためです。

!!!注記
TA-Lib 関数が実際には、渡された「期間」よりも多くのデータを必要とする場合、そうでない場合はフィーチャ データセットに NaN が設定される場合があります。余談ですが、「startup_candle_count」を 2 で乗算すると、常に完全に NaN フリーのトレーニング データセットが得られます。したがって、通常は、予想される「startup_candle_count」を 2 倍するのが最も安全です。データがクリーンであることを確認するには、次のログ メッセージを確認してください。
    ```
    2022-08-31 15:14:04 - freqtrade.freqai.data_kitchen - INFO - dropped 0 training points due to NaNs in populated dataset 4319.
    ```
## 動的なターゲットしきい値の作成

いつ取引に参加するか取引を終了するかを決定することは、現在の市場状況を反映して動的に行うことができます。 FreqAI を使用すると、モデルのトレーニングから追加情報を返すことができます (詳細は [こちら](freqai-feature-engineering.md#returning-Additional-info-from-training))。たとえば、「&*_std/mean」の戻り値は、*最新のトレーニング*中のターゲット/ラベルの統計的分布を表します。特定の予測をこれらの値と比較することで、予測の希少性を知ることができます。 `templates/FreqaiExampleStrategy.py` では、`target_roi` と `sell_roi` が平均から 1.25 Z スコア離れているように定義されており、平均に近い予測がフィルターで除外されます。
```python
dataframe["target_roi"] = dataframe["&-s_close_mean"] + dataframe["&-s_close_std"] * 1.25
dataframe["sell_roi"] = dataframe["&-s_close_mean"] - dataframe["&-s_close_std"] * 1.25
```
上で説明したトレーニングからの情報ではなく、動的ターゲットを作成するための *履歴予測* の母集団を考慮するには、構成内の `fit_live_predictions_candles` を、ターゲット統計の生成に使用する履歴予測ローソク足の数に設定します。
```json
    "freqai": {
        "fit_live_predictions_candles": 300,
    }
```
この値が設定されている場合、FreqAI は最初にトレーニング データからの予測を使用し、その後生成された実際の予測データの導入を開始します。 FreqAI は、同じ「識別子」を持つモデルを停止して再起動した場合に再ロードされるように、この履歴データを保存します。

## さまざまな予測モデルの使用

FreqAI には、フラグ `--freqaimodel` を使用してそのまま使用できる複数の予測モデル ライブラリの例があります。これらのライブラリには、`CatBoost`、`LightGBM`、および `XGBoost` 回帰、分類、およびマルチターゲット モデルが含まれており、`freqai/prediction_models/` にあります。

回帰モデルと分類モデルは、予測するターゲットが異なります。回帰モデルは、たとえば明日の BTC の価格など、連続値のターゲットを予測しますが、分類子は、たとえば、BTC の価格が明日上がるかどうかなど、離散的な値のターゲットを予測します。これは、使用しているモデル タイプに応じてターゲットを異なる方法で指定する必要があることを意味します (詳細は[下記](#setting-model-targets)を参照してください)。

前述のモデル ライブラリはすべて、勾配ブースト決定木アルゴリズムを実装しています。これらはすべてアンサンブル学習の原理に基づいて機能し、複数の単純な学習器からの予測を組み合わせて、より安定して一般化された最終予測を取得します。この場合の単純な学習者は決定木です。勾配ブースティングとは、各単純な学習器が順番に構築される学習方法を指します。後続の学習器は、前の学習器からの誤差を改善するために使用されます。さまざまなモデル ライブラリについて詳しく知りたい場合は、それぞれのドキュメントで情報を見つけることができます。

* CatBoost: https://catboost.ai/ja/docs/
* LightGBM: https://lightgbm.readthedocs.io/en/v3.3.2/#
* XGBoost: https://xgboost.readthedocs.io/en/stable/#

アルゴリズムを説明および比較するオンライン記事も多数あります。比較的軽量な例としては、[CatBoost vs. LightGBM vs. XGBoost — どれが最適ですか?] などがあります。アルゴリズム?](https://towardsdatascience.com/catboost-vs-lightgbm-vs-xgboost-c80f40662924#:~:text=In%20CatBoost%2C%20対称%20trees%2C%20or,the%20same%20 Depth%20can%20differ.) および [XGBoost、LightGBM、または CatBoost — どのブーストを行うかアルゴリズムを使用する必要がありますか?](https://medium.com/riskified-technology/xgboost-lightgbm-or-catboost-what-boosting-algorithm-Should-i-use-e7fda7bb36bc)。各モデルのパフォーマンスはアプリケーションに大きく依存するため、報告されるメトリクスはモデルの特定の用途には当てはまらない可能性があることに注意してください。
FreqAI ですでに利用可能なモデルとは別に、`IFreqaiModel` クラスを使用して独自の予測モデルをカスタマイズして作成することもできます。トレーニング手順のさまざまな側面をカスタマイズするには、`fit()`、`train()`、および `predict()` を継承することをお勧めします。カスタム FreqAI モデルを `user_data/freqaimodels` に配置できます。freqtrade は、指定された `--freqaimodel` 名に基づいてそこからモデルを取得します。この名前はカスタム モデルのクラス名に対応する必要があります。
組み込みモデルをオーバーライドしないように、必ず一意の名前を使用してください。

### モデルターゲットの設定

#### リグレッサー

リグレッサーを使用している場合は、連続値を持つターゲットを指定する必要があります。 FreqAI には、フラグ「--freqaimodel CatboostRegressor」を使用した「CatboostRegressor」など、さまざまなリグレッサーが含まれています。 100 キャンドル先の価格を予測するための回帰ターゲットを設定する方法の例は、次のようになります。
```python
df['&s-close_price'] = df['close'].shift(-100)
```
複数のターゲットを予測する場合は、上記と同じ構文を使用して複数のラベルを定義する必要があります。

#### 分類子

分類子を使用している場合は、離散値を持つターゲットを指定する必要があります。 FreqAI には、フラグ `--freqaimodel CatboostClassifier` を介した `CatboostClassifier` など、さまざまな分類器が含まれています。分類子の使用を選択した場合は、文字列を使用してクラスを設定する必要があります。たとえば、100 ローソク足の将来の価格が上がるか下がるかを予測したい場合は、次のように設定します。
```python
df['&s-up_or_down'] = np.where( df["close"].shift(-100) > df["close"], 'up', 'down')
```
複数のターゲットを予測する場合は、すべてのラベルを同じラベル列に指定する必要があります。たとえば、ラベル「同じ」を追加して、設定によって価格が変更されなかった場所を定義できます。
```python
df['&s-up_or_down'] = np.where( df["close"].shift(-100) > df["close"], 'up', 'down')
df['&s-up_or_down'] = np.where( df["close"].shift(-100) == df["close"], 'same', df['&s-up_or_down'])
```
## PyTorch モジュール

### クイックスタート

pytorch モデルをすばやく実行する最も簡単な方法は、次のコマンド (回帰タスク用) を使用することです。
```bash
freqtrade trade --config config_examples/config_freqai.example.json --strategy FreqaiExampleStrategy --freqaimodel PyTorchMLPRegressor --strategy-path freqtrade/templates 
```
!!! 「インストール/ドッカー」に注意してください
    PyTorch モジュールには、「torch」などの大きなパッケージが必要です。これは、「freqai-rl または PyTorch の依存関係も必要ですか (~700mb の追加スペースが必要です) [y/N]?」という質問に「y」と答えることで、「./setup.sh -i」中に明示的に要求する必要があります。
    docker を好むユーザーは、`_freqaitorch` が追加された docker イメージを使用する必要があります。
    このための明示的な docker-compose ファイルを `docker/docker-compose-freqai.yml` で提供します。これは、`docker compose -f docker/docker-compose-freqai.yml run ...` 経由で使用できます。または、コピーして元の docker ファイルを置き換えることもできます。
    この docker-compose ファイルには、docker コンテナー内の GPU リソースを有効にする (無効な) セクションも含まれています。これは明らかに、システムに利用可能な GPU リソースがあることを前提としています。

    PyTorch は、バージョン 2.3 で macOS x64 (Intel ベースの Apple デバイス) のサポートを終了しました。その後、freqtrade もこのプラットフォームでの PyTorch のサポートを終了しました。

### 構造

#### モデル

カスタム [`IFreqaiModel` ファイル](#using- Different-prediction-models) 内で `nn.Module` クラスを定義し、そのクラスを `def train()` 関数で使用するだけで、PyTorch で独自のニューラル ネットワーク アーキテクチャを構築できます。以下は、分類タスクに PyTorch (nn.BCELoss 基準とともに使用する必要があります) を使用したロジスティック回帰モデルの実装の例です。
```python

class LogisticRegression(nn.Module):
    def __init__(self, input_size: int):
        super().__init__()
        # Define your layers
        self.linear = nn.Linear(input_size, 1)
        self.activation = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Define the forward pass
        out = self.linear(x)
        out = self.activation(out)
        return out

class MyCoolPyTorchClassifier(BasePyTorchClassifier):
    """
    This is a custom IFreqaiModel showing how a user might setup their own 
    custom Neural Network architecture for their training.
    """

    @property
    def data_convertor(self) -> PyTorchDataConvertor:
        return DefaultPyTorchDataConvertor(target_tensor_type=torch.float)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        config = self.freqai_info.get("model_training_parameters", {})
        self.learning_rate: float = config.get("learning_rate",  3e-4)
        self.model_kwargs: dict[str, Any] = config.get("model_kwargs",  {})
        self.trainer_kwargs: dict[str, Any] = config.get("trainer_kwargs",  {})

    def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :param data_dictionary: the dictionary holding all data for train, test,
            labels, weights
        :param dk: The datakitchen object for the current coin/model
        """

        class_names = self.get_class_names()
        self.convert_label_column_to_int(data_dictionary, dk, class_names)
        n_features = data_dictionary["train_features"].shape[-1]
        model = LogisticRegression(
            input_dim=n_features
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.CrossEntropyLoss()
        init_model = self.get_init_model(dk.pair)
        trainer = PyTorchModelTrainer(
            model=model,
            optimizer=optimizer,
            criterion=criterion,
            model_meta_data={"class_names": class_names},
            device=self.device,
            init_model=init_model,
            data_convertor=self.data_convertor,
            **self.trainer_kwargs,
        )
        trainer.fit(data_dictionary, self.splits)
        return trainer

```
#### トレーナー

`PyTorchModelTrainer` は、慣用的な PyTorch トレイン ループを実行します。
モデル、損失関数、オプティマイザーを定義し、それらを適切なデバイス (GPU または CPU) に移動します。ループ内では、データローダーのバッチを反復処理し、データをデバイスに移動し、予測と損失を計算し、逆伝播し、オプティマイザーを使用してモデル パラメーターを更新します。 

さらに、トレーナーは次の責任を負います。
 - モデルの保存とロード
 - データを `pandas.DataFrame` から `torch.Tensor` に変換します。 

#### Freqai モジュールとの統合 

すべての freqai モデルと同様、PyTorch モデルは `IFreqaiModel` を継承します。 `IFreqaiModel` は 3 つの抽象メソッド、`train`、`fit`、および `predict` を宣言します。これらのメソッドを 3 つの階層レベルで実装します。
上から下へ:

1. `BasePyTorchModel` - `train` メソッドを実装します。すべての `BasePyTorch*` はそれを継承します。一般的なデータの準備 (データの正規化など) と「fit」メソッドの呼び出しを担当します。子クラスで使用される `device` 属性を設定します。親クラスで使用される `model_type` 属性を設定します。
2. `BasePyTorch*` - `predict` メソッドを実装します。ここで、「*」は分類子やリグレッサーなどのアルゴリズムのグループを表します。必要に応じてデータの前処理、予測、後処理を担当します。
3. `PyTorch*Classifier` / `PyTorch*Regressor` - `fit` メソッドを実装します。これは、トレーナーとモデル オブジェクトを初期化するトレインの主な欠陥の原因です。

![画像](assets/freqai_pytorch-diagram.png)

#### 完全な例

MLP (多層パーセプトロン) モデル、MSELoss 基準、および AdamW オプティマイザーを使用して PyTorch リグレッサーを構築します。
```python
class PyTorchMLPRegressor(BasePyTorchRegressor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        config = self.freqai_info.get("model_training_parameters", {})
        self.learning_rate: float = config.get("learning_rate",  3e-4)
        self.model_kwargs: dict[str, Any] = config.get("model_kwargs",  {})
        self.trainer_kwargs: dict[str, Any] = config.get("trainer_kwargs",  {})

    def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        n_features = data_dictionary["train_features"].shape[-1]
        model = PyTorchMLPModel(
            input_dim=n_features,
            output_dim=1,
            **self.model_kwargs
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.MSELoss()
        init_model = self.get_init_model(dk.pair)
        trainer = PyTorchModelTrainer(
            model=model,
            optimizer=optimizer,
            criterion=criterion,
            device=self.device,
            init_model=init_model,
            target_tensor_type=torch.float,
            **self.trainer_kwargs,
        )
        trainer.fit(data_dictionary)
        return trainer
```
ここでは、`fit` メソッドを実装する `PyTorchMLPRegressor` クラスを作成します。 「fit」メソッドは、トレーニングの構成要素 (モデル、オプティマイザー、基準、トレーナー) を指定します。 `BasePyTorchRegressor` と `BasePyTorchModel` の両方を継承します。前者は回帰タスクに適した `predict` メソッドを実装し、後者は train メソッドを実装します。

???注「分類子のクラス名の設定」
    分類子を使用する場合、ユーザーは `IFreqaiModel.class_names` 属性をオーバーライドしてクラス名 (またはターゲット) を宣言する必要があります。これは、「set_freqai_targets」メソッド内の FreqAI ストラテジーで「self.freqai.class_names」を設定することで実現されます。
    
    たとえば、バイナリ分類子を使用して価格変動を上昇または下降として予測する場合、クラス名を次のように設定できます。
    ```python
    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        self.freqai.class_names = ["down", "up"]
        dataframe['&s-up_or_down'] = np.where(dataframe["close"].shift(-100) >
                                                  dataframe["close"], 'up', 'down')
    
        return dataframe
    ```
完全な例を確認するには、[分類子テスト戦略クラス](https://github.com/freqtrade/freqtrade/blob/develop/tests/strategy/strats/freqai_test_classifier.py) を参照してください。


#### `torch.compile()` によるパフォーマンスの向上

Torch は、特定の GPU ハードウェアのパフォーマンスを向上させるために使用できる `torch.compile()` メソッドを提供します。詳細については、[こちら](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)をご覧ください。簡単に言うと、「model」を「torch.compile()」でラップするだけです。
```python
        model = PyTorchMLPModel(
            input_dim=n_features,
            output_dim=1,
            **self.model_kwargs
        )
        model.to(self.device)
        model = torch.compile(model)
```
その後、モデルを通常どおり使用します。これを行うと積極的な実行が削除されるため、エラーやトレースバックは有益ではなくなることに注意してください。
