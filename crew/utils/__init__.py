from crew.utils.checks import ValidationChecks
from crew.utils.company_info import get_company_name
from crew.utils.dates import (
    get_today_str,
    get_yesterday_18_est,
    get_yesterday_str,
)


# Avoid circular imports by importing stock_headlines_fetcher lazily
def fetch_stock_news(*args, **kwargs):
    from crew.analysts.stock_headlines_fetcher import (
        fetch_stock_news as _fetch_stock_news,
    )

    return _fetch_stock_news(*args, **kwargs)


def NewsItem(*args, **kwargs):
    from crew.analysts.stock_headlines_fetcher import NewsItem as _NewsItem

    return _NewsItem(*args, **kwargs)


__all__ = [
    "get_today_str",
    "get_yesterday_str",
    "get_yesterday_18_est",
    "ValidationChecks",
    "get_company_name",
    "fetch_stock_news",
    "NewsItem",
]
