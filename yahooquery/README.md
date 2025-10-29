<p align="center">
    <a href="#"><img src="docs/docs/img/full.png"></a>
</p>
<p align="center">
    <em>非公式Yahoo Finance APIのPythonラッパー</em>
</p>
<p align="center">
    <a href="https://codecov.io/gh/dpguthrie/yahooquery" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/dpguthrie/yahooquery" alt="カバレッジ">
    </a>
    <a href="https://pypi.org/project/yahooquery" target="_blank">
        <img src="https://badge.fury.io/py/yahooquery.svg" alt="パッケージバージョン">
    </a>
    <a href="https://pepy.tech/project/yahooquery" target="_blank">
        <img src="https://pepy.tech/badge/yahooquery" alt="ダウンロード">
    </a>
</p>

---

**ドキュメント**: <a target="_blank" href="https://yahooquery.dpguthrie.com">https://yahooquery.dpguthrie.com</a>

**インタラクティブデモ**: <a target="_blank" href="https://yahooquery.streamlit.app/">https://yahooquery.streamlit.app/</a>

**ソースコード**: <a target="_blank" href="https://github.com/dpguthrie/yahooquery">https://github.com/dpguthrie/yahooquery</a>

**ブログ投稿**: <a target="_blank" href="https://towardsdatascience.com/the-unofficial-yahoo-finance-api-32dcf5d53df">https://towardsdatascience.com/the-unofficial-yahoo-finance-api-32dcf5d53df</a>

---

## 概要

Yahooqueryは、非公式のYahoo Finance APIエンドポイントへのPythonインターフェースです。このパッケージを使用すると、ユーザーはYahoo Financeのフロントエンドで表示されるほぼすべてのデータを取得できます。

Yahooqueryのいくつかの機能：

- **高速**: データはWebスクレイピングではなくAPIエンドポイントを介して取得されます。さらに、非同期リクエストは簡単な設定で利用できます。
- **シンプル**: 複数のシンボルのデータは、簡単なワンライナーで取得できます。
- **ユーザーフレンドリー**: 必要に応じてPandasデータフレームが利用されます。
- **プレミアム**: Yahoo Financeプレミアム加入者は、サブスクリプションで利用可能なデータを取得できます。

## 要件

Python 3.9以降 - **バージョン2.4.0以降ではPython 3.9以降が必要です**

- [Pandas](https://pandas.pydata.org) - 高速で強力、柔軟で使いやすいオープンソースのデータ分析および操作ツール
- [Requests](https://requests.readthedocs.io/en/master/) - 人間のために作られた、エレガントでシンプルなPython用HTTPライブラリ。
- [Requests-Futures](https://github.com/ross/requests-futures) - 人間のための非同期Python HTTPリクエスト

### Yahoo Financeプレミアム加入者

- [Selenium](https://www.selenium.dev/selenium/docs/api/py/) - Webブラウザの自動化

  SeleniumはYahooへのログインにのみ利用されます。これは、ユーザーが特定のキーワード引数を渡したときに行われます。Yahooにログインすると、Yahoo Finance Premiumの加入者であるユーザーは、プレミアム加入者のみがアクセスできるデータを取得できます。

## インストール

Yahoo Financeプレミアム加入者で、サブスクリプションで利用可能なデータを取得したい場合は、次のようにします。

```bash
pip install yahooquery[premium]
```

それ以外の場合は、premium引数を省略します。

```bash
pip install yahooquery
```

インストール済みの場合は、uvでインストールすることもできます。
```bash
uv pip install yahooquery
```

## 例

非公式のYahoo Finance APIで利用可能なデータの大部分は会社に関連しており、これはyahooqueryでは`Ticker`として表されます。会社のティッカーシンボルを渡すことで`Ticker`クラスをインスタンス化できます。たとえば、Apple, Inc.のデータを取得するには、`aapl`を`Ticker`クラスの最初の引数として渡します。

```python
from yahooquery import Ticker

aapl = Ticker('aapl')

aapl.summary_detail
```

## 複数シンボルの例

`Ticker`クラスを使用すると、同じAPIでシンボルのリストのデータを簡単に取得することもできます。シンボルのリストを`Ticker`クラスの引数として渡すだけです。

```python
from yahooquery import Ticker

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

faang = Ticker(symbols)

faang.summary_detail
```

## ライセンス

このプロジェクトは、MITライセンスの条件の下でライセンスされています。