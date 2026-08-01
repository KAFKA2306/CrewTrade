"""Presentation metadata for CrewTrade research use cases.

The analytical outputs remain the source of truth. This module only provides
stable labels and explanations for the dashboard.
"""

from __future__ import annotations

from typing import Final

CASE_CATALOG: Final[dict[str, dict[str, str]]] = {
    "credit": {
        "title": "クレジット・スプレッド",
        "category": "信用環境",
        "summary": "投資適格・BBB・ハイイールドのOASを分け、信用不安と割高なリスクテイクを監視します。",
        "question": "信用リスクへの追加補償は、悪化余地に見合っているか",
        "accent": "apricot",
    },
    "imura": {
        "title": "ファンド・指数比較",
        "category": "運用評価",
        "summary": "ファンドと基準指数を同一期間・同一条件で比較し、コスト控除後の超過収益と下振れを検証します。",
        "question": "超過収益は、比較条件とリスクをそろえても残るか",
        "accent": "blue",
    },
    "index_7_portfolio": {
        "title": "7指数ポートフォリオ",
        "category": "資産配分",
        "summary": "複数指数の組み合わせを、収益率だけでなく共通ファクター、分散効果、最大下落率から評価します。",
        "question": "分散は、実際の下落局面でも機能するか",
        "accent": "lavender",
    },
    "index_etf_comparison": {
        "title": "指数ETF比較",
        "category": "商品比較",
        "summary": "連動対象、通貨、配当、費用、流動性、トラッキング差をそろえ、ETFを比較可能な形に整理します。",
        "question": "同じ指数名でも、投資結果を分ける条件は何か",
        "accent": "mint",
    },
    "legendary_investors": {
        "title": "著名投資家リサーチ",
        "category": "公開情報調査",
        "summary": "SEC提出資料と一次情報を起点に、開示遅延、再現可能性、資本配分の制約を切り分けます。",
        "question": "物語ではなく、検証可能な判断原則は何か",
        "accent": "rose",
    },
    "oracle": {
        "title": "Oracle実績・予測監査",
        "category": "企業分析・予測",
        "summary": "Oracleのクラウド実績とRPOを確認し、実測値と未検証の時系列予測を分離します。",
        "question": "クラウド成長と受注残は、設備投資回収を伴う売上・キャッシュフローへ転換するか",
        "accent": "apricot",
    },
    "precious_metals_spread": {
        "title": "貴金属スプレッド",
        "category": "相対価値",
        "summary": "金・銀・白金族の価格差と比率を同一条件で追い、平均回帰と構造変化を分けます。",
        "question": "価格差は平均回帰か、構造変化か",
        "accent": "lavender",
    },
    "securities_collateral_loan": {
        "title": "証券担保ローン",
        "category": "リスク管理",
        "summary": "実契約の金利、担保下落、警戒線、強制売却条件を明示し、意思決定余力を検証します。",
        "question": "どの下落率から意思決定の自由が失われるか",
        "accent": "rose",
    },
    "semiconductors": {
        "title": "半導体サイクル",
        "category": "産業分析",
        "summary": "市場成長を数量、価格、製品ミックス、能力、設備投資へ分解し、AI集中と循環要因を区別します。",
        "question": "利益成長は数量・価格・能力のどこから生じたか",
        "accent": "blue",
    },
    "yield_spread": {
        "title": "金利・イールドスプレッド",
        "category": "マクロ",
        "summary": "政策金利と国債カーブを分け、成長、インフレ、財政、期間プレミアムの変化を読み解きます。",
        "question": "金利差の変化は、どの期待とリスクプレミアムを反映しているか",
        "accent": "mint",
    },
}


def describe_case(slug: str) -> dict[str, str]:
    """Return stable presentation metadata for a use case slug."""
    if slug in CASE_CATALOG:
        return {"slug": slug, **CASE_CATALOG[slug]}

    title = slug.replace("_", " ").strip().title() or "名称未設定"
    return {
        "slug": slug,
        "title": title,
        "category": "未分類",
        "summary": "分析出力は存在しますが、ダッシュボード用の説明はまだ登録されていません。",
        "question": "対象、期間、計算条件をレポート本文で確認してください",
        "accent": "neutral",
    }


def format_report_date(value: str) -> str:
    """Format YYYYMMDD report folder names without guessing other formats."""
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}年{value[4:6]}月{value[6:]}日"
    return value
