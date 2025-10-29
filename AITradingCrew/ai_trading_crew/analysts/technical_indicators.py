import os
import pandas as pd
import talib
import numpy as np
import time
import sys
from datetime import datetime, timedelta
from ai_trading_crew.config import settings
from ai_trading_crew.utils.twelve_data_manager import twelve_data_manager

from dotenv import load_dotenv


# Load environment variables
load_dotenv()

class TwelveTI:
    def __init__(self, symbol: str, interval: str) -> None:
        self.symbol = symbol
        self.interval = interval
        self._data = None
        self._quote_data = None
        
        # Map interval from Twelve Data format to yfinance format
        self.yf_interval_map = {
            "1min": "1m",
            "5min": "5m",
            "15min": "15m",
            "30min": "30m",
            "45min": "45m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "1day": "1d",
            "1week": "1wk",
            "1month": "1mo"
        }
        
    def _get_data(self, period="4mo"):
        # Use the centralized data manager
        self._data = twelve_data_manager.get_time_series_data(self.symbol, self.interval, period)
        
        # Ensure consistent column naming to handle any data source variations
        column_mapping = {
            'open': 'Open',
            'high': 'High', 
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }
        
        # Only rename columns that exist and need renaming
        for old_name, new_name in column_mapping.items():
            if old_name in self._data.columns and new_name not in self._data.columns:
                self._data = self._data.rename(columns={old_name: new_name})
        
        return self._data
    


    def _get_latest_date(self):
        data = self._get_data()
        last_date = data.index[-1]
        return last_date.strftime('%Y-%m-%d')
    
    def _get_column_data(self, data, column_name):
        """Safely get column data with proper error handling"""
        if column_name not in data.columns:
            available_columns = list(data.columns)
            raise KeyError(f"Column '{column_name}' not found in data. Available columns: {available_columns}. "
                          f"Symbol: {self.symbol}, Interval: {self.interval}")
        return data[column_name].astype(float).to_numpy().flatten()

    def fetch_adx(self, time_period: int = 14):
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = self._get_column_data(data, 'High')
        low = self._get_column_data(data, 'Low')
        close = self._get_column_data(data, 'Close')
        adx = talib.ADX(high, low, close, timeperiod=tp)
        latest = adx[-1]
        last_date = self._get_latest_date()
        return f"ADX with time_period of {tp} days has a latest value of {round(latest, 4)} on {last_date}."

    def fetch_bbands(self, time_period: int = 20):
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close = data['Close'].astype(float).to_numpy().flatten()
        upper, middle, lower = talib.BBANDS(close, timeperiod=tp, nbdevup=2.0, nbdevdn=2.0, matype=0)
        u, m, l = upper[-1], middle[-1], lower[-1]
        last_date = self._get_latest_date()
        return (f"BBANDS with time_period of {tp} days, sd of 2.0 and ma_type sma "
                f"has an upper_band value of {round(u, 4)}, middle_band value of {round(m, 4)}, "
                f"and lower_band value of {round(l, 4)} on {last_date}.")

    def fetch_ema(self, time_period: int = 9):
        data = self._get_data()
        tp = time_period if time_period is not None else 9

        close = data['Close'].astype(float).to_numpy().flatten()
        ema = talib.EMA(close, timeperiod=tp)
        value = ema[-1]
        last_date = self._get_latest_date()
        return f"EMA with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_macd(self, macd_fast_period: int = 12, macd_slow_period: int = 26):
        data = self._get_data()
        fp = macd_fast_period if macd_fast_period is not None else 12
        sp = macd_slow_period if macd_slow_period is not None else 26
        sig = 9

        close = data['Close'].astype(float).to_numpy().flatten()
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=fp, slowperiod=sp, signalperiod=sig)
        v, s, h = macd[-1], macdsignal[-1], macdhist[-1]
        last_date = self._get_latest_date()
        return (f"MACD with fast_period {fp}, slow_period {sp} and signal_period {sig} "
                f"has a macd value of {round(v, 4)}, macd_signal of {round(s, 4)} "
                f"and macd_hist of {round(h, 4)} on {last_date}.")

    def fetch_percent_b(self, time_period: int = 20):
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close_arr = data['Close'].astype(float).to_numpy().flatten()
        upper, middle, lower = talib.BBANDS(close_arr, timeperiod=tp, nbdevup=2.0, nbdevdn=2.0, matype=0)
        c = close_arr[-1]
        u, l = upper[-1], lower[-1]
        percent_b_value = (c - l) / (u - l)
        last_date = self._get_latest_date()
        return (f"PERCENT_B with time_period of {tp} days, sd of 2.0 and ma_type sma "
                f"has a value of {round(percent_b_value, 4)} on {last_date}.")

    def fetch_rsi(self, time_period: int = 14):
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        close = data['Close'].astype(float).to_numpy().flatten()
        rsi = talib.RSI(close, timeperiod=tp)
        value = rsi[-1]
        last_date = self._get_latest_date()
        return f"RSI with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_sma(self, time_period: int = 20):
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close = data['Close'].astype(float).to_numpy().flatten()
        sma = talib.SMA(close, timeperiod=tp)
        value = sma[-1]
        last_date = self._get_latest_date()
        return f"SMA with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_stoch(self, fast_k_period: int = 14, slow_k_period: int = 3, slow_d_period: int = 3):
        data = self._get_data()
        fk = fast_k_period if fast_k_period is not None else 14
        sk = slow_k_period if slow_k_period is not None else 3
        sd = slow_d_period if slow_d_period is not None else 3

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=fk, slowk_period=sk, slowk_matype=0, slowd_period=sd, slowd_matype=0)
        k_val, d_val = slowk[-1], slowd[-1]
        last_date = self._get_latest_date()
        return (f"STOCH with fast_k_period {fk}, slow_k_period {sk} and slow_d_period {sd} "
                f"has slow_k value of {round(k_val, 4)} and slow_d value of {round(d_val, 4)} on {last_date}.")

    def fetch_cci(self, time_period: int = 20):
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        cci = talib.CCI(high, low, close, timeperiod=tp)
        value = cci[-1]
        last_date = self._get_latest_date()
        return f"CCI with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_sar(self):
        data = self._get_data()

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
        value = sar[-1]
        last_date = self._get_latest_date()
        return f"SAR has a value of {round(value, 4)} on {last_date}."

    def fetch_stochrsi(self, rsi_length: int = 14, stoch_length: int = 14, k_period: int = 3, d_period: int = 3):
        data = self._get_data()
        rl = rsi_length if rsi_length is not None else 14
        sl = stoch_length if stoch_length is not None else 14
        kp = k_period if k_period is not None else 3
        dp = d_period if d_period is not None else 3

        close = data['Close'].astype(float).to_numpy().flatten()
        fastk, fastd = talib.STOCHRSI(close, timeperiod=rl, fastk_period=kp, fastd_period=dp, fastd_matype=0)
        k_val, d_val = fastk[-1], fastd[-1]
        last_date = self._get_latest_date()
        return (f"STOCHRSI with rsi_length {rl}, stoch_length {sl}, "
                f"k_period {kp} and d_period {dp} has values of k: {round(k_val, 4)} and d: {round(d_val, 4)} on {last_date}.")

    def fetch_ichimoku(self, tenkan_period: int = 9, kijun_period: int = 26, senkou_span_b_period: int = 52):
        data = self._get_data(period="12mo")
        tp = tenkan_period if tenkan_period is not None else 9
        kp = kijun_period if kijun_period is not None else 26
        sb = senkou_span_b_period if senkou_span_b_period is not None else 52

        high = data['High'].astype(float)
        low = data['Low'].astype(float)
        close = data['Close'].astype(float)
        conv_line = (high.rolling(tp).max() + low.rolling(tp).min()) / 2
        base_line = (high.rolling(kp).max() + low.rolling(kp).min()) / 2
        senkou_a = ((conv_line + base_line) / 2).shift(kp)
        senkou_b = ((high.rolling(sb).max() + low.rolling(sb).min()) / 2).shift(kp)
        if len(senkou_a) < kp + 1 or len(senkou_b) < kp + 1:
            print(f"Not enough data for Ichimoku calculation with current periods for {self.symbol}")
            sys.exit(1)
        spanA = senkou_a.iloc[-1]
        spanB = senkou_b.iloc[-1]
        last_date = self._get_latest_date()
        return (f"ICHIMOKU with conversion_line_period {tp}, base_line_period {kp}, "
                f"leading_span_b_period {sb}, lagging_span_period 26 has "
                f"senkou_span_a of {round(spanA, 4)}, senkou_span_b of {round(spanB, 4)} on {last_date}.")

    def fetch_mfi(self, time_period: int = 14):
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        volume = data['Volume'].astype(float).to_numpy().flatten()
        mfi = talib.MFI(high, low, close, volume, timeperiod=tp)
        value = mfi[-1]
        last_date = self._get_latest_date()
        return f"MFI with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_obv(self):
        data = self._get_data()

        close = data['Close'].astype(float).to_numpy().flatten()
        volume = data['Volume'].astype(float).to_numpy().flatten()
        obv = talib.OBV(close, volume)
        value = obv[-1]
        last_date = self._get_latest_date()
        return f"OBV has a value of {round(float(value), 4)} on {last_date}."

    def fetch_mom(self, time_period: int = 10):
        data = self._get_data()
        tp = time_period if time_period is not None else 10

        close = data['Close'].astype(float).to_numpy().flatten()
        mom = talib.MOM(close, timeperiod=tp)
        value = mom[-1]
        last_date = self._get_latest_date()
        return f"MOM with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_willr(self, time_period: int = 14):
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        willr = talib.WILLR(high, low, close, timeperiod=tp)
        value = willr[-1]
        last_date = self._get_latest_date()
        return f"WILLR with time_period of {tp} days has a value of {round(value, 4)} on {last_date}."

    def fetch_historical_prices(self, days: int = 30):
        """
        Fetch historical price data for the symbol.
        
        Args:
            days (int): Number of days of historical data to retrieve
            
        Returns:
            pd.DataFrame: DataFrame with historical price data
        """
        data = self._get_data()
        
        # Get the last 'days' entries
        historical_data = data.tail(days).copy()
        
        # Calculate daily percentage change
        historical_data['pct_change'] = historical_data['Close'].pct_change() * 100
        
        # Sort by date descending (most recent first)
        historical_data = historical_data.sort_index(ascending=False)
        
        return historical_data
    
    def fetch_historical_adx(self, time_period: int = 14, days: int = 30):
        """Fetch historical ADX values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        adx = talib.ADX(high, low, close, timeperiod=tp)
        
        # Create DataFrame with dates and ADX values
        df = pd.DataFrame({
            'date': data.index,
            'value': adx
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_bbands(self, time_period: int = 20, days: int = 30):
        """Fetch historical Bollinger Bands values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close = data['Close'].astype(float).to_numpy().flatten()
        upper, middle, lower = talib.BBANDS(close, timeperiod=tp, nbdevup=2.0, nbdevdn=2.0, matype=0)
        
        # Create DataFrame with dates and BBANDS values (using middle band as main value)
        df = pd.DataFrame({
            'date': data.index,
            'value': middle,
            'upper': upper,
            'lower': lower
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_ema(self, time_period: int = 9, days: int = 30):
        """Fetch historical EMA values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 9

        close = data['Close'].astype(float).to_numpy().flatten()
        ema = talib.EMA(close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': ema
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_macd(self, macd_fast_period: int = 12, macd_slow_period: int = 26, days: int = 30):
        """Fetch historical MACD values"""
        data = self._get_data()
        fp = macd_fast_period if macd_fast_period is not None else 12
        sp = macd_slow_period if macd_slow_period is not None else 26
        sig = 9

        close = data['Close'].astype(float).to_numpy().flatten()
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=fp, slowperiod=sp, signalperiod=sig)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': macd,
            'signal': macdsignal,
            'hist': macdhist
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, fp, sp, sig

    def fetch_historical_percent_b(self, time_period: int = 20, days: int = 30):
        """Fetch historical Percent B values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close_arr = data['Close'].astype(float).to_numpy().flatten()
        upper, middle, lower = talib.BBANDS(close_arr, timeperiod=tp, nbdevup=2.0, nbdevdn=2.0, matype=0)
        
        percent_b_values = (close_arr - lower) / (upper - lower)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': percent_b_values
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_rsi(self, time_period: int = 14, days: int = 30):
        """Fetch historical RSI values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        close = data['Close'].astype(float).to_numpy().flatten()
        rsi = talib.RSI(close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': rsi
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_sma(self, time_period: int = 20, days: int = 30):
        """Fetch historical SMA values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        close = data['Close'].astype(float).to_numpy().flatten()
        sma = talib.SMA(close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': sma
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_stoch(self, fast_k_period: int = 14, slow_k_period: int = 3, slow_d_period: int = 3, days: int = 30):
        """Fetch historical Stochastic values"""
        data = self._get_data()
        fk = fast_k_period if fast_k_period is not None else 14
        sk = slow_k_period if slow_k_period is not None else 3
        sd = slow_d_period if slow_d_period is not None else 3

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=fk, slowk_period=sk, slowk_matype=0, slowd_period=sd, slowd_matype=0)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': slowk,
            'slowd': slowd
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, fk, sk, sd

    def fetch_historical_cci(self, time_period: int = 20, days: int = 30):
        """Fetch historical CCI values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 20

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        cci = talib.CCI(high, low, close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': cci
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_sar(self, days: int = 30):
        """Fetch historical SAR values"""
        data = self._get_data()

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': sar
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df

    def fetch_historical_stochrsi(self, rsi_length: int = 14, stoch_length: int = 14, k_period: int = 3, d_period: int = 3, days: int = 30):
        """Fetch historical StochRSI values"""
        data = self._get_data()
        rl = rsi_length if rsi_length is not None else 14
        sl = stoch_length if stoch_length is not None else 14
        kp = k_period if k_period is not None else 3
        dp = d_period if d_period is not None else 3

        close = data['Close'].astype(float).to_numpy().flatten()
        fastk, fastd = talib.STOCHRSI(close, timeperiod=rl, fastk_period=kp, fastd_period=dp, fastd_matype=0)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': fastk,
            'fastd': fastd
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, rl, sl, kp, dp

    def fetch_historical_ichimoku(self, tenkan_period: int = 9, kijun_period: int = 26, senkou_span_b_period: int = 52, days: int = 30):
        """Fetch historical Ichimoku values"""
        data = self._get_data(period="12mo")
        tp = tenkan_period if tenkan_period is not None else 9
        kp = kijun_period if kijun_period is not None else 26
        sb = senkou_span_b_period if senkou_span_b_period is not None else 52

        high = data['High'].astype(float)
        low = data['Low'].astype(float)
        close = data['Close'].astype(float)
        conv_line = (high.rolling(tp).max() + low.rolling(tp).min()) / 2
        base_line = (high.rolling(kp).max() + low.rolling(kp).min()) / 2
        senkou_a = ((conv_line + base_line) / 2).shift(kp)
        senkou_b = ((high.rolling(sb).max() + low.rolling(sb).min()) / 2).shift(kp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': senkou_a,
            'senkou_b': senkou_b
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp, kp, sb

    def fetch_historical_mfi(self, time_period: int = 14, days: int = 30):
        """Fetch historical MFI values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        volume = data['Volume'].astype(float).to_numpy().flatten()
        mfi = talib.MFI(high, low, close, volume, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': mfi
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_obv(self, days: int = 30):
        """Fetch historical OBV values"""
        data = self._get_data()

        close = data['Close'].astype(float).to_numpy().flatten()
        volume = data['Volume'].astype(float).to_numpy().flatten()
        obv = talib.OBV(close, volume)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': obv
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df

    def fetch_historical_mom(self, time_period: int = 10, days: int = 30):
        """Fetch historical Momentum values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 10

        close = data['Close'].astype(float).to_numpy().flatten()
        mom = talib.MOM(close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': mom
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def fetch_historical_willr(self, time_period: int = 14, days: int = 30):
        """Fetch historical Williams %R values"""
        data = self._get_data()
        tp = time_period if time_period is not None else 14

        high = data['High'].astype(float).to_numpy().flatten()
        low = data['Low'].astype(float).to_numpy().flatten()
        close = data['Close'].astype(float).to_numpy().flatten()
        willr = talib.WILLR(high, low, close, timeperiod=tp)
        
        df = pd.DataFrame({
            'date': data.index,
            'value': willr
        })
        df.set_index('date', inplace=True)
        df = df.dropna()
        df = df.tail(days)
        df['pct_change'] = df['value'].pct_change() * 100
        df = df.sort_index(ascending=False)
        
        return df, tp

    def _format_historical_data(self, df, indicator_name, params_str, days):
        """
        Format historical data similar to VIX format.
        
        Args:
            df (pd.DataFrame): DataFrame with historical data
            indicator_name (str): Name of the indicator
            params_str (str): String describing the parameters
            days (int): Number of days requested
            
        Returns:
            str: Formatted historical data
        """
        actual_days = len(df)
        result = ""
        
        if actual_days < days:
            result = f"WARNING: Only {actual_days} days of {indicator_name} data available instead of requested {days} days.\n\n"
        
        result += f"{indicator_name} {params_str} values for the last {actual_days} days:\n"
        
        # Sort by date ascending for display
        df_sorted = df.sort_index(ascending=True)
        latest_date = df.index[0].strftime('%Y-%m-%d') if len(df) > 0 else ""
        
        for date, row in df_sorted.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            value = "No data available" if pd.isna(row['value']) else round(float(row['value']), 4)
            
            if date_str == latest_date:
                result += f"* {date_str}: {value} (LATEST {indicator_name.upper()} VALUE)\n"
            else:
                result += f"* {date_str}: {value}\n"
        
        return result

    def _format_price_historical_data(self, df, symbol, days):
        """
        Format historical price data similar to VIX format.
        
        Args:
            df (pd.DataFrame): DataFrame with historical price data
            symbol (str): Symbol name
            days (int): Number of days requested
            
        Returns:
            str: Formatted historical price data
        """
        actual_days = len(df)
        result = ""
        
        if actual_days < days:
            result = f"WARNING: Only {actual_days} days of {symbol} price data available instead of requested {days} days.\n\n"
        
        result += f"{symbol} closing price values for the last {actual_days} days:\n"
        
        # Sort by date ascending for display
        df_sorted = df.sort_index(ascending=True)
        latest_date = df.index[0].strftime('%Y-%m-%d') if len(df) > 0 else ""
        
        for date, row in df_sorted.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            value = "No data available" if pd.isna(row['Close']) else round(float(row['Close']), 4)
            
            if date_str == latest_date:
                daily_change = row['pct_change'] if not pd.isna(row['pct_change']) else "N/A"
                daily_change_str = f"{daily_change:.2f}%" if isinstance(daily_change, (int, float)) else daily_change
                result += f"* {date_str}: {value} (LATEST PRICE VALUE, Daily change from previous day: {daily_change_str})\n"
            else:
                result += f"* {date_str}: {value}\n"
        
        return result

    def _get_quote_data(self):
        # Use the centralized data manager
        self._quote_data = twelve_data_manager.get_quote_data(self.symbol)
        return self._quote_data



    def fetch_quote(self):
        data = self._get_quote_data()
        
        # Parse the current date and calculate previous day
        current_date = datetime.strptime(data['datetime'], '%Y-%m-%d')
        previous_day = current_date - timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        
        return (f"Quote Summary for {data['symbol']} - {data['name']}:"
                f"\n• Exchange: {data['exchange']} ({data['mic_code']})"
                f"\n• Currency: {data['currency']}"
                f"\n\nDaily Statistics on {previous_day_str} :"
                f"\n• Open: {data['open']}"
                f"\n• High: {data['high']}"
                f"\n• Low: {data['low']}"
                f"\n• Close: {data['close']}"
                f"\n• Previous Close: {data['previous_close']}"
                f"\n• Change: {data['change']} ({data['percent_change']}%)"
                f"\n\nVolume Information:"
                f"\n• Current Volume: {data['volume']}"
                f"\n• Average Volume: {data['average_volume']}"
                f"\n\n52-Week Performance:"
                f"\n• Low: {data['fifty_two_week']['low']}"
                f"\n• High: {data['fifty_two_week']['high']}"
                f"\n• Low Change: {data['fifty_two_week']['low_change']} ({data['fifty_two_week']['low_change_percent']}%)"
                f"\n• High Change: {data['fifty_two_week']['high_change']} ({data['fifty_two_week']['high_change_percent']}%)"
                f"\n• Range: {data['fifty_two_week']['range']}")

    def fetch_current_price(self):
        data = self._get_quote_data()
   
        price = data["close"]
        company_name = data["name"]
        return f'The current price for {company_name} is {price}'

    def fetch_all(
        self,
        adx_time_period: int = None,
        bbands_time_period: int = None,
        ema_time_period: int = None,
        macd_fast_period: int = None,
        macd_slow_period: int = None,
        percent_b_time_period: int = None,
        rsi_time_period: int = None,
        sma_time_period: int = None,
        stoch_fast_period: int = None,
        stoch_slow_period: int = None,
        stoch_d_period: int = None,
        cci_time_period: int = None,
        mom_time_period: int = None,
        willr_time_period: int = None,
        mfi_time_period: int = None,
        rsi_length: int = None,
        stoch_length: int = None,
        k_period: int = None,
        d_period: int = None,
        tenkan_period: int = None,
        kijun_period: int = None,
        senkou_span_b_period: int = None,
    ):
        # Get the latest date for technical indicators
        last_date = self._get_latest_date()
        
        # Create the technical indicators section header
        technical_indicators = f"\n\nTechnical Indicators as of {last_date}:"
        
        return {
            "price": self.fetch_current_price(),
            "quote": self.fetch_quote(),
            "technical_indicators": technical_indicators,
            "adx": self.fetch_adx(time_period=adx_time_period),
            "bbands": self.fetch_bbands(time_period=bbands_time_period),
            "ema": self.fetch_ema(time_period=ema_time_period),
            "macd": self.fetch_macd(macd_fast_period=macd_fast_period, macd_slow_period=macd_slow_period),
            "percent_b": self.fetch_percent_b(time_period=percent_b_time_period),
            "rsi": self.fetch_rsi(time_period=rsi_time_period),
            "sma": self.fetch_sma(time_period=sma_time_period),
            "stoch": self.fetch_stoch(fast_k_period=stoch_fast_period,
                                        slow_k_period=stoch_slow_period,
                                        slow_d_period=stoch_d_period),
            "cci": self.fetch_cci(time_period=cci_time_period),
            "sar": self.fetch_sar(),
            "stochrsi": self.fetch_stochrsi(rsi_length=rsi_length, stoch_length=stoch_length,
                                            k_period=k_period, d_period=d_period),
            "ichimoku": self.fetch_ichimoku(tenkan_period=tenkan_period, kijun_period=kijun_period,
                                            senkou_span_b_period=senkou_span_b_period),
            "mfi": self.fetch_mfi(time_period=mfi_time_period),
            "obv": self.fetch_obv(),
            "mom": self.fetch_mom(time_period=mom_time_period),
            "willr": self.fetch_willr(time_period=willr_time_period),
        }

    def fetch_company_name(self, exchange: str = "NASDAQ"):
        # Use the Quote endpoint from Twelve Data API (available in free tier)
        # The quote endpoint provides the company name and is available for all plans
        quote_data = self._get_quote_data()
        return quote_data.get("name", self.symbol)


def get_ti_context(symbol: str, indicator_params: dict = settings.TECHNICAL_INDICATOR_DEFAULTS, interval: str = "1day", days: int = 30) -> str:
    ti = TwelveTI(symbol, interval)
    result = ti.fetch_all(**indicator_params)
    
    # Get specific fields for formatting
    price = result.pop("price")
    quote = result.pop("quote")
    technical_indicators = result.pop("technical_indicators", None)
    
    # Format the main sections
    formatted_output = f"{price}\n{quote}"
    
    # Add the technical indicators section if available
    if technical_indicators:
        formatted_output += f"{technical_indicators}"
    
    # Format the remaining individual indicators as bullet points
    bullet_points = []
    for key, value in result.items():
        bullet_points.append(f"• {key}: {value}")
    
    # Add historical data section
    formatted_output += "\n\n" + "="*50 + "\nHISTORICAL DATA\n" + "="*50 + "\n\n"
    
    # Add historical price data
    historical_prices = ti.fetch_historical_prices(days)
    price_history = ti._format_price_historical_data(historical_prices, symbol, days)
    formatted_output += price_history + "\n\n"
    
    # Add historical technical indicators
    # ADX
    adx_data, adx_tp = ti.fetch_historical_adx(
        time_period=indicator_params.get('adx_time_period', 14), 
        days=days
    )
    adx_history = ti._format_historical_data(
        adx_data, "ADX", f"with time_period of {adx_tp} days", days
    )
    formatted_output += adx_history + "\n\n"
    
    # BBANDS (using middle band)
    bbands_data, bbands_tp = ti.fetch_historical_bbands(
        time_period=indicator_params.get('bbands_time_period', 20), 
        days=days
    )
    bbands_history = ti._format_historical_data(
        bbands_data, "BBANDS (Middle Band)", f"with time_period of {bbands_tp} days", days
    )
    formatted_output += bbands_history + "\n\n"
    
    # EMA
    ema_data, ema_tp = ti.fetch_historical_ema(
        time_period=indicator_params.get('ema_time_period', 9), 
        days=days
    )
    ema_history = ti._format_historical_data(
        ema_data, "EMA", f"with time_period of {ema_tp} days", days
    )
    formatted_output += ema_history + "\n\n"
    
    # MACD
    macd_data, macd_fp, macd_sp, macd_sig = ti.fetch_historical_macd(
        macd_fast_period=indicator_params.get('macd_fast_period', 12),
        macd_slow_period=indicator_params.get('macd_slow_period', 26),
        days=days
    )
    macd_history = ti._format_historical_data(
        macd_data, "MACD", f"with fast_period {macd_fp}, slow_period {macd_sp} and signal_period {macd_sig}", days
    )
    formatted_output += macd_history + "\n\n"
    
    # RSI
    rsi_data, rsi_tp = ti.fetch_historical_rsi(
        time_period=indicator_params.get('rsi_time_period', 14), 
        days=days
    )
    rsi_history = ti._format_historical_data(
        rsi_data, "RSI", f"with time_period of {rsi_tp} days", days
    )
    formatted_output += rsi_history + "\n\n"
    
    # SMA
    sma_data, sma_tp = ti.fetch_historical_sma(
        time_period=indicator_params.get('sma_time_period', 20), 
        days=days
    )
    sma_history = ti._format_historical_data(
        sma_data, "SMA", f"with time_period of {sma_tp} days", days
    )
    formatted_output += sma_history + "\n\n"
    
    # CCI
    cci_data, cci_tp = ti.fetch_historical_cci(
        time_period=indicator_params.get('cci_time_period', 20), 
        days=days
    )
    cci_history = ti._format_historical_data(
        cci_data, "CCI", f"with time_period of {cci_tp} days", days
    )
    formatted_output += cci_history + "\n\n"
    
    # MFI
    mfi_data, mfi_tp = ti.fetch_historical_mfi(
        time_period=indicator_params.get('mfi_time_period', 14), 
        days=days
    )
    mfi_history = ti._format_historical_data(
        mfi_data, "MFI", f"with time_period of {mfi_tp} days", days
    )
    formatted_output += mfi_history + "\n\n"
    
    # Return the current indicators as bullet points followed by historical data
    if bullet_points:
        return formatted_output.replace(technical_indicators + "\n", technical_indicators + "\n" + "\n".join(bullet_points) + "\n")
    return formatted_output


