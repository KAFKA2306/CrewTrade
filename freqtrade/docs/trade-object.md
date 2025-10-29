# 取引オブジェクト

## 取引

freqtradeが入力するポジションは、データベースに永続化される`Trade`オブジェクトに格納されます。
これはfreqtradeのコアコンセプトであり、ドキュメントの多くのセクションで遭遇するものであり、ほとんどの場合、この場所に誘導されます。

多くの[戦略コールバック](strategy-callbacks.md)で戦略に渡されます。戦略に渡されたオブジェクトは直接変更できません。コールバックの結果に基づいて間接的な変更が発生する場合があります。

## 取引 - 利用可能な属性

以下の属性/プロパティは、個々の取引ごとに利用可能であり、`trade.<property>`（例：`trade.pair`）で使用できます。

| 属性 | データ型 | 説明 |
|------------|-------------|-------------|
| `pair` | string | この取引のペア。 |
| `safe_base_currency` | string | 基本通貨の互換性レイヤー。 |
| `safe_quote_currency` | string | 見積もり通貨の互換性レイヤー。 |
| `is_open` | boolean | 取引が現在オープンしているか、または終了しているか。 |
| `exchange` | string | この取引が実行された取引所。 |
| `open_rate` | float | この取引が入力されたレート（取引調整の場合は平均入力レート）。 |
| `open_rate_requested` | float | 取引が開かれたときに要求されたレート。 |
| `open_trade_value` | float | 手数料を含むオープントレードの価値。 |
| `close_rate` | float | 決済レート - is_open = Falseの場合にのみ設定されます。 |
| `close_rate_requested` | float | 要求された決済レート。 |
| `safe_close_rate` | float | 決済レートまたは`close_rate_requested`、どちらも利用できない場合は0.0。取引が決済された後にのみ意味があります。 |
| `stake_amount` | float | 賭け金（または見積もり）通貨での金額。 |
| `max_stake_amount` | float | この取引で使用された最大賭け金額（すべての約定済みエントリー注文の合計）。 |
| `amount` | float | 現在所有している資産/基本通貨での金額。最初の注文が約定するまで0.0になります。 |
| `amount_requested` | float | この取引で最初の入力注文の一部として最初に要求された金額。 |
| `open_date` | datetime | 取引が開かれたときのタイムスタンプ **`open_date_utc`を代わりに使用してください** |
| `open_date_utc` | datetime | 取引が開かれたときのタイムスタンプ - UTC。 |
| `close_date` | datetime | 取引が決済されたときのタイムスタンプ **`close_date_utc`を代わりに使用してください** |
| `close_date_utc` | datetime | 取引が決済されたときのタイムスタンプ - UTC。 |
| `close_profit` | float | 取引決済時の相対利益。`0.01` == 1% |
| `close_profit_abs` | float | 取引決済時の絶対利益（賭け金通貨）。 |
| `realized_profit` | float | 取引がまだオープンしている間にすでに実現された絶対利益（賭け金通貨）。 |
| `leverage` | float | この取引で使用されたレバレッジ - スポット市場ではデフォルトで1.0。 |
| `enter_tag` | string | データフレームの`enter_tag`列を介して入力時に提供されるタグ。 |
| `exit_reason` | string | 取引が決済された理由。 |
| `exit_order_status` | string | 決済注文のステータス。 |
| `strategy` | string | この取引で使用された戦略名。 |
| `timeframe` | int | この取引で使用された時間枠。 |
| `is_short` | boolean | ショートトレードの場合はTrue、それ以外の場合はFalse。 |
| `orders` | Order[] | この取引に添付された注文オブジェクトのリスト（約定済み注文とキャンセル済み注文の両方を含む）。 |
| `date_last_filled_utc` | datetime | 最後に約定した注文の時刻。 |
| `date_entry_fill_utc` | datetime | 最初に約定したエントリー注文の日付。 |
| `entry_side` | "buy" / "sell" | 取引が入力された注文サイド。 |
| `exit_side` | "buy" / "sell" | 取引の決済/ポジションの削減につながる注文サイド。 |
| `trade_direction` | "long" / "short" | テキストでの取引方向 - ロングまたはショート。 |
| `max_rate` | float | この取引中に到達した最高価格。100％正確ではありません。 |
| `min_rate` | float | この取引中に到達した最低価格。100％正確ではありません。 |
| `nr_of_successful_entries` | int | 成功した（約定した）エントリー注文の数。 |
| `nr_of_successful_exits` | int | 成功した（約定した）決済注文の数。 |
| `has_open_position` | boolean | この取引にオープンポジション（金額> 0）がある場合はTrue。最初の入力注文が未約定の間のみFalse。 |
| `has_open_orders` | boolean | 取引にオープン注文（ストップロス注文を除く）があるか。 |
| `has_open_sl_orders` | boolean | この取引にオープンストップロス注文がある場合はTrue。 |
| `open_orders` | Order[] | この取引のすべてのオープン注文（ストップロス注文を除く）。 |
| `open_sl_orders` | Order[] | この取引のすべてのオープンストップロス注文。 |
| `fully_canceled_entry_order_count` | int | 完全にキャンセルされたエントリー注文の数。 |
| `canceled_exit_order_count` | int | キャンセルされた決済注文の数。 |

