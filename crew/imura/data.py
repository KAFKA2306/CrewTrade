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
                saved_files[name] = str(self.raw_data_dir / f"{name}.csv")
            else:
                print(f"[{name}] yfinance failed/empty. Falling back to crawl.")
                crawl_targets[name] = symbol

        if crawl_targets:
            print(f"Starting async crawl for: {list(crawl_targets.keys())}")
            results = asyncio.run(self._fetch_all_crawl(crawl_targets, days))
            for name, df in results.items():
                self._save(name, df)
                saved_files[name] = str(self.raw_data_dir / f"{name}.csv")

        return saved_files

    def _fetch_yfinance(self, symbol: str) -> pd.DataFrame:
        yf_data = yf.download(symbol, period="1y", progress=False)
        if yf_data.empty:
            return pd.DataFrame()

        if isinstance(yf_data.columns, pd.MultiIndex):
            yf_data.columns = yf_data.columns.get_level_values(0)

        yf_data = yf_data.reset_index()
        col_map = {"Close": "Price", "Adj Close": "Price"}
        for k, v in col_map.items():
            if k in yf_data.columns:
                df = yf_data[["Date", k]].rename(columns={k: v})
                df["Date"] = pd.to_datetime(df["Date"]).dt.date
                return df
        return pd.DataFrame()

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
                page_data = self._parse_table(soup, start_date, end_date)

                if not page_data:
                    break

                oldest_date = min(d["Date"] for d in page_data)
                all_data.extend(page_data)
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

    def _parse_table(self, soup: BeautifulSoup, start_date, end_date) -> list:
        data = []
        table = soup.find("table")
        if not table:
            return data

        rows = table.find_all("tr")
        if len(rows) <= 1:
            return data

        header_cols = [th.text.strip() for th in rows[0].find_all("th")]
        price_idx = 1
        for i, h in enumerate(header_cols):
            if "終値" in h or "基準価額" in h:
                price_idx = i
                break

        for row in rows[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) <= price_idx:
                continue
            date_str = cols[0].text.strip()
            if not date_str:
                continue
            price_str = cols[price_idx].text.strip()

            dt = (
                datetime.datetime.strptime(date_str, "%Y年%m月%d日").date()
                if "年" in date_str
                else datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            )

            price_val = float(price_str.replace(",", ""))
            data.append({"Date": dt, "Price": price_val})

        return data
