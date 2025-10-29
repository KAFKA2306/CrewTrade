# 高度なインストール後のタスク

このページでは、ボットのインストール後に実行できる高度なタスクと設定オプションについて説明します。これらは一部の環境で役立つ場合があります。

ここで言及されている内容が何を意味するのか分からない場合は、おそらく必要ありません。

## Freqtradeの複数インスタンスの実行

このセクションでは、同じマシン上で複数のボットを同時に実行する方法を説明します。

### 考慮すべき事項

* 異なるデータベースファイルを使用する。
* 異なるTelegramボットを使用する（複数の異なる設定ファイルが必要です。Telegramが有効な場合のみ適用されます）。
* 異なるポートを使用する（Freqtrade REST APIウェブサーバーが有効な場合のみ適用されます）。

### 異なるデータベースファイル

取引、利益などを追跡するために、freqtradeはSQLiteデータベースを使用しており、過去に実行した取引や、いつでも保有している現在のポジションなど、さまざまな種類の情報を保存します。これにより、利益を追跡できるだけでなく、最も重要なこととして、ボットプロセスが再起動されたり予期せず終了した場合でも、進行中のアクティビティを追跡できます。

Freqtradeはデフォルトで、ドライラン用とライブボット用に別々のデータベースファイルを使用します（これは、設定ファイルまたはコマンドライン引数でdatabase-urlが指定されていないことを前提としています）。
ライブトレーディングモードの場合、デフォルトのデータベースは`tradesv3.sqlite`で、ドライランの場合は`tradesv3.dryrun.sqlite`になります。

これらのファイルのパスを指定するためにtradeコマンドで使用されるオプションの引数は`--db-url`で、有効なSQLAlchemy URLが必要です。
したがって、ドライランモードで設定とストラテジーの引数のみでボットを起動する場合、次の2つのコマンドは同じ結果になります。
``` bash
freqtrade trade -c MyConfig.json -s MyStrategy
# 次と同等
freqtrade trade -c MyConfig.json -s MyStrategy --db-url sqlite:///tradesv3.dryrun.sqlite
```
つまり、たとえばUSDTでの取引と別のインスタンスでのBTCでの取引の両方でストラテジーをテストするために、2つの異なるターミナルでtradeコマンドを実行している場合、異なるデータベースで実行する必要があります。

存在しないデータベースのURLを指定すると、freqtradeは指定した名前でデータベースを作成します。したがって、BTCとUSDTのステークカレンシーでカスタムストラテジーをテストするには、次のコマンドを使用できます（2つの別々のターミナルで）：
``` bash
# ターミナル1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.dryrun.sqlite
# ターミナル2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.dryrun.sqlite
```
逆に、本番モードで同じことをする場合は、少なくとも1つの新しいデータベース（デフォルトのデータベースに加えて）を作成し、「ライブ」データベースへのパスを指定する必要があります。例：
``` bash
# ターミナル1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.live.sqlite
# ターミナル2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.live.sqlite
```
sqliteデータベースの使用に関する詳細情報、たとえば手動で取引を入力または削除する方法については、[SQLチートシート](sql_cheatsheet.md)を参照してください。

### dockerを使用した複数のインスタンス

dockerを使用してfreqtradeの複数のインスタンスを実行するには、docker-compose.ymlファイルを編集し、必要なすべてのインスタンスを個別のサービスとして追加する必要があります。設定を複数のファイルに分けることができることを覚えておいてください。そのため、モジュラー化することを考えるのが良いアイデアです。そうすれば、すべてのボットに共通の何かを編集する必要がある場合、単一の設定ファイルでそれを行うことができます。
``` yml
---
version: '3'
services:
  freqtrade1:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade1
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/latest/rest-api/ documentation
    # before enabling this.
     ports:
     - "127.0.0.1:8080:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade1.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade1.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade1.json
      --strategy SampleStrategy

  freqtrade2:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade2
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/latest/rest-api/ documentation
    # before enabling this.
    ports:
      - "127.0.0.1:8081:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade2.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade2.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade2.json
      --strategy SampleStrategy

```
freqtrade1と2は任意の命名規則を使用できます。上記のように、インスタンスごとに異なるデータベースファイル、ポートマッピング、およびTelegram設定を使用する必要があることに注意してください。

## 異なるデータベースシステムの使用

