# 更新方法

freqtradeのインストールを更新するには、インストール方法に対応する以下のいずれかの方法を使用してください。

!!! Note "変更の追跡"
    重大な変更/変更された動作は、すべてのリリースとともに投稿される変更ログに記載されます。
    developブランチについては、変更に驚かないようにPRをフォローしてください。

## Docker

!!! Note "`master`イメージを使用したレガシーインストール"
    リリースイメージをmasterからstableに切り替えています。docker-fileを調整し、`freqtradeorg/freqtrade:master`を`freqtradeorg/freqtrade:stable`に置き換えてください。

``` bash
docker compose pull
docker compose up -d
```

## セットアップスクリプトによるインストール

``` bash
./setup.sh --update
```

!!! Note
    仮想環境を無効にしてこのコマンドを実行してください！

## プレーンなネイティブインストール

依存関係も更新していることを確認してください。そうしないと、気づかないうちに問題が発生する可能性があります。

``` bash
git pull
pip install -U -r requirements.txt
pip install -e .

# freqUIが最新バージョンであることを確認します
freqtrade install-ui 
```

### 更新に関する問題

更新の問題は通常、依存関係の欠落（上記の手順に従わなかった場合）または更新された依存関係のインストール失敗（たとえばTA-lib）が原因で発生します。
対応するインストールセクション（以下にリンクされている一般的な問題）を参照してください。