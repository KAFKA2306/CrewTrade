# ハイパーオプト

このページでは、最適な戦略を見つけて戦略を調整する方法について説明します。
パラメータ、ハイパーパラメータ最適化と呼ばれるプロセス。ボットは、「optuna」パッケージに含まれるアルゴリズムを使用してこれを実現します。
検索するとすべての CPU コアが消費され、ラップトップの音が戦闘機のように聞こえますが、それでも長い時間がかかります。

一般に、最適なパラメーターの検索は、いくつかのランダムな組み合わせ (詳細については [下記](#reproducible-results) を参照) から始まり、次に optuna のサンプラー アルゴリズム (現在は NSGAIIISampler) の 1 つを使用して、[損失関数] (#loss-functions) の値を最小化する検索ハイパースペース内のパラメーターの組み合わせをすばやく見つけます。

Hyperopt では、バックテストと同様に、履歴データが利用可能であることが必要です (hyperopt は、さまざまなパラメーターを使用してバックテストを何度も実行します)。
関心のあるペアと交換のデータを取得する方法については、ドキュメントの [データのダウンロード](data-download.md) セクションにアクセスしてください。

!!! Bug
    [問題 #1133](https://github.com/freqtrade/freqtrade/issues/1133) で判明したように、1 つの CPU コアのみで使用すると Hyperopt がクラッシュする可能性があります。

!!! Note
    2021.4 リリース以降、別個の hyperopt クラスを作成する必要はなくなり、ストラテジー内でパラメーターを直接構成できるようになりました。
    従来のメソッドは 2021.8 までサポートされていましたが、2021.9 では削除されました。

## hyperopt の依存関係をインストールする

Hyperopt の依存関係はボット自体の実行には必要なく、重く、一部のプラットフォーム (Raspberry PI など) では簡単に構築できないため、デフォルトではインストールされません。 Hyperopt を実行する前に、以下のこのセクションで説明するように、対応する依存関係をインストールする必要があります。

!!! Note
    Hyperopt はリソースを大量に消費するプロセスであるため、Raspberry Pi での実行は推奨もサポートもされていません。

### ドッカー

docker-image には hyperopt の依存関係が含まれているため、それ以上のアクションは必要ありません。

### 簡単インストールスクリプト (setup.sh) / 手動インストール
```bash
source .venv/bin/activate
pip install -r requirements-hyperopt.txt
```
## Hyperopt コマンドリファレンス

--8<-- "commands/hyperopt.md"

### Hyperopt チェックリスト

hyperopt のすべてのタスク/可能性に関するチェックリスト

最適化したいスペースに応じて、以下の一部のみが必要です。

* `space='buy'` でパラメータを定義 - エントリーシグナルの最適化用
* `space='sell'` でパラメータを定義 - 終了信号の最適化用

!!! Note
    `populate_indicators` は、スペースのいずれかで使用されるすべてのインジケーターを作成する必要があります。そうしないと、hyperopt が機能しません。

まれに、「HyperOpt」という名前の [ネストされたクラス](advanced-hyperopt.md#overriding-pre-define-spaces) を作成して実装する必要がある場合もあります。

* `roi_space` - カスタム ROI 最適化用 (デフォルトとは異なる最適化ハイパースペース内の ROI パラメーターの範囲が必要な場合)
* `generate_roi_table` - カスタム ROI 最適化用 (デフォルトとは異なる ROI テーブルの値の範囲、またはデフォルトの 4 ステップとは異なる ROI テーブルのエントリ (ステップ) の数が必要な場合)
* `stoploss_space` - カスタム ストップロス最適化用 (デフォルトとは異なる最適化ハイパースペースのストップロス パラメーターの範囲が必要な場合)
* `trailing_space` - カスタム トレーリング ストップ最適化用 (デフォルトとは異なる最適化ハイパースペース内のトレーリング ストップ パラメーターの範囲が必要な場合)
* `max_open_trades_space` - カスタム max_open_trades 最適化用 (デフォルトとは異なる最適化ハイパースペースの max_open_trades パラメーターの範囲が必要な場合)

!!! Tip "ROI、ストップロス、トレーリングストップロスを迅速に最適化"
    戦略を何も変更せずに、スペース「roi」、「stoploss」、「trailing」をすばやく最適化できます。
    ``` bash
    # Have a working strategy at hand.
    freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --spaces roi stoploss trailing --strategy MyWorkingStrategy --config config.json -e 100
    ```
### Hyperopt 実行ロジック

Hyperopt は最初にデータをメモリにロードし、次に `--analyze-per-epoch` が指定されていない限り、ペアごとに 1 回 `populate_indicators()` を実行してすべてのインジケーターを生成します。

次に、Hyperopt はさまざまなプロセス (プロセッサの数、または `-j <n>`) を生成し、バックテストを何度も実行して、定義された `--spaces` の一部であるパラメーターを変更します。

新しいパラメータのセットごとに、freqtrade は最初に `populate_entry_trend()` を実行し、続いて `populate_exit_trend()` を実行し、次に定期的なバックテスト プロセスを実行して取引をシミュレートします。

バックテストの後、結果は [損失関数](#loss-functions) に渡され、この結果が以前の結果より良いか悪いかを評価します。  
損失関数の結果に基づいて、hyperopt はバックテストの次のラウンドで試行する次のパラメーターのセットを決定します。

### ガードとトリガーを構成する

テスト用に新しい購入 hyperopt を追加するには、戦略ファイル内で 2 つの場所を変更する必要があります。

* hyperopt が最適化するクラス レベルでパラメーターを定義します。
* `populate_entry_trend()` 内 - 生の定数の代わりに定義されたパラメータ値を使用します。

ここには 2 つの異なるタイプのインジケーターがあります: 1. `ガード` と 2. `トリガー`。

1. ガードとは、「ADX < 10 の場合は決して買わない」、または現在の価格が EMA10 を超えている場合は決して買わないなどの条件です。
2. トリガーとは、「EMA5 が EMA10 を超えたときに買う」または「終値がボリンジャーバンドの下側に触れたときに買う」など、特定の瞬間に実際に買いをトリガーするものです。

!!! Hint "ガードとトリガー"
    技術的には、ガードとトリガーに違いはありません。  
    ただし、このガイドでは、信号が「スタック」すべきではないことを明確にするためにこの区別を行います。
    スティックシグナルは、複数のローソク足でアクティブになるシグナルです。これにより、信号の入力が遅くなる可能性があります (信号が消える直前、つまり成功の可能性が最初よりもかなり低くなります)。

ハイパー最適化では、エポック ラウンドごとに 1 つのトリガーと、場合によっては複数のガードが選択されます。

#### 終了信号の最適化

上記のエントリーシグナルと同様に、イグジットシグナルも最適化できます。
対応する設定を次のメソッドに配置します。

* hyperopt が最適化するクラスレベルでパラメータを定義します。パラメータに `sell_*` という名前を付けるか、明示的に `space='sell'` を定義します。
* `populate_exit_trend()` 内 - 生の定数の代わりに定義されたパラメータ値を使用します。

構成とルールは買いシグナルの場合と同じです。

## 謎を解く

たとえば、ロングエントリーをトリガーするためにMACDクロスを使用するか、ボリンジャーバンドを下げるかに興味があるとします。
また、これらの決定を支援するために RSI または ADX を使用するべきかどうかも疑問に思います。
RSI または ADX を使用する場合、どちらの値を使用する必要がありますか?

そこで、ハイパーパラメータの最適化を使用して、この謎を解決してみましょう。

### 使用するインジケーターの定義

まず、戦略で使用する指標を計算します。
``` python
class MyAwesomeStrategy(IStrategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate all indicators used by the strategy
        """
        dataframe['adx'] = ta.ADX(dataframe)
        dataframe['rsi'] = ta.RSI(dataframe)
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe['bb_lowerband'] = bollinger['lowerband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_upperband'] = bollinger['upperband']
        return dataframe
```
### 超最適化パラメータ

超最適化パラメータの定義を続けます。
```python
class MyAwesomeStrategy(IStrategy):
    buy_adx = DecimalParameter(20, 40, decimals=1, default=30.1, space="buy")
    buy_rsi = IntParameter(20, 40, default=30, space="buy")
    buy_adx_enabled = BooleanParameter(default=True, space="buy")
    buy_rsi_enabled = CategoricalParameter([True, False], default=False, space="buy")
    buy_trigger = CategoricalParameter(["bb_lower", "macd_cross_signal"], default="bb_lower", space="buy")
```
上記の定義では、次のようになります。最適な組み合わせを見つけるためにランダムに組み合わせたい 5 つのパラメーターがあります。  
`buy_rsi` は整数パラメータで、20 ～ 40 の間でテストされます。このスペースのサイズは 20 です。  
`buy_adx` は 10 進数のパラメーターで、小数点以下 1 桁の 20 ～ 40 の間で評価されます (つまり、値は 20.1、20.2、...)。このスペースのサイズは 200 です。  
次に、3 つのカテゴリ変数があります。最初の 2 つは「True」または「False」のいずれかです。
これらを使用して、ADX および RSI ガードを有効または無効にします。
最後のトリガーは「トリガー」と呼ばれ、どの購入トリガーを使用するかを決定するために使用します。

!!! Note "パラメータ空間の割り当て"
    パラメータは、`buy_*` または `sell_*` という名前の変数に割り当てるか、`space='buy'` を含める必要があります。 `space='sell'` がスペースに正しく割り当てられるようにします。
    スペースに使用できるパラメーターがない場合、hyperopt の実行時にスペースが見つからなかったというエラーが表示されます。  
    不明確なスペースを含むパラメーター (例: `adx_period = IntParameter(4, 24,default=14)` - 明示的または暗黙的なスペースなし) は検出されず、無視されます。

それでは、これらの値を使用して購入戦略を作成してみましょう。
```python
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        # GUARDS AND TRENDS
        if self.buy_adx_enabled.value:
            conditions.append(dataframe['adx'] > self.buy_adx.value)
        if self.buy_rsi_enabled.value:
            conditions.append(dataframe['rsi'] < self.buy_rsi.value)

        # TRIGGERS
        if self.buy_trigger.value == 'bb_lower':
            conditions.append(dataframe['close'] < dataframe['bb_lowerband'])
        if self.buy_trigger.value == 'macd_cross_signal':
            conditions.append(qtpylib.crossed_above(
                dataframe['macd'], dataframe['macdsignal']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1

        return dataframe
```
Hyperopt は、異なる値の組み合わせで `populate_entry_trend()` を何度も (`epochs`) 呼び出します。  
指定された履歴データを使用し、上記の関数で生成された購入シグナルに基づいて購入をシミュレートします。  
結果に基づいて、hyperopt はどのパラメーターの組み合わせが最良の結果をもたらしたかを示します (設定された [損失関数](#loss-functions) に基づいて)。

!!! Note
    上記の設定では、入力されたインジケーターで ADX、RSI、ボリンジャー バンドが見つかることが期待されます。
    現在ボットで使用されていないインジケーターをテストする場合は、次のことを忘れないでください。
    これをストラテジーまたは hyperopt ファイルの `populate_indicators()` メソッドに追加します。

## パラメータの種類

パラメータには 4 つのタイプがあり、それぞれ異なる目的に適しています。

* `IntParameter` - 検索空間の上限と下限を含む整数パラメータを定義します。
* `DecimalParameter` - 限られた数の小数点を持つ浮動小数点パラメータを定義します (デフォルトは 3)。ほとんどの場合、「RealParameter」の代わりにこれを使用する必要があります。
* `RealParameter` - 上限と下限の境界と精度制限のない浮動小数点パラメータを定義します。ほぼ無限の可能性を持つ空間を作り出すため、ほとんど使用されません。
* `CategoricalParameter` - あらかじめ決められた数の選択肢を持つパラメーターを定義します。
* `BooleanParameter` - `CategoricalParameter([True, False])` の短縮形 - パラメータを「有効にする」のに最適です。

### パラメータオプション

さまざまなアイデアをすばやくテストするのに役立つ 2 つのパラメーター オプションがあります。

* `optimize` - `False` に設定すると、パラメーターは最適化プロセスに含まれません。 (デフォルト: True)
* `load` - `False` に設定すると、以前の hyperopt 実行の結果 (戦略または JSON 出力ファイルの `buy_params` および `sell_params` 内) は、後続の hyperopt の開始値として使用されません。パラメータで指定されたデフォルト値が代わりに使用されます。 (デフォルト: True)

!!! Tip "バックテストにおける「load=False」の影響"
    「load」オプションを「False」に設定すると、バックテストでも、超最適化によって見つかった値ではなく、パラメーターで指定されたデフォルト値が使用されることになることに注意してください。

!!! Warning
    Hyperopttable パラメーターは「populate_indicators」では使用できません。hyperopt は各エポックのインジケーターを再計算しないため、この場合は開始値が使用されます。

## インジケーターパラメーターの最適化

EMA クロス戦略 (2 つの移動平均の交差) という単純な戦略を念頭に置いて、この戦略に最適なパラメーターを見つけたいとします。
デフォルトでは、ストップロスを 5%、テイクプロフィット (`minimal_roi`) を 10% と仮定します。これは、freqtrade は 10% の利益に達したら取引を売却することを意味します。
``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'
    minimal_roi = {
        "0":  0.10
    }
    # Define the parameter spaces
    buy_ema_short = IntParameter(3, 50, default=5)
    buy_ema_long = IntParameter(15, 200, default=50)


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""
        
        # Calculate all ema_short values
        for val in self.buy_ema_short.range:
            dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod=val)
        
        # Calculate all ema_long values
        for val in self.buy_ema_long.range:
            dataframe[f'ema_long_{val}'] = ta.EMA(dataframe, timeperiod=val)
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(qtpylib.crossed_above(
                dataframe[f'ema_short_{self.buy_ema_short.value}'], dataframe[f'ema_long_{self.buy_ema_long.value}']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(qtpylib.crossed_above(
                dataframe[f'ema_long_{self.buy_ema_long.value}'], dataframe[f'ema_short_{self.buy_ema_short.value}']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long'] = 1
        return dataframe
```
内訳:

`self.buy_ema_short.range` を使用すると、パラメータの下限値と上限値の間のすべてのエントリを含む範囲オブジェクトが返されます。
この場合 (`IntParameter(3, 50,default=5)`)、ループは 3 から 50 までのすべての数値 (`[3, 4, 5, ... 49, 50]`) に対して実行されます。
これをループ内で使用すると、hyperopt は 48 個の新しい列 (`['buy_ema_3', 'buy_ema_4', ... , 'buy_ema_50']`) を生成します。

Hyperopt 自体は、選択された値を使用して売買シグナルを作成します。

この戦略はおそらく単純すぎて一貫した利益を提供できませんが、指標パラメーターを最適化する方法の例として役立つはずです。

!!! Note
    `self.buy_ema_short.range` は、hyperopt モードと他のモードでは動作が異なります。 hyperopt の場合、上記の例では 48 個の新しい列が生成されますが、他のすべてのモード (バックテスト、ドライ/ライブ) では、選択した値の列のみが生成されます。したがって、結果の列を明示的な値 (`self.buy_ema_short.value` 以外の値) で使用することは避けてください。

!!! Note
    `range` プロパティは、`DecimalParameter` および `CategoricalParameter` と一緒に使用することもできます。 `RealParameter` は無限の検索スペースのため、このプロパティを提供しません。

???ヒント「演奏のヒント」
    通常のハイパーオプティング中、インジケーターは 1 回計算されて各エポックに供給され、コア増加の要因として RAM 使用量が直線的に増加します。これはパフォーマンスにも影響するため、RAM の使用量を削減するには 2 つの選択肢があります。

    * `ema_short` と `ema_long` の計算を `populate_indicators()` から `populate_entry_trend()` に移動します。 `populate_entry_trend()` はエポックごとに計算されるため、`.range` 機能を使用する必要はありません。
    * hyperopt は、`--analyze-per-epoch` を提供します。これは、`populate_indicators()` の実行をエポック プロセスに移動し、`.range` 機能を使用する代わりに、エポックごとにパラメーターごとに単一の値を計算します。この場合、`.range` 機能は実際に使用された値のみを返します。

    これらの代替方法では、RAM の使用量は削減されますが、CPU の使用量は増加します。ただし、メモリ不足 (OOM) の問題によりハイパーオプティングの実行が失敗する可能性は低くなります。

    `.range` 機能を使用しているか、上記の代替機能を使用しているかに関係なく、CPU/RAM の使用率が向上するため、スペース範囲をできるだけ小さくするようにしてください。

## 保護の最適化

Freqtrade は保護を最適化することもできます。保護を最適化する方法はユーザー次第であり、以下は例としてのみ考慮してください。

この戦略では、保護構成のリストを返すプロパティとして「protections」エントリを定義するだけで済みます。
``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'
    # Define the parameter spaces
    cooldown_lookback = IntParameter(2, 48, default=5, space="protection", optimize=True)
    stop_duration = IntParameter(12, 200, default=5, space="protection", optimize=True)
    use_stop_protection = BooleanParameter(default=True, space="protection", optimize=True)


    @property
    def protections(self):
        prot = []

        prot.append({
            "method": "CooldownPeriod",
            "stop_duration_candles": self.cooldown_lookback.value
        })
        if self.use_stop_protection.value:
            prot.append({
                "method": "StoplossGuard",
                "lookback_period_candles": 24 * 3,
                "trade_limit": 4,
                "stop_duration_candles": self.stop_duration.value,
                "only_per_pair": False
            })

        return prot

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ...
        
```
その後、次のように hyperopt を実行できます。
`freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --strategy MyAwesomeStrategy --spaces protection`

!!! Note
    保護スペースはデフォルト スペースの一部ではなく、パラメータ Hyperopt インターフェイスでのみ使用でき、従来の hyperopt インターフェイス (別個の hyperopt ファイルが必要) では使用できません。
    Freqtrade は、保護スペースが選択されている場合、「--enable-protections」フラグも自動的に変更します。

!!! Warning
    保護がプロパティとして定義されている場合、構成からのエントリは無視されます。
    したがって、構成内で保護を定義しないことをお勧めします。

### 以前のプロパティ設定からの移行

以前の設定からの移行は非常に簡単で、保護エントリをプロパティに変換することで実現できます。
簡単に言うと、以下の構成は以下のように変換されます。
``` python
class MyAwesomeStrategy(IStrategy):
    protections = [
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 4
        }
    ]
```
結果
``` python
class MyAwesomeStrategy(IStrategy):
    
    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 4
            }
        ]
```
その後、明らかに、潜在的な興味深いエントリもパラメータに変更して、超最適化を可能にします。

### `max_entry_position_adjustment` の最適化

「max_entry_position_adjustment」は独立したスペースではありませんが、上記のプロパティ アプローチを使用することで、hyperopt で引き続き使用できます。
``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'

    # Define the parameter spaces
    max_epa = CategoricalParameter([-1, 0, 1, 3, 5, 10], default=1, space="buy", optimize=True)

    @property
    def max_entry_position_adjustment(self):
        return self.max_epa.value
        

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ...
```
???ヒント「「IntParameter」の使用」
    この最適化に `IntParameter` を使用することもできますが、明示的に整数を返す必要があります。
    ``` python
    max_epa = IntParameter(-1, 10, default=1, space="buy", optimize=True)

    @property
    def max_entry_position_adjustment(self):
        return int(self.max_epa.value)
    ```
## 損失関数

各ハイパーパラメータ調整にはターゲットが必要です。これは通常、損失関数 (目的関数とも呼ばれる) として定義され、より望ましい結果の場合は減少し、悪い結果の場合は増加する必要があります。

損失関数は、`--hyperopt-loss <Class-name>` 引数を介して (またはオプションで `"hyperopt_loss"` キーの下の設定を介して) 指定する必要があります。
このクラスは、`user_data/hyperopts/` ディレクトリ内の独自のファイルに存在する必要があります。

現在、次の損失関数が組み込まれています。

* `ShortTradeDurHyperOptLoss` - (デフォルトのレガシー Freqtrade 超最適化損失関数) - 主に短い取引期間と損失の回避に使用されます。
* `OnlyProfitHyperOptLoss` - 利益の額のみを考慮します。
* `SharpeHyperOptLoss` - 標準偏差に対する取引収益に基づいて計算されたシャープ レシオを最適化します。
* `SharpeHyperOptLossDaily` - 標準偏差に対する **日次** のトレード リターンに基づいて計算されたシャープ レシオを最適化します。
* `SortinoHyperOptLoss` - **ダウンサイド** 標準偏差に対する取引収益に基づいて計算された Sortino Ratio を最適化します。
* `SortinoHyperOptLossDaily` - **下値** 標準偏差に対する **日次** の取引収益に基づいて計算された Sortino Ratio を最適化します。
* `MaxDrawDownHyperOptLoss` - 最大絶対ドローダウンを最適化します。
* `MaxDrawDownRelativeHyperOptLoss` - 最大相対ドローダウンを調整しながら、最大絶対ドローダウンの両方を最適化します。
* `MaxDrawDownPerPairHyperOptLoss` - ペアごとの利益/ドローダウン率を計算し、最悪の結果を客観的として返し、hyperopt にペアリスト内のすべてのペアのパラメーターを最適化させます。このようにして、良い結果を持つ 1 つ以上のペアがメトリクスを増大させるのを防ぎますが、悪い結果を持つペアは表示されないため、最適化されません。
* `CalmarHyperOptLoss` - 最大ドローダウンに対するトレードリターンに基づいて計算される Calmar Ratio を最適化します。
* `ProfitDrawDownHyperOptLoss` - 最大利益と最小ドローダウン目標によって最適化します。 hyperoptloss ファイル内の `DRAWDOWN_MULT` 変数は、ドローダウンの目的に合わせてより厳密またはより柔軟に調整できます。
* `MultiMetricHyperOptLoss` - バランスの取れたパフォーマンスを達成するために、いくつかの主要なメトリクスによって最適化します。主な焦点は、利益の最大化とドローダウンの最小化ですが、利益率、期待率、勝率などの追加の指標も考慮します。さらに、取引数が少ないエポックにはペナルティを適用し、適切な取引頻度での戦略を奨励します。

カスタム損失関数の作成については、ドキュメントの [Advanced Hyperopt](advanced-hyperopt.md) の部分で説明されています。

## Hyperoptを実行する

hyperopt 構成を更新したら、実行できるようになります。
hyperopt は最適なパラメーターを見つけるために多くの組み合わせを試行するため、良好な結果が得られるまでに時間がかかります。

接続の損失を防ぐために、「screen」または「tmux」を使用することを強くお勧めします。
```bash
freqtrade hyperopt --config config.json --hyperopt-loss <hyperoptlossname> --strategy <strategyname> -e 500 --spaces all
```
`-e` オプションは、hyperopt が実行する評価の数を設定します。 hyperopt はベイジアン検索を使用するため、一度に実行するエポックが多すぎると、より良い結果が得られない可能性があります。経験によれば、通常、最良の結果は 500 ～ 1000 エポックを経過してもあまり改善されません。  
`--early-stop` オプションは、改善のないエポックが何回経過した後に hyperopt を停止するかを設定します。適切な値は、合計エポックの 20 ～ 30% です。 0 より大きく 20 未満の値は 20 に置き換えられます。早期停止はデフォルトで無効になっています (`--early-stop=0`)。

数 1000 エポックおよび異なるランダム状態で複数の実行 (実行) を実行すると、異なる結果が生成される可能性が高くなります。

`--spaces all` オプションは、すべての可能なパラメータを最適化する必要があることを決定します。可能性としては以下のようなものがあります。

!!! Note
    Hyperopt は、hyperopt の結果を hyperopt 開始時刻のタイムスタンプとともに保存します。
    読み取りコマンド (`hyperopt-list`、`hyperopt-show`) では、`--hyperopt-filename <filename>` を使用して、古い hyperopt の結果を読み取り、表示できます。
    ファイル名のリストは「ls -l user_data/hyperopt_results/」で確認できます。

### 異なる履歴データ ソースで Hyperopt を実行する

代替の履歴データセットを使用してパラメータをハイパーオプト化したい場合は、
ディスク上にある場合は、「--datadir PATH」オプションを使用します。デフォルトでは、hyperopt はディレクトリ `user_data/data` のデータを使用します。

### より小さいテストセットで Hyperopt を実行する

`--timerange` 引数を使用して、使用するテストセットの量を変更します。
たとえば、1 か月のデータを使用するには、「--timerange 20210101-20210201」（2021 年 1 月から 2021 年 2 月まで）を hyperopt 呼び出しに渡します。

完全なコマンド:
```bash
freqtrade hyperopt --strategy <strategyname> --timerange 20210101-20210201
```
### より小さい検索スペースで Hyperopt を実行する

hyperopt が使用する検索スペースを制限するには、「--spaces」オプションを使用します。
Hyperopt にすべてを最適化させると、巨大な検索スペースが得られます。
多くの場合、最初の購入アルゴリズムを検索することから始める方が合理的かもしれません。
あるいは、あなたが持っている素晴らしい新しい購入戦略に合わせてストップロスまたは ROI テーブルを最適化したいだけかもしれません。

有効な値は次のとおりです。

* `all`: すべてを最適化します
* `buy`: 新しい購入戦略を検索するだけです
* `sell`: 新しい販売戦略を検索するだけです
* `roi`: 戦略に合わせて最小利益テーブルを最適化するだけです
* `stoploss`: 最適なストップロス値を検索します。
* `trailing`: 最適なトレーリング ストップ値を検索します。
* `trades`: 最適な最大オープン取引値を検索します。
* `protection`: 最適な保護パラメーターを検索します (これらを適切に定義する方法については、[保護セクション](#optimizing-protections) を参照してください)
* `default`: `trailing`、`trades`、および `protection` を除く `すべて`
* 上記の値のスペース区切りのリスト (例: `--spaces roi stoploss`)

「--space」コマンド ライン オプションが指定されていない場合に使用されるデフォルトの Hyperopt 検索スペースには、「trailing」ハイパースペースが含まれません。他のハイパースペースの最適なパラメーターが見つかって検証され、カスタム戦略に貼り付けられたときに、「末尾」ハイパースペースの最適化を個別に実行することをお勧めします。

## Hyperopt の結果を理解する

Hyperopt が完了したら、その結果を使用して戦略を更新できます。
hyperopt から次の結果が得られるとします。
```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }
```
この結果は次のように理解できるはずです。

* 最も効果的な購入トリガーは `bb_ lower` でした。
* `'buy_adx_enabled': False` のため、ADX を使用しないでください。
* RSI インジケーター (`'buy_rsi_enabled': True`) の使用を**検討**する必要があり、最適な値は `29.0` (`'buy_rsi': 29.0`) です。

### 戦略へのパラメータの自動適用

Hyperoptable パラメーターを使用する場合、hyperopt 実行の結果は、戦略の隣にある json ファイルに書き込まれます (つまり、`MyAwesomeStrategy.py` の場合、ファイルは `MyAwesomeStrategy.json` になります)。  
このファイルは、2 つのコマンドのいずれかに `--disable-param-export` が指定されていない限り、`hyperopt-show` サブコマンドを使用するときにも更新されます。


戦略クラスにこれらの結果を明示的に含めることもできます。 hyperopt の結果ブロックをコピーしてクラス レベルに貼り付け、古いパラメーター (存在する場合) を置き換えるだけです。次回ストラテジが実行されるときに、新しいパラメータが自動的にロードされます。

hyperopt の結果全体を戦略に転送すると、次のようになります。
```python
class MyAwesomeStrategy(IStrategy):
    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }
```
!!! Note
    構成ファイル内の値はパラメータ ファイル レベルのパラメータを上書きし、両方ともストラテジ内のパラメータを上書きします。
    したがって、普及率は次のようになります: config > パラメータ ファイル > ストラテジ `*_params` > パラメータ デフォルト

### Hyperopt ROI の結果を理解する

ROI を最適化している場合 (つまり、最適化検索スペースに「all」、「default」、または「roi」が含まれている場合)、結果は次のようになり、ROI テーブルが含まれます。
```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # ROI table:
    minimal_roi = {
        0: 0.10674,
        21: 0.09158,
        78: 0.03634,
        118: 0
    }
```
Hyperopt がバックテストやライブトレード/ドライランで見つけたこの最良の ROI テーブルを使用するには、それをカスタム戦略の `minimal_roi` 属性の値としてコピーして貼り付けます。
```
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        0: 0.10674,
        21: 0.09158,
        78: 0.03634,
        118: 0
    }
```
コメントに記載されているように、設定ファイルの `minimal_roi` 設定の値として使用することもできます。

#### デフォルトの ROI 検索スペース

ROI を最適化している場合、Freqtrade は「roi」最適化ハイパースペースを作成します。これは、ROI テーブルのコンポーネントのハイパースペースです。デフォルトでは、Freqtrade によって生成される各 ROI テーブルは 4 行 (ステップ) で構成されます。 Hyperopt は、使用されるタイムフレームに依存する ROI ステップの値の範囲を持つ ROI テーブルの適応範囲を実装します。デフォルトでは、値は次の範囲で変化します（最もよく使用されるタイムフレームの一部では、値は小数点以下 3 桁に四捨五入されます）。

| ＃ステップ | 1m |               | 5m |             | 1時間 |               | 1d |               |
| ------ | ------ | ------------- | -------- | ----------- | ---------- | ------------- | ------------ | ------------- |
| 1 | 0 | 0.011...0.119 | 0 | 0.03...0.31 | 0 | 0.068...0.711 | 0 | 0.121...1.258 |
| 2 | 2...8 | 0.007...0.042 | 10...40 | 0.02...0.11 | 120...480 | 0.045...0.252 | 2880...11520 | 0.081...0.446 |
| 3 | 4...20 | 0.003...0.015 | 20...100 | 0.01...0.04 | 240...1200 | 0.022...0.091 | 5760...28800 | 0.040...0.162 |
| 4 | 6...44 | 0.0 | 30...220 | 0.0 | 360...2640 | 0.0 | 8640...63360 | 0.0 |

ほとんどの場合、これらの範囲で十分です。ステップ内の分数 (ROI dict キー) は、使用される時間枠に応じて線形にスケールされます。ステップ内の ROI 値 (ROI dict 値) は、使用される時間枠に応じて対数的にスケールされます。

カスタム hyperopt に「generate_roi_table()」メソッドと「roi_space()」メソッドがある場合は、これらの適応 ROI テーブルと Freqtrade によってデフォルトで生成される ROI 超最適化スペースを利用するために、それらを削除してください。

ROI テーブルのコンポーネントを他の範囲で変化させる必要がある場合は、`roi_space()` メソッドをオーバーライドします。 ROI テーブルの異なる構造または他の量の行 (ステップ) が必要な場合は、`generate_roi_table()` および `roi_space()` メソッドをオーバーライドし、超最適化中に ROI テーブルを生成するための独自のカスタム アプローチを実装します。

これらのメソッドのサンプルは、[事前定義されたスペースのオーバーライド](advanced-hyperopt.md#overriding-pre-defined-spaces) にあります。

!!! Note "検索スペースの縮小"
    検索スペースをさらに制限するために、Decimal は小数点以下 3 桁 (精度 0.001) に制限されます。通常はこれで十分ですが、これより正確な値を指定すると、通常は結果が過学習になります。ただし、[事前定義されたスペースをオーバーライドする](advanced-hyperopt.md#overriding-pre-defined-spaces) ことで、これを必要に応じて変更できます。

### Hyperopt のストップロスの結果を理解する
ストップロス値を最適化している場合 (つまり、最適化検索スペースに「all」、「default」、または「stoploss」が含まれている場合)、結果は次のようになり、ストップロスが含まれます。
```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }

    stoploss: -0.27996
```
Hyperopt がバックテストやライブトレード/ドライランで見つけたこの最適なストップロス値を使用するには、それをカスタム戦略の `stoploss` 属性の値としてコピーして貼り付けます。
``` python
    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.27996
```
コメントに記載されているように、設定ファイルの「stoploss」設定の値として使用することもできます。

#### デフォルトのストップロス検索スペース

ストップロス値を最適化している場合、Freqtrade は「ストップロス」最適化ハイパースペースを作成します。デフォルトでは、そのハイパースペースのストップロス値は -0.35...-0.02 の範囲で変化しますが、ほとんどの場合これで十分です。

カスタム hyperopt ファイルに `stoploss_space()` メソッドがある場合は、Freqtrade によってデフォルトで生成される Stoploss ハイパー最適化スペースを利用するために、それを削除してください。

ハイパー最適化中にストップロス値を他の範囲で変更する必要がある場合は、`stoploss_space()` メソッドをオーバーライドし、そのメソッド内で目的の範囲を定義します。このメソッドのサンプルは、[事前定義されたスペースのオーバーライド](advanced-hyperopt.md#overriding-pre-defined-spaces) にあります。

!!! Note "検索スペースの縮小"
    検索スペースをさらに制限するために、Decimal は小数点以下 3 桁 (精度 0.001) に制限されます。通常はこれで十分ですが、これより正確な値を指定すると、通常は結果が過学習になります。ただし、[事前定義されたスペースをオーバーライドする](advanced-hyperopt.md#overriding-pre-defined-spaces) ことで、これを必要に応じて変更できます。

### Hyperopt トレーリング ストップの結果を理解する

トレーリング ストップ値を最適化している場合 (つまり、最適化検索スペースに「all」または「trailing」が含まれている場合)、結果は次のようになり、トレーリング ストップ パラメーターが含まれます。
```
Best result:

    45/100:    606 trades. Avg profit  1.04%. Total profit  0.31555614 BTC ( 630.48%). Avg duration 150.3 mins. Objective: -1.10161

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.02001
    trailing_stop_positive_offset = 0.06038
    trailing_only_offset_is_reached = True
```
Hyperopt がバックテストやライブトレード/ドライランで見つけたこれらの最適なトレーリング ストップ パラメーターを使用するには、これらをカスタム戦略の対応する属性の値としてコピーして貼り付けます。
``` python
    # Trailing stop
    # These attributes will be overridden if the config file contains corresponding values.
    trailing_stop = True
    trailing_stop_positive = 0.02001
    trailing_stop_positive_offset = 0.06038
    trailing_only_offset_is_reached = True
```
コメントに記載されているように、構成ファイル内の対応する設定の値として使用することもできます。

#### デフォルトのトレーリングストップ検索スペース

トレーリングストップ値を最適化している場合、Freqtrade は「トレーリング」最適化ハイパースペースを作成します。デフォルトでは、そのハイパースペースでは `trailing_stop` パラメータは常に True に設定され、`trailing_only_offset_is_reached` の値は True と False の間で変化し、`trailing_stop_positive` パラメータと `trailing_stop_positive_offset` パラメータの値はそれに応じて 0.02...0.35 および 0.01...0.1 の範囲で変化します。これはほとんどの場合これで十分です。

ハイパー最適化中にトレーリング ストップ パラメーターの値を他の範囲で変更する必要がある場合は、`trailing_space()` メソッドをオーバーライドし、そのメソッド内で目的の範囲を定義します。このメソッドのサンプルは、[事前定義されたスペースのオーバーライド](advanced-hyperopt.md#overriding-pre-defined-spaces) にあります。

!!! Note "検索スペースの縮小"
    検索スペースをさらに制限するために、Decimal は小数点以下 3 桁 (精度 0.001) に制限されます。通常はこれで十分ですが、これより正確な値を指定すると、通常は結果が過学習になります。ただし、[事前定義されたスペースをオーバーライドする](advanced-hyperopt.md#overriding-pre-defined-spaces) ことで、これを必要に応じて変更できます。

### 再現可能な結果

最適なパラメーターの検索は、パラメーターのハイパースペース、つまりランダムな Hyperopt エポック内のいくつか (現在 30) のランダムな組み合わせから始まります。これらのランダム エポックは、Hyperopt 出力の最初の列にアスタリスク文字 (`*`) でマークされます。

これらのランダム値を生成するための初期状態 (ランダム状態) は、「--random-state」コマンド ライン オプションの値によって制御されます。再現可能な結果を​​得るために、任意の値に設定できます。

コマンド ライン オプションでこの値を明示的に設定していない場合、Hyperopt はランダムな値をランダムな状態にシードします。各 Hyperopt 実行のランダムな状態値はログに表示されるため、それをコピーして「--random-state」コマンド ライン オプションに貼り付けて、使用された最初のランダム エポックのセットを繰り返すことができます。

コマンド ライン オプション、構成、時間範囲、Strategy クラスと Hyperopt クラス、履歴データ、損失関数を何も変更していない場合は、同じランダムな状態値を使用して同じハイパー最適化結果が得られるはずです。

## 出力フォーマット
デフォルトでは、hyperopt は結果を色付けして印刷します。利益がプラスのエポックは緑色で印刷されます。この強調表示は、後の分析で興味深いエポックを見つけるのに役立ちます。合計利益がゼロであるか、マイナスの利益 (損失) があるエポックは、通常の色で印刷されます。結果の色付けが必要ない場合 (たとえば、hyperopt 出力をファイルにリダイレクトする場合)、コマンドラインで `--no-color` オプションを指定して色付けをオフにできます。

最良の結果だけでなく、すべての結果を hyperopt 出力で表示したい場合は、「--print-all」コマンド ライン オプションを使用できます。 `--print-all` を使用すると、現在の最良の結果もデフォルトで色付けされ、太字 (明るい) スタイルで印刷されます。これは、「--no-color」コマンドラインオプションを使用してオフにすることもできます。

!!! Note "ウィンドウとカラー出力"
    Windows はカラー出力をネイティブにサポートしていないため、自動的に無効になります。 Windows 上で hyperopt のカラー出力を実行するには、WSL の使用を検討してください。

## ポジションのスタックと最大市場ポジションの無効化

状況によっては、`--eps`/`--enable-position-saking` 引数を指定して Hyperopt (およびバックテスト) を実行する必要がある場合や、オープン取引の数の制限を無効にするために `max_open_trades` を非常に高い数値に設定する必要がある場合があります。

デフォルトでは、hyperopt は Freqtrade Live Run/Dry Run の動作をエミュレートします。
ペアごとのオープントレードが許可されます。すべてのペアのオープン取引の合計数
`max_open_trades` 設定によっても制限されます。 Hyperopt/バックテスト中に、これにより次のような問題が発生する可能性があります。
潜在的な取引が、すでに開かれている取引によって隠蔽（またはマスク）されている。

`--eps`/`--enable-position-stacking` 引数により、同じペアを複数回購入するエミュレーションが可能になります。
非常に大きな数値で「--max-open-trades」を使用すると、オープン取引の数の制限が無効になります。

!!! Note
    ドライ/ライブ ランではポジション スタッキングは**使用されません**。したがって、現実に近いため、これを使用しない戦略も検証することは理にかなっています。

明示的に設定することで、構成ファイルで位置スタッキングを有効にすることもできます。
`"position_stacking"=true`。

## メモリ不足エラー

hyperopt は大量のメモリを消費するため (並列バックテスト プロセスごとに完全なデータを 1 回メモリに置く必要がある)、「メモリ不足」エラーが発生する可能性があります。
これらに対処するには、複数のオプションがあります。

※ペア数を減らしてください。
* 使用される時間範囲を減らします (`--timerange <timerange>`)。
* `--timeframe-detail` の使用は避けてください (これにより、大量の追加データがメモリにロードされます)。
* 並列プロセスの数を減らします (`-j <n>`)。
* マシンのメモリを増設してください。
* `.range` 機能で多くのパラメータを使用している場合は、`--analyze-per-epoch` を使用します。
## 目標はこの時点で以前に評価されています。

「目標は以前にこの時点で評価されています。」というメッセージが表示された場合、これはスペースが使い果たされているか、それに近いことを示しています。
基本的に、空間内のすべての点がヒットしました (または極小値がヒットしました) - そして、hyperopt は、まだ試行していない多次元空間内の点を見つけることができなくなりました。
Freqtrade は、この場合、新しいランダム化されたポイントを使用して「極小値」問題に対抗しようとします。

例：
``` python
buy_ema_short = IntParameter(5, 20, default=10, space="buy", optimize=True)
# This is the only parameter in the buy space
```
`buy_ema_short` スペースには 15 個の可能な値 (`5、6、... 19、20`) があります。ここで購入スペースに対して hyperopt を実行すると、オプションがなくなる前に hyperopt で試行できる値は 15 個だけになります。
したがって、エポックは可能な値に合わせて調整する必要があります。あるいは、「目標は前にこの時点で評価されています。」という警告が大量に表示された場合は、実行を中断する準備ができている必要があります。

## Hyperopt の結果の詳細を表示する

必要な量のエポックに対して Hyperopt を実行した後、分析のためにすべての結果をリストし、最良または収益性の高いもののみを 1 回だけ選択し、以前に評価したエポックの詳細を表示することができます。これは、`hyperopt-list` および `hyperopt-show` サブコマンドを使用して実行できます。これらのサブコマンドの使用法については、[Utils](utils.md#list-hyperopt-results) の章で説明されています。

## 戦略からのデバッグ メッセージを出力します。

戦略からデバッグ メッセージを出力したい場合は、`logging` モジュールを使用できます。デフォルトでは、Freqtrade は「INFO」以上のレベルを持つすべてのメッセージを出力します。
``` python
import logging


logger = logging.getLogger(__name__)


class MyAwesomeStrategy(IStrategy):
    ...

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.info("This is a debug message")
        ...

```
!!! Note "印刷を使用する"
    `print()` 経由で出力されたメッセージは、並列処理が無効 (`-j 1`) にならない限り、hyperopt 出力には表示されません。 
    代わりに「logging」モジュールを使用することをお勧めします。

## バックテスト結果を検証する

最適化された戦略が戦略に実装されたら、この戦略をバックテストして、すべてが期待どおりに機能していることを確認する必要があります。

Hyperopt 時と同じ結果 (取引数、取引期間、利益など) を達成するには、バックテストに hyperopt で使用したのと同じ構成とパラメーター (時間範囲、時間枠など) を使用してください。

### バックテストの結果が hyperopt の結果と一致しないのはなぜですか?

結果が一致しない場合は、次の要素を確認してください。

* `populate_indicators()` に hyperopt のパラメータを追加した可能性があります。パラメータは **すべてのエポック**に対して 1 回だけ計算されます。たとえば、複数の SMA timeperiod 値を最適化しようとしている場合、エポックごとに計算される `populate_entry_trend()` に超最適な timeperiod パラメーターを配置する必要があります。 [インジケーターパラメーターの最適化](https://www.freqtrade.io/en/stable/hyperopt/#optimizing-an-indicator-parameter)を参照してください。
* JSON パラメーター ファイルへの hyperopt パラメーターの自動エクスポートを無効にしている場合は、すべての hyperopt 値を戦略に正しく転送したかどうかを再確認してください。
* ログをチェックして、どのようなパラメータが設定され、どのような値が使用されているかを確認します。
* stoploss、max_open_trades、およびトレーリングストップロスパラメータには特に注意してください。これらは多くの場合、設定ファイルで設定され、戦略への変更をオーバーライドします。バックテストのログをチェックして、構成によって誤って設定されたパラメーター (「stoploss」、「max_open_trades」、「trailing_stop」など) が存在しないことを確認します。
* 戦略内のパラメータまたはデフォルトの hyperopt 設定をオーバーライドする予期しないパラメータ JSON ファイルがないことを確認してください。
* バックテストで有効になっている保護がハイパーオプト化時にも有効になること、またその逆の場合も同様であることを確認します。 「--space protection」を使用すると、ハイパーオプティングの保護が自動的に有効になります。
