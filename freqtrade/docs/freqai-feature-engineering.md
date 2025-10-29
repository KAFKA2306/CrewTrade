# 特徴量エンジニアリング

## 機能の定義

低レベルの特徴量エンジニアリングは、「feature_engineering_*」と呼ばれる一連の関数内のユーザー ストラテジーで実行されます。これらの関数は、「RSI」、「MFI」、「EMA」、「SMA」、時刻、出来高などの「基本特徴」を設定します。「基本特徴」はカスタム指標にすることも、見つけられるテクニカル分析ライブラリからインポートすることもできます。 FreqAI には、迅速な大規模な特徴量エンジニアリングを簡素化するための一連の機能が装備されています。

|  機能 |説明 |
|--------------|---------------|
| `feature_engineering_expand_all()` |このオプション関数は、設定で定義された `indicator_periods_candles`、`include_timeframes`、`include_shifted_candles`、および `include_corr_pairs` で定義された機能を自動的に展開します。
| `feature_engineering_expand_basic()` |このオプション関数は、設定で定義された `include_timeframes`、`include_shifted_candles`、および `include_corr_pairs` で定義された機能を自動的に拡張します。注: この関数は「indicator_periods_candles」全体に拡張*しません*。
| `feature_engineering_standard()` |このオプションの関数は、基本タイムフレームのデータフレームで 1 回呼び出されます。これは呼び出される最後の関数です。つまり、この関数に入るデータフレームには、他の `feature_engineering_expand` 関数によって作成されたベース アセットのすべてのフィーチャと列が含まれることになります。この関数は、カスタムのエキゾチックな特徴抽出 (tsfresh など) を行うのに適しています。この関数は、自動展開すべきではない機能 (曜日など) にも適しています。
| `set_freqai_targets()` |モデルのターゲットを設定するために必要な関数。 FreqAI 内部で認識されるように、すべてのターゲットの前に「&」を付ける必要があります。

