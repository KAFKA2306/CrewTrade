# プロット

このページでは、価格、指標、利益をプロットする方法を説明します。

!!! Warning "廃止されました"
    このページで説明されているコマンド (`plot-dataframe`、`plot-profit`) は廃止されたものとみなされ、メンテナンス モードになっています。
    これは主に、中規模のプロットでも発生する可能性があるパフォーマンスの問題のためですが、「ファイルを保存してブラウザで開く」という操作が UI の観点から見てあまり直感的ではないためでもあります。

    これらを削除する当面の計画はありませんが、積極的には保守されておらず、機能を維持するために大きな変更が必要な場合は短期的に削除される可能性があります。
    
    プロットのニーズには、同じパフォーマンスの問題に悩まされない [FreqUI](freq-ui.md) を使用してください。

## インストール/セットアップ

プロット モジュールは Plotly ライブラリを使用します。次のコマンドを実行して、これをインストール/アップグレードできます。
``` bash
pip install -U -r requirements-plot.txt
```
## 価格とインジケーターをプロットする

`freqtrade put-dataframe` サブコマンドは、3 つのサブプロットを含む対話型グラフを表示します。

*価格に続くローソク足とインジケーターを含むメインプロット (sma/ema)
* 音量バー
* `--indicators2` で指定された追加のインジケーター

![プロットデータフレーム](assets/plot-dataframe.png)

考えられる引数:

--8<-- "commands/plot-dataframe.md"

例:
``` bash
freqtrade plot-dataframe -p BTC/ETH --strategy AwesomeStrategy
```
`-p/--pairs` 引数を使用して、プロットしたいペアを指定できます。

!!! Note
    `freqtrade put-dataframe` サブコマンドは、ペアごとに 1 つのプロット ファイルを生成します。

カスタムインジケーターを指定します。
メインプロットには「--indicators1」を使用し、以下のサブプロットには「--indicators2」を使用します（値が価格とは異なる範囲にある場合）。
``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --indicators1 sma ema --indicators2 macd
```
### さらなる使用例

複数のペアをプロットするには、スペースで区切ります。
``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH XRP/ETH
```
時間範囲をプロットするには (ズームインするには)
``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805
```
データベースに保存されている取引をプロットするには、「--db-url」を「--trade-source DB」と組み合わせて使用​​します。
``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy --db-url sqlite:///tradesv3.dry_run.sqlite -p BTC/ETH --trade-source DB
```
バックテスト結果から取引をプロットするには、`--export-filename <filename>` を使用します。
``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy --export-filename user_data/backtest_results/backtest-result.json -p BTC/ETH
```
### プロット データフレームの基本

![プロットデータフレーム2](assets/plot-dataframe2.png)

`plot-dataframe` サブコマンドには、バックテスト データ、戦略、および戦略に対応する取引を含むバックテスト結果ファイルまたはデータベースが必要です。

結果のプロットには次の要素が含まれます。

* 緑色の三角形: 戦略からの買いシグナル。 (注: シアンの円と比較すると、すべての買いシグナルが取引を生成するわけではありません。)
* 赤い三角: 戦略からの売りシグナル。 (また、赤と緑の四角と比べて、すべての売りシグナルが取引を終了するわけではありません。)
* シアンの円: 取引エントリーポイント。
* 赤い四角: 損失または 0% の利益がある取引の取引終了ポイント。
* 緑色の四角: 収益性の高い取引の取引出口ポイント。
* `--indicators1` で指定された、ローソク足スケールに対応する値を持つインジケーター (SMA/EMA など)。
* 出来高 (メイン チャートの下部にある棒グラフ)。
* `--indicators2` で指定されたように、出来高バーの下に異なるスケールの値を持つインジケーター (MACD、RSI など)。

!!! Note "ボリンジャーバンド"
    ボリンジャー バンドは、列 `bb_ lowerband` と `bb_upperband` が存在する場合にプロットに自動的に追加され、下のバンドから上のバンドにまたがる水色の領域として描画されます。

#### 高度なプロット構成

高度なプロット構成は、`plot_config` パラメーターのストラテジで指定できます。

「plot_config」を使用する場合の追加機能は次のとおりです。

* インジケーターごとに色を指定します
* 追加のサブプロットを指定する
* 間の領域を埋めるインジケーターペアを指定します

以下のサンプル プロット構成では、インジケーターの固定色を指定しています。そうしないと、連続したプロットで毎回異なる配色が生成され、比較が困難になる可能性があります。
また、複数のサブプロットで MACD と RSI の両方を同時に表示することもできます。

プロットタイプは「type」キーを使用して設定できます。考えられるタイプは次のとおりです。

* `scatter` は `plotly.graph_objects.Scatter` クラス (デフォルト) に対応します。
* `bar` は `plotly.graph_objects.Bar` クラスに対応します。

`plotly.graph_objects.*` コンストラクターへの追加パラメーターは、`plotly` dict で指定できます。

プロセスを説明するインライン コメントを含むサンプル構成:
``` python
@property
def plot_config(self):
    """
        There are a lot of solutions how to build the return dictionary.
        The only important point is the return value.
        Example:
            plot_config = {'main_plot': {}, 'subplots': {}}

    """
    plot_config = {}
    plot_config['main_plot'] = {
        # Configuration for main plot indicators.
        # Assumes 2 parameters, emashort and emalong to be specified.
        f'ema_{self.emashort.value}': {'color': 'red'},
        f'ema_{self.emalong.value}': {'color': '#CCCCCC'},
        # By omitting color, a random color is selected.
        'sar': {},
        # fill area between senkou_a and senkou_b
        'senkou_a': {
            'color': 'green', #optional
            'fill_to': 'senkou_b',
            'fill_label': 'Ichimoku Cloud', #optional
            'fill_color': 'rgba(255,76,46,0.2)', #optional
        },
        # plot senkou_b, too. Not only the area to it.
        'senkou_b': {}
    }
    plot_config['subplots'] = {
         # Create subplot MACD
        "MACD": {
            'macd': {'color': 'blue', 'fill_to': 'macdhist'},
            'macdsignal': {'color': 'orange'},
            'macdhist': {'type': 'bar', 'plotly': {'opacity': 0.9}}
        },
        # Additional subplot RSI
        "RSI": {
            'rsi': {'color': 'red'}
        }
    }

    return plot_config
