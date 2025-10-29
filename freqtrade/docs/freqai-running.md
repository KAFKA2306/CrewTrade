# FreqAI を実行する

適応型機械学習モデルをトレーニングしてデプロイするには、ライブ デプロイメントと履歴バックテストという 2 つの方法があります。どちらの場合も、次の図に示すように、FreqAI はモデルの定期的な再トレーニングを実行/シミュレーションします。

![freqai-window](assets/freqai_moving-window.jpg)

## ライブデプロイメント

FreqAI は、次のコマンドを使用してドライ/ライブで実行できます。
```bash
freqtrade trade --strategy FreqaiExampleStrategy --config config_freqai.example.json --freqaimodel LightGBMRegressor
```
FreqAI を起動すると、構成設定に基づいて新しい「識別子」を使用して新しいモデルのトレーニングを開始します。トレーニング後、新しいモデルが利用可能になるまで、このモデルは入ってくるローソク足の予測に使用されます。新しいモデルは通常、可能な限り頻繁に生成され、FreqAI がコイン ペアの内部キューを管理して、すべてのモデルを同等に最新の状態に保つよう努めます。 FreqAI は、常に最新のトレーニング済みモデルを使用して、受信するライブ データを予測します。 FreqAI に新しいモデルをできるだけ頻繁に再トレーニングさせたくない場合は、「live_retrain_hours」を設定して、新しいモデルをトレーニングする前に少なくともその時間数待機するように FreqAI に指示できます。さらに、`expired_hours` を設定して、その時間数よりも古いモデルの予測を避けるように FreqAI に指示することができます。

