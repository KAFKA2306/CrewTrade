import os
import sys
import time
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pandas_market_calendars as mcal
from pathlib import Path


class TwelveDataManager:
    """
    Centralized manager for Twelve Data API calls with intelligent caching.
    Avoids unnecessary API calls by checking market calendar and cached data.
    """
    
    def __init__(self):
        self.api_key = os.getenv('TWELVE_API_KEY')
        if not self.api_key:
            print("TWELVE_API_KEY environment variable is not set")
            sys.exit(1)
            
        self._cache_ttl = 300  # Cache TTL in seconds (5 minutes)
        self._last_fetch_times = {}
        self._cached_data = {}
        self._last_quote_fetch_times = {}
        self._cached_quotes = {}
        
        # Company name caching
        self._cached_company_names = {}
        self._last_company_fetch_times = {}
        
        # Setup data directory
        self.data_dir = Path(__file__).parent.parent.parent / "resources" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Company names JSON file path
        self.company_names_file = self.data_dir / "company_names.json"
        
        # Initialize market calendar
        self.nyse = mcal.get_calendar('NYSE')
        
        # Load company names from JSON file
        self._load_company_names_from_file()
        
    def _load_company_names_from_file(self):
        """Load company names from JSON file"""
        if self.company_names_file.exists():
            try:
                with open(self.company_names_file, 'r') as f:
                    self._cached_company_names = json.load(f)
            except Exception as e:
                print(f"Error loading company names from file: {e}")
                self._cached_company_names = {}
        else:
            self._cached_company_names = {}
    
    def _save_company_names_to_file(self):
        """Save company names to JSON file"""
        try:
            with open(self.company_names_file, 'w') as f:
                json.dump(self._cached_company_names, f, indent=2)
            print(f"Saved company names to cache")
        except Exception as e:
            print(f"Error saving company names to file: {e}")
    
    def get_latest_market_date(self) -> str:
        """Get the latest market trading date (handles weekends and holidays)"""
        today = datetime.now().date()
        
        # Get the last 5 trading days to be safe
        schedule = self.nyse.schedule(start_date=today - timedelta(days=10), end_date=today)
        
        if len(schedule) > 0:
            latest_date = schedule.index[-1].date()
            return latest_date.strftime('%Y-%m-%d')
        else:
            # Fallback to today if something goes wrong
            return today.strftime('%Y-%m-%d')
    
    def _get_csv_path(self, symbol: str) -> Path:
        """Get the CSV file path for a symbol"""
        # Replace slashes and other problematic characters for file names
        safe_symbol = symbol.lower().replace('/', '_').replace('\\', '_')
        return self.data_dir / f"{safe_symbol}.csv"
    
    def _has_recent_data(self, symbol: str) -> bool:
        """Check if we have recent data for the symbol"""
        csv_path = self._get_csv_path(symbol)
        
        if not csv_path.exists():
            return False
            
        try:
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            if df.empty:
                return False
                
            latest_data_date = df.index[-1].strftime('%Y-%m-%d')
            latest_market_date = self.get_latest_market_date()
            
            return latest_data_date >= latest_market_date
            
        except Exception as e:
            print(f"Error reading cached data for {symbol}: {e}")
            return False
    
    def _load_cached_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Load cached data from CSV"""
        csv_path = self._get_csv_path(symbol)
        
        if not csv_path.exists():
            return None
            
        try:
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            return df if not df.empty else None
        except Exception as e:
            print(f"Error loading cached data for {symbol}: {e}")
            return None
    
    def _save_data_to_cache(self, symbol: str, data: pd.DataFrame):
        """Save data to CSV cache"""
        csv_path = self._get_csv_path(symbol)
        
        try:
            data.to_csv(csv_path)
            print(f"Saved data for {symbol} to cache")
        except Exception as e:
            print(f"Error saving data for {symbol}: {e}")
    
    def _make_api_request(self, url: str, max_retries: int = 3) -> Dict[Any, Any]:
        """Make API request with retry logic and rate limiting"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                
                if response.status_code == 429:
                    wait_time = 63 if attempt == 0 else 122
                    print(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                    
                if response.status_code != 200:
                    print(f"API request failed with status code: {response.status_code}")
                    if attempt == max_retries - 1:
                        sys.exit(1)
                    continue
                    
                data = response.json()
                
                # Check for API errors
                if data.get('status') == 'error':
                    error_msg = data.get('message', 'Unknown error')
                    if 'not found' in error_msg.lower() or 'invalid' in error_msg.lower():
                        print(f"Symbol not supported: {error_msg}")
                        sys.exit(1)
                    elif 'run out of API credits' in error_msg or 'rate limit' in error_msg.lower():
                        wait_time = 62 if attempt == 0 else 122
                        print(f"Rate limit hit, waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"API error: {error_msg}")
                        sys.exit(1)
                        
                return data
                
            except Exception as e:
                print(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    sys.exit(1)
                time.sleep(5)
        
        sys.exit(1)  # Should never reach here
    
    def get_time_series_data(self, symbol: str, interval: str = "1day", period: str = "4mo") -> pd.DataFrame:
        """
        Get time series data for a symbol with intelligent caching.
        Checks cached data first and only fetches if needed.
        """
        # Check if we have recent cached data
        if self._has_recent_data(symbol):
            
            return self._load_cached_data(symbol)
        
        # Check in-memory cache
        cache_key = f"{symbol}_{interval}_{period}"
        current_time = time.time()
        
        if (cache_key in self._cached_data and 
            current_time - self._last_fetch_times.get(cache_key, 0) < self._cache_ttl):
            
            return self._cached_data[cache_key]
        
        print(f"Fetching fresh data for {symbol} from Twelve Data API")
        
        # Fetch from API
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=5000&apikey={self.api_key}"
        data = self._make_api_request(url)
        
        if not data.get('values'):
            print(f"No data available for symbol {symbol}")
            sys.exit(1)
        
        # Convert to DataFrame
        values = data['values']
        df = pd.DataFrame(values)
        
        # Convert datetime and set as index
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        
        # Rename columns to match expected format
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col])
        
        if 'Volume' in df.columns:
            df['Volume'] = pd.to_numeric(df['Volume'])
        else:
            df['Volume'] = 0
        
        # Sort by date in ascending order
        df = df.sort_index()
        
        # Cache the data
        self._cached_data[cache_key] = df
        self._last_fetch_times[cache_key] = current_time
        
        # Save to CSV cache
        self._save_data_to_cache(symbol, df)
        
        return df
    
    def get_quote_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get quote data for a symbol with caching.
        """
        current_time = time.time()
        
        # Check in-memory cache
        if (symbol in self._cached_quotes and 
            current_time - self._last_quote_fetch_times.get(symbol, 0) < self._cache_ttl):
            return self._cached_quotes[symbol]
        
        # Try quote endpoint first
        quote_url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={self.api_key}"
        quote_data = self._make_api_request(quote_url)
        
        # If quote fails, fallback to time series
        if not quote_data or quote_data.get('status') == 'error':
            time_series_url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=30&apikey={self.api_key}"
            ts_data = self._make_api_request(time_series_url)
            
            if not ts_data.get('values'):
                print(f"No quote data available for symbol {symbol}")
                sys.exit(1)
            
            # Create quote data from time series
            current = ts_data['values'][0]
            previous = ts_data['values'][1] if len(ts_data['values']) > 1 else None
            
            # Calculate change and percent change
            change = ''
            percent_change = ''
            if previous and 'close' in current and 'close' in previous:
                current_close = float(current['close'])
                prev_close = float(previous['close'])
                change = round(current_close - prev_close, 2)
                percent_change = round((current_close - prev_close) / prev_close * 100, 2)
            
            quote_data = {
                "symbol": symbol,
                "name": ts_data['meta'].get('name', symbol),
                "exchange": ts_data['meta'].get('exchange', ''),
                "mic_code": ts_data['meta'].get('mic_code', ''),
                "currency": ts_data['meta'].get('currency', ''),
                "datetime": current.get('datetime', ''),
                "open": current.get('open', ''),
                "high": current.get('high', ''),
                "low": current.get('low', ''),
                "close": current.get('close', ''),
                "volume": current.get('volume', ''),
                "previous_close": previous.get('close', '') if previous else '',
                "change": change,
                "percent_change": percent_change,
                "average_volume": '',
                "fifty_two_week": {
                    "low": '',
                    "high": '',
                    "low_change": '',
                    "low_change_percent": '',
                    "high_change": '',
                    "high_change_percent": '',
                    "range": ''
                }
            }
        else:
            # Ensure quote_data has the right structure
            quote_data = {
                "symbol": quote_data.get('symbol', symbol),
                "name": quote_data.get('name', symbol),
                "exchange": quote_data.get('exchange', ''),
                "mic_code": quote_data.get('mic_code', ''),
                "currency": quote_data.get('currency', ''),
                "datetime": quote_data.get('datetime', ''),
                "open": quote_data.get('open', ''),
                "high": quote_data.get('high', ''),
                "low": quote_data.get('low', ''),
                "close": quote_data.get('close', ''),
                "volume": quote_data.get('volume', ''),
                "previous_close": quote_data.get('previous_close', ''),
                "change": quote_data.get('change', ''),
                "percent_change": quote_data.get('percent_change', ''),
                "average_volume": quote_data.get('average_volume', ''),
                "fifty_two_week": quote_data.get('fifty_two_week', {
                    "low": '',
                    "high": '',
                    "low_change": '',
                    "low_change_percent": '',
                    "high_change": '',
                    "high_change_percent": '',
                    "range": ''
                })
            }
        
        # Cache the data
        self._cached_quotes[symbol] = quote_data
        self._last_quote_fetch_times[symbol] = current_time
        
        return quote_data

    def get_company_name(self, symbol: str) -> str:
        """
        Get company name for a symbol with intelligent caching.
        Checks cached data first and only fetches if needed.
        """
        current_time = time.time()
        
        # Check in-memory cache first
        if (symbol in self._cached_company_names and 
            current_time - self._last_company_fetch_times.get(symbol, 0) < self._cache_ttl):
            return self._cached_company_names[symbol]
        
        # Check if we have it in the JSON file cache
        if symbol in self._cached_company_names:
            # Update in-memory cache timing
            self._last_company_fetch_times[symbol] = current_time
            return self._cached_company_names[symbol]
        
        print(f"Fetching fresh company name for {symbol} from Twelve Data API")
        
        # Fetch from API using quote data
        try:
            quote_data = self.get_quote_data(symbol)
            company_name = quote_data.get("name", symbol)
            
            # Cache the data in-memory and file
            self._cached_company_names[symbol] = company_name
            self._last_company_fetch_times[symbol] = current_time
            
            # Save to JSON file
            self._save_company_names_to_file()
            
            return company_name
            
        except Exception as e:
            print(f"Error fetching company name for {symbol}: {e}")
            return symbol


# Create a singleton instance
twelve_data_manager = TwelveDataManager() 