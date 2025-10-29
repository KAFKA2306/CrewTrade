import asyncio
import re
import random
import time
import requests
import json
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from io import StringIO
import sys
from ai_trading_crew.utils.company_info import get_company_name
import os

# List of URLs to scrape - focusing on what works
url_list = []

# Realistic user agents
USER_AGENTS = [
    # Desktop - Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Desktop - Firefox 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
]

async def extract_finviz_content(url):
    """Enhanced method to extract article content from Finviz directly"""
    try:
        print(f"Extracting content from Finviz URL: {url}")
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://finviz.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"Direct request status code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Response received successfully
            
            article_content = ""
            title = ""
            
            # Try to extract the title first
            title_selectors = [
                'h1', '.title', '.headline', '.article-title', 
                'title', '.news-title', '.post-title'
            ]
            
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    title_text = title_element.get_text(strip=True)
                    if len(title_text) > 10 and title_text.lower() != 'finviz':
                        title = title_text
                        break
            
            # Look for the main article content with multiple strategies
            content_selectors = [
                'div.text-justify',  # Finviz specific selector
                'article', '.news-content', '.content-article', '.article-content',
                '.article-body', '.post-content', '#article-body', '.main-content',
                '.content', '.article', '.news-article', '.story-content'
            ]
            
            for selector in content_selectors:
                article_element = soup.select_one(selector)
                if article_element:
                    # Remove unwanted elements
                    for unwanted in article_element.select('nav, header, footer, .ad, .advertisement, .sidebar, .menu'):
                        unwanted.decompose()
                    
                    content_text = article_element.get_text(separator='\n', strip=True)
                    if len(content_text) > 100:  # Only use if substantial content
                        article_content = content_text
                        break
            
            # If no main content found, try to extract from iframes (common in Finviz)
            if not article_content:
                iframes = soup.find_all('iframe')
                if iframes:
                    iframe_sources = []
                    for iframe in iframes:
                        src = iframe.get('src')
                        if src:
                            iframe_sources.append(src)
                            # Try to fetch content from iframe if it's from a known source
                            if any(domain in src for domain in ['zerohedge.com', 'seekingalpha.com', 'bloomberg.com', 'reuters.com']):
                                try:
                                    if src.startswith('//'):
                                        src = 'https:' + src
                                    elif src.startswith('/'):
                                        src = 'https://finviz.com' + src
                                    
                                    iframe_response = requests.get(src, headers=headers, timeout=10)
                                    if iframe_response.status_code == 200:
                                        iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                                        
                                        # Extract content from iframe
                                        iframe_content = ""
                                        for selector in content_selectors:
                                            iframe_element = iframe_soup.select_one(selector)
                                            if iframe_element:
                                                iframe_content = iframe_element.get_text(separator='\n', strip=True)
                                                if len(iframe_content) > 100:
                                                    article_content = iframe_content
                                                    break
                                        
                                        if article_content:
                                            break
                                except:
                                    continue
                    
                    if not article_content and iframe_sources:
                        article_content = f"Article content may be embedded in iframes from: {', '.join(iframe_sources)}"
            
            # If still no content, try to extract from paragraphs
            if not article_content:
                paragraphs = soup.select('p')
                if paragraphs:
                    content_parts = []
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if len(text) > 30:  # Only substantial paragraphs
                            # Skip navigation/footer content
                            if not any(skip in text.lower() for skip in [
                                'cookie', 'privacy policy', 'terms of use', 'copyright', 
                                'all rights reserved', 'finviz.com', 'navigation'
                            ]):
                                content_parts.append(text)
                    
                    if content_parts:
                        article_content = '\n\n'.join(content_parts)
            
            # Look for external article links if no content found
            if not article_content:
                external_links = soup.select('a[href*="zerohedge"], a[href*="seekingalpha"], a[href*="bloomberg"], a[href*="reuters"], a[href*="marketwatch"]')
                if external_links:
                    links = [link.get('href') for link in external_links if link.get('href')]
                    article_content = f"Article content may be available at these external links: {', '.join(links[:3])}"
            
            # Combine title and content
            result = ""
            if title:
                result += f"Title: {title}\n\n"
            
            if article_content:
                result += article_content
            else:
                result = "Could not extract article content from Finviz. The article may be embedded in an iframe or external source."
            
            # Clean up the debug file
            try:
                os.remove("finviz_response.html")
            except OSError:
                pass
            return result
            
        else:
            # Clean up the debug file on error
            try:
                os.remove("finviz_response.html")
            except OSError:
                pass
            return f"Error fetching content: HTTP {response.status_code}"
    
    except Exception as e:
        # Clean up the debug file even if we couldn't extract content
        try:
            os.remove("finviz_response.html")
        except OSError:
            pass
        return f"Error extracting Finviz content: {str(e)}"

