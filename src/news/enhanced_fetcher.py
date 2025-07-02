"""News fetcher with improved error handling for API requests"""
import aiohttp
import asyncio
import logging
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)


class NewsAPIError(Exception):
    """Custom exception for news API errors"""
    pass


class EnhancedNewsFetcher:
    """Enhanced news fetcher with robust error handling"""
    
    def __init__(self):
        self.timeout = 10.0
        self.max_retries = 3
        self.session = None
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for problematic APIs
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_coindesk_news(self) -> List[Dict]:
        """Fetch news from CoinDesk with error handling"""
        try:
            # Use alternative endpoint if main API is down
            urls = [
                "https://api.coindesk.com/v1/bpi/currentprice.json",  # Fallback endpoint
                "https://www.coindesk.com/arc/outboundfeeds/rss/"    # RSS fallback
            ]
            
            for url in urls:
                try:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            content_type = response.headers.get('content-type', '').lower()
                            
                            if 'application/json' in content_type:
                                data = await response.json()
                                return self._parse_coindesk_json(data)
                            else:
                                # Handle RSS or HTML response
                                text = await response.text()
                                return self._parse_coindesk_text(text)
                                
                except aiohttp.ClientConnectionError as e:
                    logger.warning(f"CoinDesk connection failed for {url}: {e}")
                    continue
                except aiohttp.ClientResponseError as e:
                    logger.warning(f"CoinDesk HTTP error for {url}: {e}")
                    continue
                
            # If all URLs fail, return empty list
            logger.error("All CoinDesk endpoints failed")
            return []
            
        except Exception as e:
            logger.error(f"CoinDesk fetch error: {e}")
            return []
    
    async def fetch_cointelegraph_news(self) -> List[Dict]:
        """Fetch news from Cointelegraph with improved error handling"""
        try:
            # Try multiple endpoints
            urls = [
                "https://cointelegraph.com/rss",
                "https://cointelegraph.com/api/v1/content"
            ]
            
            for url in urls:
                try:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            content_type = response.headers.get('content-type', '').lower()
                            
                            if 'application/json' in content_type:
                                try:
                                    data = await response.json()
                                    return self._parse_cointelegraph_json(data)
                                except json.JSONDecodeError as e:
                                    logger.warning(f"Cointelegraph JSON decode error: {e}")
                                    # Try to parse as text
                                    text = await response.text()
                                    return self._parse_cointelegraph_text(text)
                            else:
                                # Handle non-JSON response (likely HTML/RSS)
                                text = await response.text()
                                return self._parse_cointelegraph_text(text)
                                
                        elif response.status == 403:
                            logger.warning(f"Cointelegraph 403 Forbidden for {url}, trying alternative")
                            continue
                        else:
                            logger.warning(f"Cointelegraph returned status {response.status} for {url}")
                            continue
                            
                except aiohttp.ClientError as e:
                    logger.warning(f"Cointelegraph request error for {url}: {e}")
                    continue
            
            logger.error("All Cointelegraph endpoints failed")
            return []
            
        except Exception as e:
            logger.error(f"Cointelegraph fetch error: {e}")
            return []
    
    def _parse_coindesk_json(self, data: Dict) -> List[Dict]:
        """Parse CoinDesk JSON response"""
        try:
            # Handle different JSON structures
            if 'bpi' in data:  # Price API response
                return [{
                    'title': 'Bitcoin Price Update',
                    'description': f"Bitcoin price: {data['bpi']['USD']['rate']}",
                    'source': 'coindesk',
                    'sentiment': 'neutral'
                }]
            elif 'articles' in data:
                return [self._normalize_article(article, 'coindesk') for article in data['articles']]
            else:
                return []
        except Exception as e:
            logger.error(f"Error parsing CoinDesk JSON: {e}")
            return []
    
    def _parse_coindesk_text(self, text: str) -> List[Dict]:
        """Parse CoinDesk text/RSS response"""
        try:
            # Simple text parsing for RSS-like content
            if 'bitcoin' in text.lower() or 'crypto' in text.lower():
                return [{
                    'title': 'CoinDesk News Update',
                    'description': text[:200] + '...' if len(text) > 200 else text,
                    'source': 'coindesk',
                    'sentiment': 'neutral'
                }]
            return []
        except Exception as e:
            logger.error(f"Error parsing CoinDesk text: {e}")
            return []
    
    def _parse_cointelegraph_json(self, data: Dict) -> List[Dict]:
        """Parse Cointelegraph JSON response"""
        try:
            if isinstance(data, list):
                return [self._normalize_article(article, 'cointelegraph') for article in data]
            elif 'data' in data:
                return [self._normalize_article(article, 'cointelegraph') for article in data['data']]
            else:
                return []
        except Exception as e:
            logger.error(f"Error parsing Cointelegraph JSON: {e}")
            return []
    
    def _parse_cointelegraph_text(self, text: str) -> List[Dict]:
        """Parse Cointelegraph text/HTML response"""
        try:
            # Simple text parsing for HTML content
            if 'bitcoin' in text.lower() or 'crypto' in text.lower() or 'blockchain' in text.lower():
                return [{
                    'title': 'Cointelegraph News Update', 
                    'description': text[:200] + '...' if len(text) > 200 else text,
                    'source': 'cointelegraph',
                    'sentiment': 'neutral'
                }]
            return []
        except Exception as e:
            logger.error(f"Error parsing Cointelegraph text: {e}")
            return []
    
    def _normalize_article(self, article: Dict, source: str) -> Dict:
        """Normalize article data structure"""
        return {
            'title': article.get('title', article.get('headline', 'No title')),
            'description': article.get('description', article.get('summary', article.get('content', ''))),
            'source': source,
            'url': article.get('url', ''),
            'sentiment': 'neutral'  # Will be analyzed later
        }


async def fetch_all_news() -> List[Dict]:
    """Fetch news from all sources with error handling"""
    all_news = []
    
    async with EnhancedNewsFetcher() as fetcher:
        try:
            # Fetch from CoinDesk
            coindesk_news = await fetcher.fetch_coindesk_news()
            all_news.extend(coindesk_news)
            logger.info(f"Fetched {len(coindesk_news)} articles from CoinDesk")
        except Exception as e:
            logger.error(f"CoinDesk fetch failed: {e}")
        
        try:
            # Fetch from Cointelegraph
            cointelegraph_news = await fetcher.fetch_cointelegraph_news()
            all_news.extend(cointelegraph_news)
            logger.info(f"Fetched {len(cointelegraph_news)} articles from Cointelegraph")
        except Exception as e:
            logger.error(f"Cointelegraph fetch failed: {e}")
    
    logger.info(f"Total articles fetched: {len(all_news)}")
    return all_news


# Test function
async def test_news_fetching():
    """Test the news fetching functionality"""
    try:
        news = await fetch_all_news()
        print(f"Successfully fetched {len(news)} news articles")
        for article in news[:3]:  # Show first 3 articles
            print(f"- {article['title']} ({article['source']})")
    except Exception as e:
        print(f"News fetching test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_news_fetching())