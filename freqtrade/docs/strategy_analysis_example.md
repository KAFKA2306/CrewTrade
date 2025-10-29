# 戦略分析の例

戦略のデバッグには時間がかかる場合があります。 Freqtrade は、生データを視覚化するためのヘルパー関数を提供します。
以下では、Binance からの 5 分間のタイムフレームのデータである SampleStrategy を使用し、それらをデフォルトの場所のデータ ディレクトリにダウンロードしていることを前提としています。
詳細については、[ドキュメント](https://www.freqtrade.io/en/stable/data-download/)を参照してください。

## セットアップ

### 作業ディレクトリをリポジトリのルートに変更します
```python
import os
from pathlib import Path


# Change directory
# Modify this cell to insure that the output shows the correct path.
# Define all paths relative to the project root shown in the cell output
project_root = "somedir/freqtrade"
i = 0
try:
    os.chdir(project_root)
    if not Path("LICENSE").is_file():
        i = 0
        while i < 4 and (not Path("LICENSE").is_file()):
            os.chdir(Path(Path.cwd(), "../"))
            i += 1
        project_root = Path.cwd()
except FileNotFoundError:
    print("Please define the project root relative to the current directory")
print(Path.cwd())
```
### Freqtrade 環境を構成する
```python
from freqtrade.configuration import Configuration


# Customize these according to your needs.

# Initialize empty configuration object
config = Configuration.from_files([])
# Optionally (recommended), use existing configuration file
# config = Configuration.from_files(["user_data/config.json"])

# Define some constants
config["timeframe"] = "5m"
# Name of the strategy class
config["strategy"] = "SampleStrategy"
# Location of the data
data_location = config["datadir"]
# Pair to analyze - Only use one pair here
pair = "BTC/USDT"
```


```python
# Load data using values set above
from freqtrade.data.history import load_pair_history
from freqtrade.enums import CandleType


candles = load_pair_history(
    datadir=data_location,
    timeframe=config["timeframe"],
    pair=pair,
    data_format="json",  # Make sure to update this to your data
    candle_type=CandleType.SPOT,
)

# Confirm success
print(f"Loaded {len(candles)} rows of data for {pair} from {data_location}")
candles.head()
```
## 戦略をロードして実行する
* 戦略ファイルが変更されるたびに再実行します
```python
# Load strategy using values set above
from freqtrade.data.dataprovider import DataProvider
from freqtrade.resolvers import StrategyResolver


strategy = StrategyResolver.load_strategy(config)
strategy.dp = DataProvider(config, None, None)
strategy.ft_bot_start()

# Generate buy/sell signals using strategy
df = strategy.analyze_ticker(candles, {"pair": pair})
df.tail()
```
### 取引詳細の表示

* `data.head()` を使用することもできますが、ほとんどのインジケーターにはデータフレームの先頭に「起動」データがあることに注意してください。
* 考えられるいくつかの問題
    * データフレームの末尾に NaN 値を含む列
    * 完全に異なる単位を持つ `crossed*()` 関数で使用される列
※フルバックテストとの比較
    * `analyze_ticker()` からの 1 つのペアの出力として 200 の買いシグナルがあることは、必ずしもバックテスト中に 200 の取引が行われることを意味するわけではありません。
    * 買い条件として「df['rsi'] < 30」などの 1 つの条件だけを使用すると、各ペアに対して複数の「買い」シグナルが順番に生成されます (rsi が > 29 を返すまで)。ボットは、これらのシグナルの最初のシグナルでのみ購入するか (トレードス​​ロット (「max_open_trades」) がまだ利用可能な場合のみ)、または「スロット」が利用可能になるとすぐに中間のシグナルの 1 つで購入します。
```python
# Report results
print(f"Generated {df['enter_long'].sum()} entry signals")
data = df.set_index("date", drop=False)
data.tail()
```
## 既存のオブジェクトを Jupyter ノートブックにロードする

次のセルは、cli を使用してデータがすでに生成されていることを前提としています。  
これらを使用すると、結果をさらに深く掘り下げて分析を実行できます。分析を実行しないと、情報過多により出力が非常に理解しにくくなります。

### バックテスト結果を pandas データフレームにロードする

取引データフレームを分析します (以下のプロットにも使用されます)
```python
from freqtrade.data.btanalysis import load_backtest_data, load_backtest_stats


# if backtest_dir points to a directory, it'll automatically load the last backtest file.
backtest_dir = config["user_data_dir"] / "backtest_results"
# backtest_dir can also point to a specific file
# backtest_dir = (
#   config["user_data_dir"] / "backtest_results/backtest-result-2020-07-01_20-04-22.json"
# )
```


```python
# You can get the full backtest statistics by using the following command.
# This contains all information used to generate the backtest result.
stats = load_backtest_stats(backtest_dir)

strategy = "SampleStrategy"
# All statistics are available per strategy, so if `--strategy-list` was used during backtest,
# this will be reflected here as well.
# Example usages:
print(stats["strategy"][strategy]["results_per_pair"])
# Get pairlist used for this backtest
print(stats["strategy"][strategy]["pairlist"])
# Get market change (average change of all pairs from start to end of the backtest period)
print(stats["strategy"][strategy]["market_change"])
# Maximum drawdown ()
print(stats["strategy"][strategy]["max_drawdown_abs"])
# Maximum drawdown start and end
print(stats["strategy"][strategy]["drawdown_start"])
print(stats["strategy"][strategy]["drawdown_end"])


# Get strategy comparison (only relevant if multiple strategies were compared)
print(stats["strategy_comparison"])
```


```python
# Load backtested trades as dataframe
trades = load_backtest_data(backtest_dir)

# Show value-counts per pair
trades.groupby("pair")["exit_reason"].value_counts()
```
## 毎日の利益/資本ラインのプロット
```python
# Plotting equity line (starting with 0 on day 1 and adding daily profit for each backtested day)

import pandas as pd
import plotly.express as px

from freqtrade.configuration import Configuration
from freqtrade.data.btanalysis import load_backtest_stats


# strategy = 'SampleStrategy'
# config = Configuration.from_files(["user_data/config.json"])
# backtest_dir = config["user_data_dir"] / "backtest_results"

stats = load_backtest_stats(backtest_dir)
strategy_stats = stats["strategy"][strategy]

df = pd.DataFrame(columns=["dates", "equity"], data=strategy_stats["daily_profit"])
df["equity_daily"] = df["equity"].cumsum()

fig = px.line(df, x="dates", y="equity_daily")
fig.show()
```
### ライブ取引結果をパンダデータフレームにロードする

すでに取引を行っており、パフォーマンスを分析したい場合
```python
from freqtrade.data.btanalysis import load_trades_from_db


# Fetch trades from database
trades = load_trades_from_db("sqlite:///tradesv3.sqlite")

# Display results
trades.groupby("pair")["exit_reason"].value_counts()
```
## ロードされた取引を分析して取引の並列性を確認します
これは、バックテストと非常に高い `max_open_trades` 設定を組み合わせて使用すると、最適な `max_open_trades` パラメーターを見つけるのに役立ちます。

`analyze_trade_Parallelism()` は、各ローソク足のオープン取引の数を指定する、「open_trades」列を持つ timeseries データフレームを返します。
```python
from freqtrade.data.btanalysis import analyze_trade_parallelism


# Analyze the above
parallel_trades = analyze_trade_parallelism(trades, "5m")

parallel_trades.plot()
```
## 結果をプロットする

Freqtrade は、plotly に基づいたインタラクティブなプロット機能を提供します。
```python
from freqtrade.plot.plotting import generate_candlestick_graph


# Limit graph period to keep plotly quick and reactive

# Filter trades to one pair
trades_red = trades.loc[trades["pair"] == pair]

data_red = data["2019-06-01":"2019-06-10"]
# Generate candlestick graph
graph = generate_candlestick_graph(
    pair=pair,
    data=data_red,
    trades=trades_red,
    indicators1=["sma20", "ema50", "ema55"],
    indicators2=["rsi", "macd", "macdsignal", "macdhist"],
)
```


```python
# Show graph inline
# graph.show()

# Render graph in a separate window
graph.show(renderer="browser")
```
## トレードごとの平均利益を分布グラフとしてプロットする
```python
import plotly.figure_factory as ff


hist_data = [trades.profit_ratio]
group_labels = ["profit_ratio"]  # name of the dataset

fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
fig.show()
```
データを最適に分析する方法についてのアイデアを共有したい場合は、お気軽に問題を送信するか、このドキュメントを拡張するプル リクエストを送信してください。
