"""Deep research module for legendary investors."""

from datetime import datetime
from typing import List, Dict

from crew.analysts.fundamental_analysis import get_fundamental_context
from crew.analysts.stock_headlines_fetcher import fetch_finviz_news, fetch_tipranks_news, NewsItem


class LegendaryInvestorsResearcher:
    """Aggregates qualitative research for stocks."""

    def get_research_for_ticker(self, ticker: str) -> Dict[str, str]:
        """Gather fundamentals and news for a ticker."""
        
        # 1. Fundamental Context
        fundamental_context = get_fundamental_context(ticker)
        
        # 2. News (last 7 days)
        start_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        # We'll just fetch latest, the fetchers handle time filtering usually, 
        # but let's pass a safe start time (e.g. 7 days ago)
        # Actually existing fetchers take a start_time argument.
        # Let's say we want news from the last 30 days for context
        from datetime import timedelta
        import pytz
        
        start_time_utc = datetime.now(pytz.UTC) - timedelta(days=30)
        
        news_items: List[NewsItem] = []
        try:
            news_items.extend(fetch_finviz_news(ticker, start_time_utc))
        except Exception:
            pass
            
        try:
            news_items.extend(fetch_tipranks_news(ticker, start_time_utc))
        except Exception:
            pass
            
        # Deduplicate and sort news
        unique_news = {item.url: item for item in news_items}
        sorted_news = sorted(unique_news.values(), key=lambda x: x.published_at, reverse=True)
        top_news = sorted_news[:5]  # Top 5 news items
        
        news_summary = "Recent News:\n"
        if not top_news:
            news_summary += "No recent news found."
        else:
            for item in top_news:
                date_str = item.published_at.strftime("%Y-%m-%d")
                news_summary += f"- [{date_str}] {item.headline} ({item.source})\n"

        # 3. Derive Advanced Insights
        reason_why = self._derive_reason_why(ticker, top_news)
        evaluation = self._derive_evaluation(fundamental_context)
        rumor = self._derive_rumor(top_news)
        earnings = self._derive_earnings(fundamental_context)
        alpha = self._derive_alpha(fundamental_context)

        return {
            "fundamentals": fundamental_context,
            "news_summary": news_summary,
            "reason_why": reason_why,
            "evaluation": evaluation,
            "rumor": rumor,
            "earnings": earnings,
            "alpha": alpha,
        }

    def _derive_reason_why(self, ticker: str, news_items: List[NewsItem]) -> str:
        """Deduce reason for recent moves based on news."""
        if not news_items:
            return "No recent news to deduce reason."
        
        # Simple keyword matching on the most recent news
        latest = news_items[0]
        headline = latest.headline.lower()
        if "earnings" in headline or "eps" in headline:
            return f"Likely earnings related: {latest.headline}"
        if "acquisition" in headline or "merger" in headline or "buyout" in headline:
            return f"M&A activity: {latest.headline}"
        if "fda" in headline or "approval" in headline:
            return f"Regulatory news: {latest.headline}"
        if "upgrade" in headline or "downgrade" in headline:
            return f"Analyst rating change: {latest.headline}"
            
        return f"Market news: {latest.headline}"

    def _derive_evaluation(self, context: str) -> str:
        """Extract valuation metrics."""
        import re
        pe = re.search(r"P/E:\s*([\d\.]+)", context)
        peg = re.search(r"PEG:\s*([\d\.]+)", context)
        target = re.search(r"Target Price:\s*([\d\.]+)", context)
        
        eval_parts = []
        if pe:
            eval_parts.append(f"P/E: {pe.group(1)}")
        if peg:
            eval_parts.append(f"PEG: {peg.group(1)}")
        if target:
            eval_parts.append(f"Target: ${target.group(1)}")
            
        if not eval_parts:
            return "Valuation metrics not found in context."
        return " | ".join(eval_parts)

    def _derive_rumor(self, news_items: List[NewsItem]) -> str:
        """Check for rumors in news."""
        rumor_keywords = ["reportedly", "sources say", "considering", "exploring", "rumor", "potential", "talks"]
        for item in news_items:
            if any(k in item.headline.lower() for k in rumor_keywords):
                return f"Rumour detected: {item.headline}"
        return "No specific rumors detected in recent headlines."

    def _derive_earnings(self, context: str) -> str:
        """Extract earnings info."""
        # This assumes context contains Finviz table data which we scraped
        return "Earnings data would be extracted here from fundamental context if structured."

    def _derive_alpha(self, context: str) -> str:
        """Derive alpha/performance context."""
        import re
        perf_week = re.search(r"Perf Week:\s*([-\+\d\.]+%?)", context)
        perf_month = re.search(r"Perf Month:\s*([-\+\d\.]+%?)", context)
        
        alpha_parts = []
        if perf_week:
            alpha_parts.append(f"Week: {perf_week.group(1)}")
        if perf_month:
            alpha_parts.append(f"Month: {perf_month.group(1)}")
            
        if not alpha_parts:
            return "Performance metrics not found."
        return "Recent Perf: " + " | ".join(alpha_parts)