FreqtradeはSQLAlchemyを使用しており、複数の異なるデータベースシステムをサポートしています。そのため、多数のデータベースシステムがサポートされるはずです。
Freqtradeは追加のデータベースドライバに依存したり、インストールしたりしません。それぞれのデータベースシステムのインストール手順については、[SQLAlchemyドキュメント](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)を参照してください。

次のシステムはテスト済みで、freqtradeで動作することが確認されています：

* sqlite（デフォルト）
* PostgreSQL
* MariaDB

!!! Warning
    以下のデータベースシステムのいずれかを使用することにより、そのようなシステムの管理方法を知っていることを認めることになります。freqtradeチームは、以下のデータベースシステムのセットアップやメンテナンス（またはバックアップ）に関するサポートを提供しません。

### PostgreSQL

インストール:
`pip install "psycopg[binary]"`

使用法:
`... --db-url postgresql+psycopg://<username>:<password>@localhost:5432/<database>`

Freqtradeは起動時に必要なテーブルを自動的に作成します。

Freqtradeの異なるインスタンスを実行している場合、インスタンスごとに1つのデータベースをセットアップするか、接続に異なるユーザー/スキーマを使用する必要があります。

### MariaDB / MySQL

FreqtradeはSQLAlchemyを使用してMariaDBをサポートしており、複数の異なるデータベースシステムをサポートしています。

インストール:
`pip install pymysql`

使用法:
`... --db-url mysql+pymysql://<username>:<password>@localhost:3306/<database>`



## systemdサービスとして実行するボットの設定

`freqtrade.service`ファイルをsystemdユーザーディレクトリ（通常は`~/.config/systemd/user`）にコピーし、`WorkingDirectory`と`ExecStart`を設定に合わせて更新します。

!!! Note
    特定のシステム（Raspbianなど）は、ユーザーディレクトリからサービスユニットファイルをロードしません。この場合、`freqtrade.service`を`/etc/systemd/user/`にコピーしてください（スーパーユーザー権限が必要です）。
その後、次のコマンドでデーモンを起動できます：
```bash
systemctl --user start freqtrade
```
これを永続的にする（ユーザーがログアウトしても実行する）には、freqtradeユーザーの`linger`を有効にする必要があります。
```bash
sudo loginctl enable-linger "$USER"
```
ボットをサービスとして実行する場合、systemdサービスマネージャーをソフトウェアウォッチドッグとして使用して、freqtradeボットの状態を監視し、障害が発生した場合に再起動できます。設定で`internals.sd_notify`パラメータがtrueに設定されているか、`--sd-notify`コマンドラインオプションが使用されている場合、ボットはsd_notify（systemd通知）プロトコルを使用してsystemdにキープアライブpingメッセージを送信し、状態が変わったときに現在の状態（実行中、一時停止、停止）をsystemdに通知します。

`freqtrade.service.watchdog`ファイルには、ウォッチドッグとしてsystemdを使用するサービスユニット設定ファイルの例が含まれています。

!!! Note
    ボットがDockerコンテナで実行されている場合、ボットとsystemdサービスマネージャー間のsd_notify通信は機能しません。

## 高度なログ設定

Freqtradeはpythonが提供するデフォルトのログモジュールを使用しています。
Pythonはこの点で広範な[ログ設定](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)を可能にします - ここでカバーできる以上のものです。

freqtrade設定で`log_config`が提供されていない場合、デフォルトのログ形式（色付きターミナル出力）がデフォルトで設定されます。
`--logfile logfile.log`を使用すると、RotatingFileHandlerが有効になります。

ログ形式やRotatingFileHandlerに提供されるデフォルト設定に満足できない場合は、freqtrade設定ファイルに`log_config`設定を追加することで、好みに合わせてログをカスタマイズできます。

