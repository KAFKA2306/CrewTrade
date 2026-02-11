import re
import requests
from bs4 import BeautifulSoup
def get_fundamental_context(symbol: str) -> str:
    """
    Get formatted fundamental analysis context for a stock symbol from Finviz, TipRanks, and ValueInvesting.io.
    Args:
        symbol (str): Stock symbol
    Returns:
        str: Four sections - Finviz fundamental data, TipRanks AI analysis, TipRanks Analyst Forecast, and ValueInvesting.io Intrinsic Value
    """
    finviz_result = _get_finviz_data(symbol)
    tipranks_result = _get_tipranks_data(symbol)
    forecast_result = _get_tipranks_forecast(symbol)
    value_result = _get_valueinvesting_data(symbol)
    return f"{finviz_result}\n\n{'=' * 80}\n\n{tipranks_result}\n\n{'=' * 80}\n\n{forecast_result}\n\n{'=' * 80}\n\n{value_result}"
def _get_finviz_data(symbol: str) -> str:
    """Get fundamental data from Finviz"""
    url = f"https://finviz.com/quote.ashx?t={symbol}&p=d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://www.google.com/",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        company_name = symbol
        try:
            title_element = soup.find("title")
            if title_element and title_element.text:
                title_text = title_element.text
                if " - " in title_text:
                    parts = title_text.split(" - ")
                    if len(parts) > 1:
                        company_part = parts[1].replace(" Stock Quote", "").strip()
                        if company_part:
                            company_name = company_part
        except Exception:
            pass
        fundamentals = {}
        tables = soup.find_all("table")
        for table in tables:
            table_text = table.get_text()
            if (
                "P/E" in table_text
                and "Market Cap" in table_text
                and "ROA" in table_text
            ):
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    for i in range(0, len(cells), 2):
                        if i + 1 < len(cells):
                            label = cells[i].get_text(strip=True)
                            value = cells[i + 1].get_text(strip=True)
                            full_name = label
                            data_boxover = cells[i].get("data-boxover", "")
                            if "body=[" in data_boxover:
                                try:
                                    if body_matches := re.findall(
                                        r"body=\[([^\]]+)\]", data_boxover
                                    ):
                                        extracted_name = body_matches[
                                            -1
                                        ]
                                        if (
                                            extracted_name
                                            and not extracted_name.startswith(
                                                "tooltip_"
                                            )
                                            and len(extracted_name) > len(label)
                                        ):
                                            full_name = extracted_name
                                except Exception:
                                    pass
                            if (
                                label
                                and value
                                and label != value
                                and not label.startswith("http")
                                and not value.startswith("http")
                                and len(label) <= 30
                                and len(value) <= 50
                                and value not in ["-", "", "N/A"]
                                and
                                label
                                in [
                                    "Index",
                                    "P/E",
                                    "P/S",
                                    "P/B",
                                    "P/C",
                                    "P/FCF",
                                    "ROA",
                                    "ROE",
                                    "ROI",
                                    "EPS (ttm)",
                                    "EPS next Y",
                                    "EPS next Q",
                                    "Market Cap",
                                    "Income",
                                    "Sales",
                                    "Book/sh",
                                    "Cash/sh",
                                    "Forward P/E",
                                    "PEG",
                                    "Quick Ratio",
                                    "Current Ratio",
                                    "Debt/Eq",
                                    "LT Debt/Eq",
                                    "Gross Margin",
                                    "Oper. Margin",
                                    "Profit Margin",
                                    "Insider Own",
                                    "Inst Own",
                                    "Short Float",
                                    "Short Ratio",
                                    "Short Interest",
                                    "Shs Outstand",
                                    "Shs Float",
                                    "Perf Week",
                                    "Perf Month",
                                    "Perf Quarter",
                                    "Perf Half Y",
                                    "Perf Year",
                                    "Perf YTD",
                                    "52W Range",
                                    "52W High",
                                    "52W Low",
                                    "Beta",
                                    "ATR (14)",
                                    "RSI (14)",
                                    "Volatility",
                                    "Recom",
                                    "Target Price",
                                    "Rel Volume",
                                    "Prev Close",
                                    "Avg Volume",
                                    "Price",
                                    "Volume",
                                    "Change",
                                    "SMA20",
                                    "SMA50",
                                    "SMA200",
                                    "Dividend Est.",
                                    "Dividend TTM",
                                    "Dividend Ex-Date",
                                    "Employees",
                                    "Option/Short",
                                    "EPS this Y",
                                    "EPS next 5Y",
                                    "EPS past 5Y",
                                    "EPS Y/Y TTM",
                                    "EPS Q/Q",
                                    "Sales past 5Y",
                                    "Sales Y/Y TTM",
                                    "Sales Q/Q",
                                    "EPS Surprise",
                                    "Sales Surprise",
                                    "Insider Trans",
                                    "Inst Trans",
                                    "Payout",
                                    "Earnings",
                                ]
                                and
                                not any(
                                    exclude in label.lower()
                                    for exclude in [
                                        "analyst",
                                        "officer",
                                        "director",
                                        "ceo",
                                        "cfo",
                                        "chris",
                                        "kevan",
                                        "timothy",
                                        "katherine",
                                        "arthur",
                                        "williams",
                                        "maestri",
                                        "cowen",
                                        "rosenblatt",
                                        "jefferies",
                                        "barclays",
                                        "morgan",
                                        "china",
                                        "upgrade",
                                        "downgrade",
                                        "reiterated",
                                        "buy",
                                        "sell",
                                        "hold",
                                        "neutral",
                                        "sec",
                                        "sale",
                                        "purchase",
                                        "transaction",
                                    ]
                                )
                                and not any(
                                    exclude in value.lower()
                                    for exclude in [
                                        "analyst",
                                        "officer",
                                        "director",
                                        "ceo",
                                        "cfo",
                                        "buy",
                                        "sell",
                                        "hold",
                                        "neutral",
                                        "upgrade",
                                        "downgrade",
                                        "reiterated",
                                        "outperform",
                                        "underperform",
                                        "overweight",
                                        "underweight",
                                    ]
                                )
                            ):
                                fundamentals[label] = {
                                    "value": value,
                                    "full_name": full_name,
                                }
                break
        if not fundamentals:
            return f"No fundamental data found for {company_name} ({symbol})"
        result = f"FINVIZ Fundamental Ratios/KPIs for {company_name} ({symbol}):\n\n"
        bullet_points = []
        for label, data in fundamentals.items():
            full_name = data["full_name"]
            value = data["value"]
            bullet_points.append(f"• {full_name}: {value}")
        if bullet_points:
            result += "\n".join(bullet_points)
        else:
            result += "No fundamental data found in the expected format."
        return result
    except Exception as e:
        return (
            f"Error fetching fundamental data for {company_name} ({symbol}): {str(e)}"
        )
