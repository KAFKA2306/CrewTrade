# オーダーフローデータ

このガイドでは、Freqtradeで高度なオーダーフロー分析のために公開取引データを活用する方法を説明します。

!!! Warning "実験的機能"
    オーダーフロー機能は現在ベータ版であり、将来のリリースで変更される可能性があります。問題やフィードバックがあれば、[Freqtrade GitHubリポジトリ](https://github.com/freqtrade/freqtrade/issues)に報告してください。
    また、現在freqAIではテストされていません - これら2つの機能を組み合わせることは、現時点では範囲外と見なされます。

!!! Warning "パフォーマンス"
    オーダーフローには生の取引データが必要です。このデータはかなり大きく、freqtradeが過去Xローソク足の取引データをダウンロードする必要がある場合、初期起動が遅くなる可能性があります。さらに、この機能を有効にすると、メモリ使用量が増加します。十分なリソースが利用可能であることを確認してください。

## はじめに

### 公開取引の有効化

`config.json`ファイルで、`exchange`セクションの下にある`use_public_trades`オプションをtrueに設定します。

```json
"exchange": {
   ...
   "use_public_trades": true,
}
```

### オーダーフロー処理の設定

config.jsonのorderflowセクション内で、オーダーフロー処理の望ましい設定を定義します。ここで、次のような要因を調整できます：

- `cache_size`: 毎回計算するのではなく、キャッシュに保存される以前のオーダーフローローソク足の数
- `max_candles`: 取引データを取得するローソク足の数をフィルタリングします。
- `scale`: フットプリントチャートの価格ビンサイズを制御します。
- `stacked_imbalance_range`: 考慮される最小の連続した不均衡価格レベルを定義します。
- `imbalance_volume`: このしきい値未満のボリュームの不均衡をフィルタリングします。
- `imbalance_ratio`: この値よりも低い比率（askとbidボリュームの差）の不均衡をフィルタリングします。

```json
"orderflow": {
    "cache_size": 1000,
    "max_candles": 1500,
    "scale": 0.5,
    "stacked_imbalance_range": 3, //  少なくともこの量の不均衡が隣接して必要
    "imbalance_volume": 1, //  以下をフィルタリング
    "imbalance_ratio": 3 //  比率が低いものをフィルタリング
  },
```

## バックテスト用の取引データのダウンロード

バックテスト用の過去の取引データをダウンロードするには、freqtrade download-dataコマンドで--dl-tradesフラグを使用します。

```bash
freqtrade download-data -p BTC/USDT:USDT --timerange 20230101- --trading-mode futures --timeframes 5m --dl-trades
```

!!! Warning "データの利用可能性"
    すべての取引所が公開取引データを提供しているわけではありません。サポートされている取引所の場合、`--dl-trades`フラグでデータのダウンロードを開始すると、公開取引データが利用できない場合はfreqtradeが警告します。

## オーダーフローデータへのアクセス

有効化すると、データフレームでいくつかの新しい列が利用可能になります：

``` python

dataframe["trades"] # 各個別取引に関する情報を含みます。
dataframe["orderflow"] # フットプリントチャートのdictを表します（以下を参照）
dataframe["imbalances"] # オーダーフローの不均衡に関する情報を含みます。
dataframe["bid"] # 総bid量
dataframe["ask"] # 総ask量
dataframe["delta"] # askとbid量の差。
dataframe["min_delta"] # ローソク足内の最小delta
dataframe["max_delta"] # ローソク足内の最大delta
dataframe["total_trades"] # 総取引数
dataframe["stacked_imbalances_bid"] # スタックされたbid不均衡範囲の開始の価格レベルのリスト
dataframe["stacked_imbalances_ask"] # スタックされたask不均衡範囲の開始の価格レベルのリスト
```

ストラテジーコードでこれらの列にアクセスして、さらに分析できます。以下は例です：

``` python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # 累積deltaの計算
    dataframe["cum_delta"] = cumulative_delta(dataframe["delta"])
    # 総取引数へのアクセス
    total_trades = dataframe["total_trades"]
    ...

def cumulative_delta(delta: Series):
    cumdelta = delta.cumsum()
    return cumdelta

```

### フットプリントチャート（`dataframe["orderflow"]`）

この列は、異なる価格レベルでの買い注文と売り注文の詳細な内訳を提供し、オーダーフローのダイナミクスに関する貴重な洞察を提供します。設定の`scale`パラメータは、この表現の価格ビンサイズを決定します。

`orderflow`列には、次の構造のdictが含まれています：

``` output
{
    "price": {
        "bid_amount": 0.0,
        "ask_amount": 0.0,
        "bid": 0,
        "ask": 0,
        "delta": 0.0,
        "total_volume": 0.0,
        "total_trades": 0
    }
}
```

#### オーダーフロー列の説明

- key: 価格ビン - `scale`間隔でビン化
- `bid_amount`: 各価格レベルで購入された総量。
- `ask_amount`: 各価格レベルで販売された総量。
- `bid`: 各価格レベルでの買い注文の数。
- `ask`: 各価格レベルでの売り注文の数。
- `delta`: 各価格レベルでのaskとbid量の差。
- `total_volume`: 各価格レベルでの総量（ask量 + bid量）。
- `total_trades`: 各価格レベルでの総取引数（ask + bid）。

これらの機能を活用することで、市場のセンチメントとオーダーフロー分析に基づく潜在的な取引機会に関する貴重な洞察を得ることができます。

### 生の取引データ（`dataframe["trades"]`）

ローソク足中に発生した個別の取引のリスト。このデータは、オーダーフローダイナミクスのより細かい分析に使用できます。

各個別エントリには、次のキーを持つdictが含まれています：

- `timestamp`: 取引のタイムスタンプ。
- `date`: 取引の日付。
- `price`: 取引の価格。
- `amount`: 取引の量。
- `side`: 買いまたは売り。
- `id`: 取引の一意の識別子。
- `cost`: 取引の総コスト（価格 * 量）。

### 不均衡（`dataframe["imbalances"]`）

この列は、オーダーフローの不均衡に関する情報を含むdictを提供します。不均衡は、特定の価格レベルでaskとbid量の間に大きな差がある場合に発生します。

各行は次のようになります - 価格をインデックスとし、対応するbidとask不均衡値を列として持ちます

``` output
{
    "price": {
        "bid_imbalance": False,
        "ask_imbalance": False
    }
}
```
