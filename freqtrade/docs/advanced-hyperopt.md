# 高度なHyperopt

このページでは、通常のハイパーオプティマイゼーションクラスの作成よりも高度なコーディングスキルとPythonの知識が必要な、高度なHyperoptトピックについて説明します。

## カスタム損失関数の作成と使用

カスタム損失関数クラスを使用するには、カスタムハイパーオプト損失クラスで関数`hyperopt_loss_function`が定義されていることを確認してください。
以下のサンプルの場合、この関数が使用されるように、hyperopt呼び出しにコマンドラインパラメータ`--hyperopt-loss SuperDuperHyperOptLoss`を追加する必要があります。

以下にこのサンプルがあります。これはデフォルトのHyperopt損失実装と同じです。完全なサンプルは[userdata/hyperopts](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_loss.py)にあります。
``` python
from datetime import datetime
from typing import Any, Dict

from pandas import DataFrame

from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss

TARGET_TRADES = 600
EXPECTED_MAX_PROFIT = 3.0
MAX_ACCEPTED_TRADE_DURATION = 300

class SuperDuperHyperOptLoss(IHyperOptLoss):
    """
    Defines the default loss function for hyperopt
    """

    @staticmethod
    def hyperopt_loss_function(
        *,
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        processed: dict[str, DataFrame],
        backtest_stats: dict[str, Any],
        starting_balance: float,
        **kwargs,
    ) -> float:
        """
        Objective function, returns smaller number for better results
        This is the legacy algorithm (used until now in freqtrade).
        Weights are distributed as follows:
        * 0.4 to trade duration
        * 0.25: Avoiding trade loss
        * 1.0 to total profit, compared to the expected value (`EXPECTED_MAX_PROFIT`) defined above
        """
        total_profit = results['profit_ratio'].sum()
        trade_duration = results['trade_duration'].mean()

        trade_loss = 1 - 0.25 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - total_profit / EXPECTED_MAX_PROFIT)
        duration_loss = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)
        result = trade_loss + profit_loss + duration_loss
        return result
```
現在、引数は次のとおりです：

* `results`: 結果の取引を含むDataFrame。
    resultsでは次の列が利用可能です（`--export trades`で使用した場合のバックテストの出力ファイルに対応）：
    `pair, profit_ratio, profit_abs, open_date, open_rate, fee_open, close_date, close_rate, fee_close, amount, trade_duration, is_open, exit_reason, stake_amount, min_rate, max_rate, stop_loss_ratio, stop_loss_abs`
* `trade_count`: 取引数（`len(results)`と同じ）
* `min_date`: 使用されたタイムレンジの開始日
* `min_date`: 使用されたタイムレンジの終了日
* `config`: 使用されたConfigオブジェクト（注：ハイパーオプトスペースの一部である場合、すべてのストラテジー関連パラメータがここで更新されるわけではありません）。
* `processed`: バックテストに使用されたデータを含むペアをキーとするDataFrameのDict。
* `backtest_stats`: バックテストファイルの「strategy」サブ構造と同じ形式を使用したバックテスト統計。利用可能なフィールドは`optimize_reports.py`の`generate_strategy_stats()`で確認できます。
* `starting_balance`: バックテストに使用された開始残高。

この関数は浮動小数点数（`float`）を返す必要があります。より小さい数値は、より良い結果として解釈されます。これのパラメータとバランスはあなた次第です。

!!! Note
    この関数はエポックごとに1回呼び出されます - したがって、hyperoptを不必要に遅くしないように、これを可能な限り最適化してください。

!!! Note "`*args`と`**kwargs`"
    将来的にこのインターフェースを拡張できるように、引数`*args`と`**kwargs`をインターフェースに保持してください。

## 事前定義されたスペースのオーバーライド

事前定義されたスペース（`roi_space`、`generate_roi_table`、`stoploss_space`、`trailing_space`、`max_open_trades_space`）をオーバーライドするには、Hyperoptという名前のネストされたクラスを定義し、次のように必要なスペースを定義します：
```python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal

class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        # カスタムストップロススペースを定義します。
        def stoploss_space():
            return [SKDecimal(-0.05, -0.01, decimals=3, name='stoploss')]

        # カスタムROIスペースを定義
        def roi_space() -> List[Dimension]:
            return [
                Integer(10, 120, name='roi_t1'),
                Integer(10, 60, name='roi_t2'),
                Integer(10, 40, name='roi_t3'),
                SKDecimal(0.01, 0.04, decimals=3, name='roi_p1'),
                SKDecimal(0.01, 0.07, decimals=3, name='roi_p2'),
                SKDecimal(0.01, 0.20, decimals=3, name='roi_p3'),
            ]

        def generate_roi_table(params: Dict) -> dict[int, float]:

            roi_table = {}
            roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
            roi_table[params['roi_t3']] = params['roi_p1'] + params['roi_p2']
            roi_table[params['roi_t3'] + params['roi_t2']] = params['roi_p1']
            roi_table[params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

            return roi_table

        def trailing_space() -> List[Dimension]:
            # ここのすべてのパラメータは必須です。タイプまたは範囲のみを変更できます。
            return [
                # Trueに固定、trailing_stopを最適化する場合、常にtrailing stopを使用すると仮定します。
                Categorical([True], name='trailing_stop'),

                SKDecimal(0.01, 0.35, decimals=3, name='trailing_stop_positive'),
                # 'trailing_stop_positive_offset'は'trailing_stop_positive'より大きくする必要があるため、
                # この中間パラメータは、それらの間の差の値として使用されます。
                # 'trailing_stop_positive_offset'の値は、
                # generate_trailing_params()メソッドで構築されます。
                # これは、ROIテーブルを構築するために使用されるハイパースペース次元に似ています。
                SKDecimal(0.001, 0.1, decimals=3, name='trailing_stop_positive_offset_p1'),

                Categorical([True, False], name='trailing_only_offset_is_reached'),
        ]

        # カスタムmax_open_tradesスペースを定義
        def max_open_trades_space(self) -> List[Dimension]:
            return [
                Integer(-1, 10, name='max_open_trades'),
            ]
```
!!! Note
    すべてのオーバーライドはオプションであり、必要に応じて混合/照合できます。