def _get_tipranks_data(symbol: str) -> str:
    """Get AI stock analysis from TipRanks"""
    url = f"https://www.tipranks.com/stocks/{symbol.lower()}/stock-analysis"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://www.google.com/",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        full_text = soup.get_text()
        result = f"TipRanks AI Stock Analysis (Fundamental) for {symbol.upper()}:\n\n"
        factors_section = _extract_factors_info(full_text)
        result += factors_section + "\n\n"
        financial_section = _extract_financial_info(full_text)
        result += financial_section
        return result
    except Exception as e:
        return f"Error fetching TipRanks data for {symbol}: {str(e)}"
def _extract_rating_info(text, symbol):
    """Extract rating, performance, price target and explanation"""
    result = f"**{symbol.upper()} Rating Information:**\n"
    rating_matches = re.findall(r"Rating.*?(\d{1,2})", text, re.IGNORECASE)
    if rating_matches:
        rating = rating_matches[0]
        if 1 <= int(rating) <= 100:
            result += f"• **Rating Score**: {rating}\n"
    performance_words = [
        "Outperform",
        "Underperform",
        "Buy",
        "Hold",
        "Sell",
        "Strong Buy",
        "Moderate Buy",
    ]
    for word in performance_words:
        if word in text:
            result += f"• **Performance Assessment**: {word}\n"
            break
    price_matches = re.findall(r"Price Target.*?\$(\d+\.?\d*)", text, re.IGNORECASE)
    if price_matches:
        result += f"• **Price Target**: ${price_matches[0]}\n"
    upside_matches = re.findall(r"(\d+\.?\d*%)\s*(?:Upside)", text, re.IGNORECASE)
    if upside_matches:
        result += f"• **Upside**: {upside_matches[0]}\n"
    analysis_keywords = [
        "overall score",
        "primarily driven",
        "financial performance",
        "strong performance",
    ]
    for keyword in analysis_keywords:
        pattern = rf"([^.]*{keyword}[^.]*\.)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            clean_match = re.sub(r"\s+", " ", matches[0]).strip()
            result += f"• **Analysis**: {clean_match}\n"
            break
    return result
