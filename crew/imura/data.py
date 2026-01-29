import asyncio
import datetime
from typing import Dict

import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler

from crew.app import BaseDataPipeline


class ImuraFundDataPipeline(BaseDataPipeline):
    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        saved_files = {}

        yfinance_targets = {}
        crawl_targets = {}

        for name, symbol in targets.items():
            if symbol.endswith(".T") or symbol.endswith(".O") or len(symbol) <= 4:
                yfinance_targets[name] = symbol
            else:
                crawl_targets[name] = symbol

        for name, symbol in yfinance_targets.items():
            print(f"[{name}] Fetching via yfinance ({symbol})...")
            df = self._fetch_yfinance(symbol)
            if not df.empty:
                self._save(name, df)
                saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")
            else:
                print(f"[{name}] yfinance failed/empty. Falling back to crawl.")
                crawl_targets[name] = symbol

        if crawl_targets:
            print(f"Starting async crawl for: {list(crawl_targets.keys())}")
            results = asyncio.run(self._fetch_all_crawl(crawl_targets, days))
            for name, df in results.items():
                self._save(name, df)
                saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")

        return saved_files

    def _fetch_yfinance(self, symbol: str) -> pd.DataFrame:
        yf_data = yf.download(symbol, period="1y", progress=False)
        if yf_data.empty:
            return pd.DataFrame()

        # Handle MultiIndex columns if present
        if isinstance(yf_data.columns, pd.MultiIndex):
            yf_data.columns = yf_data.columns.get_level_values(0)

        yf_data = yf_data.reset_index()

        # Standardize columns
        col_map = {
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
            "Date": "Date",
        }

        # Check if we have the required columns
        available_cols = [c for c in col_map.keys() if c in yf_data.columns]
        if "Close" not in available_cols and "Adj Close" in yf_data.columns:
            # Use Adj Close as Close if needed, but preferably Close
            yf_data["Close"] = yf_data["Adj Close"]
            available_cols.append("Close")

        if not available_cols:
            return pd.DataFrame()

        df = yf_data[available_cols].rename(columns=col_map)

        # Ensure Price column for compatibility
        if "close" in df.columns:
            df["Price"] = df["close"]

        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df

    async def _fetch_all_crawl(
        self, targets: Dict[str, str], days: int
    ) -> Dict[str, pd.DataFrame]:
        results = {}

        async with AsyncWebCrawler(verbose=True) as crawler:
            for name, symbol in targets.items():
                print(f"[{name}] Crawling {symbol}...")
                df = await self._crawl_symbol(crawler, symbol, days)
                results[name] = df
        return results

    async def _crawl_symbol(
        self, crawler: AsyncWebCrawler, symbol: str, days: int
    ) -> pd.DataFrame:
        from playwright.async_api import async_playwright

        base_url = f"https://finance.yahoo.co.jp/quote/{symbol}/history"
        all_data = []
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(base_url, wait_until="networkidle")

            page_num = 1
            while page_num <= 50:
                await page.wait_for_selector("table", timeout=10000)
                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")
                page_data = self._parse_table(soup)

                if not page_data:
                    break

                # Filter by date range
                valid_data = []
                for d in page_data:
                    if start_date <= d["Date"] <= end_date:
                        valid_data.append(d)

                # Check bounds based on oldest item in PAGE (not just valid ones)
                if not page_data:
                    oldest_date = start_date  # benign fallback
                else:
                    oldest_date = min(d["Date"] for d in page_data)

                all_data.extend(valid_data)
                print(
                    f"[{symbol}] Page {page_num}: {len(page_data)} items, oldest: {oldest_date}"
                )

                if oldest_date <= start_date:
                    break

                await page.mouse.wheel(0, 2000)
                await page.wait_for_timeout(500)

                next_btn = await page.query_selector('p.next__37Eo, [class*="next"]')
                if not next_btn:
                    break

                await next_btn.click()
                await page.wait_for_timeout(1500)
                page_num += 1

            await browser.close()

        df = pd.DataFrame(all_data)
        if df.empty:
            return df
        df = df.sort_values("Date").drop_duplicates(subset=["Date"])
        return df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    def _parse_table(self, soup: BeautifulSoup) -> list:
        data = []
        table = soup.find("table")
        if not table:
            return data

        rows = table.find_all("tr")
        if len(rows) <= 1:
            return data

        header_cols = [th.text.strip() for th in rows[0].find_all("th")]

        # Map headers to indices
        col_indices = {}
        for i, h in enumerate(header_cols):
            if "日付" in h:
                col_indices["Date"] = i
            elif "始値" in h:
                col_indices["open"] = i
            elif "高値" in h:
                col_indices["high"] = i
            elif "安値" in h:
                col_indices["low"] = i
            elif "終値" in h or "基準価額" in h:
                col_indices["close"] = i
            elif "出来高" in h:
                col_indices["volume"] = i

        if "Date" not in col_indices or "close" not in col_indices:
            return data

        for row in rows[1:]:
            cols = row.find_all(["td", "th"])

            row_data = {}
            # Date
            date_col_idx = col_indices["Date"]
            if len(cols) <= date_col_idx:
                continue
            date_str = cols[date_col_idx].text.strip()
            if not date_str:
                continue

            try:
                dt = (
                    datetime.datetime.strptime(date_str, "%Y年%m月%d日").date()
                    if "年" in date_str
                    else datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
                )
                row_data["Date"] = dt
            except ValueError:
                continue

            # Parse other columns
            for key, idx in col_indices.items():
                if key == "Date":
                    continue
                if len(cols) <= idx:
                    continue
                val_str = cols[idx].text.strip().replace(",", "")
                try:
                    val = float(val_str) if val_str and val_str != "-" else 0.0
                    row_data[key] = val
                except ValueError:
                    row_data[key] = 0.0

            # Ensure Price compatibility
            if "close" in row_data:
                row_data["Price"] = row_data["close"]

            # If we missed OHLC, fill with close
            if "close" in row_data:
                for req in ["open", "high", "low"]:
                    if req not in row_data:
                        row_data[req] = row_data["close"]
                if "volume" not in row_data:
                    row_data["volume"] = 0.0

            data.append(row_data)

        return data
