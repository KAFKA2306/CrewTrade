# ユーティリティサブコマンド

ライブトレードおよびドライラン実行モード、`backtesting`および`hyperopt`最適化サブコマンド、および履歴データを準備する`download-data`サブコマンドに加えて、ボットには多数のユーティリティサブコマンドが含まれています。それらはこのセクションで説明されています。

## ユーザーディレクトリの作成

freqtradeのファイルを保持するディレクトリ構造を作成します。
また、開始するための戦略とハイパーオプトの例も作成します。
複数回使用できます-`--reset`を使用すると、サンプル戦略とハイパーオプトファイルがデフォルトの状態にリセットされます。

--8<-- "commands/create-userdir.md"

!!! Warning
    `--reset`を使用すると、データが失われる可能性があります。これは、すべてのサンプルファイルを再度尋ねることなく上書きするためです。

```
├── backtest_results
├── data
├── hyperopt_results
├── hyperopts
│   ├── sample_hyperopt_loss.py
├── notebooks
│   └── strategy_analysis_example.ipynb
├── plot
└── strategies
    └── sample_strategy.py
```

## 新しい構成の作成

新しい構成ファイルを作成し、構成の重要な選択肢であるいくつかの質問をします。

--8<-- "commands/new-config.md"

!!! Warning
    重要な質問のみが尋ねられます。Freqtradeは、[構成ドキュメント](configuration.md#configuration-parameters)に記載されている、はるかに多くの構成の可能性を提供します。

### 構成例の作成

```
$ freqtrade new-config --config user_data/config_binance.json

? ドライラン（シミュレートされた取引）を有効にしますか？ はい
? 賭け金通貨を挿入してください：BTC
? 賭け金額を挿入してください：0.05
? max_open_tradesを挿入してください（整数または無制限のオープントレードの場合は-1）：3
? ご希望の時間枠を挿入してください（例：5m）：5m
? 表示通貨を挿入してください（レポート用）：USD
? 取引所を選択してください binance
? Telegramを有効にしますか？ いいえ
```

## 構成の表示

構成ファイルを表示します（デフォルトでは機密性の高い値は編集されています）。
[分割構成ファイル](configuration.md#multiple-configuration-files)または[環境変数](configuration.md#environment-variables)で特に便利です。このコマンドはマージされた構成を表示します。

![構成出力の表示](assets/show-config-output.png)

--8<-- "commands/show-config.md"

``` output
結合された構成は次のとおりです。
{
  "exit_pricing": {
    "price_side": "other",
    "use_order_book": true,
    "order_book_top": 1
  },
  "stake_currency": "USDT",
  "exchange": {
    "name": "binance",
    "key": "REDACTED",
    "secret": "REDACTED",
    "ccxt_config": {},
    "ccxt_async_config": {},
  }
  // ...
}
```

!!! Warning "このコマンドによって提供される情報の共有"
    デフォルトの出力（`--show-sensitive`なし）からすべての既知の機密情報を削除しようとします。
    それでも、誤って個人情報を公開していないことを確認するために、出力で機密性の高い値を再確認してください。

## 新しい戦略の作成

SampleStrategyと同様のテンプレートから新しい戦略を作成します。
ファイルはクラス名とインラインで名前が付けられ、既存のファイルは上書きされません。

結果は`user_data/strategies/<strategyclassname>.py`にあります。

--8<-- "commands/new-strategy.md"

### 新しい戦略のサンプル使用法

```bash
freqtrade new-strategy --strategy AwesomeStrategy
```

カスタムユーザーディレクトリを使用

```bash
freqtrade new-strategy --userdir ~/.freqtrade/ --strategy AwesomeStrategy
```

高度なテンプレートを使用する（すべてのオプションの関数とメソッドを設定する）

```bash
freqtrade new-strategy --strategy AwesomeStrategy --template advanced
```

## 戦略のリスト

`list-strategies`サブコマンドを使用して、特定のディレクトリ内のすべての戦略を表示します。

このサブコマンドは、戦略の読み込みに関する環境の問題を見つけるのに役立ちます。エラーが含まれていて読み込みに失敗した戦略を持つモジュールは赤で表示され（LOAD FAILED）、名前が重複している戦略は黄色で表示されます（DUPLICATE NAME）。

--8<-- "commands/list-strategies.md"

!!! Warning
    これらのコマンドを使用すると、ディレクトリからすべてのpythonファイルを読み込もうとします。信頼できないファイルがこのディレクトリにある場合、すべてのモジュールレベルのコードが実行されるため、セキュリティリスクになる可能性があります。

例：デフォルトの戦略ディレクトリを検索します（デフォルトのuserdir内）。

``` bash
freqtrade list-strategies
```

例：userdir内の戦略ディレクトリを検索します。

``` bash
freqtrade list-strategies --userdir ~/.freqtrade/
```

例：専用の戦略パスを検索します。

``` bash
freqtrade list-strategies --strategy-path ~/.freqtrade/strategies/
```

## ハイパーオプトロス関数のリスト

`list-hyperoptloss`サブコマンドを使用して、利用可能なすべてのハイパーオプトロス関数を表示します。

環境で利用可能なすべての損失関数のクイックリストを提供します。

このサブコマンドは、損失関数の読み込みに関する環境の問題を見つけるのに役立ちます。エラーが含まれていて読み込みに失敗したHyperopt-Loss関数を持つモジュールは赤で表示され（LOAD FAILED）、名前が重複しているhyperopt-Loss関数は黄色で表示されます（DUPLICATE NAME）。

--8<-- "commands/list-hyperoptloss.md"

## freqAIモデルのリスト

`list-freqaimodels`サブコマンドを使用して、利用可能なすべてのfreqAIモデルを表示します。

このサブコマンドは、freqAIモデルの読み込みに関する環境の問題を見つけるのに役立ちます。エラーが含まれていて読み込みに失敗したモデルを持つモジュールは赤で表示され（LOAD FAILED）、名前が重複しているモデルは黄色で表示されます（DUPLICATE NAME）。

--8<-- "commands/list-freqaimodels.md"

## 取引所のリスト

`list-exchanges`サブコマンドを使用して、ボットで利用可能な取引所を表示します。

--8<-- "commands/list-exchanges.md"

例：ボットで利用可能な取引所を表示します。

```
$ freqtrade list-exchanges
Freqtradeで利用可能な取引所：
取引所名       サポート    マーケット                 理由
------------------  -----------  ----------------------  ------------------------------------------------------------------------
binance             公式     スポット、分離先物
bitmart             公式     スポット
bybit                            スポット、分離先物
gate                公式     スポット、分離先物
htx                 公式     スポット
huobi                            スポット
kraken              公式     スポット
okx                 公式     スポット、分離先物
```

!!! info ""
    出力は明確にするために削減されています-サポートされている利用可能な取引所は時間とともに変更される可能性があります。

!!! Note "不足しているオプト取引所"
    「不足しているオプト：」の値は、特別な構成が必要な場合があります（たとえば、`fetchTickers`が不足している場合はオーダーブックを使用するなど）-しかし、理論的には機能するはずです（ただし、機能することを保証することはできません）。

例：ccxtライブラリでサポートされているすべての取引所を表示します（Freqtradeで機能しないことがわかっている「悪い」ものを含む）

```
$ freqtrade list-exchanges -a
ccxtライブラリでサポートされているすべての取引所：
取引所名       有効    サポート    マーケット                 理由
------------------  -------  -----------  ----------------------  ---------------------------------------------------------------------------------
binance             True     公式     スポット、分離先物
bitflyer            False                 スポット                    不足：fetchOrder。不足しているオプト：fetchTickers。
bitmart             True     公式     スポット
bybit               True                  スポット、分離先物
gate                True     公式     スポット、分離先物
htx                 True     公式     スポット
kraken              True     公式     スポット
okx                 True     公式     スポット、分離先物
```

!!! info ""
    出力が削減されました-サポートされている利用可能な取引所は時間とともに変更される可能性があります。

## タイムフレームのリスト

`list-timeframes`サブコマンドを使用して、取引所で利用可能なタイムフレームのリストを表示します。

--8<-- "commands/list-timeframes.md"

* 例：構成ファイルで設定されている「binance」取引所のタイムフレームを表示します。

```
$ freqtrade list-timeframes -c config_binance.json
...
取引所`binance`で利用可能なタイムフレーム：1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M
```

* 例：Freqtradeで利用可能な取引所を列挙し、それぞれでサポートされているタイムフレームを出力します。
```
$ for i in `freqtrade list-exchanges -1`; do freqtrade list-timeframes --exchange $i; done
```

## ペア/マーケットのリスト

`list-pairs`および`list-markets`サブコマンドを使用すると、取引所で利用可能なペア/マーケットを表示できます。

ペアは、マーケットシンボルのベース通貨部分とクォート通貨部分の間に「/」文字があるマーケットです。
たとえば、「ETH/BTC」ペアでは、「ETH」がベース通貨、「BTC」がクォート通貨です。

Freqtradeによって取引されるペアの場合、ペアのクォート通貨は`stake_currency`構成設定の値によって定義されます。

これらのサブコマンドでペア/マーケットに関する情報を出力できます-そして、`--quote BTC`を使用してクォート通貨で出力をフィルタリングしたり、`--base ETH`を使用してベース通貨でフィルタリングしたりできます。

これらのサブコマンドには、同じ使用法と利用可能なオプションの同じセットがあります。

--8<-- "commands/list-pairs.md"

デフォルトでは、アクティブなペア/マーケットのみが表示されます。アクティブなペア/マーケットとは、現在取引所で取引できるものです。
`-a`/`-all`オプションを使用して、非アクティブなものを含むすべてのペア/マーケットのリストを表示できます。
マーケットの最小取引可能価格が非常に小さい場合、つまり`1e-11`（`0.00000000001`）未満の場合、ペアは取引不可としてリストされる場合があります。

ペア/マーケットは、出力されたシンボル文字列でソートされます。

### 例

* デフォルトの構成ファイルで指定された取引所で、クォート通貨がUSDのアクティブなペアのリストをJSON形式で出力します（つまり、「Binance」取引所のペア）。

```
$ freqtrade list-pairs --quote USD --print-json
```

* `config_binance.json`構成ファイルで指定された取引所（つまり、「Binance」取引所）のすべてのペアのリストを、ベース通貨がBTCまたはETHで、クォート通貨がUSDTまたはUSDのものを、人間が読めるリストと要約として出力します。

```
$ freqtrade list-pairs -c config_binance.json --all --base BTC ETH --quote USDT USD --print-list
```

* 取引所「Kraken」のすべてのマーケットを、表形式で出力します。

```
$ freqtrade list-markets --exchange kraken --all
```

## ペアリストのテスト

`test-pairlist`サブコマンドを使用して、[動的ペアリスト](plugins.md#pairlists)の構成をテストします。

`pairlists`属性が指定された構成が必要です。
バックテスト/ハイパーオプト中に使用する静的ペアリストを生成するために使用できます。

--8<-- "commands/test-pairlist.md"

### 例

[動的ペアリスト](plugins.md#pairlists)を使用する場合にホワイトリストを表示します。

```
freqtrade test-pairlist --config config.json --quote USDT BTC
```

## データベースの変換

`freqtrade convert-db`を使用して、データベースをあるシステムから別のシステムに変換できます（sqlite -> postgres、postgres -> 他のpostgres）。すべての取引、注文、およびPairlockを移行します。

さまざまなデータベースシステムの要件については、[対応するドキュメント](advanced-setup.md#use-a-different-database-system)を参照してください。

--8<-- "commands/convert-db.md"

!!! Warning
    これを空のターゲットデータベースでのみ使用してください。Freqtradeは通常の移行を実行しますが、エントリがすでに存在する場合は失敗する可能性があります。

## ウェブサーバーモード

!!! Warning "実験的"
    ウェブサーバーモードは、バックテストと戦略開発の生産性を向上させるための実験的なモードです。
    まだバグがある可能性があります-もしこれらに遭遇した場合は、githubの問題として報告してください。ありがとうございます。

ウェブサーバーモードでfreqtradeを実行します。
Freqtradeはウェブサーバーを起動し、FreqUIがバックテストプロセスを開始および制御できるようにします。
これには、バックテストの実行間でデータが再読み込みされないという利点があります（タイムフレームとタイムレンジが同じままである限り）。
FreqUIはバックテストの結果も表示します。

--8<-- "commands/webserver.md"

### ウェブサーバーモード-docker

docker経由でウェブサーバーモードを使用することもできます。
ワンオフコンテナを起動するには、ポートがデフォルトで公開されていないため、ポートを明示的に構成する必要があります。
`docker compose run --rm -p 127.0.0.1:8080:8080 freqtrade webserver`を使用して、停止すると削除されるワンオフコンテナを起動できます。これは、ポート8080がまだ利用可能であり、他のボットがそのポートで実行されていないことを前提としています。

または、docker-composeファイルを再構成して、コマンドを更新することもできます。

``` yml
    command: >
      webserver
      --config /freqtrade/user_data/config.json
```

これで、`docker compose up`を使用してウェブサーバーを起動できます。
これは、構成でウェブサーバーが有効になっており、docker用に構成されている（リスニングポート= `0.0.0.0`）ことを前提としています。

!!! Tip
    ライブまたはドライランボットを起動する場合は、コマンドをトレードコマンドに戻すことを忘れないでください。

## 以前のバックテスト結果の表示

以前のバックテスト結果を表示できます。
`--show-pair-list`を追加すると、構成に簡単にコピー/貼り付けできるソートされたペアリストが出力されます（不良ペアは省略されます）。

??? Warning "戦略の過剰適合"
    勝利ペアのみを使用すると、戦略が過剰適合し、将来のデータではうまく機能しなくなる可能性があります。実際のお金を危険にさらす前に、ドライランで戦略を広範囲にテストしてください。

--8<-- "commands/backtesting-show.md"

## 詳細なバックテスト分析

高度なバックテスト結果分析。

詳細は[バックテスト分析](advanced-backtesting.md#analyze-the-buyentry-and-sellexit-tags)セクションにあります。

--8<-- "commands/backtesting-analysis.md"

## ハイパーオプト結果のリスト

`hyperopt-list`サブコマンドを使用して、Hyperoptモジュールが以前に評価したハイパー最適化エポックをリストできます。

--8<-- "commands/hyperopt-list.md"

!!! Note
    `hyperopt-list`は、利用可能な最新のハイパーオプト結果ファイルを自動的に使用します。
    これを`--hyperopt-filename`引数を使用して上書きし、別の利用可能なファイル名（パスなし！）を指定できます。

### 例

すべての結果をリストし、最後に最良の結果の詳細を出力します。
```
freqtrade hyperopt-list
```

利益がプラスのエポックのみをリストします。スクリプトでリストを反復処理できるように、最良のエポックの詳細は出力しません。
```
freqtrade hyperopt-list --profitable --no-details
```

## ハイパーオプト結果の詳細の表示

`hyperopt-show`サブコマンドを使用して、Hyperoptモジュールによって以前に評価されたハイパー最適化エポックの詳細を表示できます。

--8<-- "commands/hyperopt-show.md"

!!! Note
    `hyperopt-show`は、利用可能な最新のハイパーオプト結果ファイルを自動的に使用します。
    これを`--hyperopt-filename`引数を使用して上書きし、別の利用可能なファイル名（パスなし！）を指定できます。

### 例

エポック168の詳細を出力します（エポックの番号は、`hyperopt-list`サブコマンドまたはハイパー最適化実行中のHyperopt自体によって表示されます）。

```
freqtrade hyperopt-show -n 168
```

最後の最良のエポック（つまり、すべてのエポックの中で最良）の詳細を含むJSONデータを出力します。

```
freqtrade hyperopt-show --best -n -1 --print-json --no-header
```

## 取引の表示

選択した（またはすべての）取引をデータベースから画面に出力します。

--8<-- "commands/show-trades.md"

### 例

ID 2と3の取引をjsonとして出力します

``` bash
freqtrade show-trades --db-url sqlite:///tradesv3.sqlite --trade-ids 2 3 --print-json
```

## 戦略アップデーター

リストされた戦略または戦略フォルダー内のすべての戦略をv3準拠に更新します。
コマンドが--strategy-listなしで実行される場合、戦略フォルダー内のすべての戦略が変換されます。
元の戦略は`user_data/strategies_orig_updater/`ディレクトリで引き続き利用できます。

!!! Warning "変換結果"
    戦略アップデーターは「ベストエフォート」アプローチで機能します。変換の結果を検証するために、デューデリジェンスを行ってください。
    また、結果を健全な方法でフォーマットするために、pythonフォーマッター（例：`black`）を実行することをお勧めします。

--8<-- "commands/strategy-updater.md"