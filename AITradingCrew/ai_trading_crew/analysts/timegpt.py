import pandas as pd
from datetime import datetime, timedelta
import pandas_market_calendars as mcal
from typing import Optional, Tuple, List, Dict
import logging
import numpy as np
import os
import pickle
from pandas.tseries.offsets import CustomBusinessDay
from nixtla import NixtlaClient
# Configure logging
logging.basicConfig(level=logging.INFO)

# Import settings from config
from ai_trading_crew.config import settings, AGENT_INPUTS_FOLDER
from ai_trading_crew.utils.dates import get_today_str_no_min
from ai_trading_crew.utils.twelve_data_manager import twelve_data_manager


def obtain_market_schedule(start_date: datetime, end_date: datetime, market: Optional[str] = "NYSE") -> pd.DataFrame:
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    calendar = mcal.get_calendar(market)
    market_schedule = calendar.schedule(start_date=start_str, end_date=end_str)
    return market_schedule

def obtain_business_dates(start_date: datetime, end_date: datetime, market: Optional[str] = "NYSE") -> pd.DataFrame:
    business_days = pd.date_range(start=start_date, end=end_date, freq='B')
    return pd.DataFrame(index=business_days)


def get_timegpt_forecast(symbols: List[str] = settings.SYMBOLS, time_series_defaults: Dict = settings.TIME_SERIES_DEFAULTS) -> pd.DataFrame:
    """
    Get TimeGPT forecasts with automatic caching. Calls API only once per day.
    """
    
    # Add STOCK_MARKET_OVERVIEW_SYMBOL to symbols for TimeGPT (if not already included)
    timegpt_symbols = symbols.copy()
    if settings.STOCK_MARKET_OVERVIEW_SYMBOL not in timegpt_symbols:
        timegpt_symbols.append(settings.STOCK_MARKET_OVERVIEW_SYMBOL)
    
    # Set up pickle file path in agents_inputs with current date
    today_str_no_min = get_today_str_no_min()
    input_dir = os.path.join(AGENT_INPUTS_FOLDER, today_str_no_min)
    os.makedirs(input_dir, exist_ok=True)
    pickle_file = os.path.join(input_dir, "timegpt_forecasts.pkl")
    
    # Check if pickle file exists and is from today
    if os.path.exists(pickle_file):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(pickle_file))
        today = datetime.now().date()
        
        # If file was created today, load from pickle
        if file_mtime.date() == today:
            print("Loading TimeGPT forecasts from cache...")
            with open(pickle_file, 'rb') as f:
                return pickle.load(f)
    
    # Call TimeGPT API if no cache or cache is old
    print("Calling TimeGPT API to get forecasts...")
    
    max_missing_data = time_series_defaults["max_missing_data"]
    data_folder = time_series_defaults["data_folder"]
    end_date = settings.time_series_dates["end_date"]
    start_date = settings.time_series_dates["start_date"]

    # Ensure data directory exists
    os.makedirs(data_folder, exist_ok=True)

    handler = TwelveDataHandler(
        symbols_list=timegpt_symbols,
        start_date=start_date,
        end_date=end_date,
        max_missing_data=max_missing_data,
        data_folder=data_folder
    )
    combined_df = handler.run()

    # Get forecast using Nixtla TimeGPT
    nixtla_client = NixtlaClient(api_key=os.getenv('TIMEGPT_API_KEY'))
    if not nixtla_client.validate_api_key():
        raise ValueError("Problem with Nixtla API key validation")

    # Create custom business day frequency that matches the actual trading days in the data
    # This follows Nixtla's documentation for handling irregular timestamps
    print("Creating custom market frequency for TimeGPT...")
    
    # Get all unique dates from the combined data
    all_dates = pd.to_datetime(combined_df['ds']).dt.normalize().unique()
    all_dates = pd.DatetimeIndex(sorted(all_dates))
    
    # Generate all business days in the date range
    full_business_days = pd.bdate_range(
        start=all_dates.min(),
        end=all_dates.max() + timedelta(days=30),  # Extend for forecast horizon
        freq='B'
    )
    
    # Find the market holidays (business days not in our data)
    market_holidays = full_business_days.difference(all_dates)
    
    # Create custom business day frequency excluding market holidays
    custom_market_freq = CustomBusinessDay(holidays=market_holidays)
    
    print(f"Created custom frequency excluding {len(market_holidays)} market holidays")

    # Generate forecasts using the custom frequency
    df_forecast = nixtla_client.forecast(
        df=combined_df,
        h=1,  # 1-day ahead forecast
        freq=custom_market_freq,  # Use custom market frequency instead of 'B'
        time_col='ds',
        target_col='y'
    )
    
    df_forecast['TimeGPT'] = df_forecast['TimeGPT'] * 100
    
    # Save to pickle for reuse
    with open(pickle_file, 'wb') as f:
        pickle.dump(df_forecast, f)
    
    print(f"TimeGPT forecasts saved to {pickle_file}")
    return df_forecast


