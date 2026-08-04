"""Presentation metadata for CrewTrade research use cases.

Analytical outputs remain the source of truth. This module provides stable,
human-readable navigation metadata. It must not invent numerical results.
"""

from __future__ import annotations

from typing import Final

CASE_CATALOG: Final[dict[str, dict[str, str]]] = {
    "credit": {
        "title": "クレジット・スプレッド",
        "category": "信用環境",
        "purpose": "リスク管理",
        "scope": "投資適格・BBB・ハイイールドの信用市場",
        "period": "直近観測と過去のストレス局面",
        "status": "悪化方向",
        "summary": "投資適格・BBB・ハイイールドのOASを同一日で比較し、低いリスク補償からの悪化を監視します。",
        "question": "信用リスクへの追加補償は、悪化余地に見合っているか",
        "warning": "スプレッドの縮小だけで安全性を断定しません。格付け、デフォルト、流動性を併記します。",
        "change_summary": "ETF価格差を廃止し、ICE BofA OASの実測値とz値へ更新。",
        "accent": "apricot",
    },
    "imura": {
        "title": "ファンド・指数比較",
        "category": "運用評価",
        "purpose": "運用評価",
        "scope": "ファンドと基準指数",
        "period": "同一期間・配当・費用条件",
        "status": "実績不足",
        "summary": "費用構造と実績期間を先に監査し、因子調整後・費用控除後の超過収益だけを評価します。",
        "question": "超過収益は、比較条件とリスクをそろえても残るか",
        "warning": "比較期間、配当、費用、通貨条件が一致しない結果は横並びにしません。",
        "change_summary": "公式費用と約18か月の実績期間を反映し、運用能力を未確定へ修正。",
        "accent": "blue",
    },
    "index_7_portfolio": {
        "title": "7指数ポートフォリオ",
        "category": "資産配分",
        "purpose": "資産配分",
        "scope": "株式・債券・実物資産を含む7指数",
        "period": "下落局面を含む検証期間",
        "status": "評価不能",
        "summary": "ETF実績と長期指数代替系列を分離し、共通期間・因子集中・実装コストを評価します。",
        "question": "分散は、実際の下落局面でも機能するか",
        "warning": "銘柄数ではなく、相関と共通リスク因子で実効分散を確認します。",
        "change_summary": "314Aの設定日と20年要件の不整合を検出し、現行バックテストを無効化。",
        "accent": "lavender",
    },
    "index_etf_comparison": {
        "title": "指数ETF比較",
        "category": "商品比較",
        "purpose": "運用評価",
        "scope": "同一または近接指数へ連動するETF",
        "period": "同一通貨・配当・費用条件",
        "status": "再構築中",
        "summary": "ティッカー、ISIN、正式指数、通貨、配当、ヘッジ、費用を揃えた商品だけを比較します。",
        "question": "同じ指数名でも、投資結果を分ける条件は何か",
        "warning": "名称が同じでも連動指数、為替、分配、税、流動性が異なります。",
        "change_summary": "4つの通称ラベルを再現性0%と判定し、10項目の商品契約を導入。",
        "accent": "mint",
    },
    "legendary_investors": {
        "title": "著名投資家リサーチ",
        "category": "公開情報調査",
        "purpose": "公開情報調査",
        "scope": "SEC提出資料・年次報告書・株主書簡",
        "period": "公開済みの最新標準四半期",
        "status": "開示遅延あり",
        "summary": "SECアクセッション番号、報告対象日、提出日を起点に、保有差分と開示遅延を検証します。",
        "question": "物語ではなく、検証可能な判断原則は何か",
        "warning": "13Fは四半期末の限定情報であり、現在保有、現金、空売りの全体像ではありません。",
        "change_summary": "固定銘柄配列を来歴0%と判定し、EDGARのポイント・イン・タイム台帳へ移行。",
        "accent": "rose",
    },
    "oracle": {
        "title": "Oracle実績・予測監査",
        "category": "企業分析・予測",
        "purpose": "産業・企業分析",
        "scope": "Oracleのクラウド実績・受注残・設備投資",
        "period": "開示実績と未検証予測を分離",
        "status": "回収未検証",
        "summary": "FY2026通期のクラウド成長、RPO、営業CF、FCFを分け、設備投資回収を検証します。",
        "question": "クラウド成長と受注残は、設備投資回収を伴う売上・キャッシュフローへ転換するか",
        "warning": "モデル予測を会社実績または会社予想として表示しません。",
        "change_summary": "FY2026 Q2の古い基準をQ4・通期実績へ置換し、FCF赤字を評価へ反映。",
        "accent": "apricot",
    },
    "precious_metals_spread": {
        "title": "貴金属スプレッド",
        "category": "相対価値",
        "purpose": "マクロ・市場構造",
        "scope": "金・銀・白金族の価格比とスプレッド",
        "period": "同一時点・同一通貨の時系列",
        "status": "データ契約待ち",
        "summary": "LBMAベンチマークの時点・単位・利用権を揃え、流動性差を調整した価格比を検証します。",
        "question": "価格差は平均回帰か、構造変化か",
        "warning": "単位、取引時間、通貨、先物ロールが異なる系列を直接比較しません。",
        "change_summary": "対象系列未定義とライセンス不足を検出し、日次シグナルを停止。",
        "accent": "lavender",
    },
    "securities_collateral_loan": {
        "title": "証券担保ローン",
        "category": "リスク管理",
        "purpose": "リスク管理",
        "scope": "担保評価・金利・追証・強制売却条件",
        "period": "契約条件と下落シナリオ",
        "status": "実状態未確認",
        "summary": "設定値によるLTV感度と、契約・時価・担保掛目を確認した実状態評価を分離します。",
        "question": "どの下落率から意思決定の自由が失われるか",
        "warning": "契約条項と担保掛目を確認せず、一般的な安全水準を適用しません。",
        "change_summary": "LTV算術を再計算し、契約来歴・時価・担保掛目の欠落を評価へ反映。",
        "accent": "rose",
    },
    "semiconductors": {
        "title": "半導体サイクル",
        "category": "産業分析",
        "purpose": "産業・企業分析",
        "scope": "半導体企業・需要・価格・能力・設備投資",
        "period": "四半期実績と中期能力計画",
        "status": "ビンテージ注意",
        "summary": "WSTSの確定実績と予測時点を分離し、製品群・地域・企業事業モデルへ分解します。",
        "question": "利益成長は数量・価格・能力のどこから生じたか",
        "warning": "会社実績、会社予想、業界推計、独自シナリオを混在させません。",
        "change_summary": "2025年確定値とAutumn 2025予測の分母差を定量化し、後知恵接続を禁止。",
        "accent": "blue",
    },
    "yield_spread": {
        "title": "金利・イールドスプレッド",
        "category": "マクロ",
        "purpose": "マクロ・市場構造",
        "scope": "政策金利・国債カーブ・実質金利・通貨",
        "period": "現在のカーブと過去推移",
        "status": "定義修正",
        "summary": "米国債カーブと信用OASを別系列として扱い、期間構造と信用プレミアムを分離します。",
        "question": "金利差の変化は、どの期待とリスクプレミアムを反映しているか",
        "warning": "名目金利差だけで為替方向を断定せず、実質金利、ヘッジ費用、ポジションを確認します。",
        "change_summary": "ハイイールド実効利回り－10年国債を廃止し、財務省カーブとOASへ分離。",
        "accent": "mint",
    },
}