```
??? 「属性として（以前のメソッド）」に注意してください
    また、plot_config を属性として割り当てることもできます (これがデフォルトの方法でした)。
    これには、戦略パラメーターが利用できないため、特定の構成が機能しなくなるという欠点があります。
    ``` python
        plot_config = {
            'main_plot': {
                # Configuration for main plot indicators.
                # Specifies `ema10` to be red, and `ema50` to be a shade of gray
                'ema10': {'color': 'red'},
                'ema50': {'color': '#CCCCCC'},
                # By omitting color, a random color is selected.
                'sar': {},
            # fill area between senkou_a and senkou_b
            'senkou_a': {
                'color': 'green', #optional
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud', #optional
                'fill_color': 'rgba(255,76,46,0.2)', #optional
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {}
            },
            'subplots': {
                # Create subplot MACD
                "MACD": {
                    'macd': {'color': 'blue', 'fill_to': 'macdhist'},
                    'macdsignal': {'color': 'orange'},
                    'macdhist': {'type': 'bar', 'plotly': {'opacity': 0.9}}
                },
                # Additional subplot RSI
                "RSI": {
                    'rsi': {'color': 'red'}
                }
            }
        }

    ```
!!! Note
    上記の設定は、`ema10`、`ema50`、`senkou_a`、`senkou_b`、
    `macd`、`macdsignal`、`macdhist`、および `rsi` は、ストラテジによって作成された DataFrame 内の列です。

!!! Warning
    `plotly` 引数は、plotly ライブラリでのみサポートされており、freq-ui では機能しません。

!!! Note "トレードポジションの調整"
    `position_adjustment_enable` / `adjust_trade_position()` が使用される場合、取引の最初の購入価格は複数の注文にわたって平均され、取引開始価格はローソク足の範囲外に表示される可能性が高くなります。

## 利益をプロットする

![プロット-利益](assets/plot-profit.png)

`plot-profit` サブコマンドは、3 つのプロットを含む対話型グラフを表示します。

* すべてのペアの平均終値。
※バックテストによる利益を集計したものです。
これは実際の利益ではなく、推定値であることに注意してください。
※各ペアごとの利益となります。
* 取引の並行性。
* 水中 (ドローダウン期間)。

最初のグラフは、市場全体の推移を把握するのに適しています。

2 番目のグラフは、アルゴリズムが機能するかどうかを示します。
おそらく、安定して小さな利益を生み出すアルゴリズム、または動作頻度は低いが大​​きな変動を起こすアルゴリズムが必要な場合があります。
このグラフでは、最大ドローダウン期間の開始 (および終了) も強調表示されます。

3 番目のグラフは、利益の急増を引き起こす異常値、つまりペアのイベントを特定するのに役立ちます。

4 番目のグラフは、max_open_trades が最大に達する頻度を示し、取引の並行性を分析するのに役立ちます。

`freqtrade Lot-profit` サブコマンドで可能なオプション:

--8<-- "commands/plot-profit.md"

`-p/--pairs` 引数は、この計算で考慮されるペアを制限するために使用できます。

例:

カスタム バックテスト エクスポート ファイルを使用する
``` bash
freqtrade plot-profit  -p LTC/BTC --export-filename user_data/backtest_results/backtest-result.json
```
カスタムデータベースを使用する
``` bash
freqtrade plot-profit  -p LTC/BTC --db-url sqlite:///tradesv3.sqlite --trade-source DB
```

``` bash
freqtrade --datadir user_data/data/binance_save/ plot-profit -p LTC/BTC
```