デフォルト設定は以下のようになっており、ファイルハンドラーは提供されていますが、`filename`がコメントアウトされているため有効になっていません。
この行のコメントを解除し、有効なパス/ファイル名を指定して有効にします。
``` json hl_lines="5-7 13-16 27"
{
  "log_config": {
      "version": 1,
      "formatters": {
          "basic": {
              "format": "%(message)s"
          },
          "standard": {
              "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          }
      },
      "handlers": {
          "console": {
              "class": "freqtrade.loggers.ft_rich_handler.FtRichHandler",
              "formatter": "basic"
          },
          "file": {
              "class": "logging.handlers.RotatingFileHandler",
              "formatter": "standard",
              // "filename": "someRandomLogFile.log",
              "maxBytes": 10485760,
              "backupCount": 10
          }
      },
      "root": {
          "handlers": [
              "console",
              // "file"
          ],
          "level": "INFO",
      }
  }
}
```
!!! Note "ハイライトされた行"
    上記のコードブロックでハイライトされた行は、Richハンドラーを定義し、一緒に属しています。
    フォーマッター「standard」と「file」はFileHandlerに属します。

各ハンドラーは、定義されたフォーマッターの1つを（名前で）使用する必要があり、そのクラスは利用可能で、有効なログクラスでなければなりません。
ハンドラーを実際に使用するには、「root」セグメント内の「handlers」セクションにある必要があります。
このセクションが省略されている場合、freqtradeは出力を提供しません（設定されていないハンドラーでは、とにかく）。