def _extract_factors_info(text):
    """Extract positive and negative factors"""
    result = "**Investment Factors:**\n"
    pos_start = text.find("Positive Factors")
    neg_start = text.find("Negative Factors")
    if pos_start != -1:
        result += "\n**Positive Factors:**\n"
        if neg_start != -1:
            pos_section = text[pos_start:neg_start]
        else:
            pos_section = text[pos_start : pos_start + 2000]
        lines = pos_section.split("\n")
        current_factor = ""
        found_factors = []
        for i, line in enumerate(lines[1:], 1):
            line = line.strip()
            if not line:
                continue
            if (
                len(line) < 100
                and not line.startswith("•")
                and not line.lower().startswith("negative")
                and line[0].isupper()
                and any(
                    word in line
                    for word in [
                        "Innovation",
                        "Performance",
                        "Growth",
                        "Technology",
                        "Product",
                        "Market",
                        "Strategy",
                        "Advancement",
                    ]
                )
            ):
                current_factor = line
                for j in range(i + 1, min(i + 3, len(lines))):
                    if j < len(lines):
                        desc_line = lines[j].strip()
                        if len(desc_line) > 30 and not desc_line[0].isupper():
                            found_factors.append(f"• **{current_factor}**: {desc_line}")
                            break
                        elif len(desc_line) > 30:
                            found_factors.append(f"• **{current_factor}**: {desc_line}")
                            break
        if not found_factors:
            factor_text = pos_section.replace("Positive Factors", "").strip()
            if len(factor_text) > 50:
                sentences = factor_text.split(".")
                for sentence in sentences[:3]:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and not sentence.lower().startswith(
                        "negative"
                    ):
                        found_factors.append(f"• {sentence}.")
        if found_factors:
            for factor in found_factors:
                result += f"{factor}\n"
        else:
            result += "• Positive factors information not available in current format\n"
    if neg_start != -1:
        result += "\n**Negative Factors:**\n"
        fin_start = text.find("Financial Statement", neg_start)
        if fin_start != -1:
            neg_section = text[neg_start:fin_start]
        else:
            neg_section = text[neg_start : neg_start + 2000]
        lines = neg_section.split("\n")
        current_factor = ""
        found_factors = []
        for i, line in enumerate(lines[1:], 1):
            line = line.strip()
            if not line:
                continue
            if (
                len(line) < 100
                and not line.startswith("•")
                and not line.lower().startswith("financial")
                and line[0].isupper()
                and any(
                    word in line
                    for word in [
                        "Competition",
                        "Performance",
                        "Risk",
                        "Challenge",
                        "Decline",
                        "Pressure",
                        "Policy",
                        "Tariff",
                        "Market",
                    ]
                )
            ):
                current_factor = line
                for j in range(i + 1, min(i + 3, len(lines))):
                    if j < len(lines):
                        desc_line = lines[j].strip()
                        if len(desc_line) > 30 and not desc_line[0].isupper():
                            found_factors.append(f"• **{current_factor}**: {desc_line}")
                            break
                        elif len(desc_line) > 30:
                            found_factors.append(f"• **{current_factor}**: {desc_line}")
                            break
        if not found_factors:
            factor_text = neg_section.replace("Negative Factors", "").strip()
            if len(factor_text) > 50:
                sentences = factor_text.split(".")
                for sentence in sentences[:3]:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and not sentence.lower().startswith(
                        "financial"
                    ):
                        found_factors.append(f"• {sentence}.")
        if found_factors:
            for factor in found_factors:
                result += f"{factor}\n"
        else:
            result += "• Negative factors information not available in current format\n"
    return result
