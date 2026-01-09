def get_company_name(symbol: str, exchange: str = "NASDAQ") -> str:
    """
    Get company name (Fallback to symbol to avoid API usage).
    """
    return symbol