def format_timegpt_forecast(forecast_df: pd.DataFrame, symbol: str, company_name: str) -> str:
    symbol_forecast = forecast_df[forecast_df['unique_id'] == symbol]
    
    if not symbol_forecast.empty:
        forecast_date = symbol_forecast['ds'].iloc[0].strftime('%Y-%m-%d')
        forecast_value = symbol_forecast['TimeGPT'].iloc[0]
        return f"Forecast date for {company_name}: {forecast_date}\nForecast daily return: {forecast_value:.4f} %"
    else:
        return f"No TimeGPT forecast available for {company_name}"


class TwelveDataHandler:
    def __init__(self, symbols_list: Optional[List[str]] = None, start_date: datetime = None, end_date: datetime = None, max_missing_data: float = None, data_folder: str = None):

        self.symbols = symbols_list if symbols_list is not None else settings.SYMBOLS
        if start_date is None or end_date is None or max_missing_data is None or data_folder is None:
             raise ValueError("start_date, end_date, max_missing_data, and data_folder must be provided.")

        self.start_date = start_date
        self.end_date = end_date
        self.max_missing_data = max_missing_data
        self.data_folder = data_folder

        self.market_dates = obtain_business_dates(start_date=self.start_date, end_date=self.end_date)
        self.symbol_data = {}


    def fetch_data_with_std_check(self, ticker: str) -> pd.DataFrame:
        # Calculate the period needed based on nb_years from TIME_SERIES_DEFAULTS
        nb_years = settings.TIME_SERIES_DEFAULTS["nb_years"]
        period_map = {
            1: "12mo",
            2: "24mo", 
            3: "36mo",
            4: "48mo",
            5: "60mo"
        }
        period = period_map.get(nb_years, f"{nb_years * 12}mo")
        
        # Use TwelveDataManager to get data
        data = twelve_data_manager.get_time_series_data(ticker, interval="1day", period=period)
        
        if data.empty:
            raise ValueError(f"No data fetched for ticker {ticker}.")
            
        # Reset index to get dates as a column
        data.reset_index(inplace=True)
        
        # Rename columns to match Yahoo Finance format
        data.rename(columns={'datetime': 'ds'}, inplace=True)
        data.columns = data.columns.str.lower()
        
        # Ensure ds is datetime
        data['ds'] = pd.to_datetime(data['ds'])

        # Check that the first market trading day exists in the fetched data
        first_market_date = pd.to_datetime(self.market_dates.index[0]).normalize()
        fetched_dates = pd.to_datetime(data['ds']).dt.normalize()
        if first_market_date not in fetched_dates.values:
            raise ValueError(f"Ticker {ticker} is missing the first market trading day: {first_market_date.date()}")

        # Create column 'y' as the daily return (close/open) rounded to 5 decimals
        data['y'] = ((data['close'] / data['open'])-1).round(5)

        # Calculate returns and standard deviation for the last 120 trading days.
        if len(data) >= 120:
            recent_data = data[-120:].copy()
            recent_data['return'] = recent_data['close'] / recent_data['open'] - 1
            std_dev = recent_data['return'].std()
            if std_dev == 0:
                raise ValueError(f"Standard deviation is 0 for {ticker} over the last 120 trading days.")
        else:
            raise ValueError(f"Not enough data to compute standard deviation for {ticker}.")

        data['unique_id'] = ticker

        return data

    @staticmethod
    def replace_empty_data(df: pd.DataFrame) -> pd.DataFrame:
        mask = df.isin(["", ".", None])
        rows_to_remove = mask.any(axis=1)
        return df.loc[~rows_to_remove]

    def handle_missing_data(self, data: pd.DataFrame, data_series: str) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        modified_data = data.copy()

        # Convert market dates to datetime objects
        expected_dates = pd.to_datetime(self.market_dates.index).date
        fetched_dates = pd.to_datetime(data['ds']).dt.date

        # Find missing dates
        missing_dates = [d for d in expected_dates if d not in fetched_dates.values]

        if missing_dates:
            max_count = len(expected_dates) * self.max_missing_data
            if len(missing_dates) > max_count:
                raise Exception(
                    f"For the asset {data_series} there are {len(missing_dates)} missing trading days, which exceeds the maximum threshold of {self.max_missing_data * 100} %."
                )
            for missing_date in missing_dates:
                modified_data = self.insert_missing_date(modified_data, pd.Timestamp(missing_date), 'ds')
        missing_dates_df = pd.DataFrame(index=pd.to_datetime(missing_dates))
        return modified_data, missing_dates_df




    @staticmethod
    def insert_missing_date(data: pd.DataFrame, date: pd.Timestamp, date_column: str) -> pd.DataFrame:
        # Ensure the comparison is done in datetime format.
        date = pd.to_datetime(date)
        if date not in pd.to_datetime(data[date_column]).values:
            # Get the most recent available row before the missing date.
            filtered = data[pd.to_datetime(data[date_column]) < date]
            if not filtered.empty:
                prev_date = filtered.iloc[-1]
            else:
                prev_date = data.iloc[0]
            new_row = prev_date.copy()
            new_row[date_column] = date
            # Append the new row and sort by the date column.
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            data = data.sort_values(by=date_column).reset_index(drop=True)
        return data

    def process_data(self):
        for symbol in self.symbols:

            data = self.fetch_data_with_std_check(symbol)
            data = self.replace_empty_data(data)
            data, missing = self.handle_missing_data(data, symbol)

            # Round numeric columns to 2 decimals except for 'volume' and 'y'
            numeric_cols = data.select_dtypes(include=['float']).columns
            for col in numeric_cols:
                if col not in ['volume', 'y']:
                    data[col] = data[col].round(2)

            self.symbol_data[symbol] = data
            missing_count = len(missing) if missing is not None else 0


    def run(self) -> pd.DataFrame:
        self.process_data()
        self.combine_data()
        return self.combined_df

    def combine_data(self):
        # Save individual symbol dataframes to CSV
        self.combined_df = pd.DataFrame()  # Create empty DataFrame
        for symbol, df in self.symbol_data.items():
            file_path = os.path.join(self.data_folder, f'{symbol.lower()}.csv')
            df.to_csv(file_path, index=False)

        dataframes = list(self.symbol_data.values())
        if not dataframes:
            raise ValueError("No data available to combine.")

        # Verify that all dataframes have the same columns
        expected_columns = list(dataframes[0].columns)
        for symbol, df in self.symbol_data.items():
            if list(df.columns) != expected_columns:
                raise ValueError(f"DataFrame for {symbol} does not match the expected columns: {expected_columns}")

        self.combined_df = pd.concat(dataframes, ignore_index=True)
        self.combined_df = self.combined_df.sort_values(by='ds').reset_index(drop=True)

        market_calendar = obtain_market_schedule(start_date=self.start_date, end_date=self.end_date)
        last_trading_date = pd.to_datetime(market_calendar.index[-1])
        self.combined_df = self.combined_df[pd.to_datetime(self.combined_df['ds']) <= last_trading_date]
        self.combined_df = self.combined_df.drop_duplicates(subset=['ds', 'unique_id'], keep='first')

        combined_file_path = os.path.join(self.data_folder, 'combined.csv')
        self.combined_df.to_csv(combined_file_path, index=False)
       