def _extract_financial_info(text):
    """Extract financial statement overview"""
    result = "**Financial Statement Overview:**\n"
    fin_start = text.find("Financial Statement Overview")
    if fin_start == -1:
        return "Financial statement overview not found"
    summary_start = text.find("Summary", fin_start)
    if summary_start != -1:
        summary_end = text.find("Income Statement", summary_start)
        if summary_end != -1:
            summary_text = text[
                summary_start + 7 : summary_end
            ].strip()
            if len(summary_text) > 20:
                result += f"\n**Summary**: {summary_text}\n"
    income_start = text.find("Income Statement", fin_start)
    if income_start != -1:
        result += "\n**Income Statement:**\n"
        income_section = text[income_start : income_start + 500]
        score_match = re.search(
            r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
            income_section,
            re.IGNORECASE,
        )
        if score_match:
            score, sentiment = score_match.groups()
            result += f"• Score: {score}\n"
            result += f"• Sentiment: {sentiment}\n"
        desc_start = income_start + 200
        desc_end = text.find("Balance Sheet", desc_start)
        if desc_end != -1:
            description = text[desc_start:desc_end].strip()
            clean_desc = re.sub(
                r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
                "",
                description,
                flags=re.IGNORECASE,
            )
            clean_desc = clean_desc.strip()
            if len(clean_desc) > 30:
                result += f"• Analysis: {clean_desc[:300]}...\n"
    balance_start = text.find("Balance Sheet", fin_start)
    if balance_start != -1:
        result += "\n**Balance Sheet:**\n"
        balance_section = text[balance_start : balance_start + 500]
        score_match = re.search(
            r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
            balance_section,
            re.IGNORECASE,
        )
        if score_match:
            score, sentiment = score_match.groups()
            result += f"• Score: {score}\n"
            result += f"• Sentiment: {sentiment}\n"
        desc_start = balance_start + 200
        desc_end = text.find("Cash Flow", desc_start)
        if desc_end != -1:
            description = text[desc_start:desc_end].strip()
            clean_desc = re.sub(
                r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
                "",
                description,
                flags=re.IGNORECASE,
            )
            clean_desc = clean_desc.strip()
            if len(clean_desc) > 30:
                result += f"• Analysis: {clean_desc[:300]}...\n"
    cashflow_start = text.find("Cash Flow", fin_start)
    if cashflow_start != -1:
        result += "\n**Cash Flow:**\n"
        cashflow_section = text[cashflow_start : cashflow_start + 500]
        score_match = re.search(
            r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
            cashflow_section,
            re.IGNORECASE,
        )
        if score_match:
            score, sentiment = score_match.groups()
            result += f"• Score: {score}\n"
            result += f"• Sentiment: {sentiment}\n"
        desc_start = cashflow_start + 200
        description = text[desc_start : desc_start + 400].strip()
        clean_desc = re.sub(
            r"(\d{1,2})\s*(Very Positive|Positive|Neutral|Negative|Very Negative)",
            "",
            description,
            flags=re.IGNORECASE,
        )
        clean_desc = clean_desc.strip()
        if len(clean_desc) > 30:
            result += f"• Analysis: {clean_desc[:300]}...\n"
    return result
def _get_tipranks_forecast(symbol: str) -> str:
    """Get analyst ratings and price forecast from TipRanks forecast page"""
    url = f"https://www.tipranks.com/stocks/{symbol.lower()}/forecast"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        full_text = soup.get_text()
        result = f"TipRanks Analyst Ratings & Price Forecast for {symbol.upper()}:\n\n"
        ratings_section = _extract_analyst_ratings(full_text, symbol)
        result += ratings_section + "\n\n"
        forecast_section = _extract_price_forecast(full_text, symbol)
        result += forecast_section
        return result
    except Exception as e:
        return f"Error fetching TipRanks forecast data for {symbol}: {str(e)}"
