# Windowsへのインストール

Windowsユーザーは、[Docker](docker_quickstart.md)を使用することを**強く**お勧めします。これは、はるかに簡単かつスムーズに（そしてより安全に）動作するためです。

それが不可能な場合は、Windows Linuxサブシステム（WSL）を使用してみてください。その場合、Ubuntuの手順が機能するはずです。
それ以外の場合は、以下の手順に従ってください。

すべての手順は、python 3.11以降がインストールされ、利用可能であることを前提としています。

## gitリポジトリのクローン

まず、次を実行してリポジトリをクローンします。

```powershell
git clone https://github.com/freqtrade/freqtrade.git
```

次に、スクリプトによる自動インストール（推奨）または対応する手動の手順に従って、インストール方法を選択します。

## freqtradeを自動的にインストールする

### インストールスクリプトの実行

スクリプトは、インストールする部分を決定するためにいくつかの質問をします。

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass
cd freqtrade
. .\setup.ps1
```

## freqtradeを手動でインストールする

!!! Note "64ビットPythonバージョン"
    Windowsで32ビットアプリケーションが持つメモリ制約のためにバックテストやハイパーオプトで問題が発生するのを避けるために、64ビットWindowsと64ビットPythonを使用してください。
    32ビットPythonバージョンはWindowsではサポートされなくなりました。

!!! Hint
    Windowsで[Anacondaディストリビューション](https://www.anaconda.com/distribution/)を使用すると、インストールの問題を大幅に解決できます。詳細については、ドキュメントの[Anacondaインストールセクション](installation.md#installation-with-conda)を参照してください。


### Windowsでのインストール中のエラー

```bash
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
```

残念ながら、コンパイルを必要とする多くのパッケージは、事前にビルドされたホイールを提供していません。したがって、Python環境で使用するためにC/C++コンパイラをインストールして利用できるようにすることが必須です。

Visual C++ビルドツールは[ここ](https://visualstudio.microsoft.com/visual-cpp-build-tools/)からダウンロードし、デフォルト構成で「C++によるデスクトップ開発」をインストールできます。残念ながら、これは重いダウンロード/依存関係であるため、WSL2または[docker compose](docker_quickstart.md)を最初に検討することをお勧めします。

![Windowsインストール](assets/windows_install.png)

---