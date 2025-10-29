import datetime
from datetime import date, timedelta
import pytz

def get_current_est_date() -> date:
    est = pytz.timezone('US/Eastern')
    return datetime.datetime.now(est).date()

def get_today_str() -> str:
    est = pytz.timezone('US/Eastern')
    return datetime.datetime.now(est).strftime("%Y-%m-%d %H:%M")

def get_today_str_no_min() -> str:
    """Get today's date without the time part"""
    today = get_today_str()
    return today.split(' ')[0]

def get_yesterday_str() -> str:
    yesterday = get_current_est_date() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_yesterday_18_est() -> datetime.datetime:
    est = pytz.timezone('US/Eastern')
    yesterday_date = get_current_est_date() - timedelta(days=1)
    yesterday_18 = datetime.datetime.combine(yesterday_date, datetime.time(18, 0, 0))
    return est.localize(yesterday_18) 