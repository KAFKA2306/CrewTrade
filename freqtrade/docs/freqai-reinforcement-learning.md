# 強化学習

!!! Note "設置サイズ"
    強化学習の依存関係には、「torch」などの大きなパッケージが含まれます。これは、「freqai-rl の依存関係も必要ですか (~700mb の追加スペースが必要です) [y/N]?」という質問に「y」と答えることで、「./setup.sh -i」中に明示的に要求する必要があります。
    docker を好むユーザーは、`_freqairl` が追加された docker イメージを使用する必要があります。

## 背景と用語

### RL とは何ですか? FreqAI に RL が必要な理由は何ですか?

強化学習には、*エージェント* とトレーニング *環境* という 2 つの重要なコンポーネントが含まれます。エージェントのトレーニング中、エージェントは履歴データをキャンドルごとに移動し、常に一連のアクション (ロング エントリー、ロング イグジット、ショート エントリー、ショート イグジット、ニュートラル) の 1 つを実行します。このトレーニング プロセス中、環境はこれらのアクションのパフォーマンスを追跡し、ユーザーが作成したカスタム `calculate_reward()` に従ってエージェントに報酬を与えます (ここでは、ユーザーが希望する場合に構築できるデフォルトの報酬を提供します [詳細はこちら](#creating-a-custom-reward-function))。報酬は、ニューラル ネットワークで重みをトレーニングするために使用されます。

FreqAI RL 実装の 2 番目に重要なコンポーネントは、*状態* 情報の使用です。現在の利益、現在のポジション、現在の取引期間などの状態情報が各ステップでネットワークに供給されます。これらは、トレーニング環境でエージェントをトレーニングし、ドライ/ライブでエージェントを強化するために使用されます (この機能はバックテストでは使用できません)。 *この情報はライブ展開ですぐに利用できるため、FreqAI + Freqtrade はこの強化メカニズムに完全に一致します。*

強化学習は、分類子やリグレッサーでは対応できない適応性と市場反応性の新しい層を追加するため、FreqAI にとって自然な進歩です。ただし、Classifier と Regressor には、堅牢な予測など、RL にはない強みがあります。不適切にトレーニングされた RL エージェントは、実際には取引に勝つことなく報酬を最大化するための「チート」や「トリック」を見つける可能性があります。このため、RL はより複雑であり、一般的な分類器やリグレッサーよりも高いレベルの理解が必要です。

### RL インターフェイス

現在のフレームワークでは、ユーザーが継承した `BaseReinforcementLearner` オブジェクト (例: `freqai/prediction_models/ReinforcementLearner`) である共通の「予測モデル」ファイルを介してトレーニング環境を公開することを目指しています。このユーザー クラス内では、RL 環境が利用可能であり、[以下に示す](#creating-a-custom-reward-function) のように `MyRLEnv` 経由でカスタマイズできます。
私たちは、大多数のユーザーが「calculate_reward()」関数 [詳細はこちら](#creating-a-custom-reward-function) の創造的なデザインに労力を集中し、残りの環境には手を加えないことを想定しています。他のユーザーは環境にまったく触れず、FreqAI にすでに存在する構成設定と強力な機能エンジニアリングだけを操作する可能性があります。一方、上級ユーザーが独自のモデル クラスを完全に作成できるようにします。

このフレームワークは、stable_baselines3 (torch) と基本環境クラスの OpenAI Gym に基づいて構築されています。しかし、一般的に言えば、モデル クラスは十分に分離されています。したがって、競合するライブラリの追加を既存のフレームワークに簡単に統合できます。環境については、`gym.Env` から継承しています。これは、別のライブラリに切り替えるには、まったく新しい環境を作成する必要があることを意味します。

### 重要な考慮事項

上で説明したように、エージェントは人工的な取引「環境」で「訓練」されます。私たちの場合、その環境は実際の Freqtrade バックテスト環境に非常に似ているように見えるかもしれませんが、それは *違います*。実際、RL トレーニング環境ははるかに簡素化されています。これには、`custom_exit`、`custom_stoploss` などのコールバック、レバレッジ制御などの複雑な戦略ロジックは組み込まれていません。RL 環境は、代わりに真の市場を非常に「生」で表現したものであり、エージェントは `calculate_reward()` によって強制されるポリシー (ストップロス、テイクプロフィットなど) を自由意志で学習できます。したがって、エージェントのトレーニング環境は現実世界と同一ではないことを考慮することが重要です。

## 強化学習の実行

強化学習モデルのセットアップと実行は、リグレッサーまたは分類器の実行と同じです。同じ 2 つのフラグ、`--freqaimodel` と `--strategy` をコマンド ラインで定義する必要があります。
```bash
freqtrade trade --freqaimodel ReinforcementLearner --strategy MyRLStrategy --config config.json
```
ここで、`ReinforcementLearner` は、`freqai/prediction_models/ReinforcementLearner` のテンプレート化された `ReinforcementLearner` (または、`user_data/freqaimodels` にあるカスタム ユーザー定義のもの) を使用します。一方、この戦略は、典型的なリグレッサーと同じ基本 [特徴エンジニアリング](freqai-feature-engineering.md) と `feature_engineering_*` に従います。違いはターゲットの作成にあり、強化学習ではターゲットの作成は必要ありません。ただし、FreqAI では、アクション列にデフォルト (中立) 値を設定する必要があります。
```python
    def set_freqai_targets(self, dataframe, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/latest/freqai-feature-engineering

        :param df: strategy dataframe which will receive the targets
        usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
        """
        # For RL, there are no direct targets to set. This is filler (neutral)
        # until the agent sends an action.
        dataframe["&-action"] = 0
        return dataframe
```
関数の大部分は通常のリグレッサーと同じですが、以下の関数は、トレーニング環境で生の OHLCV にアクセスできるように、ストラテジーが生の価格データをエージェントに渡す方法を示しています。
```python
    def feature_engineering_standard(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        # The following features are necessary for RL models
        dataframe[f"%-raw_close"] = dataframe["close"]
        dataframe[f"%-raw_open"] = dataframe["open"]
        dataframe[f"%-raw_high"] = dataframe["high"]
        dataframe[f"%-raw_low"] = dataframe["low"]
    return dataframe
```
最後に、作成する明示的な「ラベル」はありません。代わりに、`populate_entry/exit_trends()` でアクセスされたときにエージェントのアクションを含む `&-action` 列を割り当てる必要があります。この例では、ニュートラル アクションを 0 に設定します。この値は、使用される環境に合わせて調整する必要があります。 FreqAI は 2 つの環境を提供し、どちらもニュートラル アクションとして 0 を使用します。

ユーザーは、設定するラベルがないことに気づくと、エージェントが「独自の」入場と退出の決定を行っていることをすぐに理解するでしょう。これにより、戦略の構築がかなり簡単になります。エントリ信号とエグジット信号は整数の形式でエージェントから送信されます。これらは、戦略のエントリとエグジットを決定するために直接使用されます。
```python
    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:

        enter_long_conditions = [df["do_predict"] == 1, df["&-action"] == 1]

        if enter_long_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
            ] = (1, "long")

        enter_short_conditions = [df["do_predict"] == 1, df["&-action"] == 3]

        if enter_short_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
            ] = (1, "short")

        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        exit_long_conditions = [df["do_predict"] == 1, df["&-action"] == 2]
        if exit_long_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_long_conditions), "exit_long"] = 1

        exit_short_conditions = [df["do_predict"] == 1, df["&-action"] == 4]
        if exit_short_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_short_conditions), "exit_short"] = 1

        return df
```
「&-action」は、使用することを選択した環境に依存することを考慮することが重要です。上の例は 5 つのアクションを示しています。0 はニュートラル、1 はロングのエントリー、2 はロングのエグジット、3 はショートのエンター、4 はショートのエグジットです。

## 強化学習器の構成

「強化学習器」を設定するには、次の辞書が「freqai」設定に存在する必要があります。
```json
        "rl_config": {
            "train_cycles": 25,
            "add_state_info": true,
            "max_trade_duration_candles": 300,
            "max_training_drawdown_pct": 0.02,
            "cpu_count": 8,
            "model_type": "PPO",
            "policy_type": "MlpPolicy",
            "model_reward_parameters": {
                "rr": 1,
                "profit_aim": 0.025
            }
        }
```
パラメーターの詳細は [ここ](freqai-parameter-table.md) で見つけることができますが、一般に、`train_cycles` は、エージェントがモデルの重みをトレーニングするために人工環境内のろうそくデータを何回循環するかを決定します。 `model_type` は、[stable_baselines](https://stable-baselines3.readthedocs.io/en/master/)(外部リンク) で利用可能なモデルの 1 つを選択する文字列です。

!!! Note
    「continual_learning」を試したい場合は、メインの「freqai」設定辞書でその値を「true」に設定する必要があります。これにより、再トレーニングが開始されるたびに新しいモデルを最初から再トレーニングするのではなく、以前のモデルの最終状態から新しいモデルのトレーニングを継続するように強化学習ライブラリに指示されます。

!!! Note
    一般的な `model_training_parameters` ディクショナリには、特定の `model_type` のモデル ハイパーパラメータのカスタマイズがすべて含まれている必要があることに注意してください。たとえば、「PPO」パラメータは[ここ](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)で見つけることができます。

## カスタム報酬関数の作成

!!! danger "生産用ではありません"
    警告！
    Freqtrade ソース コードで提供される報酬関数は、可能な限り多くの環境制御機能を表示/テストするように設計された機能のショーケースです。また、小型コンピュータでも高速に実行できるように設計されています。これはベンチマークであり、ライブプロダクション用ではありません。独自のcustom_reward()関数を作成するか、Freqtradeソースコードの外で他のユーザーが作成したテンプレートを使用する必要があることに注意してください。

戦略と予測モデルの変更を始めると、強化学習器とリグレッサー/分類器のいくつかの重要な違いにすぐに気づくでしょう。まず、この戦略には目標値が設定されていません (ラベルはありません!)。代わりに、`MyRLEnv` クラス内に `calculate_reward()` 関数を設定します (以下を参照)。デフォルトの `calculate_reward()` は、報酬を作成するために必要な構成要素を示すために `prediction_models/ReinforcementLearner.py` 内に提供されていますが、これは本番用に設計されたものではありません。ユーザーは独自のカスタム強化学習モデル クラスを作成するか、Freqtrade ソース コードの外部から事前に構築されたモデル クラスを使用して「user_data/freqaimodels」に保存する必要があります。これは `calculate_reward()` の内部にあり、市場に関する創造的な理論を表現できます。たとえば、エージェントが勝った取引をした場合には報酬を与え、エージェントが負けた取引をした場合にはペナルティを与えることができます。あるいは、取引に参加したエージェントに報酬を与え、取引に長時間座りすぎたエージェントにペナルティを与えたい場合もあります。以下に、これらの報酬がすべてどのように計算されるかの例を示します。

!!! note "ヒント"
最良の報酬関数は、連続微分可能で適切にスケーリングできる関数です。言い換えれば、まれなイベントに単一の大きな負のペナルティを追加することは良い考えではなく、ニューラル ネットワークはその関数を学習できません。代わりに、コモンイベントに小さなマイナスのペナルティを追加する方が良いでしょう。これにより、エージェントはより早く学習できるようになります。これだけでなく、いくつかの線形/指数関数に従って重大度に応じて報酬/ペナルティを調整することで、報酬/ペナルティの継続性を向上させることもできます。言い換えれば、取引期間が長くなるにつれてペナルティをゆっくりと調整することになります。これは、単一の時点で単一の大きなペナルティが発生するよりも優れています。
```python
from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv, Positions


class MyCoolRLModel(ReinforcementLearner):
    """
    User created RL prediction model.

    Save this file to `freqtrade/user_data/freqaimodels`

    then use it with:

    freqtrade trade --freqaimodel MyCoolRLModel --config config.json --strategy SomeCoolStrat

    Here the users can override any of the functions
    available in the `IFreqaiModel` inheritance tree. Most importantly for RL, this
    is where the user overrides `MyRLEnv` (see below), to define custom
    `calculate_reward()` function, or to override any other parts of the environment.

    This class also allows users to override any other part of the IFreqaiModel tree.
    For example, the user can override `def fit()` or `def train()` or `def predict()`
    to take fine-tuned control over these processes.

    Another common override may be `def data_cleaning_predict()` where the user can
    take fine-tuned control over the data handling pipeline.
    """
    class MyRLEnv(Base5ActionRLEnv):
        """
        User made custom environment. This class inherits from BaseEnvironment and gym.Env.
        Users can override any functions from those parent classes. Here is an example
        of a user customized `calculate_reward()` function.

        Warning!
        This is function is a showcase of functionality designed to show as many possible
        environment control features as possible. It is also designed to run quickly
        on small computers. This is a benchmark, it is *not* for live production.
        """
        def calculate_reward(self, action: int) -> float:
            # first, penalize if the action is not valid
            if not self._is_valid(action):
                return -2
            pnl = self.get_unrealized_profit()

            factor = 100

            pair = self.pair.replace(':', '')

            # you can use feature values from dataframe
            # Assumes the shifted RSI indicator has been generated in the strategy.
            rsi_now = self.raw_features[f"%-rsi-period_10_shift-1_{pair}_"
                            f"{self.config['timeframe']}"].iloc[self._current_tick]

            # reward agent for entering trades
            if (action in (Actions.Long_enter.value, Actions.Short_enter.value)
                    and self._position == Positions.Neutral):
                if rsi_now < 40:
                    factor = 40 / rsi_now
                else:
                    factor = 1
                return 25 * factor

            # discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return -1
            max_trade_duration = self.rl_config.get('max_trade_duration_candles', 300)
            trade_duration = self._current_tick - self._last_trade_tick
            if trade_duration <= max_trade_duration:
                factor *= 1.5
            elif trade_duration > max_trade_duration:
                factor *= 0.5
            # discourage sitting in position
            if self._position in (Positions.Short, Positions.Long) and \
            action == Actions.Neutral.value:
                return -1 * trade_duration / max_trade_duration
            # close long
            if action == Actions.Long_exit.value and self._position == Positions.Long:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)
            # close short
            if action == Actions.Short_exit.value and self._position == Positions.Short:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)
            return 0.
```
## Tensorboard の使用

強化学習モデルは、トレーニング指標を追跡することで恩恵を受けます。 FreqAI は Tensorboard を統合し、ユーザーがすべてのコインおよびすべての再トレーニングにわたってトレーニングと評価のパフォーマンスを追跡できるようにします。 Tensorboard は次のコマンドでアクティブ化されます。
```bash
tensorboard --logdir user_data/models/unique-id
```
ここで、`unique-id` は、`freqai` 設定ファイルに設定された `identifier` です。ブラウザの 127.0.0.1:6006 (6006 は Tensorboard で使用されるデフォルトのポート) で出力を表示するには、このコマンドを別のシェルで実行する必要があります。

![テンソルボード](assets/tensorboard.jpg)

## カスタムログ

FreqAI は、Tensorboard ログにカスタム情報を追加するための、`self.tensorboard_log` と呼ばれる組み込みのエピソード概要ロガーも提供します。デフォルトでは、この関数は環境内のステップごとに 1 回呼び出され、エージェントのアクションを記録します。 1 つのエピソードのすべてのステップで累積されたすべての値が各エピソードの終了時に報告され、その後、次のエピソードに備えてすべてのメトリクスが 0 に完全にリセットされます。

`self.tensorboard_log` は環境内のどこでも使用できます。たとえば、これを `calculate_reward` 関数に追加して、報酬のさまざまな部分が呼び出された頻度に関するより詳細な情報を収集できます。
```python
    class MyRLEnv(Base5ActionRLEnv):
        """
        User made custom environment. This class inherits from BaseEnvironment and gym.Env.
        Users can override any functions from those parent classes. Here is an example
        of a user customized `calculate_reward()` function.
        """
        def calculate_reward(self, action: int) -> float:
            if not self._is_valid(action):
                self.tensorboard_log("invalid")
                return -2

```
!!! Note
    `self.tensorboard_log()` 関数は、インクリメントされたオブジェクトのみ、つまりトレーニング環境内のイベントやアクションを追跡するように設計されています。対象のイベントが浮動小数点の場合、その浮動小数点を 2 番目の引数として渡すことができます。 `self.tensorboard_log("float_metric1", 0.23)`。この場合、メトリック値は増加しません。

## 基本環境の選択

FreqAI は、「Base3ActionRLEnvironment」、「Base4ActionEnvironment」、「Base5ActionEnvironment」という 3 つの基本環境を提供します。名前が示すように、環境はエージェント向けにカスタマイズされており、3、4、または 5 つのアクションから選択できます。 「Base3ActionEnvironment」は最も単純で、エージェントはホールド、ロング、ショートから選択できます。この環境は、long のみのボットにも使用できます (戦略の `can_short` フラグに自動的に従います)。long は開始条件、short は終了条件です。一方、「Base4ActionEnvironment」では、エージェントはロングに入る、ショートに入る、ニュートラルを維持する、またはポジションを終了することができます。最後に、`Base5ActionEnvironment` では、エージェントは Base4 と同じアクションを持ちますが、単一の終了アクションの代わりに、ロング終了とショート終了が分離されています。環境の選択に起因する主な変更は次のとおりです。

* `calculate_reward` で利用可能なアクション
* ユーザー戦略によって消費されるアクション

FreqAI が提供するすべての環境は、すべての共有ロジックを含む「BaseEnvironment」と呼ばれるアクション/位置に依存しない環境オブジェクトを継承します。アーキテクチャは簡単にカスタマイズできるように設計されています。最も単純なカスタマイズは `calculate_reward()` です (詳細は [こちら](#creating-a-custom-reward-function) を参照してください)。ただし、カスタマイズは環境内の任意の機能にさらに拡張できます。これは、予測モデル ファイルの `MyRLEnv` 内でこれらの関数をオーバーライドするだけで実行できます。または、より高度なカスタマイズの場合は、「BaseEnvironment」から継承したまったく新しい環境を作成することをお勧めします。

!!! Note
    `Base3ActionRLEnv` のみがロングのみのトレーニング/トレードを行うことができます (ユーザー戦略属性 `can_short = False` を設定します)。
