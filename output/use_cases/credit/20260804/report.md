# クレジット・スプレッド公開状態監査

更新基準日: 2026-08-04

## 結論

ETF価格比を信用スプレッドとみなす旧分析は廃止しました。ICE BofAのOASは信用評価に適した系列ですが、FREDの公式データページには内部利用および第三者への公開に関する制約が明記されています。公開再配布の許諾を記録できるまで、CrewTrade Pagesでは数値、変化量、z値、シグナルを生成しません。

## データ

公開可能なデータ契約の状態だけを保持します。

| 項目 | 状態 |
| --- | --- |
| 正式系列 | ICE BofA option-adjusted spread |
| 旧ETF代理系列 | 廃止 |
| 内部取得 | 利用条件に従う場合のみ |
| Pagesへの数値公開 | 停止 |
| 再開条件 | ICE Data Indicesまたは権利者の公開利用許諾を記録 |

## 定量分析

公開利用許諾がないため、数値分析は実行しません。これはデータ欠損ではなく、利用権を満たさないデータを公開しないための統制です。

## 評価

| 評価軸 | 点数 | 根拠 |
| --- | ---: | --- |
| 指標定義 | 5/5 | ETF価格比ではなくOASを正式対象に固定 |
| 利用権確認 | 1/5 | 公開再配布許諾を未記録 |
| データ来歴 | 5/5 | 公式系列IDと権利者を特定 |
| 公開安全性 | 5/5 | 数値・派生値のPages公開を停止 |
| 意思決定可能性 | 1/5 | 公開分析としては再開条件待ち |
| **合計** | **17/25** | **統制停止は正常動作** |

## 限界と反証条件

- FREDで閲覧可能であることを、第三者サイトでの再配布許可と解釈しません。
- APIキーの有無と、公開利用権の有無を混同しません。
- ETF価格、総利回り、異なる残存期間の債券価格差をOASの代替にしません。
- 公開利用許諾と保存範囲を記録できた場合にのみ、正準取得・品質検査・定量分析を再開します。

## 一次情報

- FRED: ICE BofA US Corporate Index Option-Adjusted Spread — https://fred.stlouisfed.org/data/BAMLC0A0CM
- FRED: ICE BofA BBB US Corporate Index Option-Adjusted Spread — https://fred.stlouisfed.org/data/BAMLC0A4CBBB
- FRED: ICE BofA US High Yield Index Option-Adjusted Spread — https://fred.stlouisfed.org/data/BAMLH0A0HYM2
