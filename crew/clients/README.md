# データクライアント集

ユースケース間で共有される再利用可能なデータクライアント群。

## 各モジュール概要

### metals.py
貴金属（金・銀・プラチナ・パラジウム）のスポット価格とETF価格を取得。

**データソース**:
- TwelveData API（スポット価格）
- Yahoo Finance（ETF価格）

**対象ETF**:
- 1540.T (純金上場信託)
- 1541.T (純プラチナ信託)
- 1542.T (純銀信託)
- 1543.T (純パラジウム信託)

### fixed_income.py
債券ETFのヒストリカル価格データを取得。クレジットスプレッド分析用。

**対象ETF**:
- HYG (iShares iBoxx High Yield Corporate Bond)
- JNK (SPDR Bloomberg High Yield Bond)
- TLT (iShares 20+ Year Treasury Bond)
- AGG (iShares Core U.S. Aggregate Bond)

### yield_spread.py
イールドスプレッド計算用のトレジャリー利回りデータを取得。

**データソース**: FRED API

**対象指標**:
- DGS2, DGS5, DGS10, DGS30 (Treasury Constant Maturity)
- スプレッド: 10Y-2Y, 10Y-3M, 30Y-5Y等

### equities.py
株式・ETFの価格データを取得。証券担保ローン最適化用。

**データソース**: Yahoo Finance (yfinance)

**機能**:
- 複数銘柄の並列取得
- リトライ機構
- Parquetキャッシュ

### toushin_kyokai.py
投信協会の上場ファンドリストExcelを自動ダウンロード・パース。

**データソース**: https://www.toushin.or.jp/files/static/486/listed_fund_for_investor.xlsx

**抽出データ**:
- ティッカーコード
- ファンド名称
- カテゴリ分類
- 経費率

### jpx.py
JPX（日本取引所グループ）から株式・ETFの基本情報を取得（予約）。

### ticker_utils.py
ティッカーシンボルの正規化ユーティリティ。

**機能**:
- `.T` サフィックス自動付与（東証銘柄）
- 重複除去
- バリデーション

## 使用例

```python
from ai_trading_crew.use_cases.data_clients.equities import YFinanceEquityDataClient
from ai_trading_crew.use_cases.data_clients.toushin_kyokai import ToushinKyokaiDataClient

equity_client = YFinanceEquityDataClient()
df = equity_client.fetch_data(
    tickers=["1306.T", "1570.T"],
    start_date="2022-01-01",
    end_date="2025-01-01"
)

toushin_client = ToushinKyokaiDataClient()
etf_list = toushin_client.fetch_etf_list()
```

## データキャッシュ

全データクライアントはParquet形式でキャッシュし、API呼び出しを最小化：

```
resources/data/use_cases/{use_case}/raw/{datasource}_{date}.parquet
```