async def extract_seeking_alpha_content(url):
    """Specialized method to extract article content from SeekingAlpha"""
    try:
        # Use a comprehensive set of headers to simulate a legitimate browser request
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/search?q=foxconn+profit+seekingalpha',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers',
            'Cookie': '_ga=GA1.1.123456789.1234567890; machine_cookie=05a12345'
        }
        
        # Create a session to persist cookies
        session = requests.Session()
        
        # First visit Google to set referrer
        google_url = "https://www.google.com/search?q=foxconn+profit+soars+on+ai+demand+tariffs+woes+site:seekingalpha.com"
        session.get(google_url, headers=headers, timeout=10)
        
        # Now visit the actual page
        print(f"Fetching URL: {url}")
        response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"Direct request status code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # Save the response to a file for debugging
        with open("finviz_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selectors to find the article content
            # Looking for the main article content with different possible selectors
            article_content = ""
            
            # Try to find article body content
            selectors = [
                'div[data-test-id="article-content"]', 
                '.article-content-body', 
                '.article__content',
                '#article-content-body',
                '.paywall-content',
                'div.contentbox[id*="article"]',
                '.article-body-text', 
                '.article-body',
                '.article',
                '#main-content',
                '.post-content',
                'main'
            ]
            
            for selector in selectors:
                content_elements = soup.select(selector)
                if content_elements:
                    for element in content_elements:
                        # Filter out non-essential elements like ads
                        for ad in element.select('.ad-wrap, .ad-container, .banner, .advertisement'):
                            ad.decompose()
                        article_content += element.get_text(separator='\n', strip=True) + "\n\n"
                    break
            
            # If we found content, return it
            if article_content:
                # Clean up the debug file
                try:
                    os.remove("finviz_response.html")
                except OSError:
                    pass
                return article_content
            
            # Try to find title and sub-elements if we haven't found the complete article
            title_element = soup.select_one('h1.title') or soup.select_one('.title') or soup.select_one('h1')
            if title_element:
                title = title_element.get_text(strip=True)
                article_content = f"{title}\n\n"
            
            # Try to extract meta description which often contains article summary
            meta_desc = soup.select_one('meta[name="description"]')
            if meta_desc and meta_desc.get('content'):
                article_content += f"{meta_desc.get('content')}\n\n"
                
            # Try to find the time element for the article date
            time_element = soup.select_one('time') or soup.select_one('.date')
            if time_element:
                article_content += f"Published: {time_element.get_text(strip=True)}\n\n"
            
            # Try to find any paragraph content
            paragraphs = soup.select('p')
            if paragraphs:
                for p in paragraphs[:30]:  # Get first 30 paragraphs to avoid getting too much footer content
                    text = p.get_text(strip=True)
                    if len(text) > 30:  # Only include substantial paragraphs
                        # Skip navigation text, footers, etc.
                        if not any(skip in text.lower() for skip in ['cookie', 'privacy policy', 'terms of use', 'copyright', 'all rights reserved']):
                            article_content += text + "\n\n"
            
            if article_content:
                # Clean up the debug file
                try:
                    os.remove("finviz_response.html")
                except OSError:
                    pass
                return article_content
            
            # Last resort: look for any div with substantial text content
            divs = soup.select('div')
            for div in divs:
                text = div.get_text(strip=True)
                if len(text) > 200 and '<' not in text and '>' not in text:  # Long text without HTML tags
                    article_content += text + "\n\n"
                    if len(article_content) > 500:  # If we have enough content, stop
                        break
            
            if article_content:
                # Clean up the debug file
                try:
                    os.remove("finviz_response.html")
                except OSError:
                    pass
                return article_content
                
            # Clean up the debug file even if we couldn't extract content
            try:
                os.remove("finviz_response.html")
            except OSError:
                pass
            return "Could not extract article content from SeekingAlpha. Check the finviz_response.html file for debugging."
        else:
            # Clean up the debug file on error
            try:
                os.remove("finviz_response.html")
            except OSError:
                pass
            return f"Error fetching content: {response.status_code}"
    
    except Exception as e:
        # Clean up the debug file even if we couldn't extract content
        try:
            os.remove("finviz_response.html")
        except OSError:
            pass
        return f"Error extracting SeekingAlpha content: {str(e)}"

async def extract_yahoo_finance_content(url):
    """Specialized method to extract article content from Yahoo Finance"""
    try:
        print(f"Extracting content from Yahoo Finance URL: {url}")

   
        # First try with the direct browser approach since requests is getting blocked by consent pages
        browser_config = BrowserConfig(
            headless=True,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        
        yahoo_config = CrawlerRunConfig(
            wait_until="domcontentloaded",  # Use domcontentloaded which is safer
            verbose=True,
            magic=True,
            simulate_user=True,
            js_code="""
            function waitFor(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
            
            async function extractYahooContent() {
                // Wait for content to load fully
                await waitFor(2000);
                
                // Check for and handle consent dialogs
                const consentButton = document.querySelector('button[name="agree"], .consent-form .agree-button, .btn.agree, button.btn.primary, button.accept-all');
                if (consentButton) {
                    console.log('Consent button found, clicking...');
                    consentButton.click();
                    await waitFor(2000);
                }
                
                // Get the article title
                let title = '';
                const titleElement = document.querySelector('h1') || document.querySelector('.caas-title') || 
                                    document.querySelector('.headline') || document.querySelector('[data-test="article-header"]');
                if (titleElement) {
                    title = titleElement.innerText;
                }
                
                // Get the article content
                let content = '';
                
                // Try different selectors for Yahoo Finance articles
                const contentSelectors = [
                    '.caas-body',
                    '.article-body',
                    '.canvas-body',
                    '.caas-content-wrapper',
                    'article',
                    '#module-article',
                    '.article-container'
                ];
                
                for (const selector of contentSelectors) {
                    const element = document.querySelector(selector);
                    if (element) {
                        // Remove ads and other non-content elements
                        const unwantedSelectors = [
                            'nav', 'header', 'footer', '.ad', 
                            '.advertisement', '.promoted-content',
                            '.sidebar', '.related-content'
                        ];
                        
                        for (const sel of unwantedSelectors) {
                            const elements = element.querySelectorAll(sel);
                            for (const el of elements) {
                                if (el && el.parentNode) {
                                    el.parentNode.removeChild(el);
                                }
                            }
                        }
                        
                        content = element.innerText;
                        break;
                    }
                }
                
                // If we couldn't find content through specific containers, 
                // try to gather paragraphs that might be article content
                if (!content) {
                    const paragraphs = document.querySelectorAll('p');
                    if (paragraphs && paragraphs.length) {
                        const paragraphTexts = [];
                        for (let i = 0; i < paragraphs.length; i++) {
                            const p = paragraphs[i];
                            if (p.innerText && p.innerText.length > 30) {
                                // Skip likely footer/header text
                                const text = p.innerText.toLowerCase();
                                if (!text.includes('cookie') && !text.includes('privacy policy') && 
                                    !text.includes('terms of use') && !text.includes('all rights reserved')) {
                                    paragraphTexts.push(p.innerText);
                                }
                            }
                        }
                        
                        if (paragraphTexts.length > 0) {
                            content = paragraphTexts.join('\\n\\n');
                        }
                    }
                }
                
                return { title, content };
            }
            
            // Execute the extraction
            const extractedData = await extractYahooContent();
            
            // Create a clean version of the page with just our extracted content
            if (extractedData.title || extractedData.content) {
                document.body.innerHTML = `
                    <div id="extracted-article">
                        <h1>${extractedData.title || ''}</h1>
                        <div>${extractedData.content || ''}</div>
                    </div>
                `;
            }
            """
        )
        
        # Extract article from specific source if we can identify it
        # Check if it's a WSJ article republished on Yahoo Finance
        if 'wall-street-journal' in url.lower() or 'wsj' in url.lower():
            # Try to extract the WSJ article ID from the URL or article title
            article_content = await extract_wsj_content(url)
            if article_content and len(article_content) > 200:
                return article_content
        
        async with AsyncWebCrawler() as crawler:
            crawler.config = browser_config
            print(f"Running AsyncWebCrawler for Yahoo Finance URL...")
            result = await crawler.arun(url=url, config=yahoo_config)
            
            if result and result.success:
                # First check if we have a clean extracted article div
                if result.html and '<div id="extracted-article">' in result.html:
                    match = re.search(r'<div id="extracted-article">(.*?)</div>', result.html, re.DOTALL)
                    if match:
                        extracted_content = match.group(1)
                        # Clean up the HTML tags
                        soup = BeautifulSoup(extracted_content, 'html.parser')
                        return soup.get_text(separator='\n\n', strip=True)
                
                # If we have markdown, use that
                if result.markdown and len(result.markdown) > 200:
                    return result.markdown
                
                # If we have text content
                if hasattr(result, 'text') and result.text and len(result.text) > 200:
                    return result.text
                
                # If we have HTML but couldn't extract structured content, try to extract from the HTML
                if result.html:
                    try:
                        soup = BeautifulSoup(result.html, 'html.parser')
                        article_content = ""
                        
                        # Look for title
                        title_element = soup.select_one('h1') or soup.select_one('.caas-title') or soup.select_one('.headline')
                        if title_element:
                            article_content = f"{title_element.get_text(strip=True)}\n\n"
                        
                        # Try to find article content
                        content_selectors = [
                            '.caas-body', 
                            '.article-body',
                            '.canvas-body',
                            '.wafer-caas-body',
                            '.caas-content-wrapper',
                            'article',
                            '.content-inner',
                            '.article-content',
                            '#module-article'
                        ]
                        
                        for selector in content_selectors:
                            content_element = soup.select_one(selector)
                            if content_element:
                                # Filter out non-article elements
                                for el in content_element.select('nav, header, footer, .ad, .advertisement'):
                                    if el:
                                        el.decompose()
                                
                                article_content += content_element.get_text(separator='\n\n', strip=True)
                                break
                        
                        # If we have enough content, return it
                        if len(article_content) > 200:
                            return article_content
                        
                        # Otherwise try to gather paragraphs
                        paragraphs = []
                        for p in soup.select('p'):
                            text = p.get_text(strip=True)
                            if len(text) > 30:
                                # Skip likely footer/header/navigation text
                                if not any(skip in text.lower() for skip in ['cookie', 'privacy policy', 'terms of use', 'copyright', 'all rights reserved']):
                                    paragraphs.append(text)
                        
                        if paragraphs:
                            return article_content + '\n\n' + '\n\n'.join(paragraphs)
                        
                    except Exception as e:
                        print(f"Error extracting from HTML: {str(e)}")
                    
                    # If we get here, save the HTML for debugging and return a message
                    with open("yahoo_finance_response.html", "w", encoding="utf-8") as f:
                        f.write(result.html)
                    
                    return "Could not extract article content from Yahoo Finance. Check the yahoo_finance_response.html file."
            else:
                error_msg = result.error_message if result else "Unknown error"
                print(f"Error with AsyncWebCrawler: {error_msg}")
                
                # Try with straightforward HTML parsing as a fallback
                return await extract_yahoo_finance_direct(url)
        
    except Exception as e:
        print(f"Error extracting Yahoo Finance content: {str(e)}")
        # Try with straightforward HTML parsing as a fallback
        return await extract_yahoo_finance_direct(url)

async def extract_yahoo_finance_direct(url):
    """Fallback method to extract Yahoo Finance content with direct HTML parsing"""
    try:
        # Use a comprehensive set of headers to simulate a legitimate browser request
        user_agent = random.choice(USER_AGENTS)
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/search?q=berkshire+sells+financial+stocks+yahoo+finance',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            # Special cookie to bypass consent page
            'Cookie': 'AO=o=1; B=2515fh324h34f&b=3&s=55; GUC=AQEBAQFliuqCZwIhWASF; cmp=t=1715009307&j=0; gpp=DBABBgA~1-DBABBgA; gpp_sid=-1; A1=d=AQABBC5AimUCEGECLV7cRfilk0HxGCmw2hgFEgEBAQHqimXSZwAAAAAA_eMAAA&S=AQAAAmuuLR75uRxc7g7YNP8X7Cw'
        }
        
        # Directly try Article API endpoint
        if '/m/' in url:
            article_id = url.split('/m/')[1].split('/')[0]
            # Try archive.is/archive.today which might have cached the article
            archive_url = f"https://archive.is/https://finance.yahoo.com/m/{article_id}/"
            
            # Try multiple approaches
            urls_to_try = [
                url,  # Original URL
                f"https://finance.yahoo.com/amphtml/{article_id}",  # AMP version
                f"https://finance.yahoo.com/news/{article_id}",  # News format
                archive_url  # Archive.is version
            ]
            
            for try_url in urls_to_try:
                print(f"Trying URL: {try_url}")
                response = requests.get(try_url, headers=headers, timeout=15)
                print(f"Status code: {response.status_code}")
                
                if response.status_code == 200 and "consent.yahoo.com" not in response.url:
                    # Save response for debugging
                    with open("yahoo_finance_response.html", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    article_content = ""
                    
                    # Look for title
                    title_element = soup.select_one('h1') or soup.select_one('.caas-title') or soup.select_one('.headline')
                    if title_element:
                        article_content = f"{title_element.get_text(strip=True)}\n\n"
                    
                    # Look for article content
                    selectors = ['.caas-body', '.article-body', '.canvas-body', '.article-content', 'article']
                    for selector in selectors:
                        element = soup.select_one(selector)
                        if element:
                            # Remove ads and other non-content
                            for ad in element.select('.ad-wrap, .ad-container, .banner, .advertisement'):
                                ad.decompose()
                            article_content += element.get_text(separator='\n\n', strip=True)
                            break
                    
                    # If we found article content, return it
                    if len(article_content) > 200:
                        return article_content
        
        return "Could not extract Yahoo Finance article content using direct methods."
    
    except Exception as e:
        return f"Error with direct extraction: {str(e)}"

async def extract_wsj_content(url):
    """Extract content from a Wall Street Journal article (potentially via Yahoo Finance)"""
    try:
        # Use specialized headers for WSJ content
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site'
        }
        
        # Try both original URL or extract WSJ URL if this is on Yahoo Finance
        article_title = ""
        
        # Original yahoo url might have the WSJ article title in it
        if '/m/' in url:
            # Extract part that might contain title
            parts = url.split('/m/')[1].split('/')
            if len(parts) > 0:
                article_id = parts[0]
                # Check if there's a slug after the ID
                if '-' in article_id:
                    potential_title = article_id.split('-')
                    if len(potential_title) > 4:  # Assume it's a slug if more than 4 parts
                        article_title = ' '.join([p for p in potential_title if len(p) > 2]).title()
                
        # If we have a title, try to find the article directly
        article_content = ""
        
        if article_title:
            article_title_query = article_title.replace(' ', '+')
            search_url = f"https://www.wsj.com/search?query={article_title_query}&isToggleOn=true&operator=AND&sort=date-desc&duration=1y&startDate=2025/05/01&endDate=2025/05/16&source=wsjie%2Cblog%2Cwsjvideo%2Cinteractivemedia%2Cwsjsitesrch%2Cwsjpro"
            
            print(f"Searching WSJ for article: {article_title}")
            print(f"Search URL: {search_url}")
            
            search_response = requests.get(search_url, headers=headers, timeout=15)
            if search_response.status_code == 200:
                search_soup = BeautifulSoup(search_response.text, 'html.parser')
                
                # Look for article links
                article_links = search_soup.select('a.headline')
                if article_links:
                    # Use the first result
                    article_url = article_links[0].get('href')
                    if 'wsj.com' not in article_url:
                        article_url = f"https://www.wsj.com{article_url}"
                        
                    print(f"Found WSJ article: {article_url}")
                    
                    # Try to get the article
                    article_response = requests.get(article_url, headers=headers, timeout=15)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        
                        # Extract title
                        title_element = article_soup.select_one('h1.headline')
                        if title_element:
                            article_content = f"{title_element.get_text(strip=True)}\n\n"
                        
                        # Extract content - WSJ specific selectors
                        content_selectors = ['.article-content', '.wsj-snippet-body', '.article-wrap', '.paywall-article']
                        for selector in content_selectors:
                            content_element = article_soup.select_one(selector)
                            if content_element:
                                # Get all paragraphs
                                paragraphs = content_element.select('p')
                                for p in paragraphs:
                                    text = p.get_text(strip=True)
                                    if len(text) > 20:
                                        article_content += text + "\n\n"
        
        # As a fallback, also try to extract the WSJ article content from the Yahoo page
        if not article_content or len(article_content) < 200:
            # Use our main extraction to get what information we can from the Yahoo version
            yahoo_content = await extract_yahoo_finance_direct(url)
            if yahoo_content and len(yahoo_content.strip()) > 200:
                # Look for the "The Wall Street Journal" credit
                wsj_marker_idx = yahoo_content.find("The Wall Street Journal")
                if wsj_marker_idx != -1:
                    if article_content:  # If we already have some content, append
                        article_content += "\n\nFrom Yahoo Finance version:\n\n" + yahoo_content
                    else:
                        article_content = yahoo_content
        
        if article_content and len(article_content) > 200:
            # Add a note about the source
            article_content += "\n\n(Source: Wall Street Journal via Yahoo Finance)"
            return article_content
        
        return ""  # Return empty string if extraction failed
        
    except Exception as e:
        print(f"Error extracting WSJ content: {str(e)}")
        return ""

async def extract_benzinga_content(url):
    """Specialized method to extract article content from Benzinga"""
    try:
        print(f"Extracting content from Benzinga URL: {url}")


        # Use a similar approach to other extraction methods
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/search?q=apple+iphone+production+benzinga',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Create a session to persist cookies
        session = requests.Session()
        
        # Now visit the actual page
        print(f"Fetching URL: {url}")
        response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"Direct request status code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # Response received successfully
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selectors to find the article content
            article_content = ""
            
            # Try to find article body content
            selectors = [
                '.article-body-container',
                '.article-content', 
                '.article-body', 
                'article',
                '#article-content',
                '.content',
                '.content-article',
                '.story-body',
                'main'
            ]
            
            for selector in selectors:
                content_elements = soup.select(selector)
                if content_elements:
                    for element in content_elements:
                        # Filter out non-essential elements like ads
                        for ad in element.select('.ad-wrap, .ad-container, .banner, .advertisement, .sidebar'):
                            ad.decompose()
                        article_content += element.get_text(separator='\n', strip=True) + "\n\n"
                    break
            
            # If we found content, return it
            if article_content:
                return article_content
            
            # Try to find title and paragraph content
            title_element = soup.select_one('h1.title') or soup.select_one('.title') or soup.select_one('h1')
            if title_element:
                title = title_element.get_text(strip=True)
                article_content = f"{title}\n\n"
            
            # Try to find the author info
            author_element = soup.select_one('.author-name') or soup.select_one('.author') or soup.select_one('.byline')
            if author_element:
                article_content += f"By {author_element.get_text(strip=True)}\n\n"
            
            # Try to find paragraphs
            paragraphs = soup.select('p')
            if paragraphs:
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 30:  # Only include substantial paragraphs
                        # Skip navigation text, footers, etc.
                        if not any(skip in text.lower() for skip in ['cookie', 'privacy policy', 'terms of use', 'copyright', 'all rights reserved']):
                            article_content += text + "\n\n"
            
            if article_content:
                article_content += "(Source: Benzinga)"
                return article_content
                
            return "Could not extract article content from Benzinga. Check the benzinga_response.html file for debugging."
        else:
            return f"Error fetching content: {response.status_code}"
    
    except Exception as e:
        return f"Error extracting Benzinga content: {str(e)}"



async def main(url_list_to_use=None):
    # Standard browser configuration 
    browser_config = BrowserConfig(
        headless=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    
    # Use provided URL list or default
    urls_to_process = url_list_to_use or url_list
    
    # Standard configuration
    standard_config = CrawlerRunConfig(
        wait_until="domcontentloaded",
        verbose=True,
        magic=True,
        simulate_user=True
    )
    
    # Finviz-specific configuration with direct article targeting
    finviz_config = CrawlerRunConfig(
        wait_until="domcontentloaded",
        verbose=True,
        magic=True,
        simulate_user=True,
        js_code="""
        function extractFinvizArticle() {
            // In Finviz, look for the main article content
            try {
                // Check if we're on a Finviz article page
                if (window.location.href.includes('finviz.com/news/')) {
                    // For Finviz, the actual article text might be inside an iframe
                    const frames = document.querySelectorAll('iframe');
                    if (frames.length > 0) {
                        for (let i = 0; i < frames.length; i++) {
                            try {
                                const frameContent = frames[i].contentDocument || frames[i].contentWindow.document;
                                if (frameContent && frameContent.body) {
                                    return frameContent.body.innerText;
                                }
                            } catch (e) {
                                console.log('Error accessing frame:', e);
                            }
                        }
                    }
                    
                    // Look for article content in the main page
                    const articleContent = document.querySelector('div.content-article') || 
                                          document.querySelector('article') || 
                                          document.querySelector('.article-content') ||
                                          document.querySelector('.article') ||
                                          document.querySelector('.post-content');
                    
                    if (articleContent) {
                        return articleContent.innerText;
                    }
                    
                    // Look for blog links that might contain the article
                    const blogLinks = document.querySelectorAll('a[href*="blog"], a[href*="zerohedge"], a[href*="seekingalpha"]');
                    if (blogLinks.length > 0) {
                        // Extract all blog links
                        const links = Array.from(blogLinks).map(link => link.href);
                        return "Article might be at one of these links: " + links.join(', ');
                    }
                }
            } catch (e) {
                console.log('Error extracting Finviz article:', e);
            }
            return null;
        }
        
        const articleContent = extractFinvizArticle();
        if (articleContent) {
            document.body.innerHTML = `<div id="extracted-article">${articleContent}</div>`;
        }
        """
    )
    
    # SeekingAlpha-specific configuration with article targeting
    seeking_alpha_config = CrawlerRunConfig(
        wait_until="domcontentloaded",  # Changed to domcontentloaded to avoid timeout
        verbose=True,
        magic=True,
        simulate_user=True,
        js_code="""
        function extractSeekingAlphaArticle() {
            try {
                // Check if we're on a SeekingAlpha page
                if (window.location.href.includes('seekingalpha.com')) {
                    // Try multiple selectors to find the article content
                    const selectors = [
                        'div[data-test-id="article-content"]', 
                        '.article-content-body', 
                        '.article__content',
                        '#article-content-body',
                        '.paywall-content',
                        'div.contentbox[id*="article"]',
                        '.article-body',
                        '.article'
                    ];
                    
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            // Found article content
                            return element.innerText;
                        }
                    }
                    
                    // If we can't find the main container, try to get elements separately
                    let content = '';
                    
                    // Try to get the title
                    const title = document.querySelector('h1.title') || document.querySelector('.title') || document.querySelector('h1');
                    if (title) {
                        content += title.innerText + '\\n\\n';
                    }
                    
                    // Try to get all paragraphs that might be article content
                    const paragraphs = document.querySelectorAll('p');
                    if (paragraphs && paragraphs.length > 0) {
                        for (let i = 0; i < Math.min(paragraphs.length, 20); i++) {
                            const p = paragraphs[i];
                            if (p.innerText.length > 50) { // Only include substantial paragraphs
                                content += p.innerText + '\\n\\n';
                            }
                        }
                    }
                    
                    if (content) {
                        return content;
                    }
                }
            } catch (e) {
                console.log('Error extracting SeekingAlpha article:', e);
            }
            return null;
        }
        
        const articleContent = extractSeekingAlphaArticle();
        if (articleContent) {
            document.body.innerHTML = `<div id="extracted-article">${articleContent}</div>`;
        }
        """
    )
    
    # Yahoo Finance-specific configuration with article targeting
    yahoo_finance_config = CrawlerRunConfig(
        wait_until="domcontentloaded",
        verbose=True,
        magic=True,
        simulate_user=True,
        js_code="""
        function extractYahooFinanceArticle() {
            try {
                // Check if we're on a Yahoo Finance page
                if (window.location.href.includes('finance.yahoo.com')) {
                    // Try multiple selectors to find the article content
                    const selectors = [
                        '.caas-body',
                        '.article-body',
                        '.canvas-body',
                        '.wafer-caas-body',
                        '.caas-content-wrapper',
                        'article',
                        '.content-inner',
                        '#module-article'
                    ];
                    
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            // Found article content
                            // Filter out any unwanted elements
                            const clone = element.cloneNode(true);
                            const removeSelectors = ['nav', 'header', 'footer', '.ad', '.advertisement', '.promo'];
                            for (const sel of removeSelectors) {
                                const elements = clone.querySelectorAll(sel);
                                for (const el of elements) {
                                    if (el.parentNode) {
                                        el.parentNode.removeChild(el);
                                    }
                                }
                            }
                            return clone.innerText;
                        }
                    }
                    
                    // If we can't find the main container, try to get elements separately
                    let content = '';
                    
                    // Try to get the title
                    const title = document.querySelector('h1') || document.querySelector('.caas-title');
                    if (title) {
                        content += title.innerText + '\\n\\n';
                    }
                    
                    // Try to get all paragraphs that might be article content
                    const paragraphs = document.querySelectorAll('p');
                    if (paragraphs && paragraphs.length > 0) {
                        for (let i = 0; i < paragraphs.length; i++) {
                            const p = paragraphs[i];
                            if (p.innerText.length > 20) { // Only include substantial paragraphs
                                // Skip navigation/footer content
                                const text = p.innerText.toLowerCase();
                                if (!text.includes('cookie') && !text.includes('privacy policy') && 
                                    !text.includes('terms') && !text.includes('copyright')) {
                                    content += p.innerText + '\\n\\n';
                                }
                            }
                        }
                    }
                    
                    if (content) {
                        return content;
                    }
                }
            } catch (e) {
                console.log('Error extracting Yahoo Finance article:', e);
            }
            return null;
        }
        
        const articleContent = extractYahooFinanceArticle();
        if (articleContent) {
            document.body.innerHTML = `<div id="extracted-article">${articleContent}</div>`;
        }
        """
    )
    
    # Benzinga-specific configuration with article targeting
    benzinga_config = CrawlerRunConfig(
        wait_until="domcontentloaded",
        verbose=True,
        magic=True,
        simulate_user=True,
        js_code="""
        function extractBenzingaArticle() {
            try {
                // Check if we're on a Benzinga page
                if (window.location.href.includes('benzinga.com')) {
                    // Try multiple selectors to find the article content
                    const selectors = [
                        '.article-body-container',
                        '.article-content',
                        '.article-body',
                        'article',
                        '#article-content',
                        '.content',
                        '.story-body'
                    ];
                    
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            // Found article content
                            // Filter out any unwanted elements
                            const clone = element.cloneNode(true);
                            const removeSelectors = ['nav', 'header', 'footer', '.ad', '.advertisement'];
                            for (const sel of removeSelectors) {
                                const elements = clone.querySelectorAll(sel);
                                for (const el of elements) {
                                    if (el.parentNode) {
                                        el.parentNode.removeChild(el);
                                    }
                                }
                            }
                            return clone.innerText;
                        }
                    }
                    
                    // If we can't find the main container, try to get elements separately
                    let content = '';
                    
                    // Try to get the title
                    const title = document.querySelector('h1') || document.querySelector('.title');
                    if (title) {
                        content += title.innerText + '\\n\\n';
                    }
                    
                    // Try to get the author
                    const author = document.querySelector('.author-name') || document.querySelector('.author');
                    if (author) {
                        content += 'By ' + author.innerText + '\\n\\n';
                    }
                    
                    // Try to get all paragraphs that might be article content
                    const paragraphs = document.querySelectorAll('p');
                    if (paragraphs && paragraphs.length > 0) {
                        for (let i = 0; i < paragraphs.length; i++) {
                            const p = paragraphs[i];
                            if (p.innerText.length > 20) { // Only include substantial paragraphs
                                // Skip navigation/footer content
                                const text = p.innerText.toLowerCase();
                                if (!text.includes('cookie') && !text.includes('privacy policy') && 
                                    !text.includes('terms') && !text.includes('copyright')) {
                                    content += p.innerText + '\\n\\n';
                                }
                            }
                        }
                    }
                    
                    if (content) {
                        return content;
                    }
                }
            } catch (e) {
                console.log('Error extracting Benzinga article:', e);
            }
            return null;
        }
        
        const articleContent = extractBenzingaArticle();
        if (articleContent) {
            document.body.innerHTML = `<div id="extracted-article">${articleContent}</div>`;
        }
        """
    )
    

    
    # Run crawler for each URL
    all_articles_content = []
    async with AsyncWebCrawler() as crawler:
        for url in urls_to_process:
            article_output = []
            article_output.append(f"\nCrawling: {url}")
            
            try:
                # For SeekingAlpha, directly use our extraction function without the crawler
                if "seekingalpha.com" in url:
                    article_output.append(f"Using direct extraction for SeekingAlpha")
                    domain = url.split('/')[2]
                    article_output.append(f"\n--- ARTICLE FROM {domain.upper()} ---\n")
                    article_output.append(f"URL: {url}")
                    article_content = await extract_seeking_alpha_content(url)
                    article_output.append(article_content)
                    article_output.append("\n" + "-" * 80)
                    all_articles_content.append("\n".join(article_output))
                    continue
                
                # For Yahoo Finance, directly use our extraction function without the crawler
                if "finance.yahoo.com" in url:
                    article_output.append(f"Using direct extraction for Yahoo Finance")
                    domain = url.split('/')[2]
                    article_output.append(f"\n--- ARTICLE FROM {domain.upper()} ---\n")
                    article_output.append(f"URL: {url}")
                    article_content = await extract_yahoo_finance_content(url)
                    article_output.append(article_content)
                    article_output.append("\n" + "-" * 80)
                    all_articles_content.append("\n".join(article_output))
                    continue
                
                # For Benzinga, directly use our extraction function without the crawler
                if "benzinga.com" in url:
                    article_output.append(f"Using direct extraction for Benzinga")
                    domain = url.split('/')[2]
                    article_output.append(f"\n--- ARTICLE FROM {domain.upper()} ---\n")
                    article_output.append(f"URL: {url}")
                    article_content = await extract_benzinga_content(url)
                    article_output.append(article_content)
                    article_output.append("\n" + "-" * 80)
                    all_articles_content.append("\n".join(article_output))
                    continue
                

                
                # For Finviz, directly use our extraction function without the crawler
                if "finviz.com" in url:
                    article_output.append(f"Using direct extraction for Finviz")
                    domain = url.split('/')[2]
                    article_output.append(f"\n--- ARTICLE FROM {domain.upper()} ---\n")
                    article_output.append(f"URL: {url}")
                    article_content = await extract_finviz_content(url)
                    article_output.append(article_content)
                    article_output.append("\n" + "-" * 80)
                    all_articles_content.append("\n".join(article_output))
                    continue
                
                # For other sites, use the crawler
                current_config = standard_config
                current_browser = browser_config
                
                # Use specialized config based on the domain
                if "finviz.com" in url:
                    print(f"Using Finviz-specific configuration")
                    current_config = finviz_config
                elif "finance.yahoo.com" in url:
                    print(f"Using Yahoo Finance-specific configuration")
                    current_config = yahoo_finance_config
                elif "benzinga.com" in url:
                    print(f"Using Benzinga-specific configuration")
                    current_config = benzinga_config
                
                crawler.config = current_browser
                
                # Run the crawler
                result = await crawler.arun(url=url, config=current_config)
                
                if result and result.success:
                    # Extract domain for display
                    domain = url.split('/')[2]
                    article_output.append(f"\n--- ARTICLE FROM {domain.upper()} ---\n")
                    article_output.append(f"URL: {url}")
                    
                    # Show content based on availability
                    if result.markdown and len(result.markdown.strip()) > 0 and "cookie policy" not in result.markdown.lower():
                        article_output.append("MARKDOWN CONTENT:")
                        # Check if this is a navigation menu rather than article content
                        if "finviz.com" in url and len(result.markdown) > 10000:
                            # For Finviz, try alternative extraction method
                            article_output.append("Navigation menu detected. Extracting article content directly...")
                            article_content = await extract_finviz_content(url)
                            article_output.append(article_content)
                        else:
                            # Print regular markdown content
                            article_output.append(result.markdown)
                    # Check for text content as another option
                    elif hasattr(result, 'text') and result.text and len(result.text.strip()) > 0:
                        article_output.append("TEXT CONTENT:")
                        article_output.append(result.text)
                    else:
                        # Search for extracted article content in HTML
                        if result.html:
                            extracted_content = None
                            
                            # Look for our extracted article div
                            match = re.search(r'<div id="extracted-article">(.*?)</div>', result.html, re.DOTALL)
                            if match:
                                extracted_content = match.group(1)
                            
                            if extracted_content:
                                article_output.append("EXTRACTED ARTICLE CONTENT:")
                                article_output.append(extracted_content)
                            else:
                                # No markdown or extracted content, try direct extraction methods
                                if "finviz.com" in url:
                                    article_output.append("Trying direct extraction method for Finviz...")
                                    article_content = await extract_finviz_content(url)
                                    article_output.append(article_content)
                     
                                elif "benzinga.com" in url:
                                    article_output.append("Trying direct extraction method for Benzinga...")
                                    article_content = await extract_benzinga_content(url)
                                    article_output.append(article_content)

                                    article_output.append(article_content)
                                else:
                                    # No extraction method available
                                    article_output.append("No article content extracted.")
                                    article_output.append("\nRAW HTML SNIPPET:")
                                    article_output.append(result.html[:1000] if result.html else "No HTML available")
                                    article_output.append("...")
                    
                else:
                    article_output.append(f"Error: {result.error_message if result else 'No result'}")
            except Exception as e:
                article_output.append(f"Unexpected error: {str(e)}")
            
            article_output.append("\n" + "-" * 80)
            all_articles_content.append("\n".join(article_output))
    
    return "\n".join(all_articles_content)

async def get_stock_news(ticker_symbol,file_path):
    """
    Extracts stock news articles from URLs found in the specified file.
    
    Args:
        file_path (str): Path to the file containing URLs, one per line.
                         Defaults to RELEVANT_ARTICLES_FILE from config.
    
    Returns:
        str: A formatted string containing all the extracted articles with clear separations.
    """
   
    company_name = ""
    try:
        company_name = get_company_name(ticker_symbol)
    except Exception as e:
        print(f"Error getting company name: {e}")
        company_name = ticker_symbol  # Fallback to symbol if name lookup fails
    
 
    # Extract URLs from the file
    extracted_urls = []
    
    with open(file_path, 'r') as file:
        content = file.read()
        # Find all URLs in the content
        url_pattern = r'https?://[^\s<>"\']+'
        extracted_urls = re.findall(url_pattern, content)
    
    if not extracted_urls:
        return f"No URLs found in {file_path}"
    
    # Filter out GuruFocus URLs completely
    filtered_urls = []
    for url in extracted_urls:
        if "gurufocus.com" not in url.lower():
            filtered_urls.append(url)
    
    if not filtered_urls:
        return f"No valid URLs found in {file_path} (GuruFocus URLs are excluded)"
    
    # Process the articles and get the content
    result = await main(filtered_urls)
    
    # Clean up the output to match the required format
    cleaned_result = []
    
    for article in result.split("-" * 80):
        if not article.strip():
            continue
            
        article_lines = article.strip().split('\n')
        cleaned_article = []
        
        article_title = None
        url_line = None
        source_domain = None
        
        # Process the basic metadata first
        for line in article_lines:
            if "--- ARTICLE FROM" in line:
                source_domain = line.strip().replace("--- ARTICLE FROM ", "").replace(" ---", "")
            elif line.startswith("URL:"):
                url_line = line.strip()
                
        # Skip if we don't have basic URL info
        if not url_line:
            continue
            
        # Process content based on source domain
        if "BENZINGA.COM" in (source_domain or ""):
            # Handle Benzinga specific content
            title_found = False
            content_lines = []
            
            for line in article_lines:
                # Skip crawling info and other metadata
                if "Crawling:" in line or "Fetching URL:" in line or "Direct request" in line or "Final URL:" in line:
                    continue
                    
                # Generic title finding from content - first substantial line after URL and metadata
                if not title_found and not line.startswith("URL:") and len(line.strip()) > 10 and "Using direct" not in line and "--- ARTICLE FROM" not in line:
                    # This is likely the title
                    if not line.startswith("Crawling:"):
                        article_title = line.strip()
                        title_found = True
                elif title_found and ("By" in line and len(line) < 50) or "Benzinga" in line:
                    # Start collecting content after we've found the author/byline
                    content_lines.append(line)
                elif len(content_lines) > 0:
                    # Skip footer content but keep the rest
                    if any(skip in line for skip in ["Benzinga Rankings", "Trade confidently", "A newsletter built", "Disclosure:"]):
                        continue
                    content_lines.append(line)
        
        elif "FINVIZ.COM" in (source_domain or ""):
            # Handle Finviz specific content
            title_found = False
            content_lines = []
            
            for line in article_lines:
                # Skip crawling info and other metadata
                if "Crawling:" in line or "Fetching URL:" in line or "Direct request" in line or "Final URL:" in line or "Using direct" in line:
                    continue
                    
                # Look for title - first substantial line after URL and metadata
                if not title_found and not line.startswith("URL:") and len(line.strip()) > 10 and "--- ARTICLE FROM" not in line and line.startswith("Title:"):
                    article_title = line.replace("Title:", "").strip()
                    title_found = True
                    continue
                elif title_found:
                    # Collect content after title
                    if line.strip() and not line.startswith("URL:") and "--- ARTICLE FROM" not in line:
                        content_lines.append(line)
        
        else:
            # Handle general content (other sources)
            content_start = False
            content_lines = []
            
            for i, line in enumerate(article_lines):
                if any(marker in line for marker in ["MARKDOWN CONTENT:", "TEXT CONTENT:", "EXTRACTED ARTICLE CONTENT:", "Navigation menu detected."]):
                    content_start = True
                    continue
                elif content_start:
                    # Skip diagnostic and UI lines
                    if not any(skip in line for skip in [
                        "Crawling:", "Using direct", "Trying direct", "Error:", "RAW HTML SNIPPET", 
                        "No article content extracted", "Unexpected error:"
                    ]) and not any(ui_text in line.lower() for skip_patterns in [
                        ["cookie", "privacy policy", "terms of use", "copyright", "all rights reserved"],
                        ["benzinga rankings", "give you vital metrics", "trade confidently", "newsletter built for"],
                        ["see the 10 stocks", "stock advisor returns as of", "motley fool", "disclosure policy"],
                        ["mentioned in this article", "latest news"]
                    ] for ui_text in skip_patterns):
                        # If this is likely the title (first non-empty line of content)
                        if not article_title and line.strip() and len(content_lines) == 0:
                            article_title = line.strip()
                        else:
                            content_lines.append(line)
        
        # Format the output according to requirements
        if article_title and url_line:
            cleaned_article.append(f"Title: {article_title}")
            cleaned_article.append(url_line)
            
            if len(content_lines) > 0:
                # Clean up content - remove consecutive empty lines
                content_text = "\n".join(content_lines)
                content_text = re.sub(r'\n\s*\n', '\n\n', content_text)
                
                # Remove any "Latest News" sections and everything after them
                if "Latest News" in content_text:
                    content_text = content_text.split("Latest News")[0]
                
                # Remove stock promotion sections
                if "Should you invest $1,000 in " in content_text:
                    content_text = content_text.split("Should you invest $1,000 in ")[0]
                
                cleaned_article.append(content_text)
                cleaned_result.append("\n".join(cleaned_article))
    
    if not cleaned_result:
        return "No article content could be extracted from the provided URLs."
    
    # Add proper spacing between separator and content
    formatted_result = []
    
    for article in cleaned_result:
        formatted_result.append(article)
    
    return "\n\n" + "-" * 80 + "\n\n".join(formatted_result)


def get_stock_news_sync(ticker_symbol, file_path):
    """
    Synchronous wrapper for get_stock_news that maintains backward compatibility.
    
    Args:
        ticker_symbol: Stock symbol to get news for
        file_path: Path to the file containing URLs
    
    Returns:
        str: Formatted string containing extracted articles
    """
    return asyncio.run(get_stock_news(ticker_symbol, file_path))