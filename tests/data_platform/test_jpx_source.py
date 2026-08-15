from datetime import date

from crew.data_platform.sources.jpx import parse_jpx_etf_master


def test_parse_jpx_etf_master() -> None:
    payload = """
    <html><body><table>
      <tr>
        <th>連動対象指標</th><th>コード</th><th>名称</th><th>管理会社<br>（検索コード）</th>
        <th>信託報酬</th><th>長期投資向け<br>（注1）</th><th>マーケットメイカー<br>（注9）</th>
        <th>パンフレット</th><th>銘柄詳細</th>
      </tr>
      <tr>
        <td>TOPIX</td><td><a>1308</a></td><td>上場インデックスファンドTOPIX <a>iNAV</a></td>
        <td>アモーヴァ・アセットマネジメント(13084)</td><td>0.046%</td><td>●</td><td>★</td>
        <td></td><td></td>
      </tr>
      <tr>
        <td>-</td><td><a>314A</a></td><td>架空アクティブETF</td>
        <td>テスト運用会社(ABC1)</td><td>-</td><td></td><td></td><td></td><td></td>
      </tr>
    </table></body></html>
    """.encode()

    rows = parse_jpx_etf_master(payload, as_of_date=date(2026, 8, 15))

    assert rows == [
        {
            "as_of_date": date(2026, 8, 15),
            "ticker": "1308",
            "index_name": "TOPIX",
            "official_name": "上場インデックスファンドTOPIX",
            "manager": "アモーヴァ・アセットマネジメント",
            "manager_search_code": "13084",
            "trust_fee_text": "0.046%",
            "long_term_flag": True,
            "market_maker_status": "star",
        },
        {
            "as_of_date": date(2026, 8, 15),
            "ticker": "314A",
            "index_name": None,
            "official_name": "架空アクティブETF",
            "manager": "テスト運用会社",
            "manager_search_code": "ABC1",
            "trust_fee_text": None,
            "long_term_flag": False,
            "market_maker_status": "none",
        },
    ]
