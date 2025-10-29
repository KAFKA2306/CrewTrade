"""
Utility functions for company information.
Separate from technical_indicators to avoid circular imports.
"""

from ai_trading_crew.utils.twelve_data_manager import twelve_data_manager


def get_company_name(symbol: str, exchange: str = "NASDAQ") -> str:
    """
    Get company name for a given symbol using the centralized TwelveData manager with caching.
    
    Args:
        symbol (str): Stock symbol
        exchange (str): Exchange name (default: NASDAQ)
        
    Returns:
        str: Company name or symbol if name not found
    """
    try:
        return twelve_data_manager.get_company_name(symbol)
    except Exception:
        return symbol 