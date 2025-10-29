import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import time
import random
from ai_trading_crew.utils.twelve_data_manager import twelve_data_manager

# Load environment variables
load_dotenv()

class HistoricalMarketFetcher:
    def __init__(self):
        # No need for API key management - handled by centralized manager
        pass
        
    def get_vix(self, days: int = 30) -> str:
        """
        Get VIX (Volatility Index) data for the specified number of days from Yahoo Finance.
        Returns formatted data in a way that's easily readable for LLMs.
        
        Args:
            days (int): Number of days of VIX data to retrieve (default: 30)
        
        Returns:
            str: Formatted VIX data with current value clearly marked
        """
        vix_data = self.fetch_vix_historical_data(days)
        return self._format_vix_data_simple(vix_data, days)
        
    def get_global_market(self, days: int = 30) -> str:
        """
        Get global market data for key assets for the specified number of days from TwelveData API.
        Returns formatted data in a way that's easily readable for LLMs.
        
        Assets include: EUR/USD, Nifty 50, Shanghai Composite, Bitcoin, Gold, and US 10-Year Treasury Yield.
        
        Args:
            days (int): Number of days of data to retrieve (default: 30)
        
        Returns:
            str: Formatted global market data with current values and daily changes clearly marked
        """
        # Define TwelveData symbols for each asset
        tickers = {
            "EUR/USD": "EUR/USD",
           # "Nifty 50": "NIFTY50",  # TwelveData symbol for Nifty 50 index
            #"Shanghai Composite": "000001.SS",  # Shanghai Composite index
            "Bitcoin": "BTC/USD",
            "Gold": "GLD",  # ETF as backup, or XAU/USD
            "China": "MCHI",  # iShares MSCI China ETF
            "India": "INDA",  # iShares MSCI India ETF
            "US 2-Year Yield": "US2Y",  # US Treasury Yield 2 Years
            "US 10-Year Yield": "IEF",  # iShares 7-10 Year Treasury Bond ETF (closest to 10-year yield)
            "S&P 500": "SPY"  # ETF for S&P 500
        }
        
        results = []
        
        # Fetch data for each asset
        for asset_name, ticker in tickers.items():
            try:
                asset_data = self.fetch_twelve_data_asset(ticker, days)
                formatted_data = self._format_asset_data(asset_data, asset_name, days)
                results.append(formatted_data)
            except Exception as e:
                # If one asset fails, don't fail the entire function
                results.append(f"{asset_name}: Error retrieving data - {str(e)}")
        
        # Combine all results
        return "\n\n".join(results)



    def fetch_twelve_data_asset(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """
        Fetch historical data for an asset using the centralized TwelveData manager.
        
        Args:
            symbol (str): TwelveData symbol
            days (int): Number of days of data to retrieve (default: 30)
        
        Returns:
            pd.DataFrame: DataFrame with asset data including close prices
        """
        try:
            # Use the centralized data manager
            df = twelve_data_manager.get_time_series_data(symbol, "1day", "4mo")
            
            # Convert to the format expected by the rest of the code
            df_result = pd.DataFrame()
            df_result['value'] = df['Close']
            df_result.index = df.index
            
            # Sort by date descending (most recent first)
            df_result = df_result.sort_index(ascending=False)
            
            # Calculate daily percentage change
            df_result["pct_change"] = df_result["value"].pct_change(-1) * 100  # Negative because data is sorted in descending order
            
            return df_result.head(days)
        
        except Exception as e:
            raise ValueError(f"Error fetching data for {symbol} from TwelveData API: {str(e)}")
            
    def fetch_vix_historical_data(self, days: int = 30) -> pd.DataFrame:
        """
        Fetch historical VIX data from Yahoo Finance API directly.
        
        Args:
            days (int): Number of days of VIX data to retrieve (default: 30)
        
        Returns:
            pd.DataFrame: DataFrame with VIX data
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days * 2)
            end_timestamp = int(end_date.timestamp())
            start_timestamp = int(start_date.timestamp())
            url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0"
            }
            params = {
                "period1": start_timestamp,
                "period2": end_timestamp,
                "interval": "1d",
                "includePrePost": "false",
                "events": "history",
                "corsDomain": "finance.yahoo.com",
                ".tsrc": "finance",
                ".rand": str(random.randint(1, 1000000))
            }
            time.sleep(1)
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if not data or "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                raise ValueError("No VIX data returned from Yahoo Finance API")
            result_data = data["chart"]["result"][0]
            quote = result_data["indicators"]["quote"][0]
            timestamps = result_data["timestamp"]
            df = pd.DataFrame({
                "date": [datetime.fromtimestamp(ts) for ts in timestamps],
                "value": quote["close"]
            })
            df.set_index("date", inplace=True)
            df = df.dropna(subset=["value"])
            df = df.sort_index(ascending=False)
            df = df.head(days)
            
            # Calculate daily percentage change
            df["pct_change"] = df["value"].pct_change(-1) * 100  # Negative because data is sorted in descending order
            
            return df
        except Exception as e:
            raise ValueError(f"Error fetching VIX data from Yahoo Finance API: {str(e)}")
            
    def _format_vix_data_simple(self, vix_data: pd.DataFrame, days: int) -> str:
        """
        Format VIX data in a readable way for LLMs.
        
        Args:
            vix_data (pd.DataFrame): DataFrame with VIX data
            days (int): Number of days requested
            
        Returns:
            str: Formatted VIX data
        """
        actual_days = len(vix_data)
        result = ""
        if actual_days < days:
            result = f"WARNING: Only {actual_days} days of VIX data available instead of requested {days} days.\n\n"
        result += f"VIX (CBOE Volatility Index) values for the last {actual_days} days:\n"
        vix_data_sorted = vix_data.sort_index(ascending=True)
        latest_date = vix_data.index[0].strftime('%Y-%m-%d')
        for date, row in vix_data_sorted.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            vix_value = "No data available" if pd.isna(row['value']) else round(float(row['value']), 2)
            if date_str == latest_date:
                result += f"* {date_str}: {vix_value} (LATEST VIX VALUE, Daily change from previous day: {row['pct_change']:.2f}%)\n"
            else:
                result += f"* {date_str}: {vix_value}\n"
        return result
        
    def _format_asset_data(self, asset_data: pd.DataFrame, asset_name: str, days: int) -> str:
        """
        Format asset data in a readable way for LLMs, including daily percentage change.
        
        Args:
            asset_data (pd.DataFrame): DataFrame with asset data
            asset_name (str): Name of the asset
            days (int): Number of days requested
            
        Returns:
            str: Formatted asset data
        """
        actual_days = len(asset_data)
        result = ""
        
        if actual_days < days:
            result = f"WARNING: Only {actual_days} days of {asset_name} data available instead of requested {days} days.\n\n"
        
        result += f"{asset_name} values for the last {actual_days} days:\n"
        
        # Sort by date ascending
        asset_data_sorted = asset_data.sort_index(ascending=True)
        latest_date = asset_data.index[0].strftime('%Y-%m-%d') if len(asset_data) > 0 else ""
        
        for date, row in asset_data_sorted.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            value = "No data available" if pd.isna(row['value']) else round(float(row['value']), 4)
            
            if date_str == latest_date:
                daily_change = row['pct_change'] if not pd.isna(row['pct_change']) else "N/A"
                daily_change_str = f"{daily_change:.2f}%" if isinstance(daily_change, (int, float)) else daily_change
                result += f"* {date_str}: {value} (LATEST VALUE,  Daily change from previous day: {daily_change_str})\n"
            else:
                result += f"* {date_str}: {value}\n"
        
        return result