PURPOSE_ORDER: Final[tuple[str, ...]] = (
    "運用評価",
    "資産配分",
    "リスク管理",
    "産業・企業分析",
    "マクロ・市場構造",
    "公開情報調査",
    "未分類",
)


def describe_case(slug: str) -> dict[str, str]:
    """Return stable presentation metadata for a use case slug."""
    if slug in CASE_CATALOG:
        return {"slug": slug, **CASE_CATALOG[slug]}

    title = slug.replace("_", " ").strip().title() or "名称未設定"
    return {
        "slug": slug,
        "title": title,
        "category": "未分類",
        "purpose": "未分類",
        "scope": "対象未登録",
        "period": "レポート本文で確認",
        "status": "説明未登録",
        "summary": "分析出力は存在しますが、ダッシュボード用の説明はまだ登録されていません。",
        "question": "対象、期間、計算条件をレポート本文で確認してください",
        "warning": "表示メタデータが未登録です。本文を一次情報として確認してください。",
        "change_summary": "差分要約は未登録です。",
        "accent": "neutral",
    }


def purpose_rank(value: str) -> int:
    """Return a deterministic display rank for research purposes."""
    try:
        return PURPOSE_ORDER.index(value)
    except ValueError:
        return len(PURPOSE_ORDER)


def format_report_date(value: str) -> str:
    """Format YYYYMMDD report folder names without guessing other formats."""
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}年{value[4:6]}月{value[6:]}日"
    return value
