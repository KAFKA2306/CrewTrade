# SQL ヘルパー

このページには、sqlite データベースにクエリを実行する場合のヘルプが含まれています。

!!! Tip "その他のデータベース システム"
    PostgreSQL や MariaDB などの他のデータベース システムを使用する場合は、同じクエリを使用できますが、データベース システムにそれぞれのクライアントを使用する必要があります。 freqtrade で別のデータベース システムをセットアップする方法については、[ここをクリック](advanced-setup.md#use-a- Different-database-system) を参照してください。

!!! Warning
    SQL に慣れていない場合は、データベースでクエリを実行するときに細心の注意を払う必要があります。  
    クエリを実行する前に、必ずデータベースのバックアップを作成してください。

## sqlite3をインストールする

Sqlite3 はターミナルベースの sqlite アプリケーションです。
使い慣れている場合は、SqliteBrowser のようなビジュアル データベース エディターを自由に使用してください。

### Ubuntu/Debian のインストール
```bash
sudo apt-get install sqlite3
```
### docker 経由で sqlite3 を使用する

freqtrade docker イメージには sqlite3 が含まれているため、ホスト システムに何もインストールせずにデータベースを編集できます。
``` bash
docker compose exec freqtrade /bin/bash
sqlite3 <database-file>.sqlite
```
## DBを開く
```bash
sqlite3
.open <filepath>
```
## テーブル構造

### リストテーブル
```bash
.tables
```
### 表示テーブル構造
```bash
.schema <table_name>
```
### テーブル内のすべての取引を取得します
```sql
SELECT * FROM trades;
```
## 破壊的なクエリ

データベースに書き込むクエリ。
freqtrade はすべてのデータベース操作をそれ自体で処理しようとするか、API またはテレグラム コマンドを介して公開するため、通常、これらのクエリは必要ありません。

!!! Warning
    以下のクエリを実行する前に、データベースのバックアップがあることを確認してください。

!!! Danger
    また、ボットがデータベースに接続されている間は、書き込みクエリ (「更新」、「挿入」、「削除」) を **決して** 実行しないでください。
    これにより、データ破損が発生する可能性があり、データ破損が発生する可能性が高く、回復の可能性はありません。

### 取引所を手動で終了した後も取引がまだ開いている問題を修正

!!! Warning
    取引所でペアを手動で販売してもボットは検出されず、とにかく売ろうとします。可能な限り、/forceexit <tradeid> を使用して同じことを実行する必要があります。  
    手動で変更を加える前に、データベース ファイルをバックアップすることを強くお勧めします。

!!! Note
    /forceexit の注文は次の反復でボットによって自動的にクローズされるため、/forceexit の後にこれは必要ありません。
```sql
UPDATE trades
SET is_open=0,
  close_date=<close_date>,
  close_rate=<close_rate>,
  close_profit = close_rate / open_rate - 1,
  close_profit_abs = (amount * <close_rate> * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason=<exit_reason>
WHERE id=<trade_ID_to_update>;
```
＃＃＃＃ 例
```sql
UPDATE trades
SET is_open=0,
  close_date='2020-06-20 03:08:45.103418',
  close_rate=0.19638016,
  close_profit=0.0496,
  close_profit_abs = (amount * 0.19638016 * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason='force_exit'  
WHERE id=31;
```
### データベースから取引を削除します

!!! Tip "RPC メソッドを使用して取引を削除する"
    Telegram または REST API 経由で `/delete <tradeid>` を使用することを検討してください。これが取引を削除するための推奨される方法です。

それでもデータベースから取引を直接削除したい場合は、以下のクエリを使用できます。

!!! Danger
    一部のシステム (Ubuntu) では、sqlite3 パッケージ内の外部キーが無効になっています。 sqlite を使用する場合 - 上記のクエリの前に `PRAGMA foreign_keys = ON` を実行して、外部キーがオンになっていることを確認してください。
```sql
DELETE FROM trades WHERE id = <tradeid>;

DELETE FROM trades WHERE id = 31;
```
!!! Warning
    これにより、この取引がデータベースから削除されます。正しい ID を取得していることを確認し、`where` 句を指定せずにこのクエリを**決して**実行しないでください。
