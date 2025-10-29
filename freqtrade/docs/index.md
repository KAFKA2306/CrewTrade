![freqtrade](assets/freqtrade_poweredby.svg)

[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04864/status.svg)](https://doi.org/10.21105/joss.04864)
[![カバレッジ ステータス](https://coveralls.io/repos/github/freqtrade/freqtrade/badge.svg?branch=develop&service=github)](https://coveralls.io/github/freqtrade/freqtrade?branch=develop)

<!-- GitHub アクション ボタン -->
[:octicons-star-16: スター](https://github.com/freqtrade/freqtrade){ .md-button .md-button--sm }
[:octicons-repo-forked-16: フォーク](https://github.com/freqtrade/freqtrade/fork){ .md-button .md-button--sm }
[:octicons-download-16: ダウンロード](https://github.com/freqtrade/freqtrade/archive/stable.zip){ .md-button .md-button--sm }

## はじめに

Freqtrade は、Python で書かれた無料のオープンソース暗号取引ボットです。すべての主要な交換をサポートし、Telegram または WebUI 経由で制御できるように設計されています。バックテスト、プロット、資金管理ツールのほか、機械学習による戦略の最適化が含まれています。

!!! Danger "免責事項"
    このソフトウェアは教育目的のみを目的としています。失うのが怖いお金を危険にさらさないでください。ソフトウェアはご自身の責任で使用してください。著者およびすべての関連会社は、お客様の取引結果に対して一切の責任を負いません。

    必ずドライランで取引ボットを実行することから始めて、その仕組みと予想される利益/損失を理解するまで資金を関与させないでください。

    基本的なコーディング スキルと Python の知識があることを強くお勧めします。遠慮せずにソース コードを読み、このボットのメカニズム、アルゴリズム、実装されている技術を理解してください。

![freqtrade スクリーンショット](assets/freqtrade-screenshot.png)

## 特徴

- 戦略を開発する: [pandas](https://pandas.pydata.org/) を使用して、Python で戦略を作成します。インスピレーションを与える戦略の例は、[戦略リポジトリ](https://github.com/freqtrade/freqtrade-strategies) で入手できます。
- マーケット データのダウンロード: 取引所および取引したい市場の履歴データをダウンロードします。
- バックテスト: ダウンロードした履歴データで戦略をテストします。
- 最適化: 機械学習手法を採用した超最適化を使用して、戦略に最適なパラメーターを見つけます。戦略の買い、売り、利益確定 (ROI)、ストップロス、トレーリングストップロスのパラメーターを最適化できます。
- 市場の選択: 静的リストを作成するか、上位の取引高や価格に基づいて自動リストを使用します (バックテスト中は利用できません)。取引したくない市場を明示的にブラックリストに登録することもできます。
- 実行: シミュレートされたお金で戦略をテストするか (ドライラン モード)、実際のお金で戦略を展開します (ライブ トレード モード)。
- 制御/監視: Telegram または WebUI を使用します (ボットの開始/停止、損益の表示、毎日の概要、現在のオープン取引結果など)。
- 分析: バックテスト データまたは Freqtrade 取引履歴 (SQL データベース) のいずれかに対して、自動化された標準プロットやデータを [対話型環境] (data-analysis.md) にロードする方法など、さらなる分析を実行できます。

## サポートされている取引所マーケットプレイス

各取引所に最終的に必要となる特別な構成については、[取引所固有のメモ](exchanges.md) をお読みください。

- [X] [バイナンス](https://www.binance.com/)
- [X] [BingX](https://bingx.com/invite/0EM9RX)
- [X] [Bitget](https://www.bitget.com/)
- [X] [ビットマート](https://bitmart.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [HTX](https://www.htx.com/)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (分散型取引所、または DEX)
- [X] [クラーケン](https://kraken.com/)
- [X] [OKX](https://okx.com/)
- [X] [MyOKX](https://okx.com/) (OKX EEA)
- [ ] [<img alt="ccxt" width="30px" src="assets/ccxt-logo.svg" />](https://github.com/ccxt/ccxt/) を介して他の多くの可能性があります。 _(動作は保証できません)_

### サポートされている先物取引所 (実験的)

- [X] [バイナンス](https://www.binance.com/)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (分散型取引所、または DEX)
- [X] [OKX](https://okx.com/)

始める前に、[取引所固有の注意事項](exchanges.md) および [レバレッジを使用した取引](leverage.md) のドキュメントを必ずお読みください。

### コミュニティテスト済み

コミュニティによって動作が確認された取引所:

- [X] [Bitvavo](https://bitvavo.com/)
- [X] [Kucoin](https://www.kucoin.com/)

## コミュニティ ショーケース

--8<-- "includes/showcase.md"

## 要件

### ハードウェア要件

このボットを実行するには、少なくとも次のものを備えた Linux クラウド インスタンスをお勧めします。

- 2GB RAM
- 1GBのディスク容量
- 2vCPU

### ソフトウェア要件

- ドッカー (推奨)

あるいは

- Python 3.11+
- ピップ (pip3)
- git
- TA-Lib
- virtualenv (推奨)

## サポート

### ヘルプ / Discord

ドキュメントに記載されていない質問や、ボットに関する詳細情報が必要な場合、または単に同じ考えを持つ人々と交流したい場合は、Freqtrade [discord サーバー](https://discord.gg/p7nuUNVfP7) に参加することをお勧めします。

## 試す準備はできましたか?

まず、インストール ガイド [docker の場合](docker_quickstart.md) (推奨)、または [docker を使用しないインストール](installation.md) のインストール ガイドを読んでください。