def _extract_analyst_ratings(text, symbol):
    """Extract analyst ratings breakdown"""
    result = f"**{symbol.upper()} Analyst Ratings:**\n"
    overall_rating_patterns = [
        r"(Strong Buy|Strong Sell|Buy|Sell|Hold)\s*(\d+)\s*Ratings",
        r"(\d+)\s*Ratings\s*(Strong Buy|Strong Sell|Buy|Sell|Hold)",
        r"consensus.*?(Strong Buy|Strong Sell|Buy|Sell|Hold)",
        r"Strong Buy(\d+)Ratings",
    ]
    overall_rating = ""
    total_ratings = ""
    for pattern in overall_rating_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.group(1).isdigit():
                total_ratings = match.group(1)
                overall_rating = match.group(2)
            else:
                overall_rating = match.group(1)
                if len(match.groups()) > 1 and match.group(2).isdigit():
                    total_ratings = match.group(2)
            break
    if not overall_rating:
        consensus_patterns = [
            r"rating consensus.*?(Strong Buy|Buy|Hold|Sell|Strong Sell)",
            r"consensus rating.*?(Strong Buy|Buy|Hold|Sell|Strong Sell)",
        ]
        for pattern in consensus_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                overall_rating = match.group(1)
                break
    if overall_rating:
        result += f"• **Overall Rating**: {overall_rating}\n"
    if not total_ratings:
        total_patterns = [
            r"Based on (\d+) analysts",
            r"(\d+) Wall Street analysts",
            r"(\d+)\s*Ratings",
            r"(\d+) analysts giving stock ratings",
        ]
        for pattern in total_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                total_ratings = match.group(1)
                break
    if total_ratings:
        result += f"• **Total Ratings**: {total_ratings}\n"
    breakdown_patterns = [
        r"(\d+)\s*Buy\s*(\d+)\s*Hold\s*(\d+)\s*Sell",
        r"(\d+) buy ratings,?\s*(\d+) hold ratings,?\s*(\d+) sell ratings",
        r"(\d+) Buy\s*(\d+) Hold\s*(\d+) Sell",
        r"(\d+)\s*Buy(\d+)\s*Hold(\d+)\s*Sell",
    ]
    buy_count = hold_count = sell_count = ""
    for pattern in breakdown_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            buy_count, hold_count, sell_count = match.groups()
            break
    if not buy_count:
        buy_match = re.search(r"(\d+)\s*buy", text, re.IGNORECASE)
        if buy_match:
            buy_count = buy_match.group(1)
    if not hold_count:
        hold_match = re.search(r"(\d+)\s*hold", text, re.IGNORECASE)
        if hold_match:
            hold_count = hold_match.group(1)
    if not sell_count:
        sell_match = re.search(r"(\d+)\s*sell", text, re.IGNORECASE)
        if sell_match:
            sell_count = sell_match.group(1)
    if buy_count or hold_count or sell_count:
        result += "• **Ratings Breakdown**:\n"
        if buy_count:
            result += f"  - Buy: {buy_count}\n"
        if hold_count:
            result += f"  - Hold: {hold_count}\n"
        if sell_count:
            result += f"  - Sell: {sell_count}\n"
    time_patterns = [
        r"in the past (\d+ months?)",
        r"last (\d+ months?)",
        r"past (\d+ months?)",
    ]
    for pattern in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            time_period = match.group(1)
            result += f"• **Time Period**: {time_period}\n"
            break
    return result