### ストップロス関連の属性

| 属性 | データ型 | 説明 |
|------------|-------------|-------------|
| `stop_loss` | float | ストップロスの絶対値。 |
| `stop_loss_pct` | float | ストップロスの相対値。 |
| `initial_stop_loss` | float | 初期ストップロスの絶対値。 |
| `initial_stop_loss_pct` | float | 初期ストップロスの相対値。 |
| `stoploss_last_update_utc` | datetime | 取引所注文更新の最後のストップロスのタイムスタンプ。 |
| `stoploss_or_liquidation` | float | ストップロスまたは清算価格のより制限的な方を返し、ストップロスがトリガーされる価格に対応します。 |

### 先物/証拠金取引の属性

| 属性 | データ型 | 説明 |
|------------|-------------|-------------|
| `liquidation_price` | float | レバレッジ取引の清算価格。 |
| `interest_rate` | float | 証拠金取引の金利。 |
| `funding_fees` | float | 先物取引の合計資金調達手数料。 |

## クラスメソッド

以下はクラスメソッドです。これらは一般的な情報を返し、通常はデータベースに対する明示的なクエリになります。
`Trade.<method>`として使用できます。例：`open_trades = Trade.get_open_trade_count()`

!!! Warning "バックテスト/ハイパーオプト"
    ほとんどのメソッドは、バックテスト/ハイパーオプトとライブ/ドライモードの両方で機能します。
    バックテスト中は、[戦略コールバック](strategy-callbacks.md)での使用に限定されます。`populate_*()`メソッドでの使用はサポートされておらず、誤った結果になります。

### get_trades_proxy

戦略が既存の（オープンまたはクローズ）取引に関する情報を必要とする場合は、`Trade.get_trades_proxy()`を使用するのが最善です。

使用法：

``` python
from freqtrade.persistence import Trade
from datetime import timedelta

# ...
trade_hist = Trade.get_trades_proxy(pair='ETH/USDT', is_open=False, open_date=current_date - timedelta(days=2))

```

`get_trades_proxy()`は、次のキーワード引数をサポートしています。すべての引数はオプションです。引数なしで`get_trades_proxy()`を呼び出すと、データベース内のすべての取引のリストが返されます。

* `pair` 例：`pair='ETH/USDT'`
* `is_open` 例：`is_open=False`
* `open_date` 例：`open_date=current_date - timedelta(days=2)`
* `close_date` 例：`close_date=current_date - timedelta(days=5)`

### get_open_trade_count

現在オープンしている取引の数を取得します

``` python
from freqtrade.persistence import Trade
# ...
open_trades = Trade.get_open_trade_count()
```

### get_total_closed_profit

ボットがこれまでに生成した合計利益を取得します。
すべての決済済み取引の`close_profit_abs`を集計します。

``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.get_total_closed_profit()
```

### total_open_trades_stakes

現在取引中の合計賭け金額を取得します。

``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.total_open_trades_stakes()
```

