# 高度なバックテスト分析

## エントリータグとイグジットタグの分析

ストラテジーが異なるエントリー条件をマークアップするために使用されるエントリータグに従ってどのように動作するかを理解することが役立つ場合があります。デフォルトのバックテスト出力で提供されるものよりも、各エントリーとイグジットの条件についてより複雑な統計を見たい場合があります。また、取引をオープンしたシグナルローソク足のインジケータ値を決定したい場合もあります。

!!! Note
    以下のエントリー理由分析は、バックテストでのみ利用可能で、*hyperoptでは利用できません*。

シグナル**と**取引のエクスポートを有効にするには、`--export`オプションを`signals`に設定してバックテストを実行する必要があります：
``` bash
freqtrade backtesting -c <config.json> --timeframe <tf> --strategy <strategy_name> --timerange=<timerange> --export=signals
```
これにより、freqtradeはストラテジー、ペア、およびエントリーとイグジットシグナルをもたらしたローソク足の対応するDataFrameのpickle化された辞書を出力するように指示されます。
ストラテジーが行うエントリーの数によっては、このファイルはかなり大きくなる可能性があるため、定期的に`user_data/backtest_results`フォルダーをチェックして、古いエクスポートを削除してください。

次のバックテストを実行する前に、古いバックテスト結果を削除するか、バックテストを`--cache none`オプションで実行して、キャッシュされた結果が使用されないようにしてください。

すべてがうまくいけば、`user_data/backtest_results`フォルダーに`backtest-result-{timestamp}_signals.pkl`と`backtest-result-{timestamp}_exited.pkl`ファイルが表示されるはずです。