def _extract_price_forecast(text, symbol):
    """Extract 12-month price forecast information"""
    result = f"**{symbol.upper()} Stock 12 Month Forecast:**\n"
    avg_price_patterns = [
        r"Average Price Target\s*\$(\d+\.?\d*)",
        r"average price target is \$(\d+\.?\d*)",
        r"\$(\d+\.?\d*)\s*▲.*?Upside",
        r"price target.*?\$(\d+\.?\d*)",
        r"Average Price Target\$(\d+\.?\d*)",
        r"target.*?\$(\d+\.\d+)",
    ]
    avg_price = ""
    for pattern in avg_price_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            avg_price = match.group(1)
            break
    if avg_price:
        result += f"• **Average Price Target**: ${avg_price}\n"
    upside_patterns = [
        r"(\d+\.?\d*)%\s*Upside",
        r"▲\(\s*(\d+\.?\d*)%\s*Upside\)",
        r"represents.*?(\d+\.?\d*)%.*?change",
    ]
    upside = ""
    for pattern in upside_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            upside = match.group(1)
            break
    if upside:
        result += f"• **Upside Potential**: {upside}%\n"
    high_patterns = [
        r"high forecast of \$(\d+\.?\d*)",
        r"Highest Price Target\s*\$(\d+\.?\d*)",
        r"high.*?\$(\d+\.?\d*)",
    ]
    high_price = ""
    for pattern in high_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            high_price = match.group(1)
            break
    if high_price:
        result += f"• **Highest Price Target**: ${high_price}\n"
    low_patterns = [
        r"low forecast of \$(\d+\.?\d*)",
        r"Lowest Price Target\s*\$(\d+\.?\d*)",
        r"low.*?\$(\d+\.?\d*)",
    ]
    low_price = ""
    for pattern in low_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            low_price = match.group(1)
            break
    if low_price:
        result += f"• **Lowest Price Target**: ${low_price}\n"
    current_patterns = [
        r"last price of \$(\d+\.?\d*)",
        r"current price of \$(\d+\.?\d*)",
        r"from.*?\$(\d+\.?\d*)",
    ]
    current_price = ""
    for pattern in current_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            current_price = match.group(1)
            break
    if current_price:
        result += f"• **Current Price**: ${current_price}\n"
    analyst_count_patterns = [
        r"Based on (\d+)\s+Wall Street analysts",
        r"(\d+) analysts offering.*?price targets",
        r"(\d+) Wall Street analysts.*?price targets",
    ]
    analyst_count = ""
    for pattern in analyst_count_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            analyst_count = match.group(1)
            break
    if analyst_count:
        result += f"• **Number of Analysts**: {analyst_count}\n"
    return result
def _get_valueinvesting_data(symbol: str) -> str:
    """Get intrinsic value analysis from ValueInvesting.io"""
    url = f"https://valueinvesting.io/{symbol}/valuation/intrinsic-value"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        full_text = soup.get_text()
        result = f"ValueInvesting.io Intrinsic Value Analysis for {symbol.upper()}:\n\n"
        overview_section = _extract_intrinsic_overview(full_text, symbol)
        result += overview_section + "\n\n"
        valuation_section = _extract_valuation_summary(full_text)
        result += valuation_section
        return result
    except Exception as e:
        return f"Error fetching ValueInvesting.io data for {symbol}: {str(e)}"
def _extract_intrinsic_overview(text, symbol):
    """Extract intrinsic value, upside, and valuation assessment"""
    result = f"**{symbol.upper()} Intrinsic Value Overview:**\n"
    intrinsic_patterns = [
        r"(\d+\.?\d*)\s*USD\s*Intrinsic Value",
        r"Intrinsic Value.*?(\d+\.?\d*)\s*USD",
        r"intrinsic value.*?(\d+\.?\d*)\s*USD",
        r"(\d+\.?\d*)\s*USD.*?Intrinsic",
    ]
    intrinsic_value = ""
    for pattern in intrinsic_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            intrinsic_value = match.group(1)
            break
    if intrinsic_value:
        result += f"• **Intrinsic Value**: {intrinsic_value} USD\n"
    upside_patterns = [
        r"(\d+\.?\d*)%\s*upside",
        r"upside.*?(\d+\.?\d*)%",
        r"(\d+\.?\d*)%\s*undervalued",
        r"(\d+\.?\d*)%\s*overvalued",
    ]
    upside = ""
    for pattern in upside_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            upside = match.group(1)
            break
    if upside:
        result += f"• **Upside**: {upside}%\n"
    assessment_patterns = [
        r"(undervalued|overvalued|fairly valued)",
        r"stock is (undervalued|overvalued|fairly valued)",
        r"appears to be (undervalued|overvalued|fairly valued)",
    ]
    assessment = ""
    for pattern in assessment_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            assessment = match.group(1)
            break
    if assessment:
        result += f"• **Valuation Assessment**: {assessment.title()}\n"
    price_patterns = [
        r"(\d+\.?\d*)\s*USD\s*Stock Price",
        r"Stock Price.*?(\d+\.?\d*)\s*USD",
        r"market price of (\d+\.?\d*)\s*USD",
        r"Price:\s*(\d+\.?\d*)\s*USD",
    ]
    current_price = ""
    for pattern in price_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            current_price = match.group(1)
            break
    if current_price:
        result += f"• **Current Stock Price**: {current_price} USD\n"
    model_patterns = [
        r"DCF Model",
        r"Discounted Cash Flow",
        r"Peter Lynch",
        r"Benjamin Graham",
    ]
    models_found = []
    for pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            models_found.append(pattern)
    if models_found:
        result += f"• **Valuation Models**: {', '.join(models_found)}\n"
    return result
