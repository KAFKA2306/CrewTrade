# Jupyter ノートブックを使用したボット データの分析

Jupyter ノートブックを使用すると、バックテストの結果や取引履歴を簡単に分析できます。サンプル ノートブックは、「freqtrade create-userdir --userdir user_data」でユーザー ディレクトリを初期化した後、「user_data/notebooks/」にあります。

## Docker を使ったクイックスタート

Freqtrade は、jupyter lab サーバーを起動する docker-compose ファイルを提供します。
次のコマンドを使用してこのサーバーを実行できます: `docker compose -f docker/docker-compose-jupyter.yml up`

これにより、jupyter lab を実行する dockercontainer が作成され、`https://127.0.0.1:8888/lab` を使用してアクセスできるようになります。
簡素化されたログインのために、起動後にコンソールに出力されるリンクを使用してください。

詳細については、「[Docker を使用したデータ分析](docker_quickstart.md#data-analysis-using-docker-compose)」セクションを参照してください。

### プロのヒント

* 使用方法については、[jupyter.org](https://jupyter.org/documentation)を参照してください。
* conda または venv 環境内から Jupyter ノートブック サーバーを起動するか、[nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels) を使用することを忘れないでください*
* 変更内容が次回の freqtrade 更新で上書きされないように、使用する前にサンプル ノートブックをコピーしてください。

### システム全体に Jupyter をインストールして仮想環境を使用する

場合によっては、Jupyter ノートブックのシステム全体のインストールを使用し、仮想環境から jupyter カーネルを使用することが必要な場合があります。
これにより、システムごとに完全な jupyter スイートを複数回インストールすることがなくなり、タスク (freqtrade / その他の分析タスク) 間を簡単に切り替えることができます。

これを機能させるには、まず仮想環境をアクティブ化し、次のコマンドを実行します。
``` bash
# Activate virtual environment
source .venv/bin/activate

pip install ipykernel
ipython kernel install --user --name=freqtrade
# Restart jupyter (lab / notebook)
# select kernel "freqtrade" in the notebook
```
!!!注記
    このセクションは完全を期すために提供されており、Freqtrade チームはこのセットアップに関する問題に対して完全なサポートを提供しません。また、Jupyter ノートブックを起動して実行する最も簡単な方法である仮想環境に Jupyter を直接インストールすることをお勧めします。この設定に関するヘルプについては、[Project Jupyter](https://jupyter.org/) [ドキュメント](https://jupyter.org/documentation) または [ヘルプ チャネル](https://jupyter.org/community) を参照してください。

!!!警告
    一部のタスクはノートブックでは特にうまく機能しません。たとえば、非同期実行を使用するものはすべて、Jupyter にとって問題になります。また、freqtrade の主なエントリ ポイントはシェル cli であるため、ノートブックで純粋な Python を使用すると、ヘルパー関数に必要なオブジェクトとパラメーターを提供する引数がバイパスされます。これらの値を設定するか、必要なオブジェクトを手動で作成する必要がある場合があります。

## 推奨されるワークフロー

|タスク |ツール |
  --- | ---
ボットの操作 | CLI
反復的なタスク |シェルスクリプト
データ分析と可視化 |ノート

1. CLI を使用して、

    * 過去のデータをダウンロード
    * バックテストを実行する
    * リアルタイムデータで実行
    * 結果のエクスポート

1. これらのアクションをシェル スクリプトに収集します

    * 複雑なコマンドを引数付きで保存
    * 複数ステップの操作を実行する
    * テスト戦略と分析用のデータの準備を自動化します

1. ノートを使用して、

    * データを視覚化する
    * マングルとプロットによる洞察の生成

## ユーティリティ スニペットの例

### ディレクトリをルートに変更します

Jupyter ノートブックはノートブック ディレクトリから実行されます。次のスニペットはプロジェクト ルートを検索するため、相対パスの一貫性が保たれます。
```python
import os
from pathlib import Path

# Change directory
# Modify this cell to insure that the output shows the correct path.
# Define all paths relative to the project root shown in the cell output
project_root = "somedir/freqtrade"
i=0
try:
    os.chdir(project_root)
    assert Path('LICENSE').is_file()
except:
    while i<4 and (not Path('LICENSE').is_file()):
        os.chdir(Path(Path.cwd(), '../'))
        i+=1
    project_root = Path.cwd()
print(Path.cwd())
```
### 複数の構成ファイルをロードする

このオプションは、複数の構成を渡した結果を検査するのに役立ちます。
これは構成の初期化全体でも実行されるため、構成は完全に初期化され、他のメソッドに渡されます。
``` python
import json
from freqtrade.configuration import Configuration

# Load config from multiple files
config = Configuration.from_files(["config1.json", "config2.json"])

# Show the config in memory
print(json.dumps(config['original_config'], indent=2))
```
インタラクティブ環境の場合は、「user_data_dir」を指定する追加構成を用意し、これを最後に渡します。これにより、ボットの実行中にディレクトリを変更する必要がなくなります。
ディレクトリが変更されない限り、相対パスは jupyter ノートブックの保存場所から始まるため、相対パスは避けた方がよいでしょう。
``` json
{
    "user_data_dir": "~/.freqtrade/"
}
```
### 詳細なデータ分析ドキュメント

* [戦略デバッグ](strategy_analysis_example.md) - Jupyter ノートブックとしても利用可能 (`user_data/notebooks/strategy_analysis_example.ipynb`)
* [プロット](plotting.md)
* [タグ分析](advanced-backtesting.md)

データを最適に分析する方法についてのアイデアを共有したい場合は、お気軽に問題を送信するか、このドキュメントを拡張するプル リクエストを送信してください。