一方、高レベルの特徴エンジニアリングは、FreqAI 設定の「feature_parameters」:{}` 内で処理されます。このファイル内では、「相関ペアを含む」、「有益なタイムフレームを含む」、さらには「最近のローソク足を含む」など、「base_features」に加えて大規模な機能拡張を決定することができます。

機能定義が正しい規則に従っていることを確認するために、ソースが提供する戦略例 (`templates/FreqaiExampleStrategy.py` にあります) 内のテンプレート `feature_engineering_*` 関数から開始することをお勧めします。以下は、戦略でインジケーターとラベルを設定する方法の例です。
```python
    def feature_engineering_expand_all(self, dataframe: DataFrame, period, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        Access metadata such as the current pair/timeframe/period with:

        `metadata["pair"]` `metadata["tf"]`  `metadata["period"]`

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        :param metadata: metadata of current pair
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

    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
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

        Access metadata such as the current pair/timeframe with:

        `metadata["pair"]` `metadata["tf"]`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param metadata: metadata of current pair
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe

    def feature_engineering_standard(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This optional function will be called once with the dataframe of the base timeframe.
        This is the final function to be called, which means that the dataframe entering this
        function will contain all the features and columns created by all other
        freqai_feature_engineering_* functions.

        This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
        This function is a good place for any feature that should not be auto-expanded upon
        (e.g. day of the week).

        Access metadata such as the current pair with:

        `metadata["pair"]`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param metadata: metadata of current pair
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        Access metadata such as the current pair with:

        `metadata["pair"]`

        :param df: strategy dataframe which will receive the targets
        :param metadata: metadata of current pair
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
提示された例では、ユーザーは `bb_ lowerband` を特徴としてモデルに渡したくありません。
したがって、先頭に「%」を付けていません。ただし、ユーザーは `bb_width` を
トレーニング/予測用のモデルなので、先頭に「%」が付加されています。

「基本機能」を定義したら、次のステップは、構成ファイル内の強力な「feature_parameters」を使用してそれらを拡張することです。
```json
    "freqai": {
        //...
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
        //...
    }
```
上記の設定の `include_timeframes` は、ストラテジー内の `feature_engineering_expand_*()` への各呼び出しのタイムフレーム (`tf`) です。ここで示したケースでは、ユーザーは機能セットに含める「rsi」、「mfi」、「roc」、および「bb_width」の「5m」、「15m」、および「4h」タイムフレームを要求しています。

「include_corr_pairlist」を使用して、定義された各機能を情報ペアにも含めるように要求できます。これは、機能セットには、構成で定義された相関ペア (提示された例では「ETH/USD」、「LINK/USD」、および「BNB/USD」) のすべての「include_timeframes」にある「feature_engineering_expand_*()」のすべての機能が含まれることを意味します。

`include_shifted_candles` は、機能セットに含める以前のキャンドルの数を示します。たとえば、「include_shifted_candles: 2」は、機能セット内の各機能の過去 2 つのローソク足を含めるよう FreqAI に指示します。

提示された戦略例のユーザーが作成したフィーチャの合計数は、「include_timeframes」の長さ * 数になります。 `feature_engineering_expand_*()` の機能 * `include_corr_pairlist` の長さ * いいえ。 `include_shifted_candles` * `indicator_periods_candles` の長さ
 $= 3 * 3 * 3 * 2 * 2 = 108$。
 
!!! note「クリエイティブ特徴量エンジニアリングについて詳しく学ぶ」
    ユーザーが創造的に機能を設計する方法を学習できるようにすることを目的とした [中記事](https://emergentmethods.medium.com/freqai-from-price-to-prediction-6fadac18b665) をご覧ください。

### `metadata` を使用して `feature_engineering_*` 関数をより細かく制御します

すべての `feature_engineering_*` および `set_freqai_targets()` 関数には、FreqAI が機能構築のために自動化している `pair`、`tf` (タイムフレーム)、および `period` に関する情報を含む `metadata` 辞書が渡されます。そのため、ユーザーは特定の時間枠、期間、ペアなどの機能をブロック/予約する基準として「feature_engineering_*」関数内の「メタデータ」を使用できます。
```python
def feature_engineering_expand_all(self, dataframe: DataFrame, period, metadata, **kwargs) -> DataFrame:
    if metadata["tf"] == "1h":
        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
```
これにより、`ta.ROC()` が `"1h"` 以外のタイムフレームに追加されることがブロックされます。

### トレーニングから追加情報を返す

重要なメトリックは、カスタム予測モデル クラス内の `dk.data['extra_returns_per_train']['my_new_value'] = XYZ` に割り当てることで、各モデルのトレーニングの最後に戦略に返すことができます。 

FreqAI は、このディクショナリに割り当てられた `my_new_value` を取得し、ストラテジーに返されるデータフレームに適合するようにそれを拡張します。その後、「dataframe['my_new_value']」を通じて、返されたメトリクスを戦略で使用できます。 FreqAI で戻り値をどのように使用できるかの例は、[動的ターゲットしきい値の作成](freqai-configuration.md#creating-a-dynamic-target-threshold) に使用される `&*_mean` 値と `&*_std` 値です。

ユーザーが取引データベースからのライブ指標を使用したい別の例を以下に示します。
```json
    "freqai": {
        "extra_returns_per_train": {"total_profit": 4}
    }
```
FreqAI が適切なデータフレーム形状を返すことができるように、構成で標準辞書を設定する必要があります。これらの値は予測モデルによってオーバーライドされる可能性がありますが、モデルがまだ値を設定していない場合、またはデフォルトの初期値が必要な場合には、事前に設定された値が返されます。

### 時間的重要性に対する特徴の重み付け

FreqAI を使用すると、指数関数を使用して過去のデータよりも最近のデータに重み付けを強くする「weight_factor」を設定できます。

$$ W_i = \exp(\frac{-i}{\alpha*n}) $$

ここで、$W_i$ は、$n$ データ ポイントの合計セット内のデータ ポイント $i$ の重みです。以下の図は、特徴セット内のデータ ポイントに対するさまざまな重み係数の影響を示しています。

![ウェイトファクター](assets/freqai_weight-factor.jpg)

## データ パイプラインの構築

デフォルトでは、FreqAI はユーザー構成設定に基づいて動的パイプラインを構築します。デフォルト設定は堅牢で、さまざまな方法で動作するように設計されています。これら 2 つのステップは、`MinMaxScaler(-1,1)` と、分散が 0 の列を削除する `VarianceThreshold` です。ユーザーは、より多くの構成パラメータを使用して他のステップをアクティブ化できます。たとえば、ユーザーが「use_SVM_to_remove_outliers: true」を「freqai」設定に追加すると、FreqAI は自動的に [`SVMOutlierExtractor`](#identifying-outliers-using-a-support-vector-machine-svm) をパイプラインに追加します。同様に、ユーザーは「principal_component_analysis: true」を「freqai」設定に追加して PCA をアクティブ化できます。 [DissimilarityIndex](#identifying-outliers-with-the-dissimilarity-index-di) は、「DI_threshold: 1」でアクティブになります。最後に、「noise_standard_deviation: 0.1」を使用してデータにノイズを追加することもできます。最後に、ユーザーは「use_DBSCAN_to_remove_outliers: true」を使用して [DBSCAN](#identifying-outliers-with-dbscan) 外れ値の除去を追加できます。

!!!注「さらに詳しい情報が利用可能です」
    これらのパラメータの詳細については、[パラメータ テーブル](freqai-parameter-table.md)を参照してください。


### パイプラインのカスタマイズ

ユーザーは、独自のデータ パイプラインを構築して、ニーズに合わせてデータ パイプラインをカスタマイズすることをお勧めします。これは、`IFreqaiModel` の `train()` 関数内の目的の `Pipeline` オブジェクトに `dk.feature_pipeline` を設定するだけで実行できます。または、`train()` 関数に触れたくない場合は、`IFreqaiModel` の `define_data_pipeline`/`define_label_pipeline` 関数をオーバーライドすることもできます。

!!!注「さらに詳しい情報が利用可能です」
    FreqAI は [`DataSieve`](https://github.com/emergentmethods/datasieve) パイプラインを使用します。これは SKlearn パイプライン API に従いますが、他の機能の中でも、X、y、sample_weight ベクトル点の削除、特徴の削除、特徴名の後の一貫性が追加されています。
```python
from datasieve.transforms import SKLearnWrapper, DissimilarityIndex
from datasieve.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer, StandardScaler
from freqai.base_models import BaseRegressionModel


class MyFreqaiModel(BaseRegressionModel):
    """
    Some cool custom model
    """
    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        My custom fit function
        """
        model = cool_model.fit()
        return model

    def define_data_pipeline(self) -> Pipeline:
        """
        User defines their custom feature pipeline here (if they wish)
        """
        feature_pipeline = Pipeline([
            ('qt', SKLearnWrapper(QuantileTransformer(output_distribution='normal'))),
            ('di', ds.DissimilarityIndex(di_threshold=1))
        ])

        return feature_pipeline
    
    def define_label_pipeline(self) -> Pipeline:
        """
        User defines their custom label pipeline here (if they wish)
        """
        label_pipeline = Pipeline([
            ('qt', SKLearnWrapper(StandardScaler())),
        ])

        return label_pipeline
```
ここでは、トレーニングと予測中に機能セットに使用される正確なパイプラインを定義しています。上に示したように、「SKLearnWrapper」クラスでラップすることで、*ほとんどの* SKLearn 変換ステップを使用できます。さらに、[`DataSieve` ライブラリ](https://github.com/emergentmethods/datasieve) で利用可能な変換を使用できます。 

データシーブの `BaseTransform` から継承するクラスを作成し、`fit()`、`transform()`、および `inverse_transform()` メソッドを実装することで、独自の変換を簡単に追加できます。
```python
from datasieve.transforms.base_transform import BaseTransform
# import whatever else you need

class MyCoolTransform(BaseTransform):
    def __init__(self, **kwargs):
        self.param1 = kwargs.get('param1', 1)

    def fit(self, X, y=None, sample_weight=None, feature_list=None, **kwargs):
        # do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list

    def transform(self, X, y=None, sample_weight=None,
                  feature_list=None, outlier_check=False, **kwargs):
        # do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list

    def inverse_transform(self, X, y=None, sample_weight=None, feature_list=None, **kwargs):
        # do/dont do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list
```
!!! 「ヒント」に注意してください
    このカスタム クラスは、`IFreqaiModel` と同じファイルで定義できます。

### カスタム `IFreqaiModel` を新しいパイプラインに移行する

カスタム `train()`/`predict()` 関数を使用して独自のカスタム `IFreqaiModel` を作成し、*かつ* まだ `data_cleaning_train/predict()` に依存している場合は、新しいパイプラインに移行する必要があります。モデルが `data_cleaning_train/predict()` に依存していない場合は、この移行について心配する必要はありません。

移行の詳細については、[こちら](strategy_migration.md#freqai-new-data-pipeline)をご覧ください。

## 外れ値の検出

株式市場と仮想通貨市場は、異常値のデータポイントという形での高レベルの非パターンノイズに悩まされています。 FreqAI は、そのような外れ値を特定し、リスクを軽減するためのさまざまな方法を実装しています。

### 相違指数 (DI) を使用した外れ値の特定

相違指数 (DI) は、モデルによって行われた各予測に関連する不確実性を定量化することを目的としています。 

構成に次のステートメントを含めることで、DI を使用してトレーニング/テスト データ セットから異常値データ ポイントを削除するように FreqAI に指示できます。
```json
    "freqai": {
        "feature_parameters" : {
            "DI_threshold": 1
        }
    }
```
これにより、`DissimilarityIndex` ステップが `feature_pipeline` に追加され、しきい値が 1 に設定されます。DI を使用すると、外れ値 (モデルの特徴空間に存在しない) の予測を、確実性のレベルが低いために除外できます。これを行うために、FreqAI は、各トレーニング データ ポイント (特徴ベクトル)、$X_{a}$、および他のすべてのトレーニング データ ポイント間の距離を測定します。

$$ d_{ab} = \sqrt{\sum_{j=1}^p(X_{a,j}-X_{b,j})^2} $$

ここで、$d_{ab}$ は正規化された点 $a$ と $b$ の間の距離、$p$ は特徴の数、つまりベクトル $X$ の長さです。一連のトレーニング データ ポイントの特性距離 $\overline{d}$ は、単に平均距離の平均です。

$$ \overline{d} = \sum_{a=1}^n(\sum_{b=1}^n(d_{ab}/n)/n) $$

$\overline{d}$ はトレーニング データの広がりを定量化します。これは、新しい予測特徴ベクトル $X_k$ とすべてのトレーニング データの間の距離と比較されます。

$$ d_k = \arg \min d_{k,i} $$

これにより、次のような相違指数の推定が可能になります。

$$ DI_k = d_k/\overline{d} $$

「DI_threshold」を通じて DI を微調整して、トレーニング済みモデルの外挿を増減させることができます。より高い「DI_threshold」は、DI がより寛大で、トレーニング データからさらに離れた予測を使用できることを意味しますが、より低い「DI_threshold」は逆の効果があり、より多くの予測が破棄されます。

以下は、3D データセットの DI を説明する図です。

![DI](assets/freqai_DI.jpg)

### サポート ベクター マシン (SVM) を使用した外れ値の特定

次のステートメントを構成に含めることで、サポート ベクター マシン (SVM) を使用してトレーニング/テスト データ セットから異常値データ ポイントを削除するように FreqAI に指示できます。
```json
    "freqai": {
        "feature_parameters" : {
            "use_SVM_to_remove_outliers": true
        }
    }
```
これにより、「SVMOutlierExtractor」ステップが「feature_pipeline」に追加されます。 SVM はトレーニング データに基づいてトレーニングされ、SVM が特徴空間を超えているとみなしたデータ ポイントは削除されます。

構成内の「feature_parameters.svm_params」ディクショナリを介して、「shuffle」や「nu」などの追加パラメータを SVM に提供することを選択できます。

パラメータ「shuffle」は、一貫した結果を保証するためにデフォルトで「False」に設定されています。 「True」に設定されている場合、同じデータセットに対して SVM を複数回実行すると、アルゴリズムが要求された「tol」に達するには「max_iter」が低すぎるため、異なる結果が生じる可能性があります。 `max_iter` を増やすとこの問題は解決しますが、手順にかかる時間が長くなります。

パラメーター `nu` は、*非常に*広範に、外れ値とみなされるデータ ポイントの量であり、0 から 1 の間にある必要があります。

### DBSCAN による外れ値の特定

設定で「use_DBSCAN_to_remove_outliers」を有効にすることで、DBSCAN を使用してトレーニング/テスト データ セットから外れ値をクラスタリングして削除したり、予測から受信した外れ値を削除したりするように FreqAI を設定できます。
```json
    "freqai": {
        "feature_parameters" : {
            "use_DBSCAN_to_remove_outliers": true
        }
    }
```
これにより、「DataSieveDBSCAN」ステップが「feature_pipeline」に追加されます。これは、必要なクラスターの数を知る必要なく、データをクラスター化する教師なし機械学習アルゴリズムです。

データ ポイントの数 $N$ と距離 $\varepsilon$ が与えられると、DBSCAN は $\varepsilon$ の距離内に $N-1$ 個の他のデータ ポイントを持つすべてのデータ ポイントを *コア ポイント* として設定することによってデータ セットをクラスター化します。 *コア ポイント*から $\varepsilon$ の距離内にあるが、それ自体から $\varepsilon$ の距離内に $N-1$ 個の他のデータ ポイントがないデータ ポイントは、*エッジ ポイント*とみなされます。クラスターは、*コア ポイント* と *エッジ ポイント* の集合になります。 $<\varepsilon$ の距離に他のデータ ポイントがないデータ ポイントは外れ値とみなされます。以下の図は、$N = 3$ のクラスターを示しています。

![dbscan](assets/freqai_dbscan.jpg)

FreqAI は `sklearn.cluster.DBSCAN` (詳細は scikit-learn の Web ページ [こちら](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) (外部 Web サイト) で参照できます) を使用し、`min_samples` ($N$) を no.1 の 1/4 として使用します。特徴セット内の時点 (ローソク足) の数。 `eps` ($\varepsilon$) は、特徴セット内のすべてのデータ ポイントのペアごとの距離の最近傍から計算される *k 距離グラフ* のエルボ ポイントとして自動的に計算されます。


### 主成分分析によるデータの次元削減

構成でプリンシパル_コンポーネント_分析を有効にすることで、機能の次元を減らすことができます。
```json
    "freqai": {
        "feature_parameters" : {
            "principal_component_analysis": true
        }
    }
```
これにより、特徴に対して PCA が実行され、データ セットの説明分散が 0.999 以上になるように次元が削減されます。データの次元を削減すると、モデルのトレーニングが高速化されるため、より最新のモデルを使用できるようになります。
