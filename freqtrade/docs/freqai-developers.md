# 開発

## プロジェクトのアーキテクチャ

FreqAI のアーキテクチャと機能は一般化されており、独自の機能、機能、モデルなどの開発を促進します。

クラス構造と詳細なアルゴリズムの概要を次の図に示します。

![画像](assets/freqai_algorithm-diagram.jpg)

図に示すように、FreqAI を構成する 3 つの異なるオブジェクトがあります。

* **IFreqaiModel** - データの収集、保存、処理、機能の設計、トレーニングの実行、および推論モデルに必要なロジックをすべて含む単一の永続オブジェクト。
* **FreqaiDataKitchen** - 固有のアセット/モデルごとに固有に作成される非永続オブジェクト。メタデータ以外にも、さまざまなデータ処理ツールも含まれています。
* **FreqaiDataDrawer** - すべての履歴予測、モデル、および保存/読み込みメソッドを含む単一の永続オブジェクト。

`IFreqaiModel` から直接継承するさまざまな組み込み [予測モデル](freqai-configuration.md#using- Different-prediction-models) があります。これらの各モデルは、「IFreqaiModel」のすべてのメソッドに完全にアクセスできるため、これらの関数を自由にオーバーライドできます。ただし、上級ユーザーはおそらく `fit()`、`train()`、`predict()`、および `data_cleaning_train/predict()` のオーバーライドに固執するでしょう。

## データ処理

FreqAI は、後処理を簡素化し、自動データ再読み込みによって衝突耐性を強化する方法でモデル ファイル、予測データ、メタデータを整理することを目的としています。データはファイル構造「user_data_dir/models/」に保存され、トレーニングとバックテストに関連するすべてのデータが含まれます。 `FreqaiDataKitchen()` は適切なトレーニングと推論のためにファイル構造に大きく依存しているため、手動で変更しないでください。

### ファイル構造

ファイル構造は、[config](freqai-configuration.md#setting-up-the-configuration-file) に設定されたモデル `identifier` に基づいて自動生成されます。次の構造は、後処理のためにデータが保存される場所を示しています。

|構造 |説明 |
|----------|---------------|
| `config_*.json` |モデル固有の構成ファイルのコピー。 |
| `歴史的予測.pkl` |ライブ デプロイメント中の「識別子」モデルの存続期間中に生成されたすべての履歴予測を含むファイル。 `history_predictions.pkl` は、クラッシュまたは設定変更後にモデルをリロードするために使用されます。メイン ファイルが破損した場合に備えて、バックアップ ファイルが常に保持されます。 FreqAI は **自動的に** 破損を検出し、破損したファイルをバックアップと置き換えます。 |
| `pair_dictionary.json` |トレーニング キューと、最後にトレーニングされたモデルのディスク上の場所を含むファイル。 |
| `サブトレイン-*_TIMESTAMP` |単一のモデルに関連付けられたすべてのファイルを含むフォルダー。たとえば、次のとおりです。<br>
|| `*_metadata.json` - 正規化の最大/最小、期待されるトレーニング特徴リストなどのモデルのメタデータ。<br>
|| `*_model.*` - クラッシュからの再ロードのためにディスクに保存されたモデル ファイル。 `joblib` (一般的なブースティング ライブラリ)、`zip` (stable_baselines)、`hd5` (keras タイプ) などを指定できます。 <br>
|| `*_pca_object.pkl` - 目に見えない予測特徴を変換するために使用される [主成分分析 (PCA)](freqai-feature-engineering.md#data-Dimensionity-reduction-with-principal-component-analysis) 変換 (構成で `principal_component_analysis: True` が設定されている場合)。 <br>
|| `*_svm_model.pkl` - 目に見えない予測機能の異常値を検出するために使用される [サポート ベクター マシン (SVM)](freqai-feature-engineering.md#identifying-outliers-using-a-support-vector-machine-svm) モデル (構成で `use_SVM_to_remove_outliers: True` が設定されている場合)。 <br>
|| `*_trained_df.pkl` - `identifier` モデルのトレーニングに使用されるすべてのトレーニング特徴を含むデータフレーム。これは、[相違指数 (DI)](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di) の計算に使用され、後処理にも使用できます。 <br>
|| `*_trained_dates.df.pkl` - `trained_df.pkl` に関連付けられた日付。後処理に役立ちます。 |

ファイル構造の例は次のようになります。
```
├── models
│   └── unique-id
│       ├── config_freqai.example.json
│       ├── historic_predictions.backup.pkl
│       ├── historic_predictions.pkl
│       ├── pair_dictionary.json
│       ├── sub-train-1INCH_1662821319
│       │   ├── cb_1inch_1662821319_metadata.json
│       │   ├── cb_1inch_1662821319_model.joblib
│       │   ├── cb_1inch_1662821319_pca_object.pkl
│       │   ├── cb_1inch_1662821319_svm_model.joblib
│       │   ├── cb_1inch_1662821319_trained_dates_df.pkl
│       │   └── cb_1inch_1662821319_trained_df.pkl
│       ├── sub-train-1INCH_1662821371
│       │   ├── cb_1inch_1662821371_metadata.json
│       │   ├── cb_1inch_1662821371_model.joblib
│       │   ├── cb_1inch_1662821371_pca_object.pkl
│       │   ├── cb_1inch_1662821371_svm_model.joblib
│       │   ├── cb_1inch_1662821371_trained_dates_df.pkl
│       │   └── cb_1inch_1662821371_trained_df.pkl
│       ├── sub-train-ADA_1662821344
│       │   ├── cb_ada_1662821344_metadata.json
│       │   ├── cb_ada_1662821344_model.joblib
│       │   ├── cb_ada_1662821344_pca_object.pkl
│       │   ├── cb_ada_1662821344_svm_model.joblib
│       │   ├── cb_ada_1662821344_trained_dates_df.pkl
│       │   └── cb_ada_1662821344_trained_df.pkl
│       └── sub-train-ADA_1662821399
│           ├── cb_ada_1662821399_metadata.json
│           ├── cb_ada_1662821399_model.joblib
│           ├── cb_ada_1662821399_pca_object.pkl
│           ├── cb_ada_1662821399_svm_model.joblib
│           ├── cb_ada_1662821399_trained_dates_df.pkl
│           └── cb_ada_1662821399_trained_df.pkl

```