トレーニングされたモデルはデフォルトでディスクに保存され、バックテスト中またはクラッシュ後に再利用できるようになります。設定で `"purge_old_models": true` を設定することで、ディスク領域を節約するために [古いモデルをパージ](#purging-old-model-data) することを選択できます。

保存されたバックテスト モデル (または以前にクラッシュしたドライ/ライブ セッション) からドライ/ライブ実行を開始するには、特定のモデルの「識別子」を指定するだけです。
```json
    "freqai": {
        "identifier": "example",
        "live_retrain_hours": 0.5
    }
```
この場合、FreqAI は事前トレーニングされたモデルで開始されますが、モデルがトレーニングされてからどのくらいの時間が経過したかを確認します。ロードされたモデルの終了から完全な「live_retrain_hours」が経過すると、FreqAI は新しいモデルのトレーニングを開始します。

### データの自動ダウンロード

FreqAI は、定義された `train_period_days` および `startup_candle_count` を通じてモデルのトレーニングを確実にするために必要な適切な量のデータを自動的にダウンロードします (これらのパラメーターの詳細な説明については、[パラメーター テーブル](freqai-parameter-table.md) を参照してください)。 

### 予測データの保存

特定の「識別子」モデルの存続期間中に行われたすべての予測は「history_predictions.pkl」に保存され、クラッシュや構成の変更後に再ロードできるようになります。

### 古いモデルデータの削除

FreqAI は、トレーニングが成功するたびに新しいモデル ファイルを保存します。新しい市場条件に適応するために新しいモデルが生成されると、これらのファイルは廃止されます。高頻度の再トレーニングで FreqAI を長期間実行したままにする場合は、設定で「purge_old_models」を有効にする必要があります。
```json
    "freqai": {
        "purge_old_models": 4,
    }
```
これにより、ディスク領域を節約するために、最近トレーニングされた 4 つのモデルよりも古いすべてのモデルが自動的に削除されます。 「0」を入力してもモデルは削除されません。

## バックテスト

FreqAI バックテスト モジュールは、次のコマンドで実行できます。
```bash
freqtrade backtesting --strategy FreqaiExampleStrategy --strategy-path freqtrade/templates --config config_examples/config_freqai.example.json --freqaimodel LightGBMRegressor --timerange 20210501-20210701
```
このコマンドが既存の構成ファイルで実行されたことがない場合、FreqAI は新しいモデルをトレーニングします
各ペア、展開された `--timerange` 内の各バックテスト ウィンドウについて。

バックテスト モードでは、展開前に [必要なデータをダウンロードする](#downloading-data-to-cover-the-full-backtest-period) 必要があります (FreqAI がデータのダウンロードを自動的に処理するドライ/ライブ モードとは異なります)。ダウンロードされたデータの時間範囲がバックテストの時間範囲よりも長いことを考慮する必要があります。これは、設定されたバックテスト時間範囲の最初のローソク足で予測できるようにモデルをトレーニングするために、FreqAI が必要なバックテスト時間範囲よりも前のデータを必要とするためです。ダウンロードするデータの計算方法の詳細については、[こちら](#decding-the-size-of-the-sliding-training-window-and-backtesting-duration)を参照してください。

!!! Note "モデルの再利用"
    トレーニングが完了したら、同じ構成ファイルを使用してバックテストを再度実行できます。
    FreqAI は、トレーニングに時間を費やす代わりに、トレーニングされたモデルを見つけてロードします。これは便利です
    戦略内の売買基準を微調整（またはハイパーオプト）したい場合。もしあなたが
    同じ構成ファイルを使用して新しいモデルを再トレーニングしたい場合は、単に「識別子」を変更する必要があります。
    このようにして、「識別子」を指定するだけで、希望するモデルの使用に戻ることができます。

!!! Note
    バックテストは、バックテスト ウィンドウごとに `set_freqai_targets()` を 1 回呼び出します (ウィンドウの数は、完全なバックテストの時間範囲を `backtest_period_days` パラメーターで割ったものです)。これを行うことは、ターゲットが先読みバイアスなしでドライ/ライブ動作をシミュレートすることを意味します。ただし、`feature_engineering_*()` での特徴の定義は、トレーニング時間範囲全体で 1 回実行されます。これは、機能が将来を先取りしたものではないことを確認する必要があることを意味します。
    先読みバイアスの詳細については、[よくある間違い](strategy-customization.md#common-mistakes-when-developing-strategies) を参照してください。

---

### バックテスト予測データの保存

戦略を微調整できるようにするため (**機能ではありません**!)、FreqAI はバックテスト中に予測を自動的に保存し、同じ「識別子」モデルを使用して将来のバックテストやライブ実行で再利用できるようにします。これにより、開始/終了基準の **高レベルのハイパーオプティング** を可能にすることを目的としたパフォーマンスの強化が提供されます。

「backtesting_predictions」という追加のディレクトリが「feather」形式で保存されたすべての予測を含み、「unique-id」フォルダに作成されます。

**機能**を変更するには、構成に新しい「識別子」を設定して、新しいモデルをトレーニングするように FreqAI に信号を送信する必要があります**。
特定のバックテスト中に生成されたモデルを保存して、新しいモデルをトレーニングする代わりに、そのうちの 1 つからライブ デプロイメントを開始できるようにするには、構成で `save_backtest_models` を `True` に設定する必要があります。

!!! Note
    モデルを確実に再利用できるようにするために、freqAI は長さ 1 のデータフレームを使用してストラテジーを呼び出します。 
    同じ機能を生成するために戦略でこれより多くのデータが必要な場合、ライブ デプロイメントでバックテスト予測を再利用することはできず、新しいバックテストごとに「識別子」を更新する必要があります。

### 収集された予測をライブでバックテストする

FreqAI を使用すると、バックテスト パラメーター `--freqai-backtest-live-models` を通じてライブ履歴予測を再利用できます。これは、ドライランで生成された予測を比較や他の調査のために再利用したい場合に役立ちます。

`--timerange` パラメータは、履歴予測ファイル内のデータを通じて自動的に計算されるため、通知する必要はありません。

### バックテスト期間全体をカバーするデータをダウンロードする

ライブ/ドライ展開の場合、FreqAI は必要なデータを自動的にダウンロードします。ただし、バックテスト機能を使用するには、`download-data` を使用して必要なデータをダウンロードする必要があります (詳細は [こちら](data-download.md#data-downloading))。バックテストの時間範囲の開始「前」に十分な量のトレーニング データがあることを確認するには、どのくらいの「追加」データをダウンロードする必要があるかを理解することに細心の注意を払う必要があります。追加データの量は、時間範囲の開始日を、希望するバックテスト時間範囲の先頭から `train_period_days` と `startup_candle_count` (これらのパラメーターの詳細な説明については、[パラメーター テーブル](freqai-parameter-table.md) を参照してください) だけ後方に移動することによって大まかに見積もることができます。 

例として、[example config](freqai-configuration.md#setting-up-the-configuration-file) を使用して `--timerange 20210501-20210701` をバックテストするには、`train_period_days` を 30 に設定し、最大 1 時間の `include_timeframes` で `startup_candle_count: 40` を設定します。ダウンロードされたデータの開始日は、`20210501` - 30 日 - 40 * 1 時間 / 24 時間 = 20210330 (目的のトレーニング時間範囲の開始日より 31.7 日前) である必要があります。

### スライディング トレーニング ウィンドウのサイズとバックテスト期間の決定

バックテストの時間範囲は、設定ファイル内の一般的な `--timerange` パラメータで定義されます。スライディング トレーニング ウィンドウの期間は `train_period_days` で設定され、`backtest_period_days` はスライディング バックテスト ウィンドウで、どちらも日数で設定されます (`backtest_period_days` は
ライブ/ドライ モードでの日次再トレーニングを示す浮動小数点数)。提示された [設定例](freqai-configuration.md#setting-up-the-configuration-file) (`config_examples/config_freqai.example.json` にあります) では、ユーザーは FreqAI に 30 日間のトレーニング期間とその後の 7 日間のバックテストを使用するよう求めています。モデルのトレーニング後、FreqAI はその後 7 日間バックテストを実行します。次に、「スライディング ウィンドウ」は 1 週間前に進み (ライブ モードで週に 1 回 FreqAI の再トレーニングをエミュレート)、新しいモデルは過去 30 日間 (前のモデルでバックテストに使用された 7 日間を含む) をトレーニングに使用します。これは `--timerange` の終わりまで繰り返されます。  これは、「--timerange 20210501-20210701」を設定すると、FreqAI は「--timerange」の最後に 8 つの個別のモデルをトレーニングしたことになります (全範囲が 8 週間で構成されるため)。

!!! Note
    端数の `backtest_period_days` は許可されていますが、全範囲をバックテストするために FreqAI がトレーニングする必要があるモデルの数を決定するために、`--timerange` がこの値で除算されることに注意する必要があります。たとえば、「--timerange」を 10 日、「backtest_period_days」を 0.1 に設定すると、FreqAI は完全なバックテストを完了するためにペアごとに 100 個のモデルをトレーニングする必要があります。このため、FreqAI 適応トレーニングの実際のバックテストには「非常に」長い時間がかかります。モデルを完全にテストする最良の方法は、モデルをドライで実行し、継続的にトレーニングさせることです。この場合、バックテストにはドライランとまったく同じ時間がかかります。

## モデルの有効期限の定義

ドライ/ライブ モード中、FreqAI は各コイン ペアを順番にトレーニングします (メインの Freqtrade ボットとは別のスレッド/GPU で)。これは、モデル間には常に年齢の不一致があることを意味します。 50 ペアでトレーニングし、各ペアのトレーニングに 5 分かかる場合、最も古いモデルは 4 時間以上前のものになります。戦略の特性時間スケール (目標取引期間) が 4 時間未満の場合、これは望ましくない可能性があります。設定ファイルで `expiration_hours` を設定することで、モデルの古い時間が特定の時間未満である場合にのみ取引エントリを行うように決定できます。
```json
    "freqai": {
        "expiration_hours": 0.5,
    }
```
提示された構成例では、ユーザーは 30 時間未満のモデルの予測のみを許可します。

## モデル学習プロセスの制御

モデル トレーニング パラメーターは、選択した機械学習ライブラリに固有です。 FreqAI では、構成内の `model_training_parameters` 辞書を使用して、任意のライブラリの任意のパラメータを設定できます。設定例 (`config_examples/config_freqai.example.json` にあります) には、`Catboost` および `LightGBM` に関連付けられたパラメーターの例がいくつか示されていますが、これらのライブラリで使用可能なパラメーターや、実装することを選択したその他の機械学習ライブラリを追加することもできます。

データ分割パラメータは「data_split_parameters」で定義されます。これには、scikit-learn の「train_test_split()」関数に関連付けられた任意のパラメータを指定できます。 `train_test_split()` には、データをシャッフルしたり、シャッフルせずに保持したりできる `shuffle` と呼ばれるパラメータがあります。これは、時間的に自動相関したデータによるトレーニングのバイアスを回避するのに特に役立ちます。これらのパラメーターの詳細については、[scikit-learn Web サイト](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) (外部 Web サイト) を参照してください。

FreqAI 固有のパラメータ `label_period_candles` は、`labels` に使用されるオフセット (将来へのキャンドルの数) を定義します。提示された [設定例](freqai-configuration.md#setting-up-the-configuration-file) では、ユーザーは将来の 24 のローソク足である「ラベル」を求めています。

## 継続的な学習

設定で「continual_learning」: true を設定することで、継続的学習スキームの採用を選択できます。 「continual_learning」を有効にすると、最初のモデルを最初からトレーニングした後、後続のトレーニングは前のトレーニングの最終モデル状態から開始されます。これにより、新しいモデルに以前の状態の「記憶」が与えられます。デフォルトでは、これは「False」に設定されています。これは、すべての新しいモデルが、以前のモデルからの入力なしで、最初からトレーニングされることを意味します。

???+ 危険 「継続的な学習により、一定のパラメータ空間が強制されます」
    「continual_learning」は、モデルのパラメータ空間がトレーニング間で「変更できない」ことを意味するため、「continual_learning」が有効な場合、「principal_component_analysis」は自動的に無効になります。ヒント: PCA はパラメーター空間と特徴の数を変更します。PCA の詳細については、[こちら](freqai-feature-engineering.md#data-Dimensionity-reduction-with-principal-component-analysis) をご覧ください。

???+危険「実験的な機能」
これは現時点では増分学習に対する素朴なアプローチであり、市場がモデルから遠ざかるにつれて過剰適合したり極小値に陥ったりする可能性が高いことに注意してください。 FreqAI には主に実験目的で利用できるメカニズムがあり、仮想通貨市場のような混沌としたシステムで継続的に学習するためのより成熟したアプローチに備えることができます。

## ハイパーオプト

[典型的な Freqtrade hyperopt](hyperopt.md) と同じコマンドを使用して hyperopt できます。
```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy FreqaiExampleStrategy --freqaimodel LightGBMRegressor --strategy-path freqtrade/templates --config config_examples/config_freqai.example.json --timerange 20220428-20220507
```
`hyperopt` では、[バックテスト](#backtesting) を行う場合と同じ方法でデータを事前にダウンロードする必要があります。さらに、FreqAI 戦略をハイパーオプト化しようとする場合は、いくつかの制限を考慮する必要があります。

- `--analyze-per-epoch` hyperopt パラメータは FreqAI と互換性がありません。
- `feature_engineering_*()` および `set_freqai_targets()` 関数でインジケーターをハイパーオプトすることはできません。これは、hyperopt を使用してモデル パラメーターを最適化できないことを意味します。この例外とは別に、他のすべての [スペース](hyperopt.md#running-hyperopt-with-smaller-search-space) を最適化することができます。
- バックテストの手順は hyperopt にも適用されます。

hyperopt と FreqAI を組み合わせる最良の方法は、ハイパーオプトの入口/出口のしきい値/基準に焦点を当てることです。機能で使用されていないパラメーターのハイパーオプト化に重点を置く必要があります。たとえば、特徴作成時にローリング ウィンドウの長さをハイパーオプトしたり、予測を変更する FreqAI 構成の一部を変更したりしないでください。 FreqAI 戦略を効率的に高度に最適化するために、FreqAI は予測をデータフレームとして保存し、再利用します。したがって、入口/出口のしきい値/基準のみをハイパーオプトする必要があります。

FreqAI の超最適パラメータの好例は、[相違指数 (DI)](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di) `DI_values` のしきい値であり、これを超えるとデータ ポイントが外れ値と見なされます。
```python
di_max = IntParameter(low=1, high=20, default=10, space='buy', optimize=True, load=True)
dataframe['outlier'] = np.where(dataframe['DI_values'] > self.di_max.value/10, 1, 0)
```
この特定の hyperopt は、特定のパラメータ空間に適切な「DI_values」を理解するのに役立ちます。

## Tensorboard の使用

!!! note "可用性"
    FreqAI には、XGBoost、すべての PyTorch モデル、強化学習、Catboost など、さまざまなモデル用のテンソルボードが含まれています。 Tensorboard を別のモデル タイプに統合したい場合は、[Freqtrade GitHub](https://github.com/freqtrade/freqtrade/issues) で問題を開いてください。

!!! danger "要件"
    Tensorboard のロギングには、FreqAI トーチのインストール/Docker イメージが必要です。


tensorboard を使用する最も簡単な方法は、設定ファイルで `freqai.activate_tensorboard` が `True` (デフォルト設定) に設定されていることを確認し、FreqAI を実行してから、別のシェルを開いて次を実行することです。
```bash
cd freqtrade
tensorboard --logdir user_data/models/unique-id
```
ここで、`unique-id` は、`freqai` 設定ファイルに設定された `identifier` です。 This command must be run in a separate shell if you wish to view the output in your browser at 127.0.0.1:6060 (6060 is the default port used by Tensorboard).

![テンソルボード](assets/tensorboard.jpg)


!!! note "パフォーマンスを向上させるために非アクティブ化します"
    Tensorboard ロギングはトレーニングを遅くする可能性があるため、運用環境で使用する場合は無効にする必要があります。