!!! Tip "明示的なログ設定"
    メインのfreqtrade設定ファイルからログ設定を抽出し、[複数の設定ファイル](configuration.md#multiple-configuration-files)機能を介してボットに提供することをお勧めします。これにより、不必要なコードの重複を避けることができます。

---

多くのLinuxシステムでは、ボットを設定して、ログメッセージを`syslog`または`journald`システムサービスに送信できます。リモート`syslog`サーバーへのログ記録はWindowsでも利用できます。この場合、`--logfile`コマンドラインオプションの特別な値を使用できます。

### syslogへのログ記録

Freqtradeのログメッセージをローカルまたはリモートの`syslog`サービスに送信するには、`"log_config"`設定オプションを使用してログを設定します。
``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "syslog_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers?
      "syslog": {
         "class": "logging.handlers.SysLogHandler",
          "formatter": "syslog_fmt",
          // Use one of the other options above as address instead?
          "address": "/dev/log"
      }
    },
    "root": {
      "handlers": [
        // other handlers
        "syslog",

      ]
    }

  }
}
```
たとえばコンソールにもログ出力を持つために、[追加のログハンドラー](#advanced-logging)を設定する必要がある場合があります。

#### syslogの使用法

ログメッセージは`user`ファシリティで`syslog`に送信されます。したがって、次のコマンドで表示できます：

* `tail -f /var/log/user`、または
* 包括的なグラフィカルビューア（たとえば、Ubuntu用の「Log File Viewer」）をインストールします。

多くのシステムでは、`syslog`（`rsyslog`）は`journald`からデータを取得します（逆も同様）。したがって、syslogまたはjournaldのどちらも使用でき、メッセージは`journalctl`とsyslogビューアユーティリティの両方で表示できます。あなたにとってより良い方法で、これらを任意の方法で組み合わせることができます。

`rsyslog`の場合、ボットからのメッセージを別の専用ログファイルにリダイレクトできます。これを実現するには、次を追加します
```
if $programname startswith "freqtrade" then -/var/log/freqtrade.log
```
rsyslog設定ファイルの1つ、たとえば`/etc/rsyslog.d/50-default.conf`の最後に。

`syslog`（`rsyslog`）の場合、削減モードをオンにできます。これにより、繰り返しメッセージの数が減ります。たとえば、ボットで他に何も起こらない場合、複数のボットのハートビートメッセージは単一のメッセージに減らされます。これを実現するには、`/etc/rsyslog.conf`で次のように設定します：
```
# Filter duplicated messages
$RepeatedMsgReduction on
```
#### syslogのアドレス指定

syslogアドレスは、Unixドメインソケット（ソケットファイル名）またはUDPソケット仕様（IPアドレスとUDPポートが`:`文字で区切られたもの）のいずれかです。

したがって、次が可能なアドレスの例です：

* `"address": "/dev/log"` -- `/dev/log`ソケットを使用してsyslog（rsyslog）にログを記録します。ほとんどのシステムに適しています。
* `"address": "/var/run/syslog"` -- `/var/run/syslog`ソケットを使用してsyslog（rsyslog）にログを記録します。macOSでこれを使用します。
* `"address": "localhost:514"` -- ポート514でリッスンしている場合、UDPソケットを使用してローカルsyslogにログを記録します。
* `"address": "<ip>:514"` -- リモートsyslogのIPアドレスとポート514にログを記録します。これは、外部syslogサーバーへのリモートログ記録のためにWindowsで使用できます。

??? Info "非推奨 - コマンドライン経由でsyslogを設定"
    `--logfile syslog:<syslog_address>` -- `<syslog_address>`をsyslogアドレスとして使用して、`syslog`サービスにログメッセージを送信します。

    syslogアドレスは、Unixドメインソケット（ソケットファイル名）またはUDPソケット仕様（IPアドレスとUDPポートが`:`文字で区切られたもの）のいずれかです。

    したがって、次が可能な使用例です：

    * `--logfile syslog:/dev/log` -- `/dev/log`ソケットを使用してsyslog（rsyslog）にログを記録します。ほとんどのシステムに適しています。
    * `--logfile syslog` -- 上記と同じで、`/dev/log`のショートカットです。
    * `--logfile syslog:/var/run/syslog` -- `/var/run/syslog`ソケットを使用してsyslog（rsyslog）にログを記録します。macOSでこれを使用します。
    * `--logfile syslog:localhost:514` -- ポート514でリッスンしている場合、UDPソケットを使用してローカルsyslogにログを記録します。
    * `--logfile syslog:<ip>:514` -- リモートsyslogのIPアドレスとポート514にログを記録します。これは、外部syslogサーバーへのリモートログ記録のためにWindowsで使用できます。

### journaldへのログ記録

これには、依存関係として`cysystemd` pythonパッケージがインストールされている必要があります（`pip install cysystemd`）。Windowsでは利用できません。したがって、journaldログ機能全体は、Windowsで実行されているボットでは利用できません。
Freqtradeのログメッセージを`journald`システムサービスに送信するには、次の設定スニペットを設定に追加します。
``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "journald_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers?
      "journald": {
         "class": "cysystemd.journal.JournaldLogHandler",
          "formatter": "journald_fmt",
      }
    },
    "root": {
      "handlers": [
        // ..
        "journald",

      ]
    }

  }
}
```
たとえばコンソールにもログ出力を持つために、[追加のログハンドラー](#advanced-logging)を設定する必要がある場合があります。

ログメッセージは`user`ファシリティで`journald`に送信されます。したがって、次のコマンドで表示できます：

* `journalctl -f` -- `journald`によって取得された他のログメッセージとともに、`journald`に送信されたFreqtradeログメッセージを表示します。
* `journalctl -f -u freqtrade.service` -- ボットが`systemd`サービスとして実行されている場合、このコマンドを使用できます。

メッセージをフィルタリングするための`journalctl`ユーティリティには他にも多くのオプションがあります。詳細については、このユーティリティのマニュアルページを参照してください。

多くのシステムでは、`syslog`（`rsyslog`）は`journald`からデータを取得します（逆も同様）。したがって、`--logfile syslog`または`--logfile journald`のどちらも使用でき、メッセージは`journalctl`とsyslogビューアユーティリティの両方で表示できます。あなたにとってより良い方法で、これらを任意の方法で組み合わせることができます。

??? Info "非推奨 - コマンドライン経由でjournaldを設定"
    Freqtradeのログメッセージを`journald`システムサービスに送信するには、次の形式の値で`--logfile`コマンドラインオプションを使用します：

    `--logfile journald` -- `journald`にログメッセージを送信します。

### JSON形式のログ

デフォルトの出力ストリームをJSON形式を使用するように設定することもできます。
「fmt_dict」属性は、json出力のキーと[python logging LogRecord属性](https://docs.python.org/3/library/logging.html#logrecord-attributes)を定義します。

以下の設定は、デフォルト出力をJSONに変更します。ただし、同じフォーマッターを`RotatingFileHandler`と組み合わせて使用することもできます。
1つの形式を人間が読める形式で保持することをお勧めします。
``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
       "json": {
          "()": "freqtrade.loggers.json_formatter.JsonFormatter",
          "fmt_dict": {
              "timestamp": "asctime",
              "level": "levelname",
              "logger": "name",
              "message": "message"
          }
      }
    },
    "handlers": {
      // Other handlers?
      "jsonStream": {
          "class": "logging.StreamHandler",
          "formatter": "json"
      }
    },
    "root": {
      "handlers": [
        // ..
        "jsonStream",

      ]
    }

  }
}
```
