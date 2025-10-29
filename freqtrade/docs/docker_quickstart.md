# Docker で Freqtrade を使用する

このページではDockerでボットを実行する方法を説明します。そのまま使えるようにするものではありません。引き続きドキュメントを読み、適切な構成方法を理解する必要があります。

## Docker をインストールする

まずは、ご使用のプラットフォーム用の Docker / Docker Desktop をダウンロードしてインストールします。

* [Mac](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Linux](https://docs.docker.com/install/)

!!!情報「Docker Compose インストール」
    Freqtrade のドキュメントでは、Docker デスクトップ (または docker compose プラグイン) の使用を前提としています。  
    docker-compose スタンドアロン インストールはまだ機能しますが、機能するにはすべての `docker compose` コマンドを `docker compose` から `docker-compose` に変更する必要があります (たとえば、`docker compose up -d` は `docker-compose up -d` になります)。

???警告「Windows 上の Docker」
    Windows システムに docker をインストールしたばかりの場合は、必ずシステムを再起動してください。再起動しないと、docker コンテナへのネットワーク接続に関連する説明できない問題が発生する可能性があります。

## Docker を使用した Freqtrade

Freqtrade は、[Dockerhub](https://hub.docker.com/r/freqtradeorg/freqtrade/) で公式の Docker イメージを提供しており、すぐに使用できる [docker compose ファイル](https://github.com/freqtrade/freqtrade/blob/stable/docker-compose.yml) も提供しています。

!!!注記
    - 次のセクションでは、「docker」がインストールされており、ログインしたユーザーが使用できることを前提としています。
    - 以下のすべてのコマンドは相対ディレクトリを使用するため、`docker-compose.yml` ファイルを含むディレクトリから実行する必要があります。

### Docker クイック スタート

新しいディレクトリを作成し、[docker-compose ファイル](https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml) をこのディレクトリに配置します。
``` bash
mkdir ft_userdata
cd ft_userdata/
# Download the docker-compose file from the repository
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Pull the freqtrade image
docker compose pull

# Create user directory structure
docker compose run --rm freqtrade create-userdir --userdir user_data

# Create configuration - Requires answering interactive questions
docker compose run --rm freqtrade new-config --config user_data/config.json
```
上記のスニペットは、「ft_userdata」という新しいディレクトリを作成し、最新の構成ファイルをダウンロードして、freqtrade イメージをプルします。
スニペットの最後の 2 つのステップでは、`user_data` を含むディレクトリと、選択に基づいたデフォルト設定を (対話的に) 作成します。

!!!質問「ボットの設定を編集するにはどうすればよいですか?」
    構成はいつでも編集できます。上記の構成を使用する場合、この構成は `user_data/config.json` (ディレクトリ `ft_userdata` 内) として利用できます。

    `docker-compose.yml` ファイルのコマンド セクションを編集して、ストラテジーとコマンドの両方を変更することもできます。

#### カスタム戦略の追加

1. 設定は「user_data/config.json」として利用できるようになりました。
2. カスタム戦略をディレクトリ `user_data/strategies/` にコピーします。
3. Strategy クラス名を `docker-compose.yml` ファイルに追加します。

「SampleStrategy」はデフォルトで実行されます。

!!!危険「『SampleStrategy』は単なるデモです!」
    「SampleStrategy」は参照用にあり、独自の戦略のアイデアを提供します。
    リアルマネーを危険にさらす前に、常に戦略をバックテストし、しばらく予行演習を行ってください。
    戦略開発の詳細については、[戦略ドキュメント](strategy-customization.md) を参照してください。

これが完了すると、取引モード (上記で作成した対応する質問への回答に応じて、ドライランまたはライブ取引) でボットを起動する準備が整います。
``` bash
docker compose up -d
```
!!!警告「デフォルト設定」
    生成された構成はほとんど機能しますが、ボットを開始する前に、すべてのオプションが希望するもの (価格設定、ペアリストなど) に対応していることを確認する必要があります。

#### UI へのアクセス

「new-config」ステップで FreqUI を有効にすることを選択した場合は、ポート「localhost:8080」で freqUI を使用できるようになります。

これで、ブラウザに「localhost:8080」と入力して UI にアクセスできるようになります。

??? 「リモートサーバー上の UI アクセス」に注意してください
    VPS 上で実行している場合は、ボットに接続するために ssh トンネルを使用するか、VPN (openVPN、ワイヤーガード) をセットアップすることを検討する必要があります。
    これにより、freqUI がインターネットに直接公開されなくなりますが、これはセキュリティ上の理由から推奨されません (freqUI はそのままでは https をサポートしません)。
    これらのツールのセットアップはこのチュートリアルの一部ではありませんが、インターネット上で多くの優れたチュートリアルが見つかります。
    この構成の詳細については、[Docker を使用した API 構成](rest-api.md#configuration-with-docker) セクションもお読みください。

#### ボットの監視

「docker compose ps」を使用して、実行中のインスタンスを確認できます。
これにより、サービス「freqtrade」が「running」としてリストされるはずです。そうでない場合は、ログを確認してください (次の点を参照)。

#### Docker 構成ログ

ログは `user_data/logs/freqtrade.log` に書き込まれます。  
コマンド `docker compose logs -f` を使用して最新のログを確認することもできます。

#### データベース

データベースは「user_data/tradesv3.sqlite」にあります。

#### docker を使用して freqtrade を更新する

「docker」を使用する場合の freqtrade の更新は、次の 2 つのコマンドを実行するだけで簡単です。
``` bash
# Download the latest image
docker compose pull
# Restart the image
docker compose up -d
```
これにより、最初に最新のイメージがプルされ、次にプルされたばかりのバージョンでコンテナーが再起動されます。

!!!警告「変更ログを確認してください」
    重大な変更や必要な手動介入がないか常に変更ログを確認し、更新後にボットが正しく起動することを確認する必要があります。

### docker-compose ファイルの編集

上級ユーザーは、docker-compose ファイルをさらに編集して、考えられるすべてのオプションまたは引数を含めることができます。

すべての freqtrade 引数は、「docker compose run --rm freqtrade <command> <optional argument>」を実行することで利用可能になります。

!!!警告「取引コマンドの「docker compose」」
    取引コマンド (`freqtrade trade <...>`) は、`docker compose run` を介して実行されるべきではなく、代わりに `docker compose up -d` を使用する必要があります。
    これにより、コンテナーが適切に開始されていること (ポート転送を含む) が確認され、システムの再起動後にコンテナーが確実に再起動されます。
    freqUI を使用する場合は、[それに応じて設定](rest-api.md#configuration-with-docker) も必ず調整してください。そうしないと、UI が使用できなくなります。

!!! 「`docker compose run --rm`」に注意してください。
    `--rm` を含めると完了後にコンテナが削除され、取引モード (`freqtrade trade` コマンドで実行) を除くすべてのモードで強く推奨されます。

??? 「docker compose を使用しない docker の使用」に注意してください。
    「`docker compose run --rm`」では、構成ファイルを指定する必要があります。
    「list-pairs」などの認証を必要としない一部の freqtrade コマンドは、代わりに「docker run --rm」を使用して実行できます。  
    たとえば、「docker run --rm freqtradeorg/freqtrade:stable list-pairs --exchange binance --quote BTC --print-json」などです。  
    これは、実行中のコンテナに影響を与えることなく、交換情報を取得して「config.json」に追加する場合に役立ちます。

#### 例: Docker を使用してデータをダウンロードする

Binance から ETH/BTC ペアと 1 時間のタイムフレームの 5 日間のバックテスト データをダウンロードします。データはホスト上のディレクトリ `user_data/data/` に保存されます。
``` bash
docker compose run --rm freqtrade download-data --pairs ETH/BTC --exchange binance --days 5 -t 1h
```
データのダウンロードの詳細については、[データ ダウンロード ドキュメント](data-download.md)を参照してください。

#### 例: Docker を使用したバックテスト

SampleStrategy と指定された期間の履歴データのバックテストを Docker コンテナーで 5 分間のタイムフレームで実行します。
``` bash
docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20190801-20191001 -i 5m
```
詳細については、[バックテストのドキュメント](backtesting.md) にアクセスしてください。

### docker による追加の依存関係

戦略でデフォルトのイメージに含まれていない依存関係が必要な場合は、ホスト上にイメージを構築する必要があります。
このためには、追加の依存関係のインストール手順を含む Dockerfile を作成してください (例については、[docker/Dockerfile.custom](https://github.com/freqtrade/freqtrade/blob/develop/docker/Dockerfile.custom) を参照してください)。

次に、`docker-compose.yml` ファイルを変更してビルド ステップのコメントを解除し、名前の衝突を避けるためにイメージの名前を変更する必要もあります。
``` yaml
    image: freqtrade_custom
    build:
      context: .
      dockerfile: "./Dockerfile.<yourextension>"
```
次に、「docker compose build --pull」を実行して docker イメージを構築し、上記のコマンドを使用して実行します。

### Docker を使用したプロット

コマンド `freqtrade Lot-profit` および `freqtrade put-dataframe` ([Documentation](plotting.md)) は、`docker-compose.yml` ファイル内の画像を `*_plot` に変更することで利用可能になります。
これらのコマンドは次のように使用できます。
``` bash
docker compose run --rm freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805
```
出力は「user_data/plot」ディレクトリに保存され、最新のブラウザで開くことができます。

### docker compose を使用したデータ分析

Freqtrade は、jupyter lab サーバーを起動する docker-compose ファイルを提供します。
次のコマンドを使用してこのサーバーを実行できます。
``` bash
docker compose -f docker/docker-compose-jupyter.yml up
```
これにより、jupyter lab を実行する docker コンテナが作成され、「https://127.0.0.1:8888/lab」を使用してアクセスできるようになります。
簡素化されたログインのために、起動後にコンソールに出力されるリンクを使用してください。

このイメージの一部はマシン上に構築されるため、freqtrade (および依存関係) を最新の状態に保つために、イメージを時々再構築することをお勧めします。
``` bash
docker compose -f docker/docker-compose-jupyter.yml build --no-cache
```
## トラブルシューティング

### Windows 上の Docker

* エラー: `「このリクエストのタイムスタンプは、recvWindow の外にあります。」`  
  マーケット API リクエストには同期されたクロックが必要ですが、Docker コンテナ内の時刻は時間の経過とともに少し過去にシフトします。
  この問題を一時的に解決するには、「wsl --shutdown」を実行し、docker を再起動する必要があります (Windows 10 では、そうするように求めるポップアップが表示されます)。
  永続的な解決策は、Linux ホスト上で Docker コンテナをホストするか、スケジューラを使用して時々 wsl を再起動することです。
  ``` bash
  taskkill /IM "Docker Desktop.exe" /F
  wsl --shutdown
  start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
  ```
※APIに接続できない（Windows）  
  Windows を使用していて、Docker (デスクトップ) をインストールしたばかりの場合は、必ずシステムを再起動してください。 Docker を再起動しないと、ネットワーク接続に問題が発生する可能性があります。
  当然、[設定](#accessing-the-ui) もそれに応じて設定する必要があります。

!!!警告
    上記の理由により、本番環境のセットアップでは Windows で Docker を使用することはお勧めしません。実験、データダウンロード、バックテストの場合にのみ使用してください。
    freqtrade を確実に実行するには、linux-VPS を使用するのが最適です。
