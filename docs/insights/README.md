# 知見ドキュメント

プロジェクトの分析レポートと知見をまとめたドキュメント一覧です。

## エグゼクティブサマリー (Executive Summary)

本プロジェクト「crewTrade」における分析の核心は、**「ヒストリカルデータの限界と、それを補完する堅牢なリスク管理」**にあります。

証券担保ローンの長期バックテスト（2009-2025）から、**将来のボラティリティは過去の最適化結果を一貫して上回る（約1.5倍）**という「フォワード・ルッキング・バイアス」のリスクが定量的に明らかになりました。これに対し、単純なパラメータ最適化ではなく、安全バッファの拡大やレジーム判定といった構造的な対策が不可欠です。

同時に、ユースケースとして井村ファンド分析やAIブログリサーチなど、定量的モデルとは異なる**オルタナティブな視点**も並行して蓄積し、多角的な投資判断を目指します。

## 構成

### [証券担保ローン (Securities Collateral Loan)](file:///home/kafka/projects/crewTrade/docs/insights/securities_collateral_loan/README.md)
証券担保ローン戦略の詳細分析です。2009年から2025年までの複数年にわたるバックテスト結果と、将来のボラティリティリスク評価を含みます。

### [ユースケース (Use Cases)](file:///home/kafka/projects/crewTrade/docs/insights/use_cases/README.md)
様々な特定のユースケースや実験的戦略のコレクションです:
- 井村ファンド分析 (Imura Fund Analysis)
- 7資産ポートフォリオ (Index 7 Portfolio)
- ETF比較 (ETF Comparison)
- オラクル (Oracle)
- 貴金属スプレッド (Precious Metals Spread)
- 利回りスプレッド (Yield Spread)

## 使い方
各ディレクトリに移動して、詳細な結果やレポートを参照してください。