def _extract_valuation_summary(text):
    """Extract complete valuation summary table"""
    result = "**Valuation Summary:**\n"
    valuation_patterns = [
        (r"DCF \(Growth 5y\).*?(\d+\.?\d+).*?(\d+\.?\d*)%", "DCF (Growth 5Y)"),
        (r"DCF \(Growth 10y\).*?(\d+\.?\d+).*?(\d+\.?\d*)%", "DCF (Growth 10Y)"),
        (r"DCF \(EBITDA 5y\).*?(\d+\.?\d+).*?(\d+\.?\d*)%", "DCF (EBITDA 5Y)"),
        (r"DCF \(EBITDA 10y\).*?(\d+\.?\d+).*?(\d+\.?\d*)%", "DCF (EBITDA 10Y)"),
        (r"Fair Value.*?(\d+\.?\d+).*?(\d+\.?\d*)%", "Fair Value"),
        (r"P/E.*?(\d+\.?\d+).*?(-?\d+\.?\d*)%", "P/E Multiple"),
        (r"EV/EBITDA.*?(\d+\.?\d+).*?(-?\d+\.?\d*)%", "EV/EBITDA Multiple"),
        (r"EPV.*?(\d+\.?\d+).*?(-?\d+\.?\d*)%", "Earnings Power Value"),
        (r"DDM - Stable.*?(\d+\.?\d+).*?(-?\d+\.?\d*)%", "DDM Stable Growth"),
        (r"DDM - Multi.*?(\d+\.?\d+).*?(-?\d+\.?\d*)%", "DDM Multi-Stage"),
    ]
    found_valuations = []
    for pattern, name in valuation_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1)
            upside = match.group(2)
            found_valuations.append(f"• **{name}**: {value} USD ({upside}% upside)")
    if not found_valuations:
        table_lines = text.split("\n")
        i = 0
        while i < len(table_lines):
            line = table_lines[i].strip()
            if line == "DCF (Growth 5y)" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **DCF (Growth 5Y)**: {numbers[0]} USD")
            elif line == "DCF (Growth 10y)" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **DCF (Growth 10Y)**: {numbers[0]} USD")
            elif line == "DCF (EBITDA 5y)" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **DCF (EBITDA 5Y)**: {numbers[0]} USD")
            elif line == "DCF (EBITDA 10y)" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **DCF (EBITDA 10Y)**: {numbers[0]} USD")
            elif line == "Fair Value" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **Fair Value**: {numbers[0]} USD")
            elif line == "P/E" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(f"• **P/E Multiple**: {numbers[0]} USD")
            elif line == "EV/EBITDA" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(
                        f"• **EV/EBITDA Multiple**: {numbers[0]} USD"
                    )
            elif line == "EPV" and i + 2 < len(table_lines):
                value_line = table_lines[i + 2].strip()
                numbers = re.findall(r"(\d+\.?\d+)", value_line)
                if numbers:
                    found_valuations.append(
                        f"• **Earnings Power Value**: {numbers[0]} USD"
                    )
            i += 1
    if found_valuations:
        result += "\n" + "\n".join(found_valuations)
    else:
        result += "\n• Valuation summary table not available in current format"
    insights_patterns = [
        r"(The stock.*?valued.*?\.)",
        r"(Based on.*?analysis.*?\.)",
        r"(Our.*?model.*?suggests.*?\.)",
    ]
    insights_found = []
    for pattern in insights_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        insights_found.extend(matches[:2])
    if insights_found:
        result += "\n\n**Insights:**\n"
        for insight in insights_found:
            clean_insight = re.sub(r"\s+", " ", insight).strip()
            result += f"• {clean_insight}\n"
    return result