### 動的パラメータ

パラメータは動的に定義することもできますが、[`bot_start()`コールバック](strategy-callbacks.md#bot-start)が呼び出されると、インスタンスで利用可能である必要があります。
``` python

class MyAwesomeStrategy(IStrategy):

    def bot_start(self, **kwargs) -> None:
        self.buy_adx = IntParameter(20, 30, default=30, optimize=True)

    # ...
```
!!! Warning
    この方法で作成されたパラメータは、`list-strategies`パラメータカウントに表示されません。

### ベースエスティメータのオーバーライド

Hyperoptサブクラスで`generate_estimator()`を実装することにより、Hyperopt用の独自のoptunaサンプラーを定義できます。
```python
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def generate_estimator(dimensions: List['Dimension'], **kwargs):
            return "NSGAIIISampler"

```
可能な値は、「NSGAIISampler」、「TPESampler」、「GPSampler」、「CmaEsSampler」、「NSGAIIISampler」、「QMCSampler」のいずれか（詳細は[optuna-samplersドキュメント](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html)にあります）、または「`optuna.samplers.BaseSampler`を継承するクラスのインスタンス」です。

たとえば、optunahubから追加のサンプラーを見つけるには、いくつかの調査が必要になります。

!!! Note
    カスタムエスティメータを提供できますが、可能なパラメータを調査し、どれを使用すべきかを分析/理解するのはユーザーとしてのあなた次第です。
    これについて不確かな場合は、さらなるパラメータなしでデフォルトの1つ（`"NSGAIIISampler"`は最も汎用的であることが証明されています）を使用するのが最善です。

??? Example "Optunahubから`AutoSampler`を使用"

    [AutoSamplerドキュメント](https://hub.optuna.org/samplers/auto_sampler/)

    必要な依存関係をインストール
    ``` bash
    pip install optunahub cmaes torch scipy
    ```
ストラテジーで`generate_estimator()`を実装
    ``` python
    # ...
    from freqtrade.strategy.interface import IStrategy
    from typing import List
    import optunahub
    # ...

    class my_strategy(IStrategy):
        class HyperOpt:
            def generate_estimator(dimensions: List["Dimension"], **kwargs):
                if "random_state" in kwargs.keys():
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler(seed=kwargs["random_state"])
                else:
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler()

    ```
明らかに、同じアプローチは、optunaがサポートする他のすべてのサンプラーで機能します。


## スペースオプション

追加のスペースについて、scikit-optimize（Freqtradeと組み合わせて）は次のスペースタイプを提供します：

* `Categorical` - カテゴリのリストから選択（例：`Categorical(['a', 'b', 'c'], name="cat")`）
* `Integer` - 整数の範囲から選択（例：`Integer(1, 10, name='rsi')`）
* `SKDecimal` - 限定された精度の小数の範囲から選択（例：`SKDecimal(0.1, 0.5, decimals=3, name='adx')`）。*Freqtradeでのみ利用可能*。
* `Real` - 完全な精度の小数の範囲から選択（例：`Real(0.1, 0.5, name='adx')`

これらすべてを`freqtrade.optimize.space`からインポートできますが、`Categorical`、`Integer`、`Real`は、対応するscikit-optimizeスペースの単なるエイリアスです。`SKDecimal`は、より高速な最適化のためにfreqtradeによって提供されています。
``` python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal, Real  # noqa
```
!!! Hint "SKDecimal と実数"
    ほとんどすべてのケースで、`Real`スペースの代わりに`SKDecimal`を使用することをお勧めします。Realスペースは完全な精度（最大約16桁）を提供しますが、この精度はほとんど必要なく、不必要に長いhyperopt時間につながります。

    かなり小さいスペースの定義を仮定（`SKDecimal(0.10, 0.15, decimals=2, name='xxx')`） - SKDecimalは5つの可能性（`[0.10, 0.11, 0.12, 0.13, 0.14, 0.15]`）を持ちます。

    一方、対応するrealスペース`Real(0.10, 0.15 name='xxx')`には、ほぼ無制限の数の可能性（`[0.10, 0.010000000001, 0.010000000002, ... 0.014999999999, 0.01500000000]`）があります。
