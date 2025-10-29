import datetime
import time
import pytz
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union, Tuple, Optional
from dataclasses import dataclass
import re
import json
import dateutil.parser
from ai_trading_crew.utils.company_info import get_company_name
import os

@dataclass
class NewsItem:
    headline: str
    url: str
    source: str
    published_at: datetime.datetime

def parse_time_input(time_input: Union[str, int]) -> datetime.datetime:
    """Convert input time to datetime object in UTC"""
    est = pytz.timezone('US/Eastern')
    
    if isinstance(time_input, str):
        try:
            dt = datetime.datetime.strptime(time_input, "%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.datetime.strptime(time_input, "%Y-%m-%d")
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        dt = est.localize(dt)
        return dt.astimezone(pytz.UTC)
    elif isinstance(time_input, int):
        return datetime.datetime.fromtimestamp(time_input, pytz.UTC)
    else:
        raise ValueError("Time input must be a string in format 'YYYY-MM-DD HH:MM' or a Unix timestamp")

def fetch_finviz_news(ticker: str, start_time: datetime.datetime) -> List[NewsItem]:
    """Fetch news from Finviz"""
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
        with open("finviz_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_table = soup.find('table', class_='fullview-news-outer')
        if not news_table:
            # Clean up the debug file
            try:
                os.remove("finviz_response.html")
            except OSError:
                pass
            return []
        rows = news_table.find_all('tr')
        results = []
        est = pytz.timezone('US/Eastern')
        current_date = datetime.datetime.now(est).date()
        now = datetime.datetime.now(est)
        current_date_reference = None
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) < 2:
                    continue
                date_cell = cells[0]
                date_str = date_cell.text.strip()
                title_cell = cells[1]
                link = title_cell.find('a')
                if not link:
                    continue
                headline = link.text.strip()
                article_url = link.get('href')
                if article_url and article_url.startswith('/'):
                    article_url = f"https://finviz.com{article_url}"
                source_text = title_cell.find('span', class_='news_source')
                source = "Finviz"
                if source_text:
                    source_str = source_text.text.strip()
                    if source_str.startswith('(') and source_str.endswith(')'):
                        source = source_str[1:-1]
                article_date = None
                if "Today" in date_str:
                    time_part = date_str.replace("Today", "").strip()
                    current_date_reference = current_date
                    if ":" in time_part:
                        if "AM" in time_part or "PM" in time_part:
                            try:
                                time_obj = datetime.datetime.strptime(time_part, "%I:%M%p").time()
                            except ValueError:
                                try:
                                    time_obj = datetime.datetime.strptime(time_part, "%I:%M %p").time()
                                except ValueError:
                                    continue
                        else:
                            try:
                                hour, minute = map(int, time_part.split(':'))
                                time_obj = datetime.time(hour, minute)
                            except ValueError:
                                continue
                        article_date = datetime.datetime.combine(current_date, time_obj)
                        article_date = est.localize(article_date)
                elif "Yesterday" in date_str:
                    time_part = date_str.replace("Yesterday", "").strip()
                    yesterday = current_date - datetime.timedelta(days=1)
                    current_date_reference = yesterday
                    if ":" in time_part:
                        if "AM" in time_part or "PM" in time_part:
                            try:
                                time_obj = datetime.datetime.strptime(time_part, "%I:%M%p").time()
                            except ValueError:
                                try:
                                    time_obj = datetime.datetime.strptime(time_part, "%I:%M %p").time()
                                except ValueError:
                                    continue
                        else:
                            try:
                                hour, minute = map(int, time_part.split(':'))
                                time_obj = datetime.time(hour, minute)
                            except ValueError:
                                continue
                        article_date = datetime.datetime.combine(yesterday, time_obj)
                        article_date = est.localize(article_date)
                elif "-" in date_str and len(date_str.split("-")) == 3:
                    parts = date_str.split()
                    date_part = parts[0]
                    time_part = parts[1] if len(parts) > 1 else None
                    try:
                        month_str, day_str, year_str = date_part.split("-")
                        month_map = {
                            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                        }
                        month_num = month_map.get(month_str, 1)
                        day_num = int(day_str)
                        year_num = int(year_str)
                        if year_num < 100:
                            year_num += 2000
                        date_obj = datetime.date(year_num, month_num, day_num)
                        current_date_reference = date_obj
                        if time_part:
                            if ":" in time_part:
                                if "AM" in time_part or "PM" in time_part:
                                    hour_str, minute_sec = time_part.split(":")
                                    hour = int(hour_str)
                                    minute_str = minute_sec
                                    for suffix in ["AM", "PM", " AM", " PM"]:
                                        if minute_str.endswith(suffix):
                                            minute_str = minute_str[:-len(suffix)]
                                            break
                                    minute = int(minute_str)
                                    if ("PM" in minute_sec or " PM" in minute_sec) and hour < 12:
                                        hour += 12
                                    if ("AM" in minute_sec or " AM" in minute_sec) and hour == 12:
                                        hour = 0
                                    article_date = datetime.datetime(year_num, month_num, day_num, hour, minute)
                                else:
                                    hour, minute = map(int, time_part.split(":"))
                                    article_date = datetime.datetime(year_num, month_num, day_num, hour, minute)
                            else:
                                article_date = datetime.datetime(year_num, month_num, day_num, 12, 0)
                        else:
                            article_date = datetime.datetime(year_num, month_num, day_num, 12, 0)
                        article_date = est.localize(article_date)
                    except Exception:
                        continue
                elif ":" in date_str and ("AM" in date_str or "PM" in date_str) and current_date_reference:
                    try:
                        try:
                            time_obj = datetime.datetime.strptime(date_str, "%I:%M%p").time()
                        except ValueError:
                            try:
                                time_obj = datetime.datetime.strptime(date_str, "%I:%M %p").time()
                            except ValueError:
                                continue
                        ref_date = current_date_reference
                        if isinstance(ref_date, datetime.datetime):
                            ref_date = ref_date.date()
                        article_date = datetime.datetime.combine(ref_date, time_obj)
                        article_date = est.localize(article_date)
                    except Exception:
                        continue
                if article_date is None:
                    continue
                article_date_utc = article_date.astimezone(pytz.UTC)
                if article_date_utc >= start_time:
                    results.append(NewsItem(
                        headline=headline,
                        url=article_url,
                        source=source,
                        published_at=article_date_utc
                    ))
            except Exception:
                continue
        
        # Clean up the debug file after processing
        try:
            os.remove("finviz_response.html")
        except OSError:
            pass
            
        return results
    except Exception:
        # Clean up the debug file on exception
        try:
            os.remove("finviz_response.html")
        except OSError:
            pass
        return []

def fetch_tipranks_news(ticker: str, start_time: datetime.datetime) -> List[NewsItem]:
    """Fetch news from TipRanks website specifically from the All News tab"""
    results = []
    est = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(est)
    news_url = f"https://www.tipranks.com/stocks/{ticker.lower()}/stock-news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.tipranks.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    try:
        response = requests.get(news_url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            for link in soup.find_all('a'):
                try:
                    if not link.has_attr('href') or any(nav in link['href'] for nav in ["/search", "/topic/", "/category/", "#", "javascript:"]):
                        continue
                    url = link['href']
                    if '/news/' in url or '/analysis/' in url:
                        headline_elem = None
                        for heading_tag in ['h1', 'h2', 'h3', 'h4']:
                            if link.find(heading_tag):
                                headline_elem = link.find(heading_tag)
                                break
                        if not headline_elem:
                            for text_elem in link.find_all(['div', 'span']):
                                if text_elem.text and len(text_elem.text.strip()) > 20:
                                    headline_elem = text_elem
                                    break
                        if not headline_elem and len(link.text.strip()) > 20:
                            headline = link.text.strip()
                        elif headline_elem:
                            headline = headline_elem.text.strip()
                        else:
                            continue
                        if headline in ["All News", "Bearish News", "Bullish News", "News & Insights"] or headline.startswith("More"):
                            continue
                        for prefix in ["Premium", "Market News", "Stock Analysis & Ideas", "Ratings", "Company Announcements", "Weekend Updates"]:
                            if headline.startswith(prefix):
                                headline = headline[len(prefix):].strip()
                                break
                        if url.startswith('/'):
                            url = f"https://www.tipranks.com{url}"
                        found_time = False
                        article_date = None
                        time_texts = []
                        for time_elem in link.find_all(['div', 'span', 'time']):
                            time_text = time_elem.text.strip().lower()
                            if 'ago' in time_text:
                                time_texts.append(time_text)
                        parent = link.parent
                        if parent:
                            for sibling in parent.find_all(['div', 'span', 'time']):
                                if sibling != link:
                                    time_text = sibling.text.strip().lower()
                                    if 'ago' in time_text:
                                        time_texts.append(time_text)
                            parent_siblings = list(parent.next_siblings) + list(parent.previous_siblings)
                            for p_sibling in parent_siblings:
                                if hasattr(p_sibling, 'find_all'):
                                    for time_elem in p_sibling.find_all(['div', 'span', 'time']):
                                        time_text = time_elem.text.strip().lower()
                                        if 'ago' in time_text:
                                            time_texts.append(time_text)
                                elif hasattr(p_sibling, 'text') and 'ago' in p_sibling.text.lower():
                                    time_texts.append(p_sibling.text.strip().lower())
                        for time_text in time_texts:
                            try:
                                time_value = ''.join(filter(str.isdigit, time_text))
                                if not time_value:
                                    continue
                                time_value = int(time_value)
                                if 'hour' in time_text or 'hr' in time_text or 'h ' in time_text or 'h,' in time_text or ' h' in time_text:
                                    article_date = now - datetime.timedelta(hours=time_value)
                                    found_time = True
                                    break
                                elif 'day' in time_text or ' d ' in time_text or 'd,' in time_text or ' d' in time_text:
                                    article_date = now - datetime.timedelta(days=time_value)
                                    found_time = True
                                    break
                                elif 'min' in time_text or ' m ' in time_text or 'm,' in time_text or ' m' in time_text:
                                    article_date = now - datetime.timedelta(minutes=time_value)
                                    found_time = True
                                    break
                                elif 'week' in time_text or ' w ' in time_text:
                                    article_date = now - datetime.timedelta(weeks=time_value)
                                    found_time = True
                                    break
                            except (ValueError, TypeError):
                                continue
                        if not found_time:
                            if (now.date() - start_time.astimezone(est).date()).days == 0:
                                continue
                            article_date = now
                        if article_date.tzinfo is None:
                            article_date = est.localize(article_date)
                        article_date_utc = article_date.astimezone(pytz.UTC)
                        if article_date_utc >= start_time:
                            news_items.append(NewsItem(
                                headline=headline,
                                url=url,
                                source="TipRanks",
                                published_at=article_date_utc
                            ))
                except Exception:
                    continue
            unique_urls = {}
            for item in news_items:
                if "More" in item.headline or any(nav in item.url for nav in ["/topic/", "/stocks/", "/search?"]):
                    continue
                if item.url not in unique_urls:
                    unique_urls[item.url] = item
            results = list(unique_urls.values())
        return results
    except Exception:
        return []

def fetch_seeking_alpha_news(ticker: str, start_time: datetime.datetime) -> List[NewsItem]:
    """Fetch news from Seeking Alpha using API endpoint"""
    est = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(est)
    url = f"https://seekingalpha.com/api/v3/symbols/{ticker}/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    results = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            try:
                json_data = response.json()
                if isinstance(json_data, dict) and 'data' in json_data:
                    items = json_data.get('data', [])
                    for item in items:
                        attributes = item.get('attributes', {})
                        title = attributes.get('title', '')
                        if not title:
                            continue
                        links = item.get('links', {})
                        url_path = links.get('self', '')
                        if url_path:
                            article_url = f"https://seekingalpha.com{url_path}"
                        else:
                            continue
                        pub_date = None
                        date_str = attributes.get('publishOn', '')
                        if date_str:
                            try:
                                pub_date = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                            except ValueError:
                                try:
                                    pub_date = dateutil.parser.parse(date_str)
                                except Exception:
                                    continue
                        if not pub_date:
                            continue
                        if pub_date.tzinfo is None:
                            pub_date = est.localize(pub_date)
                        pub_date_utc = pub_date.astimezone(pytz.UTC)
                        if pub_date_utc > now.astimezone(pytz.UTC):
                            pub_date_utc = now.astimezone(pytz.UTC)
                        if pub_date_utc >= start_time:
                            results.append(NewsItem(
                                headline=title,
                                url=article_url,
                                source="Seeking Alpha",
                                published_at=pub_date_utc
                            ))
            except (ValueError, json.JSONDecodeError):
                pass
    except Exception:
        pass
    return results

def fetch_marketwatch_news(ticker: str, start_time: datetime.datetime) -> List[NewsItem]:
    url = f"https://www.marketwatch.com/investing/stock/{ticker.lower()}"
    
    # List of user agents to try
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    
    # Try with different user agents
    for user_agent in user_agents:
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save the HTML for debugging (commented out)
                # with open("marketwatch_response.html", "w", encoding="utf-8") as f:
                #     f.write(response.text)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                est = pytz.timezone('US/Eastern')
                results: List[NewsItem] = []
                
                # Try to directly access known structure for news items
                # First check for "Other News" or "Other Sources" sections
                news_sections = []
                
                # Look for section headings first
                for heading_text in ["other news", "other sources", "latest news", "press releases"]:
                    heading_elements = soup.find_all(string=lambda s: s and heading_text in s.lower())
                    for heading in heading_elements:
                        parent = heading.parent
                        if parent:
                            # Try to find the nearest container holding news items
                            container = parent
                            # Navigate up to find a suitable container
                            for _ in range(5):
                                if container.parent:
                                    container = container.parent
                                    # Check if this contains list items or links
                                    news_items = container.find_all(['li', 'div', 'article'], class_=lambda c: c and ('article' in str(c).lower() or 'story' in str(c).lower()))
                                    if news_items:
                                        news_sections.append((heading.strip(), container, news_items))
                                        break
                
                # Process each news section
                for section_name, container, items in news_sections:
                    source_name = "MarketWatch - Other Sources"
                    if "press release" in section_name.lower():
                        source_name = "MarketWatch - Press Releases"
                    
                    for item in items:
                        try:
                            # Find the link
                            link = item.find('a', href=True)
                            if not link:
                                continue
                            
                            article_url = link['href']
                            if article_url.startswith('/'):
                                article_url = f"https://www.marketwatch.com{article_url}"
                            
                            # Get the headline
                            headline = link.get_text(strip=True)
                            if not headline or len(headline) < 5:
                                continue
                            
                            # Find the date
                            pub_date = None
                            time_tag = item.find('time')
                            if time_tag and time_tag.has_attr('datetime'):
                                try:
                                    pub_date = dateutil.parser.parse(time_tag['datetime'])
                                except:
                                    pass
                            
                            # Look for date in text
                            if not pub_date:
                                text = item.get_text(" ", strip=True)
                                date_patterns = [
                                    r'([A-Z][a-z]{2,8}\.\s\d{1,2},\s\d{4}\s+at\s+[\d:]+\s[ap]\.m\.)',
                                    r'([A-Z][a-z]{2,8}\s\d{1,2},\s\d{4}\s+at\s+[\d:]+\s[ap]\.m\.)',
                                    r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s*[ap]\.?m\.?)'
                                ]
                                
                                for pattern in date_patterns:
                                    match = re.search(pattern, text)
                                    if match:
                                        try:
                                            date_str = match.group(1)
                                            pub_date = dateutil.parser.parse(date_str + " ET" if "ET" not in date_str else date_str)
                                            break
                                        except:
                                            continue
                            
                            # Use current time as fallback
                            if not pub_date:
                                # For debugging purposes, use current time minus 1 day to ensure inclusion
                                pub_date = datetime.datetime.now(est) - datetime.timedelta(days=1)
                            
                            if pub_date.tzinfo is None:
                                pub_date = est.localize(pub_date)
                            
                            pub_date_utc = pub_date.astimezone(pytz.UTC)
                            
                            if pub_date_utc >= start_time:
                                results.append(NewsItem(
                                    headline=headline,
                                    url=article_url,
                                    source=source_name,
                                    published_at=pub_date_utc
                                ))
                        except Exception:
                            pass
                
                # If we didn't find proper sections, try a more general approach
                if not results:
                    # Look for any divs that might contain news items
                    news_containers = soup.find_all(['div', 'ul', 'section'], class_=lambda c: c and any(term in str(c).lower() for term in ['news', 'article', 'story', 'collection', 'list']))
                    
                    for container in news_containers:
                        # Find links directly
                        links = container.find_all('a', href=True)
                        for link in links:
                            try:
                                url = link['href']
                                if not url or url.startswith('#') or 'javascript:' in url:
                                    continue
                                
                                headline = link.get_text(strip=True)
                                if not headline or len(headline) < 10:
                                    continue
                                
                                if url.startswith('/'):
                                    url = f"https://www.marketwatch.com{url}"
                                
                                # Use current time minus 1 day as fallback date
                                pub_date = datetime.datetime.now(est) - datetime.timedelta(days=1)
                                if pub_date.tzinfo is None:
                                    pub_date = est.localize(pub_date)
                                
                                pub_date_utc = pub_date.astimezone(pytz.UTC)
                                
                                if pub_date_utc >= start_time:
                                    results.append(NewsItem(
                                        headline=headline,
                                        url=url,
                                        source="MarketWatch - Other Sources",
                                        published_at=pub_date_utc
                                    ))
                            except Exception:
                                pass
                
                # If we found results, break the loop
                if results:
                    return results
        except Exception:
            pass
    
    # Try an alternative URL structure as a fallback
    try:
        alt_url = f"https://www.marketwatch.com/search?q={ticker}&ts=0&tab=All%20News"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'no-cache'
        }
        
        response = requests.get(alt_url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            est = pytz.timezone('US/Eastern')
            results = []
            
            # Search results typically have a consistent structure
            articles = soup.find_all(['div', 'li'], class_=lambda c: c and ('article' in str(c).lower() or 'search-result' in str(c).lower()))
            
            for article in articles:
                try:
                    link = article.find('a', href=True)
                    if not link:
                        continue
                    
                    headline = None
                    headline_tag = article.find(['h2', 'h3', 'h4', 'div'], class_=lambda c: c and ('title' in str(c).lower() or 'headline' in str(c).lower()))
                    
                    if headline_tag:
                        headline = headline_tag.get_text(strip=True)
                    elif link.get_text(strip=True):
                        headline = link.get_text(strip=True)
                    
                    if not headline or len(headline) < 5:
                        continue
                    
                    url = link['href']
                    if url.startswith('/'):
                        url = f"https://www.marketwatch.com{url}"
                    
                    # Get date
                    pub_date = None
                    time_tag = article.find('time')
                    if time_tag and time_tag.has_attr('datetime'):
                        try:
                            pub_date = dateutil.parser.parse(time_tag['datetime'])
                        except:
                            pass
                    
                    if not pub_date:
                        # Look for date text
                        date_tag = article.find(['span', 'div'], class_=lambda c: c and ('date' in str(c).lower() or 'time' in str(c).lower() or 'published' in str(c).lower()))
                        if date_tag:
                            try:
                                pub_date = dateutil.parser.parse(date_tag.get_text(strip=True) + " ET")
                            except:
                                pass
                    
                    if not pub_date:
                        # Fallback date
                        pub_date = datetime.datetime.now(est) - datetime.timedelta(days=1)
                    
                    if pub_date.tzinfo is None:
                        pub_date = est.localize(pub_date)
                    
                    pub_date_utc = pub_date.astimezone(pytz.UTC)
                    
                    if pub_date_utc >= start_time:
                        results.append(NewsItem(
                            headline=headline,
                            url=url,
                            source="MarketWatch - Other Sources",
                            published_at=pub_date_utc
                        ))
                except Exception:
                    pass
            
            return results
    except Exception:
        pass
    
    # Return empty list if all attempts failed
    return []

def fetch_stock_news(ticker: str, start_time: Union[str, int]) -> List[NewsItem]:
    """
    Fetch stock news from multiple sources including MarketWatch
    """
    start_datetime = parse_time_input(start_time)
    finviz_news = fetch_finviz_news(ticker, start_datetime)
    tipranks_news = fetch_tipranks_news(ticker, start_datetime)
    seeking_alpha_news = fetch_seeking_alpha_news(ticker, start_datetime)
    marketwatch_news = fetch_marketwatch_news(ticker, start_datetime)

    # Remove duplicates from MarketWatch news (they sometimes appear twice in the same section)
    unique_mw_urls = {}
    deduplicated_mw_news = []
    for item in marketwatch_news:
        if item.url not in unique_mw_urls:
            unique_mw_urls[item.url] = item
            deduplicated_mw_news.append(item)
    
    all_news = finviz_news + tipranks_news + seeking_alpha_news + deduplicated_mw_news
    filtered_news = []
    for news_item in all_news:
        if "/topic/" in news_item.url or "/category/" in news_item.url:
            continue
        if news_item.headline in ["More AAPL News >", "More News >"]:
            continue
        if news_item.source.startswith("TipRanks"):
            if news_item.headline.startswith("Premium"):
                parts = news_item.headline.split("Premium")
                if len(parts) > 1:
                    clean_headline = parts[1].strip()
                    if clean_headline:
                        news_item.headline = clean_headline
            for category in ["Market News", "Stock Analysis & Ideas", "Ratings", "Company Announcements", "Weekend Updates"]:
                if news_item.headline.startswith(category):
                    parts = news_item.headline.split(category)
                    if len(parts) > 1:
                        clean_headline = parts[1].strip()
                        if clean_headline:
                            news_item.headline = clean_headline
                            break
        filtered_news.append(news_item)
        
    # Simple deduplication - only exact headline matches and URL matches
    seen_urls = set()
    seen_exact_headlines = set()
    deduplicated_news = []
    
    for news_item in filtered_news:
        # Only deduplicate exact same headlines or same URLs
        if news_item.url in seen_urls:
            continue
        if news_item.headline in seen_exact_headlines:
            continue
            
        seen_exact_headlines.add(news_item.headline)
        seen_urls.add(news_item.url)
        deduplicated_news.append(news_item)
        
    deduplicated_news.sort(key=lambda x: x.published_at, reverse=True)
    return deduplicated_news

def get_news_context(symbol: str, start_time: str) -> str:
    """
    Get formatted news context for a stock symbol since a specific time.
    """
    news_items = fetch_stock_news(symbol, start_time)
    company_name = get_company_name(symbol)
    if not news_items:
        return f"No news found for {company_name} since {start_time}"
    
    # Create the formatted news content with consistent line breaks
    result = f"News for {company_name} since {start_time}:\n\n"
    for i, item in enumerate(news_items):
        est = pytz.timezone('US/Eastern')
        published_at_est = item.published_at.astimezone(est)
        formatted_date = published_at_est.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        # Clean up the headline text - replace problematic Unicode characters
        headline = item.headline
        # Fix curly single quotes
        headline = headline.replace('\u2019', "'").replace('\u2018', "'")
        headline = headline.replace('\u2032', "'").replace('\u02bc', "'")
        headline = headline.replace('â\x80\x99', "'")
        
        # Fix curly double quotes
        headline = headline.replace('\u201c', '"').replace('\u201d', '"')
        headline = headline.replace('â\x80\x9c', '"').replace('â\x80\x9d', '"')
        
        # Fix other common problematic characters
        headline = headline.replace('\u2013', '-').replace('\u2014', '--')  # en/em dashes
        headline = headline.replace('\u2026', '...').replace('\u00a0', ' ')  # ellipsis, non-breaking space
        headline = headline.replace('\u00ad', '')  # soft hyphen
        
        # Remove any remaining non-ascii characters
        headline = ''.join(c if ord(c) < 128 else ' ' for c in headline)
        headline = headline.replace('   ', ' ').replace('  ', ' ').strip()  # Clean up extra spaces
        
        # Ensure proper formatting with normalized line breaks
        result += f"{i+1}. [{item.source}] {headline}\n"
        result += f"   Published: {formatted_date}\n"
        result += f"   URL: {item.url}\n\n"
    
    # Ensure consistent encoding and line endings
    result = result.replace('\r\n', '\n').replace('\r', '\n')
    
    # Make a final pass to ensure only ASCII characters remain
    result = result.encode('ascii', 'replace').decode('ascii')
    
    return result