エントリー/イグジットタグを分析するには、スペース区切りの引数で提供される`--analysis-groups`オプションとともに`freqtrade backtesting-analysis`コマンドを使用する必要があります：
``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 1 2 3 4 5
```
このコマンドは、最後のバックテスト結果から読み取ります。`--analysis-groups`オプションは、各グループまたは取引の利益を示すさまざまな表形式の出力を指定するために使用されます。
最も単純なもの（0）から、ペア、エントリータグ、イグジットタグごとに最も詳細なもの（4）まであります：

* 0: enter_tagごとの全体的な勝率と利益の要約
* 1: enter_tagでグループ化された利益の要約
* 2: enter_tagとexit_tagでグループ化された利益の要約
* 3: ペアとenter_tagでグループ化された利益の要約
* 4: ペア、enter_、exit_tagでグループ化された利益の要約（これはかなり大きくなる可能性があります）
* 5: exit_tagでグループ化された利益の要約

`-h`オプションを使用して実行すると、より多くのオプションが利用可能です。

### backtest-filenameの使用

デフォルトでは、`backtesting-analysis`は`user_data/backtest_results`ディレクトリ内の最新のバックテスト結果を処理します。
以前のバックテストの結果を分析したい場合は、`--backtest-filename`オプションを使用して目的のファイルを指定します。これにより、関連するバックテスト結果のファイル名を提供することで、いつでも過去のバックテスト出力を再訪して再分析できます：
``` bash
freqtrade backtesting-analysis -c <config.json> --timeframe <tf> --strategy <strategy_name> --timerange <timerange> --export signals --backtest-filename backtest-result-2025-03-05_20-38-34.zip
```
エクスポートされたタイムスタンプ付きファイル名とともに、ログに次のような出力が表示されるはずです：
```
2022-06-14 16:28:32,698 - freqtrade.misc - INFO - dumping json to "mystrat_backtest-2022-06-14_16-28-32.json"
```
その後、そのファイル名を`backtesting-analysis`で使用できます：
```
freqtrade backtesting-analysis -c <config.json> --backtest-filename=mystrat_backtest-2022-06-14_16-28-32.json
```
別の結果ディレクトリからの結果を使用するには、`--backtest-directory`を使用してディレクトリを指定できます
``` bash
freqtrade backtesting-analysis -c <config.json> --backtest-directory custom_results/ --backtest-filename mystrat_backtest-2022-06-14_16-28-32.json
```
### 表示するエントリータグとイグジットタグの調整

表示される出力で特定のエントリーとイグジットタグのみを表示するには、次の2つのオプションを使用します：
```
--enter-reason-list : 分析するエントリーシグナルのスペース区切りリスト。デフォルト: "all"
--exit-reason-list : 分析するイグジットシグナルのスペース区切りリスト。デフォルト: "all"
```
例：
```bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss
```
### シグナルローソク足のインジケータの出力

`freqtrade backtesting-analysis`の真の力は、シグナルローソク足に存在するインジケータ値を出力して、エントリーシグナルインジケータの細かい調査と調整を可能にすることから来ます。特定のインジケータのセットの列を出力するには、`--indicator-list`
オプションを使用します：
```bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss --indicator-list rsi rsi_1h bb_lowerband ema_9 macd macdsignal
```
インジケータは、ストラテジーのメインDataFrame（メインタイムフレームまたは情報タイムフレームのいずれか）に存在する必要があります。そうでない場合、スクリプト出力で単純に無視されます。

!!! Note "インジケータリスト"
    インジケータ値は、エントリーポイントとイグジットポイントの両方で表示されます。`--indicator-list all`が指定されている場合、
    エントリーポイントのインジケータのみが表示され、ストラテジーによっては非常に大きなリストになる可能性があるため、これを回避します。

分析に含まれているため、自動的にアクセス可能なローソク足と取引関連のフィールドがあり、これらには次のものが含まれます：

- **open_date     :** 取引オープン日時
- **close_date    :** 取引クローズ日時
- **min_rate      :** ポジション全体で見られる最小価格
- **max_rate      :** ポジション全体で見られる最大価格
- **open          :** シグナルローソク足のオープン価格
- **close         :** シグナルローソク足のクローズ価格
- **high          :** シグナルローソク足の高値
- **low           :** シグナルローソク足の安値
- **volume        :** シグナルローソク足のボリューム
- **profit_ratio  :** 取引利益率
- **profit_abs    :** 取引の絶対利益

#### インジケータ値のサンプル出力
```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen
```
この例では、
取引のエントリーポイントとイグジットポイントの両方で`chikou_span`と`tenkan_sen`のインジケータ値を表示することを目指しています。

インジケータのサンプル出力は次のようになります：

| pair      | open_date                 | enter_reason | exit_reason | chikou_span (entry) | tenkan_sen (entry) | chikou_span (exit) | tenkan_sen (exit) |
|-----------|---------------------------|--------------|-------------|---------------------|--------------------|--------------------|-------------------|
| DOGE/USDT | 2024-07-06 00:35:00+00:00 |              | exit_signal | 0.105               | 0.106              | 0.105              | 0.107             |
| BTC/USDT  | 2024-08-05 14:20:00+00:00 |              | roi         | 54643.440           | 51696.400          | 54386.000          | 52072.010         |

表に示されているように、`chikou_span (entry)`は取引エントリー時のインジケータ値を表し、
`chikou_span (exit)`はイグジット時の値を反映しています。
このインジケータ値の詳細なビューは分析を強化します。

`(entry)`と`(exit)`の接尾辞がインジケータに追加され、
取引のエントリーポイントとイグジットポイントの値を区別します。

!!! Note "取引全体のインジケータ"
    特定の取引全体のインジケータには、`(entry)`または`(exit)`の接尾辞がありません。これらのインジケータには次のものが含まれます：`pair`、`stake_amount`、
    `max_stake_amount`、`amount`、`open_date`、`close_date`、`open_rate`、`close_rate`、`fee_open`、`fee_close`、`trade_duration`、
    `profit_ratio`、`profit_abs`、`exit_reason`、`initial_stop_loss_abs`、`initial_stop_loss_ratio`、`stop_loss_abs`、`stop_loss_ratio`、
    `min_rate`、`max_rate`、`is_open`、`enter_tag`、`leverage`、`is_short`、`open_timestamp`、`close_timestamp`、`orders`

#### エントリーシグナルまたはイグジットシグナルに基づくインジケータのフィルタリング

`--indicator-list`オプションは、デフォルトでエントリーシグナルとイグジットシグナルの両方のインジケータ値を表示します。エントリーシグナルのインジケータ値のみをフィルタリングするには、`--entry-only`引数を使用できます。同様に、イグジットシグナルでのみインジケータ値を表示するには、`--exit-only`引数を使用します。

例：エントリーシグナルでのインジケータ値を表示：
```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --entry-only
```
例：イグジットシグナルでのインジケータ値を表示：
```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --exit-only
```
!!! note
    これらのフィルターを使用する場合、インジケータ名には`(entry)`または`(exit)`の接尾辞が付きません。

### 日付による取引出力のフィルタリング

バックテストされたタイムレンジ内の日付間の取引のみを表示するには、通常の`timerange`オプションを`YYYYMMDD-[YYYYMMDD]`形式で指定します：
```
--timerange : 出力取引をフィルタリングするタイムレンジ、開始日は含み、終了日は除く。例：20220101-20221231
```
たとえば、バックテストのタイムレンジが`20220101-20221231`だったが、1月の取引のみを出力したい場合：
```bash
freqtrade backtesting-analysis -c <config.json> --timerange 20220101-20220201
```
### 拒否されたシグナルの出力

拒否されたシグナルを出力するには、`--rejected-signals`オプションを使用します。
```bash
freqtrade backtesting-analysis -c <config.json> --rejected-signals
```
### テーブルをCSVに書き込む

一部の表形式の出力は大きくなる可能性があるため、ターミナルに出力することは好ましくありません。
`--analysis-to-csv`オプションを使用して、標準出力へのテーブルの出力を無効にし、CSVファイルに書き込みます。
```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv
```
デフォルトでは、`backtesting-analysis`コマンドで指定した出力テーブルごとに1つのファイルを書き込みます。例：
```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --rejected-signals --analysis-groups 0 1
```
これにより、`user_data/backtest_results`に次のファイルが書き込まれます：

* rejected_signals.csv
* group_0.csv
* group_1.csv

ファイルが書き込まれる場所を上書きするには、`--analysis-csv-path`オプションも指定します。
```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --analysis-csv-path another/data/path/
```
