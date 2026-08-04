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
        "status": "要監視",
        "summary": "投資適格・BBB・ハイイールドのOASを分け、信用不安と割高なリスクテイクを監視します。",
        "question": "信用リスクへの追加補償は、悪化余地に見合っているか",
        "warning": "スプレッドの縮小だけで安全性を断定しません。格付け、デフォルト、流動性を併記します。",
        "change_summary": "最新スナップショットのデータ時点と監視条件を更新。",
        "accent": "apricot",
    },
    "imura": {
        "title": "ファンド・指数比較",
        "category": "運用評価",
        "purpose": "運用評価",
        "scope": "ファンドと基準指数",
        "period": "同一期間・配当・費用条件",
        "status": "比較可能",
        "summary": "ファンドと基準指数を同一期間・同一条件で比較し、コスト控除後の超過収益と下振れを検証します。",
        "question": "超過収益は、比較条件とリスクをそろえても残るか",
        "warning": "比較期間、配当、費用、通貨条件が一致しない結果は横並びにしません。",
        "change_summary": "比較条件とリスク指標を最新レポートへ統合。",
        "accent": "blue",
    },
    "index_7_portfolio": {
        "title": "7指数ポートフォリオ",
        "category": "資産配分",
        "purpose": "資産配分",
        "scope": "株式・債券・実物資産を含む7指数",
        "period": "下落局面を含む検証期間",
        "status": "比較可能",
        "summary": "複数指数の組み合わせを、収益率だけでなく共通ファクター、分散効果、最大下落率から評価します。",
        "question": "分散は、実際の下落局面でも機能するか",
        "warning": "銘柄数ではなく、相関と共通リスク因子で実効分散を確認します。",
        "change_summary": "共通ファクターと下落局面の検証を最新化。",
        "accent": "lavender",
    },
    "index_etf_comparison": {
        "title": "指数ETF比較",
        "category": "商品比較",
        "purpose": "運用評価",
        "scope": "同一または近接指数へ連動するETF",
        "period": "同一通貨・配当・費用条件",
        "status": "比較可能",
        "summary": "連動対象、通貨、配当、費用、流動性、トラッキング差をそろえ、ETFを比較可能な形に整理します。",
        "question": "同じ指数名でも、投資結果を分ける条件は何か",
        "warning": "名称が同じでも連動指数、為替、分配、税、流動性が異なります。",
        "change_summary": "費用とトラッキング差を含む比較軸へ更新。",
        "accent": "mint",
    },
    "legendary_investors": {
        "title": "著名投資家リサーチ",
        "category": "公開情報調査",
        "purpose": "公開情報調査",
        "scope": "SEC提出資料・年次報告書・株主書簡",
        "period": "公開済みの最新標準四半期",
        "status": "開示遅延あり",
        "summary": "SEC提出資料と一次情報を起点に、開示遅延、再現可能性、資本配分の制約を切り分けます。",
        "question": "物語ではなく、検証可能な判断原則は何か",
        "warning": "13Fは四半期末の限定情報であり、現在保有、現金、空売りの全体像ではありません。",
        "change_summary": "利用可能な開示四半期と提出期限を更新。",
        "accent": "rose",
    },
    "oracle": {
        "title": "Oracle実績・予測監査",
        "category": "企業分析・予測",
        "purpose": "産業・企業分析",
        "scope": "Oracleのクラウド実績・受注残・設備投資",
        "period": "開示実績と未検証予測を分離",
        "status": "要検証",
        "summary": "Oracleのクラウド実績とRPOを確認し、実測値と未検証の時系列予測を分離します。",
        "question": "クラウド成長と受注残は、設備投資回収を伴う売上・キャッシュフローへ転換するか",
        "warning": "モデル予測を会社実績または会社予想として表示しません。",
        "change_summary": "実績・会社開示・モデル予測の境界を再整理。",
        "accent": "apricot",
    },
    "precious_metals_spread": {
        "title": "貴金属スプレッド",
        "category": "相対価値",
        "purpose": "マクロ・市場構造",
        "scope": "金・銀・白金族の価格比とスプレッド",
        "period": "同一時点・同一通貨の時系列",
        "status": "要監視",
        "summary": "金・銀・白金族の価格差と比率を同一条件で追い、平均回帰と構造変化を分けます。",
        "question": "価格差は平均回帰か、構造変化か",
        "warning": "単位、取引時間、通貨、先物ロールが異なる系列を直接比較しません。",
        "change_summary": "系列条件と構造変化の監査観点を更新。",
        "accent": "lavender",
    },
    "securities_collateral_loan": {
        "title": "証券担保ローン",
        "category": "リスク管理",
        "purpose": "リスク管理",
        "scope": "担保評価・金利・追証・強制売却条件",
        "period": "契約条件と下落シナリオ",
        "status": "契約依存",
        "summary": "実契約の金利、担保下落、警戒線、強制売却条件を明示し、意思決定余力を検証します。",
        "question": "どの下落率から意思決定の自由が失われるか",
        "warning": "契約条項と担保掛目を確認せず、一般的な安全水準を適用しません。",
        "change_summary": "警戒線と強制売却条件の表示を更新。",
        "accent": "rose",
    },
    "semiconductors": {
        "title": "半導体サイクル",
        "category": "産業分析",
        "purpose": "産業・企業分析",
        "scope": "半導体企業・需要・価格・能力・設備投資",
        "period": "四半期実績と中期能力計画",
        "status": "継続更新",
        "summary": "市場成長を数量、価格、製品ミックス、能力、設備投資へ分解し、AI集中と循環要因を区別します。",
        "question": "利益成長は数量・価格・能力のどこから生じたか",
        "warning": "会社実績、会社予想、業界推計、独自シナリオを混在させません。",
        "change_summary": "数量・価格・能力の分解と一次資料を更新。",
        "accent": "blue",
    },
    "yield_spread": {
        "title": "金利・イールドスプレッド",
        "category": "マクロ",
        "purpose": "マクロ・市場構造",
        "scope": "政策金利・国債カーブ・実質金利・通貨",
        "period": "現在のカーブと過去推移",
        "status": "継続更新",
        "summary": "政策金利と国債カーブを分け、成長、インフレ、財政、期間プレミアムの変化を読み解きます。",
        "question": "金利差の変化は、どの期待とリスクプレミアムを反映しているか",
        "warning": "名目金利差だけで為替方向を断定せず、実質金利、ヘッジ費用、ポジションを確認します。",
        "change_summary": "金利差の構成要因と比較条件を更新。",
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
