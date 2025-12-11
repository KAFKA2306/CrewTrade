import datetime
from pathlib import Path
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


class ImuraFundDataPipeline:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_data(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        saved_files = {}
        for name, symbol in targets.items():
            df = self._get_historical_data(symbol, days)
            file_path = self.raw_data_dir / f"{name}.csv"
            df.to_csv(file_path, index=False)
            saved_files[name] = str(file_path)
        return saved_files

    def _get_historical_data(self, symbol: str, days: int) -> pd.DataFrame:
        url = f"https://finance.yahoo.co.jp/quote/{symbol}/history"
        all_data = []
        page = 1
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        str_start = start_date.strftime("%Y%m%d")
        current_to_date = end_date
        str_to = current_to_date.strftime("%Y%m%d")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        while True:
            params = {"from": str_start, "to": str_to, "timeFrame": "d", "page": page}
            print(f"Fetching {symbol} page {page}...")
            resp = requests.get(url, params=params, headers=headers)
            soup = BeautifulSoup(resp.content, "html.parser")
            table = soup.find("table")
            if not table:
                break
            rows = table.find_all("tr")
            if len(rows) <= 1:
                break

            header_cols = [th.text.strip() for th in rows[0].find_all("th")]
            price_idx = 1
            for i, h in enumerate(header_cols):
                if "终値" in h or "基準価額" in h:
                    price_idx = i
                    break

            data_found = False
            for row in rows[1:]:
                cols = row.find_all(["td", "th"])
                if len(cols) <= price_idx:
                    continue
                date_str = cols[0].text.strip()
                price_str = cols[price_idx].text.strip()
                dt = (
                    datetime.datetime.strptime(date_str, "%Y年%m月%d日").date()
                    if "年" in date_str
                    else datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
                )
                all_data.append(
                    {"Date": dt, "Price": float(price_str.replace(",", ""))}
                )
                data_found = True

            if not data_found:
                break
            page += 1

        df = pd.DataFrame(all_data)
        if df.empty:
            return df
        df = df.sort_values("Date").drop_duplicates(subset=["Date"])
        return df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
