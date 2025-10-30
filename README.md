

## プロジェクト概要
AI Trading Crew は CrewAI を基盤としたマルチエージェント分析フレームワークです。既存の株式リサーチ機能に加え、ユースケース単位で分析フローを拡張できる構造を採用しました。最初の拡張ユースケースとして、以下の 4 本の東京証券取引所 ETF（1540, 1541, 1542, 1543）と対応する貴金属スポット価格、および為替レートを組み合わせた**価格乖離（スプレッド）分析**を実装するための設計を示します。

- 1540：純金上場信託（換金総額型）
- 1541：純プラチナ上場信託（換金総額型）
- 1542：純銀上場信託（換金総額型）
- 1543：純パラジウム上場信託（換金総額型）

これらの ETF は 1 口あたりに対応する貴金属グラム数が決まっているため、スポット価格（USD 建て）と USD/JPY レートから理論価格（円建て）を算出できます。本 README では、最小限の変更で既存リポジトリに調和させながら、構造的・ロジカルに分析基盤を拡張する手順をまとめます。

---

## 新ユースケースの狙い
- ETF 終値と理論的な貴金属価格（FX 換算後）の乖離を定量化
- 乖離の水準・方向・持続時間を指標化し、裁定機会や異常検知のヒントを得る
- FX 変動の影響を分離して、貴金属本体の需給要因を評価
- 今後追加する他ユースケース（コモディティ・マクロ連動戦略など）のテンプレート化

---

## ディレクトリ方針
既存構成に影響を与えないよう、ユースケース専用の名前空間を導入します。

```
ai_trading_crew/
  analysts/
  config/
  utils/
  use_cases/
    __init__.py
    base.py               # 共通のパイプライン定義
    registry.py           # ユースケース登録窓口
    data_clients/
      __init__.py
      metals.py           # ETF・貴金属・為替データ取得
    precious_metals_spread/
      __init__.py
      config.py           # ETF→金属対応、閾値設定
      data_pipeline.py    # データ取得とパース
      analysis.py         # 乖離指標算出
      reporting.py        # Markdown / Parquet 出力
config/
  use_cases/
    precious_metals_spread.yaml   # 実行パラメータ
output/
  use_cases/
    precious_metals_spread/
      {YYYYMMDD}/edge_report.md
resources/
  data/
    use_cases/
      precious_metals_spread/
        raw/*.parquet
        processed/edges.parquet
```

- `use_cases/base.py`：Pydantic 設定 → データ取得 → 解析 → レポートのテンプレートクラス
- `registry.py`：ユースケース名とクラスをマッピングし、実行時に選択可能にする。
- `data_clients/metals.py`：`yfinance` とローカルキャッシュを組み合わせ、ETF（1540.T など）、貴金属スポット（GC=F 等）、為替（USDJPY=X）を取得。
- `precious_metals_spread` 配下にロジックをカプセル化し、他ユースケース追加時も同じ構成を踏襲。

---

## データ取得ロジック
1. **ETF 終値**：`1540.T`, `1541.T`, `1542.T`, `1543.T`
2. **貴金属スポット**：`GC=F`, `PL=F`, `SI=F`, `PA=F`
3. **為替レート**：`USDJPY=X`

取得手順の例（擬似コード）：
```python
import yfinance as yf

etf = yf.download(['1540.T', '1541.T', '1542.T', '1543.T'], period='2y')
metals = yf.download(['GC=F', 'PL=F', 'SI=F', 'PA=F'], period='2y')
fx = yf.download('USDJPY=X', period='2y')
```

- 日次終値を採用し、東京市場休場日に合わせて前営業日で前方補完。
- 生データは `resources/data/use_cases/precious_metals_spread/raw/` に Parquet 形式で保存し、再取得を最小化。

---

## 理論価格と乖離指標
1. 貴金属スポット（USD/トロイオンス）を円換算し、グラムベースへ変換。
   - `price_jpy_per_gram = (spot_usd / 31.1034768) * usd_jpy`
2. 各 ETF の 1 口あたり金属量を乗じて理論価格を算出。
   - 1540：1g、1541：1g、1542：100g、1543：10g
3. 実際の ETF 終値との差分と乖離率を計算。
   - `gap = etf_close - theoretical_price`
   - `gap_pct = gap / theoretical_price`
4. 20 日移動平均・移動標準偏差から z-score を算出し、±2σ 超で「エッジ」と判定。
5. 乖離拡大時の USDJPY 変化率も併せて記録し、FX ショック由来か判断する補助情報を付与。

計算結果は `processed/edges.parquet` に集約し、日付と ETF ごとの乖離指標を保持します。

---

## レポート出力
- Markdown レポート例：`output/use_cases/precious_metals_spread/20251029/edge_report.md`
- 内容：
  - 日付、対象 ETF、乖離率、z-score、FX 変動、シグナル判定
  - 簡潔な解釈（例：「1542 が銀スポットの急騰に追随せず割安。前日比で USDJPY -0.6% 下落、円高が一因」）
- 将来的には既存の DayTrader エージェントへ入力して、文章生成に活用することも可能です。

---

## 実行イメージ
将来的に `use_case_runner` を追加し、コマンドラインからユースケース単位で起動できるようにします。

```bash
# 例: 貴金属乖離分析を実行
python -m ai_trading_crew.use_case_runner precious_metals_spread \
  --config config/use_cases/precious_metals_spread.yaml
```

設定ファイルには、取得期間、再取得のクールタイム、エッジ判定閾値、レポート出力先などをまとめて管理します。

---

## 導入手順（共通）
1. `.env` で API キーを設定（OpenRouter / TwelveData / TimeGPT / RapidAPI）
2. `uv sync` などで依存を揃える
3. 既存の株式分析フローは `python -m ai_trading_crew.main` で利用可能
4. 貴金属ユースケースは `use_cases` 名前空間から段階的に組み込む
