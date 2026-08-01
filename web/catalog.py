"""Presentation metadata for CrewTrade research use cases.

The analytical outputs remain the source of truth. This module only provides
stable labels and explanations for the dashboard.
"""

from __future__ import annotations

from typing import Final

CASE_CATALOG: Final[dict[str, dict[str, str]]] = {
    "imura": {
        "title": "ファンド・指数比較",
        "category": "運用評価",
        "summary": "ファンドと基準指数を同一期間・同一条件で比較し、リターンと下振れを分けて確認します。",
        "question": "超過収益は、比較条件とリスクをそろえても残るか",
        "accent": "blue",
    },
    "index_7_portfolio": {
        "title": "7指数ポートフォリオ",
        "category": "資産配分",
        "summary": "複数指数の組み合わせを、収益率だけでなく分散効果と最大下落率から評価します。",
        "question": "分散は、実際の下落局面で機能したか",
        "accent": "lavender",
    },
    "index_etf_comparison": {
        "title": "指数ETF比較",
        "category": "商品比較",
        "summary": "連動対象、通貨、コスト、値動きの差をそろえ、ETFを比較可能な形に整理します。",
        "question": "同じ指数名でも、投資結果を分ける条件は何か",
        "accent": "mint",
    },
    "legendary_investors": {
        "title": "著名投資家リサーチ",
        "category": "公開情報調査",
        "summary": "公開資料と一次情報を起点に、投資判断の背景・再現可能性・制約を切り分けます。",
        "question": "物語ではなく、検証可能な判断原則は何か",
        "accent": "rose",
    },
    "oracle": {
        "title": "個別企業・時系列予測",
        "category": "予測実験",
        "summary": "企業データと時系列モデルを扱い、予測値と実測値、学習期間と評価期間を分離します。",
        "question": "予測はアウト・オブ・サンプルでも情報を持つか",
        "accent": "apricot",
    },
    "precious_metals_spread": {
        "title": "貴金属スプレッド",
        "category": "相対価値",
        "summary": "金属間の価格差と比率を追い、単純な価格上昇とは異なる相対変化を確認します。",
        "question": "価格差は平均回帰か、構造変化か",
        "accent": "lavender",
    },
    "securities_collateral_loan": {
        "title": "証券担保ローン",
        "category": "リスク管理",
        "summary": "担保下落、金利、追証、強制売却の条件を明示し、資金調達の耐久力を検証します。",
        "question": "どの下落率から意思決定の自由が失われるか",
        "accent": "rose",
    },
    "semiconductors": {
        "title": "半導体サイクル",
        "category": "産業分析",
        "summary": "需要、価格、設備投資、在庫、利益を分解し、循環要因と構造要因を区別します。",
        "question": "利益成長は数量・価格・能力のどこから生じたか",
        "accent": "blue",
    },
    "yield_spread": {
        "title": "金利・イールドスプレッド",
        "category": "マクロ",
        "summary": "金利水準と期間差を追い、景気・流動性・期待インフレの変化を読み解きます。",
        "question": "金利差の変化は、どの期待を反映しているか",
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
