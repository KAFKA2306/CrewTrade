# 開発ヘルプ

このページは、Freqtrade の開発者、Freqtrade のコードベースやドキュメントに貢献したい人、または実行しているアプリケーションのソース コードを理解したい人を対象としています。

すべての貢献、バグレポート、バグ修正、ドキュメントの改善、拡張機能、アイデアを歓迎します。 [GitHub](https://github.com) で [問題を追跡](https://github.com/freqtrade/freqtrade/issues) しており、[discord](https://discord.gg/p7nuUNVfP7) に質問できる開発チャンネルもあります。

## ドキュメント

ドキュメントは [https://freqtrade.io](https://www.freqtrade.io/) で入手でき、新機能の PR ごとに提供する必要があります。

ドキュメントの特別なフィールド (メモ ボックスなど) は、[ここ](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) にあります。

ドキュメントをローカルでテストするには、次のコマンドを使用します。
``` bash
pip install -r docs/requirements-docs.txt
mkdocs serve
```
これにより、ローカル サーバー (通常はポート 8000) が起動し、すべてが期待通りに動作しているかどうかを確認できます。

## 開発者のセットアップ

開発環境を構成するには、提供されている [DevContainer](#devcontainer-setup) を使用するか、`setup.sh` スクリプトを使用して、「Dev [y/N] の依存関係をインストールしますか?」という質問に「y」と答えることができます。
あるいは (たとえば、システムが setup.sh スクリプトでサポートされていない場合)、手動インストール プロセスに従い、`pip3 install -r required-dev.txt` を実行し、続いて `pip3 install -e .[all]` を実行します。

これにより、「pytest」、「ruff」、「mypy」、「coveralls」など、開発に必要なツールがすべてインストールされます。

次に、「pre-commit install」を実行して git フック スクリプトをインストールします。これにより、コミットする前に変更がローカルで検証されます。
これにより、いくつかの基本的な書式設定チェックがマシン上でローカルに行われるため、CI を待つ時間が大幅に短縮されます。

プル リクエストを開く前に、[貢献ガイドライン](https://github.com/freqtrade/freqtrade/blob/develop/CONTRIBUTING.md) をよく理解してください。

### Devcontainer のセットアップ

最も速く簡単に始める方法は、[VSCode](https://code.visualstudio.com/) をリモート コンテナー拡張機能とともに使用することです。
これにより、開発者は、ローカル マシンに freqtrade 固有の依存関係をインストールする必要がなく、必要なすべての依存関係を使用してボットを起動できるようになります。

#### Devcontainer の依存関係

* [VSCode](https://code.visualstudio.com/)
* [docker](https://docs.docker.com/install/)
* [リモート コンテナー拡張機能のドキュメント](https://code.visualstudio.com/docs/remote)

[リモート コンテナ拡張機能](https://code.visualstudio.com/docs/remote) の詳細については、ドキュメントを参照してください。

### テスト

新しいコードは基本的な単体テストでカバーする必要があります。機能の複雑さに応じて、レビュー担当者はより詳細な単体テストを要求する場合があります。
必要に応じて、Freqtrade チームが適切なテストの作成を支援し、指導します (ただし、誰かがあなたの代わりにテストを書いてくれることを期待しないでください)。

#### テストの実行方法

ルート フォルダーで `pytest` を使用して、利用可能なすべてのテストケースを実行し、ローカル環境が正しく設定されていることを確認します。

!!! 「機能ブランチ」に注意してください
    テストは「develop」ブランチと「stable」ブランチで合格することが期待されます。他のブランチは作業が進行中であり、テストはまだ機能していない可能性があります。

#### テストでのログの内容の確認

Freqtrade は、テストでログの内容をチェックするために 2 つの主なメソッド、`log_has()` と `log_has_re()` を使用します (動的ログ メッセージの場合、正規表現を使用してチェックします)。
これらは「conftest.py」から入手でき、任意のテスト モジュールにインポートできます。

サンプルチェックは次のようになります。
``` python
from tests.conftest import log_has, log_has_re

def test_method_to_test(caplog):
    method_to_test()

    assert log_has("This event happened", caplog)
    # Check regex with trailing number ...
    assert log_has_re(r"This dynamic event happened and produced \d+", caplog)

```
### デバッグ構成

freqtrade をデバッグするには、次の起動構成 (`.vscode/launch.json` にあります) を備えた VSCode (Python 拡張機能を含む) をお勧めします。
詳細はセットアップごとに明らかに異なりますが、開始するにはこれでうまくいくはずです。
``` json
{
    "name": "freqtrade trade",
    "type": "debugpy",
    "request": "launch",
    "module": "freqtrade",
    "console": "integratedTerminal",
    "args": [
        "trade",
        // Optional:
        // "--userdir", "user_data",
        "--strategy", 
        "MyAwesomeStrategy",
    ]
},
```
コマンドライン引数は `"args"` 配列に追加できます。
このメソッドは、ストラテジ内にブレークポイントを設定することにより、ストラテジのデバッグにも使用できます。

Pycharm でも同様の設定を行うことができます。モジュール名として「freqtrade」を使用し、コマンドライン引数を「パラメータ」として設定します。

???ヒント「venv の正しい使い方」
    仮想環境を使用する場合 (そうすべきです)、問題や「不明なインポート」エラーを避けるために、エディターが正しい仮想環境を使用していることを確認してください。

    #### Vscode

    「Python: Select Interpreter」コマンドを使用して、VSCode で正しい環境を選択できます。これにより、拡張機能が検出した環境が表示されます。
    環境が検出されない場合は、手動でパスを選択することもできます。

    #### Pycharm

    pycharm では、「実行/デバッグ構成」ウィンドウで適切な環境を選択できます。
    ![Pycharm デバッグ構成](assets/pycharm_debug.png)

!!! 「起動ディレクトリ」についての注意
    これは、リポジトリがチェックアウトされており、エディタがリポジトリのルート レベルで起動されていることを前提としています (したがって、pyproject.toml はリポジトリの最上位にあります)。

## エラー処理

Freqtrade 例外はすべて `FreqtradeException` から継承されます。
ただし、この一般的なクラスのエラーは直接使用しないでください。代わりに、複数の特殊なサブ例外が存在します。

以下は、例外継承階層の概要です。
```
+ FreqtradeException
|
+---+ OperationalException
|   |
|   +---+ ConfigurationError
|
+---+ DependencyException
|   |
|   +---+ PricingError
|   |
|   +---+ ExchangeError
|       |
|       +---+ TemporaryError
|       |
|       +---+ DDosProtection
|       |
|       +---+ InvalidOrderException
|           |
|           +---+ RetryableOrderError
|           |
|           +---+ InsufficientFundsError
|
+---+ StrategyError
```
---

## プラグイン

### ペアリスト

試してみたい新しいペア選択アルゴリズムに関する素晴らしいアイデアがありますか?素晴らしい。
できれば、これを上流に貢献していただければ幸いです。

動機が何であれ、これにより、新しいペアリスト ハンドラーの開発を始めることができるはずです。

まず、[VolumePairList](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/plugins/pairlist/VolumePairList.py) ハンドラーを確認し、このファイルを新しいペアリスト ハンドラーの名前でコピーするのが最適です。

これは単純なハンドラーですが、開発を開始する方法の良い例として役立ちます。

次に、ハンドラーのクラス名を変更します (理想的には、これをモジュールのファイル名に合わせます)。

基本クラスは、交換 (`self._exchange`)、ペアリスト マネージャー (`self._pairlistmanager`) のインスタンスに加えて、メイン設定 (`self._config`)、ペアリスト専用設定 (`self._pairlistconfig`)、およびペアリストのリスト内の絶対位置を提供します。
```python
        self._exchange = exchange
        self._pairlistmanager = pairlistmanager
        self._config = config
        self._pairlistconfig = pairlistconfig
        self._pairlist_pos = pairlist_pos
```
!!! ヒント
    ペアリストを変数 `AVAILABLE_PAIRLISTS` の下の `constants.py` に登録することを忘れないでください。そうしないと選択できなくなります。

次に、アクションが必要なメソッドを順に見ていきましょう。

#### ペアリスト構成

ペアリスト ハンドラーのチェーンの構成は、要素 `"pairlists"` のボット構成ファイルで行われます。これは、チェーン内の各ペアリスト ハンドラーの構成パラメーターの配列です。

慣例により、「number_assets」はペアリストに保持するペアの最大数を指定するために使用されます。一貫したユーザーエクスペリエンスを確保するには、これに従ってください。

必要に応じて追加のパラメータを設定できます。たとえば、`VolumePairList` は、`"sort_key"` を使用して並べ替え値を指定します。ただし、優れたアルゴリズムが成功し、動的に動作するために必要なものは何でも自由に指定してください。

#### short_desc

Telegram メッセージに使用される説明を返します。

これには、ペアリスト ハンドラーの名前と、アセットの数を含む短い説明が含まれている必要があります。 「ペアリスト名 - 上位/下位 X ペア」の形式に従ってください。

#### gen_pairlist

ペアリスト ハンドラーがチェーン内の先頭のペアリスト ハンドラーとして使用できる場合は、このメソッドをオーバーライドして、チェーン内のすべてのペアリスト ハンドラーによって処理される最初のペアリストを定義します。例としては、`StaticPairList` や ` VolumePairList` があります。

これはボットの反復ごとに呼び出されます (ペアリスト ハンドラーが最初の場所にある場合のみ)。そのため、コンピューティング/ネットワークの負荷が高い計算にはキャッシュを実装することを検討してください。

結果のペアリストを返す必要があります (ペアリスト ハンドラーのチェーンに渡すことができます)。

検証はオプションであり、親クラスはデフォルトのフィルタリングを行うために `verify_blacklist(pairlist)` と `_whitelist_for_active_markets(pairlist)` を公開します。結果を特定の数のペアに制限する場合、これを使用します。これにより、最終結果が予想より短くなりません。

#### フィルターペアリスト

このメソッドは、ペアリスト マネージャーによってチェーン内の各ペアリスト ハンドラーに対して呼び出されます。

これはボットの反復ごとに呼び出されます。そのため、コンピューティング/ネットワークの負荷が高い計算のためにキャッシュを実装することを検討してください。

これには、ペアリスト (以前のペアリストの結果である可能性があります) と、`get_tickers()` のプリフェッチされたバージョンである `tickers` が渡されます。

基本クラスのデフォルト実装は、ペアリスト内の各ペアに対して `_validate_pair()` メソッドを呼び出すだけですが、これをオーバーライドすることもできます。したがって、ペアリスト ハンドラーに `_validate_pair()` を実装するか、別の処理を行うために `filter_pairlist()` をオーバーライドする必要があります。

オーバーライドされた場合は、結果のペアリストを返す必要があります (その後、チェーン内の次のペアリスト ハンドラーに渡すことができます)。
検証はオプションであり、親クラスはデフォルトのフィルターを実行するための `verify_blacklist(pairlist)` と `_whitelist_for_active_markets(pairlist)` を公開します。結果を特定のペア数に制限する場合、これを使用して、最終結果が予想より短くならないようにします。

`VolumePairList` では、さまざまなソート方法を実装し、早期の検証を行って、予想される数のペアのみが返されるようにします。

##### サンプル
``` python
    def filter_pairlist(self, pairlist: list[str], tickers: dict) -> List[str]:
        # Generate dynamic whitelist
        pairs = self._calculate_pairlist(pairlist, tickers)
        return pairs
```
### 保護

保護について理解するには、[保護に関するドキュメント](plugins.md#protections) を読むことをお勧めします。
このガイドは、新しい保護を開発したい開発者を対象としています。

保護では datetime を直接使用する必要はありませんが、日付の計算には提供された `date_now` 変数を使用してください。これにより、保護をバックテストする機能が維持されます。

!!! ヒント「新しい保護を作成する」
    良い例として、既存の保護の 1 つをコピーするのが最適です。

#### 新しい保護の実装

すべての Protection 実装には、親クラスとして `IProtection` が必要です。
このため、次のメソッドを実装する必要があります。

* `short_desc()`
* `global_stop()`
* `stop_per_pair()`。

`global_stop()` と `stop_per_pair()` は、以下で構成される ProtectionReturn オブジェクトを返さなければなりません。

* ロックペア - ブール値
* ロック期限 - 日時 - いつまでペアをロックするか (次の新しいローソク足に切り上げられます)
*reason - データベースへのログ記録と保存に使用される文字列
* lock_side - 長い、短い、または '*'。

「until」部分は、提供されている「calculate_lock_end()」メソッドを使用して計算する必要があります。

すべての保護では、`"stop_duration"` / `"stop_duration_candles"` を使用して、ペア (またはすべてのペア) をロックする期間を定義する必要があります。
この内容は、`self._stop_duration` として各保護に利用可能になります。

保護にルックバック期間が必要な場合は、「lookback_period」/「lockback_period_candles」を使用して、すべての保護を調整してください。

#### グローバル ストップとローカル ストップ

プロテクションには、制限付きで取引を停止する 2 つの異なる方法があります。

* ペアごと（ローカル）
* すべてのペア (グローバル)

##### 保護 - ペアごと

ペアごとのアプローチを実装する保護では、「has_local_stop=True」を設定する必要があります。
メソッド `stop_per_pair()` は取引が終了する (決済注文が完了する) たびに呼び出されます。

##### 保護 - グローバルな保護

これらの保護はすべてのペアにわたって評価を行う必要があり、その結果、すべてのペアの取引がロックされます (グローバル ペアロックと呼ばれます)。
グローバル保護は、グローバル ストップに対して評価されるように「has_global_stop=True」を設定する必要があります。
メソッド `global_stop()` は取引が終了する (決済注文が完了する) たびに呼び出されます。

##### 保護 - ロック終了時刻の計算

プロテクションは、考慮する最後の取引に基づいてロックの終了時間を計算する必要があります。
これにより、ルックバック期間が実際のロック期間よりも長い場合の再ロックが回避されます。

`IProtection` 親クラスは、`calculate_lock_end()` でこのためのヘルパー メソッドを提供します。

---

## 新しい Exchange (WIP) を実装する

!!! 注記
    このセクションは進行中の作業であり、Freqtrade で新しい取引所をテストする方法に関する完全なガイドではありません。

!!! 注記
    以下のテストを実行する前に、必ず最新バージョンの CCXT を使用してください。
有効化された仮想環境で `pip install -U ccxt` を実行すると、ccxt の最新バージョンを入手できます。
    ネイティブ Docker はこれらのテストではサポートされていませんが、利用可能な開発コンテナは必要なアクションをすべてサポートし、最終的には必要な変更をサポートします。

CCXT でサポートされているほとんどの交換は、そのままで動作します。

特定の交換クラスを実装する必要がある場合、これらは「freqtrade/exchange」ソース フォルダーにあります。また、読み込みロジックに新しい取引所を認識させるために、インポートを `freqtrade/exchange/__init__.py` に追加する必要があります。  
何が必要になるかを把握するために、既存の Exchange 実装を確認することをお勧めします。

!!! 警告
    交換の実装とテストには多くの試行錯誤が必要となる場合があるため、この点に留意してください。
    これは初心者向けのタスクではないため、ある程度の開発経験も必要です。

取引所のパブリック エンドポイントをすばやくテストするには、取引所の構成を「tests/exchange_online/conftest.py」に追加し、「pytest --longrun testing/exchange_online/test_ccxt_compat.py」でこれらのテストを実行します。
これらのテストを正常に完了することは良い基準点になります (実際には要件です)。ただし、これはパブリック エンドポイントのみをテストし、プライベート エンドポイント (順序の生成など) はテストしないため、正しい交換機能は保証されません。

また、長期間 (複数か月) の「freqtrade download-data」を使用して、データが正しくダウンロードされたことを確認してください (穴がなく、指定された時間範囲が実際にダウンロードされた)。

これらは、取引所がサポート対象またはコミュニティテスト済み (ホームページにリストされている) としてリストされるための前提条件です。
以下は、交換をより良くする (機能を完全なものにする) 「追加機能」ですが、2 つのカテゴリのいずれにも絶対に必要なわけではありません。

追加のテスト/完了する手順:

* `fetch_ohlcv()` によって提供されたデータを検証し、最終的にはこの交換のために `ohlcv_candle_limit` を調整します
* L2 オーダーブックの制限範囲を確認 (API ドキュメント) - 最終的には必要に応じて設定します
※残高が正しく表示されているか確認してください(※)
* 成行注文の作成 (*)
* 指値注文の作成 (*)
* 注文をキャンセルする (*)
* 完全なトレード (エントリー + エグジット) (*)
  * 取引所とボットの間で結果の計算を比較
  * 手数料が正しく適用されていることを確認します (データベースを取引所と照合して確認します)。

(*) 取引所の API キーと残高が必要です。

### 取引所のストップロス

新しい取引所が API を介して Exchange 注文のストップロスをサポートしているかどうかを確認します。
CCXT は取引所でのストップロスの統合をまだ提供していないため、取引所固有のパラメーターを独自に実装する必要があります。この実装例については、`binance.py` をご覧ください。これを正確に行う方法については、Exchange の API のドキュメントを詳しく調べる必要があります。 [CCXT Issues](https://github.com/ccxt/ccxt/issues) も、他の人が自分のプロジェクトに同様のものを実装している可能性があるため、大きな助けとなる可能性があります。

### 未完成のキャンドル

ローソク足 (OHLCV) データを取得する際、(取引所によっては) 不完全なローソク足を取得してしまう可能性があります。
これを実証するために、物事をシンプルにするために毎日のローソク足 (`"1d"`) を使用します。
API (`ct.fetch_ohlcv()`) に時間枠を問い合わせて、最後のエントリの日付を確認します。このエントリが変更されるか、「不完全な」ローソク足の日付を表示する場合は、これを削除する必要があります。インディケータは完全なローソク足のみが渡されると想定しており、多くの誤った買いシグナルを生成するため、不完全なローソク足があることには問題があるからです。したがって、デフォルトでは、最後のローソク足が不完全であると想定して削除します。

新しい交換がどのように動作するかを確認するには、次のスニペットを使用できます。
``` python
import ccxt
from datetime import datetime, timezone
from freqtrade.data.converter import ohlcv_to_dataframe
ct = ccxt.binance()  # Use the exchange you're testing
timeframe = "1d"
pair = "BTC/USDT"  # Make sure to use a pair that exists on that exchange!
raw = ct.fetch_ohlcv(pair, timeframe=timeframe)

# convert to dataframe
df1 = ohlcv_to_dataframe(raw, timeframe, pair=pair, drop_incomplete=False)

print(df1.tail(1))
print(datetime.now(timezone.utc))
```

``` output
                         date      open      high       low     close  volume  
499 2019-06-08 00:00:00+00:00  0.000007  0.000007  0.000007  0.000007   26264344.0  
2019-06-09 12:30:27.873327
```
出力には、Exchange からの最後のエントリと現在の UTC 日付が表示されます。
日付が同じ日を示している場合、最後のローソク足は不完全であると見なされるため、削除する必要があります (交換クラスの設定 `"ohlcv_partial_candle"` はそのまま / True のままにしておきます)。それ以外の場合は、キャンドルをドロップしないように「ohlcv_partial_candle」を「False」に設定します (上記の例を参照)。
もう 1 つの方法は、このコマンドを連続して複数回実行し、(日付は同じまま) ボリュームが変化しているかどうかを観察することです。

### Binance のキャッシュされたレバレッジ層を更新する

レバレッジ層の更新は定期的に行う必要があり、先物が有効になっている認証済みアカウントが必要です。
``` python
import ccxt
import json
from pathlib import Path

exchange = ccxt.binance({
    'apiKey': '<apikey>',
    'secret': '<secret>',
    'options': {'defaultType': 'swap'}
    })
_ = exchange.load_markets()

lev_tiers = exchange.fetch_leverage_tiers()

# Assumes this is running in the root of the repository.
file = Path('freqtrade/exchange/binance_leverage_tiers.json')
json.dump(dict(sorted(lev_tiers.items())), file.open('w'), indent=2)

```
このファイルはアップストリームに提供されるため、他の人もこのファイルから恩恵を受けることができます。

## サンプルノートブックの更新

jupyter ノートブックをドキュメントと一致させるには、サンプル ノートブックを更新した後に次のコマンドを実行する必要があります。
``` bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace freqtrade/templates/strategy_analysis_example.ipynb
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to markdown freqtrade/templates/strategy_analysis_example.ipynb --stdout > docs/strategy_analysis_example.md
```
## バックテストのドキュメント結果

バックテスト出力を生成するには、次のコマンドを使用してください。
``` bash
# Assume a dedicated user directory for this output
freqtrade create-userdir --userdir user_data_bttest/
# set can_short = True
sed -i "s/can_short: bool = False/can_short: bool = True/" user_data_bttest/strategies/sample_strategy.py

freqtrade download-data --timerange 20250625-20250801 --config tests/testdata/config.tests.usdt.json --userdir user_data_bttest/ -t 5m

freqtrade backtesting --config tests/testdata/config.tests.usdt.json -s SampleStrategy --userdir user_data_bttest/ --cache none --timerange 20250701-20250801
```
## 継続的インテグレーション

これは、CI パイプラインに関して行われたいくつかの決定を文書化したものです。

* CI は、Linux (ubuntu)、macOS、Windows のすべての OS バリアントで実行されます。
* Docker イメージは、「stable」ブランチと「develop」ブランチ用にビルドされ、マルチアーキテクチャ ビルドとしてビルドされ、同じタグを介して複数のプラットフォームをサポートします。
* Plot の依存関係を含む Docker イメージは、`stable_plot` および `develop_plot` としても利用できます。
* Docker イメージには、このイメージのベースとなるコミットを含むファイル `/freqtrade/freqtrade_commit` が含まれています。
* 完全な Docker イメージの再構築は、スケジュールに従って週に 1 回実行されます。
* デプロイメントは ubuntu 上で実行されます。
* PR を「stable」または「develop」にマージするには、すべてのテストに合格する必要があります。

## リリースの作成

ドキュメントのこの部分は保守者を対象としており、リリースの作成方法を示しています。

### リリースブランチを作成する

!!! 注記
    「stable」ブランチが最新であることを確認してください。

まず、約 1 週間前のコミットを選択します (リリースへの最新の追加を含めないため)。
``` bash
# create new branch
git checkout -b new_release <commitid>
```
このコミットと現在の状態の間に重要なバグ修正が行われたかどうかを判断し、最終的にはそれらを厳選します。

* リリース ブランチ (安定版) をこのブランチにマージします。
* `freqtrade/__init__.py` を編集し、現在の日付に一致するバージョンを追加します (たとえば、2019 年 7 月の場合は `2019.7`)。その月に 2 番目のリリースを行う必要がある場合、マイナー バージョンは「2019.7.1」になります。 pypi へのプッシュの失敗を避けるために、バージョン番号は PEP0440 の許可されたバージョンに従う必要があります。
* この部分をコミットします。
* そのブランチをリモートにプッシュし、**安定したブランチ**に対して PR を作成します。
* 開発バージョンをパターン「2019.8-dev」に従って次のバージョンに更新します。

### git コミットから変更ログを作成する
``` bash
# Needs to be done before merging / pulling that branch.
git log --oneline --no-decorate --no-merges stable..new_release
```
リリース ログを短くするには、完全な git 変更ログを折りたたみ可能な詳細セクションにラップするのが最善です。
```markdown
<details>
<summary>Expand full changelog</summary>

... Full git changelog

</details>
```
### FreqUI リリース

FreqUI が大幅に更新された場合は、リリース ブランチをマージする前に必ずリリースを作成してください。
リリースをマージする前に、リリース上の freqUI CI が完了し、渡されていることを確認してください。

### Github リリース/タグを作成する

安定版に対する PR がマージされたら (マージ直後が最適):

* Github UI の「新しいリリースのドラフト」ボタンを使用します (サブセクションのリリース)。
※タグにはバージョン番号を指定してください。
* 参照として「stable」を使用します (このステップは、上記の PR がマージされた後に行われます)。
* 上記の変更ログをリリース コメント (コードブロックとして) として使用します。
* 新しいリリースには以下のスニペットを使用してください

???ヒント「リリーステンプレート」
    ````
    --8<-- "includes/release_template.md"
    ````
## リリース

### ピピ

!!! 警告「手動リリース」
    このプロセスは、Github Actions の一部として自動化されています。  
    手動での pypi プッシュは必要ありません。

???例「手動リリース」
    pypi リリースを手動で作成するには、次のコマンドを実行してください。

    追加の要件: `wheel`、`twine` (アップロード用)、適切な権限を持つ pypi のアカウント。
    ``` bash
    pip install -U build
    python -m build --sdist --wheel

    # For pypi test (to check if some change to the installation did work)
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

    # For production:
    twine upload dist/*
    ```
非リリースを本稼働/実際の pypi インスタンスにプッシュしないでください。