## バックテスト/ハイパーオプトでサポートされていないクラスメソッド

以下のクラスメソッドは、バックテスト/ハイパーオプトモードではサポートされていません。

### get_overall_performance

`/performance`テレグラムコマンドと同様に、全体的なパフォーマンスを取得します。

``` python
from freqtrade.persistence import Trade

# ...
if self.config['runmode'].value in ('live', 'dry_run'):
    performance = Trade.get_overall_performance()
```

サンプル戻り値：ETH/BTCには5つの取引があり、合計利益は1.5％（比率0.015）でした。

``` json
{"pair": "ETH/BTC", "profit": 0.015, "count": 5}
```

### get_trading_volume

注文に基づいて合計取引量を取得します。

``` python
from freqtrade.persistence import Trade

# ...
volume = Trade.get_trading_volume()
```

## 注文オブジェクト

`Order`オブジェクトは、取引所での注文（またはドライランモードでのシミュレートされた注文）を表します。
`Order`オブジェクトは、常に対応する[`Trade`](#trade-object)に結び付けられ、取引のコンテキストでのみ意味があります。

### 注文 - 利用可能な属性

注文オブジェクトは通常、取引に添付されます。
ここのほとんどのプロパティは、取引所の応答に依存するため、Noneになる可能性があります。

| 属性 | データ型 | 説明 |
|------------|-------------|-------------|
| `trade` | Trade | この注文が添付されている取引オブジェクト |
| `ft_pair` | string | この注文のペア |
| `ft_is_open` | boolean | 注文はまだオープンですか？ |
| `ft_order_side` | string | 注文サイド（'buy'、'sell'、または'stoploss'） |
| `ft_cancel_reason` | string | 注文がキャンセルされた理由 |
| `ft_order_tag` | string | カスタム注文タグ |
| `order_id` | string | 取引所注文ID |
| `order_type` | string | 取引所で定義されている注文タイプ - 通常はマーケット、リミット、またはストップロス |
| `status` | string | [ccxtの注文構造](https://docs.ccxt.com/#/README?id=order-structure)で定義されているステータス。通常はオープン、クローズ、期限切れ、キャンセル、または拒否 |
| `side` | string | 買いまたは売り |
| `price` | float | 注文が出された価格 |
| `average` | float | 注文が約定した平均価格 |
| `amount` | float | 基本通貨での金額 |
| `filled` | float | 約定済み金額（基本通貨）（代わりに`safe_filled`を使用） |
| `safe_filled` | float | 約定済み金額（基本通貨） - Noneでないことが保証されています |
| `safe_amount` | float | 金額 - Noneの場合はft_amountにフォールバックします |
| `safe_price` | float | 価格 - 平均、価格、ストップ価格、ft_priceを介してフォールバックします |
| `safe_placement_price` | float | 注文が出された価格 |
| `remaining` | float | 残りの金額（代わりに`safe_remaining`を使用） |
| `safe_remaining` | float | 残りの金額 - 取引所から取得されるか、計算されます。 |
| `safe_cost` | float | 注文のコスト - Noneでないことが保証されています |
| `safe_fee_base` | float | 基本通貨での手数料 - Noneでないことが保証されています |
| `safe_amount_after_fee` | float | 手数料を差し引いた後の金額 |
| `cost` | float | 注文のコスト - 通常は平均*約定済み（*先物取引では取引所によって異なります。レバレッジの有無にかかわらずコストが含まれる場合があり、契約単位である場合があります*） |
| `stop_price` | float | ストップ注文のストップ価格。ストップロス注文以外は空です。 |
| `stake_amount` | float | この注文に使用された賭け金額。 |
| `stake_amount_filled` | float | この注文に使用された約定済み賭け金額。 |
| `order_date` | datetime | 注文作成日 **代わりに`order_date_utc`を使用してください** |
| `order_date_utc` | datetime | 注文作成日（UTC） |
| `order_filled_date` | datetime |  注文約定日 **代わりに`order_filled_utc`を使用してください** |
| `order_filled_utc` | datetime | 注文約定日 |
| `order_update_date` | datetime | 最終注文更新日 |