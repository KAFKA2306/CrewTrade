![freqai-ロゴ](assets/freqai_doc_logo.svg)

# 周波数AI

## はじめに

FreqAI は、一連の入力信号を考慮して市場予測を生成する予測機械学習モデルのトレーニングに関連するさまざまなタスクを自動化するように設計されたソフトウェアです。一般に、FreqAI は、リアルタイム データに堅牢な機械学習ライブラリを簡単にデプロイするためのサンドボックスになることを目指しています ([詳細](#freqai-position-in-open-source-machine-learning-landscape))。

!!! Note
    FreqAI は、今後も非営利のオープンソース プロジェクトです。 FreqAI は暗号トークンを「持たず」、FreqAI はシグナルを販売しません。また、FreqAI は現在の [freqtrade ドキュメント](https://www.freqtrade.io/en/latest/freqai/) 以外にドメインを持ちません。

特徴は次のとおりです。

* **自己適応型再トレーニング** - [ライブ デプロイメント](freqai-running.md#live-deployments) 中にモデルを再トレーニングし、監視された方法で市場に自己適応させます。
* **迅速な機能エンジニアリング** - ユーザーが作成したシンプルな戦略に基づいて、大規模で豊富な [機能セット](freqai-feature-engineering.md#feature-engineering) (10,000 以上の機能) を作成します。
* **高パフォーマンス** - スレッド化により、モデル推論 (予測) やボット取引操作とは別のスレッド (または利用可能な場合は GPU) で適応モデルの再トレーニングが可能になります。最新のモデルとデータは RAM に保存され、迅速な推論が可能になります。
* **現実的なバックテスト** - 再トレーニングを自動化する [バックテスト モジュール](freqai-running.md#backtesting) を使用して、履歴データに対する自己適応トレーニングをエミュレートします。
* **拡張性** - 一般化された堅牢なアーキテクチャにより、Python で利用可能な任意の [機械学習ライブラリ/メソッド](freqai-configuration.md#using-Difference-prediction-models) を組み込むことができます。現在、分類子、回帰子、畳み込みニューラル ネットワークを含む 8 つの例が利用可能です
* **スマートな外れ値の削除** - さまざまな [外れ値検出手法](freqai-feature-engineering.md#outlier-detection) を使用して、トレーニングおよび予測データ セットから外れ値を削除します。
* **クラッシュ耐性** - トレーニングされたモデルをディスクに保存して、クラッシュからのリロードを迅速かつ簡単にし、持続的なドライ/ライブ実行のために [古いファイルをパージ](freqai-running.md#purging-old-model-data) します。
* **自動データ正規化** - スマートで統計的に安全な方法で [データを正規化](freqai-feature-engineering.md#building-the-data-pipeline)
* **自動データ ダウンロード** - データ ダウンロードの時間範囲を計算し、履歴データを更新します (ライブ デプロイメントの場合)
* **受信データのクリーニング** - トレーニングとモデル推論の前に NaN を安全に処理します
* **次元削減** - [主成分分析](freqai-feature-engineering.md#data-Dimensionity-reduction-with-principal-component-analysis) を介してトレーニング データのサイズを削減します。
* **ボット フリートの展開** - [コンシューマー](プロデューサー-コンシューマー.md) のフリートがシグナルを使用している間に、1 つのボットを設定してモデルをトレーニングします。

## クイックスタート

FreqAI をすばやくテストする最も簡単な方法は、次のコマンドを使用してドライ モードで実行することです。
```bash
freqtrade trade --config config_examples/config_freqai.example.json --strategy FreqaiExampleStrategy --freqaimodel LightGBMRegressor --strategy-path freqtrade/templates
```
You will see the boot-up process of automatic data downloading, followed by simultaneous training and trading. 

!!! danger "生産用ではありません"
    Freqtrade ソース コードで提供されるサンプル戦略は、さまざまな FreqAI 機能を紹介/テストするために設計されています。 It is also designed to run on small computers so that it can be used as a benchmark between developers and users.これは実稼働環境で実行するように設計されていません。

開始点として使用する戦略、予測モデル、構成の例は、次の場所にあります。
`freqtrade/templates/FreqaiExampleStrategy.py`、`freqtrade/freqai/prediction_models/LightGBMRegressor.py`、および
それぞれ「config_examples/config_freqai.example.json」。

## 一般的なアプローチ

FreqAI には、一連のカスタム *ベース インジケーター* ([一般的な Freqtrade 戦略](strategy-customization.md) と同じ方法) およびターゲット値 (*ラベル*) を提供します。 For each pair in the whitelist, FreqAI trains a model to predict the target values based on the input of custom indicators.その後、市場の状況に適応するために、モデルは所定の頻度で一貫して再トレーニングされます。 FreqAI は、バックテスト戦略 (履歴データの定期的な再トレーニングによる現実のエミュレーション) とドライ/ライブ ランの展開の両方の機能を提供します。ドライ/ライブ条件では、FreqAI をバックグラウンド スレッドで継続的に再トレーニングするように設定して、モデルを可能な限り最新の状態に保つことができます。

An overview of the algorithm, explaining the data processing pipeline and model usage, is shown below.

![freqai-algo](assets/freqai_algo.jpg)

### 機械学習の重要な語彙

**Features** - the parameters, based on historic data, on which a model is trained. All features for a single candle are stored as a vector. FreqAI では、戦略で構築できるあらゆるものから特徴データ セットを構築します。

**ラベル** - モデルがトレーニングされる目標値。 Each feature vector is associated with a single label that is defined by you within the strategy.これらのラベルは意図的に将来を見据えており、予測できるようにモデルをトレーニングするものです。

**トレーニング** - 特徴セットを関連するラベルに一致させるようにモデルを「教える」プロセス。異なるタイプのモデルは異なる方法で「学習」します。つまり、特定のアプリケーションでは、あるモデルが別のモデルよりも優れている可能性があります。 FreqAI にすでに実装されているさまざまなモデルの詳細については、[こちら](freqai-configuration.md#using- Different-prediction-models) を参照してください。

**トレーニング データ** - ターゲットの予測方法をモデルに「教える」ためにトレーニング中にモデルに供給される特徴データ セットのサブセット。このデータは、モデル内の重みの接続に直接影響します。
**テスト データ** - トレーニング後のモデルのパフォーマンスを評価するために使用される特徴データ セットのサブセット。このデータは、モデル内の節点の重みには影響しません。

**推論** - トレーニングされたモデルに、予測を行うための新しい目に見えないデータを供給するプロセス。 

## 前提条件をインストールする

通常の Freqtrade インストール プロセスでは、FreqAI の依存関係をインストールするかどうかを尋ねられます。 FreqAI を使用したい場合は、この質問に「はい」と答える必要があります。 「はい」と答えなかった場合は、インストール後に次のコマンドを使用してこれらの依存関係を手動でインストールできます。
``` bash
pip install -r requirements-freqai.txt
```
!!! Note
    Catboost は、このプラットフォームにホイールが提供されていないため、低電力アーム デバイス (ラズベリー) にはインストールされません。

### docker での使用法

docker を使用している場合は、FreqAI 依存関係を持つ専用のタグが `:freqai` として利用可能です。そのため、docker compose ファイル内の image 行を `image: freqtradeorg/freqtrade:stable_freqai` に置き換えることができます。このイメージには、通常の FreqAI 依存関係が含まれています。ネイティブ インストールと同様に、Catboost は ARM ベースのデバイスでは利用できません。 PyTorch または強化学習を使用したい場合は、トーチまたは RL タグ、`image: freqtradeorg/freqtrade:stable_freqaitorch`、`image: freqtradeorg/freqtrade:stable_freqairl` を使用する必要があります。

!!! note "docker-compose-freqai.yml"
    このための明示的な docker-compose ファイルを `docker/docker-compose-freqai.yml` で提供します。これは、`docker compose -f docker/docker-compose-freqai.yml run ...` 経由で使用できます。または、コピーして元の docker ファイルを置き換えることもできます。この docker-compose ファイルには、docker コンテナー内の GPU リソースを有効にする (無効な) セクションも含まれています。これは明らかに、システムに利用可能な GPU リソースがあることを前提としています。

### オープンソース機械学習環境における FreqAI の地位

株式/暗号通貨市場などのカオスな時系列ベースのシステムを予測するには、幅広い仮説のテストに向けた広範なツールのセットが必要です。幸いなことに、最近の堅牢な機械学習ライブラリ (「scikit-learn」など) の成熟により、幅広い研究の可能性が開かれました。さまざまな分野の科学者が、確立された豊富な機械学習アルゴリズムを使用して研究のプロトタイプを簡単に作成できるようになりました。同様に、これらのユーザーフレンドリーなライブラリにより、「市民科学者」は基本的な Python スキルをデータ探索に使用できるようになります。ただし、これらの機械学習ライブラリを過去のデータ ソースとライブのカオス データ ソースで活用することは、ロジスティック的に困難でコストがかかる可能性があります。さらに、堅牢なデータの収集、保管、処理には、さまざまな課題があります。 [`FreqAI`](#freqai) は、市場予測のための適応モデリングのライブ展開を目的とした、一般化された拡張可能なオープンソース フレームワークを提供することを目的としています。 「FreqAI」フレームワークは、事実上、オープンソースの機械学習ライブラリの豊かな世界のためのサンドボックスです。ユーザーは、「FreqAI」サンドボックス内で、さまざまなサードパーティ ライブラリを組み合わせて、無料のライブ 24 時間年中無休のカオス データ ソース (仮想通貨交換データ) で創造的な仮説をテストできることに気づきました。 

### FreqAI を引用

FreqAI は [Journal of Open Source Software に掲載](https://joss.theoj.org/papers/10.21105/joss.04864) です。 FreqAI が研究に役立つと思われる場合は、次の引用を使用してください。
```bibtex
@article{Caulk2022, 
    doi = {10.21105/joss.04864},
    url = {https://doi.org/10.21105/joss.04864},
    year = {2022}, publisher = {The Open Journal},
    volume = {7}, number = {80}, pages = {4864},
    author = {Robert A. Caulk and Elin Törnquist and Matthias Voppichler and Andrew R. Lawless and Ryan McMullan and Wagner Costa Santos and Timothy C. Pogue and Johan van der Vlugt and Stefan P. Gehring and Pascal Schmidt},
    title = {FreqAI: generalizing adaptive modeling for chaotic time-series market forecasts},
    journal = {Journal of Open Source Software} } 
```
## よくある落とし穴

FreqAI は、動的な ` VolumePairlists` (または、ペアを動的に追加および削除するペアリスト フィルター) と組み合わせることはできません。
これはパフォーマンス上の理由からです。FreqAI は迅速な予測/再トレーニングを行うことに依存しています。これを効果的に行うには、
ドライ/ライブ インスタンスの開始時にすべてのトレーニング データをダウンロードする必要があります。 FreqAI の保存と追加
今後の再トレーニングのために新しいキャンドルが自動的に作成されます。これは、ボリューム ペアリストにより、ドライ ランの後半で新しいペアが到着した場合、データの準備ができていないことを意味します。ただし、FreqAI は、合計ペアリストを一定に保つ「ShufflePairlist」または「 VolumePairlist」を使用して動作します (ただし、ボリュームに応じてペアを並べ替えます)。

## 追加の学習教材

ここでは、FreqAI のさまざまなコンポーネントを詳しく説明するいくつかの外部資料をまとめています。

- [リアルタイムの直接対決: XGBoost と CatBoost を使用した金融市場データの適応モデリング](https://emergentmethods.medium.com/real-time-head-to-head-adaptive-modeling-of-financial-market-data-using-xgboost-and-catboost-995a115a7495)
- [FreqAI - 価格から予測まで](https://emergentmethods.medium.com/freqai-from-price-to-prediction-6fadac18b665)


## サポート

FreqAI のサポートは、[Freqtrade discord](https://discord.gg/Jd8JYeWHc4)、専用の [FreqAI discord](https://discord.gg/7AMWACmbjT)、[github issues](https://github.com/freqtrade/freqtrade/issues) など、さまざまな場所で見つけることができます。

## クレジット

FreqAI は、特定のスキルセットをプロジェクトに貢献する個人のグループによって開発されています。

構想とソフトウェア開発:
ロバート・コーク @robcaulk

理論的なブレインストーミングとデータ分析:
エリン・トーンクイスト @th0rntwig

コードレビューとソフトウェアアーキテクチャのブレーンストーミング:
@xmatthias

ソフトウェア開発:
ワーグナー・コスタ @wagnercosta
エムレ・スゼン @aemr3
ティモシー・ポーグ @wizrds

ベータテストとバグ報告:
Stefan Gehring @bloodhunter4rc、@longyu、Andrew Lawless @paranoidandy、Pascal Schmidt @smidelis、Ryan McMullan @smarmau、Juha Nykänen @suikula、Johan van der Vlugt @jooopiert、Richard Józsa @richardjosza
