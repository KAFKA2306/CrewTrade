# インストール

このページでは、ボットを実行するための環境を準備する方法を説明します。

freqtradeドキュメントでは、freqtradeをインストールするさまざまな方法を説明しています

* [Dockerイメージ](docker_quickstart.md)（別ページ）
* [スクリプトインストール](#script-installation)
* [手動インストール](#manual-installation)
* [Condaを使用したインストール](#installation-with-conda)

freqtradeの動作を評価する間、事前構築された[dockerイメージ](docker_quickstart.md)を使用してすぐに開始することを検討してください。

------

## 情報

Windowsインストールについては、[Windowsインストールガイド](windows_installation.md)を使用してください。

FreqtradeをインストールおよびLMするための最も簡単な方法は、ボットのGithubリポジトリをクローンしてから、プラットフォームで利用可能な場合は`./setup.sh`スクリプトを実行することです。

!!! Note "バージョンに関する考慮事項"
    リポジトリをクローンすると、デフォルトの作業ブランチは`develop`という名前です。このブランチには、最新の機能がすべて含まれています（自動テストのおかげで比較的安定していると考えられます）。
    `stable`ブランチには、最新リリースのコードが含まれています（通常、パッケージングバグを防ぐために、`develop`ブランチの約1週間前のスナップショットで月に1回実行されるため、潜在的により安定しています）。

!!! Note
    [uv](https://docs.astral.sh/uv/)、またはPython3.11以上と対応する`pip`が利用可能であることが前提です。そうでない場合、インストールスクリプトは警告を出して停止します。Freqtradeリポジトリをクローンするには`git`も必要です。
    また、インストールが正常に完了するには、Pythonヘッダー（`python<yourversion>-dev` / `python<yourversion>-devel`）が利用可能である必要があります。

!!! Warning "最新の時計"
    ボットを実行しているシステムの時計は正確でなければならず、取引所との通信の問題を回避するために、NTPサーバーに十分頻繁に同期する必要があります。

------

## 要件

これらの要件は、[スクリプトインストール](#script-installation)と[手動インストール](#manual-installation)の両方に適用されます。

!!! Note "ARM64システム"
ARM64システム（MacOS M1やOracle VMなど）を実行している場合は、[docker](docker_quickstart.md)を使用してfreqtradeを実行してください。
    手動で作業すればネイティブインストールも可能ですが、現時点ではサポートされていません。

### インストールガイド

* [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html)（推奨）

### インストールコード

Ubuntu、MacOS、およびWindowsのインストール手順を含めて/収集しました。これらはガイドラインであり、他のディストリビューションでの成功は異なる場合があります。
OS固有の手順が最初にリストされ、以下の共通セクションはすべてのシステムに必要です。

!!! Note
    Python3.11以上と対応するpipが利用可能であることが前提です。

=== "Debian/Ubuntu"
    #### 必要な依存関係をインストール
    ```bash
    # リポジトリを更新
    sudo apt-get update

    # パッケージをインストール
    sudo apt install -y python3-pip python3-venv python3-dev python3-pandas git curl
    ```
=== "MacOS"
    #### 必要な依存関係をインストール

    まだ持っていない場合は、[Homebrew](https://brew.sh/)をインストールしてください。
    ```bash
    # パッケージをインストール
    brew install gettext libomp
    ```
    !!! Note
        `setup.sh`スクリプトは、brewがシステムにインストールされていることを前提として、これらの依存関係をインストールします。

=== "RaspberryPi/Raspbian"
    以下は、最新の[Raspbian Buster liteイメージ](https://www.raspberrypi.org/downloads/raspbian/)を前提としています。
    このイメージにはpython3.11がプリインストールされているため、freqtradeを簡単に起動できます。

    Raspbian Buster liteイメージを使用したRaspberry Pi 3でテストされ、すべての更新が適用されています。
    ```bash
    sudo apt-get install python3-venv libatlas-base-dev cmake curl libffi-dev
    # piwheels.orgを使用してインストールを高速化
    sudo echo "[global]\nextra-index-url=https://www.piwheels.org/simple" > tee /etc/pip.conf

    git clone https://github.com/freqtrade/freqtrade.git
    cd freqtrade

    bash setup.sh -i
    ```
    !!! Note "インストール期間"
        インターネット速度とRaspberry Piのバージョンによっては、インストールに数時間かかる場合があります。
        このため、[Docker quickstartドキュメント](docker_quickstart.md)に従って、Raspberry用の事前構築されたdockerイメージを使用することをお勧めします。

    !!! Note
        上記はhyperoptの依存関係をインストールしません。これらをインストールするには、`python3 -m pip install -e .[hyperopt]`を使用してください。
        Raspberry Piでhyperoptを実行することはお勧めしません。これは非常にリソースを消費する操作であり、強力なマシンで実行する必要があるためです。

------

## Freqtradeリポジトリ

Freqtradeは、コードが`github.com`でホストされているオープンソース暗号通貨トレーディングボットです
```bash
# freqtradeリポジトリの`develop`ブランチをダウンロード
git clone https://github.com/freqtrade/freqtrade.git

# ダウンロードしたディレクトリに入る
cd freqtrade

# 選択肢(1): 初心者ユーザー
git checkout stable

# 選択肢(2): 上級ユーザー
git checkout develop
```
(1) このコマンドは、クローンされたリポジトリを`stable`ブランチの使用に切り替えます。(2) `develop`ブランチにとどまりたい場合は必要ありません。

後で`git checkout stable`/`git checkout develop`コマンドを使用して、いつでもブランチ間を切り替えることができます。

??? Note "pypiからインストール"
    Freqtradeをインストールする別の方法は、[pypi](https://pypi.org/project/freqtrade/)からです。欠点は、この方法ではta-libを事前に正しくインストールする必要があり、したがって現在Freqtradeをインストールする推奨方法ではないことです。
    ``` bash
    pip install freqtrade
    ```
------

## スクリプトインストール

Freqtradeをインストールする最初の方法は、提供されているLinux/MacOS `./setup.sh`スクリプトを使用することです。これにより、すべての依存関係がインストールされ、ボットの設定が支援されます。

[要件](#requirements)を満たし、[Freqtradeリポジトリ](#freqtrade-repository)をダウンロードしていることを確認してください。

### /setup.sh -installを使用（Linux/MacOS）

Debian、Ubuntu、またはMacOSの場合、freqtradeはfreqtradeをインストールするスクリプトを提供します。
```bash
# --install、ゼロからfreqtradeをインストール
./setup.sh -i
```
### 仮想環境をアクティブ化

新しいターミナルを開くたびに、`source .venv/bin/activate`を実行して仮想環境をアクティブ化する必要があります。
```bash
# 仮想環境をアクティブ化
source ./.venv/bin/activate
```
[これでボットを実行する準備ができました](#you-are-ready)。

### /setup.shスクリプトのその他のオプション

`./script.sh`を使用して、ボットのコードベースを更新、設定、リセットすることもできます
```bash
# --update、git pullコマンドで更新
./setup.sh -u
# --reset、develop/stableブランチをハードリセット
./setup.sh -r
```

```
** --install **

このオプションを使用すると、スクリプトはボットとほとんどの依存関係をインストールします:
これが機能するには、事前にgitとpython3.11+をインストールしておく必要があります。

* `ta-lib`などの必須ソフトウェア
* `.venv/`の下に仮想環境をセットアップ

このオプションは、インストールタスクと`--reset`の組み合わせです

** --update **

このオプションは、現在のブランチの最新バージョンをプルし、仮想環境を更新します。ボットを更新するには、定期的にこのオプションを使用してスクリプトを実行してください。

** --reset **

このオプションは、ブランチをハードリセットし（`stable`または`develop`のいずれかの場合のみ）、仮想環境を再作成します。
```
-----

## 手動インストール

[要件](#requirements)を満たし、[Freqtradeリポジトリ](#freqtrade-repository)をダウンロードしていることを確認してください。

### Python仮想環境（virtualenv）のセットアップ

freqtradeは分離された`virtual environment`で実行されます
```bash
# ディレクトリ/freqtrade/.venvに仮想環境を作成
python3 -m venv .venv

# 仮想環境を実行
source .venv/bin/activate
```
### Python依存関係をインストール
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
# freqtradeをインストール
python3 -m pip install -e .
```
[これでボットを実行する準備ができました](#you-are-ready)。

### （オプション）インストール後のタスク

!!! Note
    サーバーでボットを実行する場合は、ログアウト時にボットが停止するのを避けるために、[Docker](docker_quickstart.md)またはターミナルマルチプレクサ（`screen`や[`tmux`](https://en.wikipedia.org/wiki/Tmux)など）の使用を検討してください。

ソフトウェアスイート`systemd`を使用するLinuxでは、オプションのインストール後のタスクとして、ボットを`systemd service`として実行するようにセットアップしたり、ログメッセージを`syslog`/`rsyslog`または`journald`デーモンに送信するように設定したりできます。詳細については、[高度なロギング](advanced-setup.md#advanced-logging)を参照してください。

------

## Condaを使用したインストール

FreqtradeはMinicondaまたはAnacondaでもインストールできます。インストールフットプリントが小さいため、Minicondaの使用をお勧めします。Condaは、Freqtradeプログラムの広範なライブラリ依存関係を自動的に準備および管理します。

### Condaとは？

Condaは、複数のプログラミング言語用のパッケージ、依存関係、環境マネージャーです：[condaドキュメント](https://docs.conda.io/projects/conda/en/latest/index.html)

### condaを使用したインストール

#### Condaのインストール

[Linuxへのインストール](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent)

[Windowsへのインストール](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)

すべての質問に答えてください。インストール後、ターミナルをオフにしてから再度オンにする必要があります。

#### Freqtradeのダウンロード

freqtradeをダウンロードしてインストールします。
```bash
# freqtradeをダウンロード
git clone https://github.com/freqtrade/freqtrade.git

# ダウンロードしたディレクトリ'freqtrade'に入る
cd freqtrade
```
#### Freqtradeインストール: Conda環境
```bash
conda create --name freqtrade python=3.12
```
!!! Note "Conda環境の作成"
    conda `create -n`コマンドは、選択したライブラリのすべてのネストされた依存関係を自動的にインストールします。インストールコマンドの一般的な構造は次のとおりです：
    ```bash
    # 独自のパッケージを選択
    conda env create -n [環境名] [Pythonバージョン] [パッケージ]
    ```
#### freqtrade環境への入退出

利用可能な環境を確認するには、次のように入力します
```bash
conda env list
```
インストールされた環境に入る
```bash
# conda環境に入る
conda activate freqtrade

# conda環境を終了 - 今はしないでください
conda deactivate
```
pipで最後のPython依存関係をインストール
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```
[これでボットを実行する準備ができました](#you-are-ready)。

### 重要なショートカット
```bash
# インストールされたconda環境をリスト
conda env list

# base環境をアクティブ化
conda activate

# freqtrade環境をアクティブ化
conda activate freqtrade

# conda環境を非アクティブ化
conda deactivate
```
### anacondaに関する詳細情報

!!! Info "新しい重いパッケージ"
    作成時に選択したパッケージが入力された新しいConda環境を作成する方が、以前に設定された環境に大規模で重いライブラリまたはアプリケーションをインストールするよりも時間がかからない場合があります。

!!! Warning "conda内でのpipインストール"
    condaのドキュメントでは、内部的な問題が発生する可能性があるため、conda内でpipを使用すべきではないと述べています。
    しかし、それらはまれです。[Anaconda Blogpost](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)

    それにもかかわらず、そのため、`conda-forge`チャンネルが推奨されます：

    * より多くのライブラリが利用可能（`pip`の必要性が少ない）
    * `conda-forge`は`pip`とよりうまく機能する
    * ライブラリが新しい

ハッピートレーディング！

-----

## 準備完了

ここまで来たので、freqtradeのインストールに成功しました。

### 設定の初期化
```bash
# ステップ1 - ユーザーフォルダーを初期化
freqtrade create-userdir --userdir user_data

# ステップ2 - 新しい設定ファイルを作成
freqtrade new-config --config user_data/config.json
```
実行する準備ができました。[ボット設定](configuration.md)を読み、`dry_run: True`で開始し、すべてが機能していることを確認してください。

設定のセットアップ方法については、[ボット設定](configuration.md)ドキュメントページを参照してください。

### ボットを起動
```bash
freqtrade trade --config user_data/config.json --strategy SampleStrategy
```
!!! Warning
    ドキュメントの残りの部分を読み、使用する戦略をバックテストし、実際のお金で取引を有効にする前にドライランを使用する必要があります。

-----

## トラブルシューティング

### 一般的な問題：「command not found」

(1)`Script`または(2)`Manual`インストールを使用した場合、仮想環境でボットを実行する必要があります。以下のようなエラーが発生した場合は、venvがアクティブになっていることを確認してください。
```bash
# もし:
bash: freqtrade: command not found

# その場合は仮想環境をアクティブ化
source ./.venv/bin/activate
```
### MacOSインストールエラー

新しいバージョンのMacOSでは、`error: command 'g++' failed with exit status 1`のようなエラーでインストールが失敗する場合があります。

このエラーは、このバージョンのMacOSではデフォルトでインストールされていないSDKヘッダーの明示的なインストールが必要になります。
MacOS 10.14の場合、これは以下のコマンドで実行できます。
```bash
open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg
```
このファイルが存在しない場合は、おそらく別のバージョンのMacOSを使用しているため、特定の解決の詳細についてインターネットを参照する必要があるかもしれません。
