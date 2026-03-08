# news_scraper.py (updated collection methods)
import requests
import sqlite3
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import logging
import random
import os

# Set up logging
DB_DIR = "db"
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(DB_DIR, 'news_scraper.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self, db_path: str = os.path.join(DB_DIR, "news_data.db")):
        """
        News scraper with multiple collection strategies and detailed logging
        """
        self.db_path = db_path
        self.setup_database()
        self.last_collection_time = self.get_last_collection_time()
        
        # Load news sources from external file
        try:
            from news_sources import NEWS_SOURCES
            self.news_sources = NEWS_SOURCES
            logger.info(f"Loaded {len(self.news_sources)} news sources")
        except ImportError:
            logger.warning("news_sources.py not found, using default sources")
            self.news_sources = self.get_default_sources()
        
        # User agents to rotate and avoid blocking
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    def get_default_sources(self) -> List[Dict]:
        """Default news sources with archive support"""
        return [
            {
                'name': 'BBC News',
                'base_url': 'https://www.bbc.com',
                'url': 'https://www.bbc.com/news',
                'archive_url_pattern': 'https://www.bbc.com/news/archive/{year}-{month:02d}-{day:02d}',
                'selectors': {
                    'article_links': 'a[href*="/news/"]',
                    'title': 'h1',
                    'content': ['div[data-component="text-block"]', 'article']
                },
                'supports_archive': True,
                'max_articles': 20
            },
            {
                'name': 'Reuters',
                'base_url': 'https://www.reuters.com',
                'url': 'https://www.reuters.com/world/',
                'archive_url_pattern': 'https://www.reuters.com/world/archive/{year}-{month:02d}-{day:02d}/',
                'selectors': {
                    'article_links': 'a[href*="/world/"]',
                    'title': 'h1',
                    'content': ['div[data-testid="ArticleBody"]', 'div[class*="ArticleBody"]']
                },
                'supports_archive': True,
                'max_articles': 20
            }
        ]
    
    def setup_database(self):
        """Create database table for news articles"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT,
                url TEXT UNIQUE,
                source TEXT,
                published_at TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                collection_method TEXT
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_collected_at ON news_articles(collected_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_published_at ON news_articles(published_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON news_articles(source)')
        
        conn.commit()
        conn.close()
        logger.info("Database setup completed")
        logger.info(f"Database location: {self.db_path}")
    
    def get_last_collection_time(self) -> Optional[datetime]:
        """Get the timestamp of the last collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT MAX(collected_at) FROM news_articles')
        result = cursor.fetchone()[0]
        
        conn.close()
        
        if result:
            try:
                return datetime.fromisoformat(result.replace('Z', '+00:00'))
            except:
                return None
        return None
    
    def get_collection_window(self, initial_collection_days: int = 365*10) -> tuple:
        """Get the time window for data collection"""
        now = datetime.now()
        
        # If this is first run or no previous data, collect default period
        if not self.last_collection_time:
            from_time = now - timedelta(days=initial_collection_days)
            logger.info(f"First collection - will collect last {initial_collection_days} days of data")
        else:
            from_time = self.last_collection_time
            logger.info(f"Collecting data from {from_time} to {now}")
        
        return from_time, now
    
    def get_random_headers(self) -> Dict[str, str]:
        """Get random headers to avoid blocking"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
        }
    
    def scrape_page(self, url: str) -> Optional[BeautifulSoup]:
        """Scrape a webpage and return BeautifulSoup object"""
        try:
            headers = self.get_random_headers()
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_current_news(self, source_config: Dict) -> List[Dict]:
        """Scrape current news from main pages"""
        articles = []
        source_name = source_config.get('name', 'Unknown')
        logger.info(f"Scraping current news from {source_name}...")
        
        soup = self.scrape_page(source_config['url'])
        if not soup:
            logger.warning(f"Failed to scrape {source_name} main page")
            return articles
        
        try:
            # Find article links based on selectors
            link_selector = source_config['selectors'].get('article_links', 'a')
            article_links = soup.select(link_selector)
            
            logger.info(f"Found {len(article_links)} potential article links from {source_name}")
            
            processed_urls = []
            max_articles = source_config.get('max_articles', 15)
            
            for link in article_links[:max_articles]:
                try:
                    href = link.get('href')
                    if not href:
                        continue
                    
                    # Make absolute URL
                    if href.startswith('/'):
                        full_url = urljoin(source_config['base_url'], href)
                    else:
                        full_url = href
                    
                    # Validate URL
                    if source_config['base_url'] in full_url and full_url not in processed_urls:
                        article_data = self.scrape_article(full_url, source_config)
                        if article_data:
                            article_data['collection_method'] = 'current'
                            articles.append(article_data)
                            processed_urls.append(full_url)
                    
                    # Be respectful - add delay
                    time.sleep(1)
                    
                except Exception as e:
                    logger.debug(f"Error processing link from {source_name}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping source {source_name}: {e}")
        
        logger.info(f"✓ Successfully scraped {len(articles)} articles from {source_name}")
        return articles
    
    def scrape_historical_archive(self, source_config: Dict, target_date: datetime) -> List[Dict]:
        """Scrape historical news from archive pages"""
        if not source_config.get('supports_archive', False):
            logger.debug(f"{source_config['name']} does not support archive scraping")
            return []
        
        articles = []
        source_name = source_config.get('name', 'Unknown')
        
        # Generate archive URL
        try:
            archive_url = source_config['archive_url_pattern'].format(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day
            )
        except KeyError:
            logger.warning(f"No archive URL pattern for {source_name}")
            return articles
        
        logger.info(f"Scraping archive for {source_name} - {target_date.strftime('%Y-%m-%d')}")
        
        soup = self.scrape_page(archive_url)
        if not soup:
            logger.debug(f"No archive data found for {source_name} on {target_date.strftime('%Y-%m-%d')}")
            return articles
        
        try:
            # Find article links in archive
            link_selector = source_config['selectors'].get('article_links', 'a')
            article_links = soup.select(link_selector)
            
            logger.info(f"Found {len(article_links)} potential historical articles from {source_name}")
            
            processed_urls = []
            max_articles = source_config.get('max_articles', 10)
            
            for link in article_links[:max_articles]:
                try:
                    href = link.get('href')
                    if not href:
                        continue
                    
                    # Make absolute URL
                    if href.startswith('/'):
                        full_url = urljoin(source_config['base_url'], href)
                    else:
                        full_url = href
                    
                    # Validate URL
                    if source_config['base_url'] in full_url and full_url not in processed_urls:
                        article_data = self.scrape_article(full_url, source_config)
                        if article_data:
                            # Set the historical date
                            article_data['published_at'] = target_date.isoformat()
                            article_data['collection_method'] = 'archive'
                            articles.append(article_data)
                            processed_urls.append(full_url)
                    
                    # Be respectful - add delay
                    time.sleep(1.5)
                    
                except Exception as e:
                    logger.debug(f"Error processing archive link from {source_name}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping archive for {source_name}: {e}")
        
        if articles:
            logger.info(f"✓ Successfully scraped {len(articles)} historical articles from {source_name}")
        else:
            logger.info(f"○ No historical articles found for {source_name} on {target_date.strftime('%Y-%m-%d')}")
        
        return articles
    
    def scrape_article(self, url: str, source_config: Dict) -> Optional[Dict]:
        """Scrape individual article from any source"""
        soup = self.scrape_page(url)
        if not soup:
            return None
        
        try:
            # Extract title
            title_selector = source_config['selectors'].get('title', 'h1')
            title_elem = soup.select_one(title_selector)
            title = title_elem.get_text().strip() if title_elem else "No title"
            
            # Extract content
            content = ""
            content_selectors = source_config['selectors'].get('content', [])
            if isinstance(content_selectors, str):
                content_selectors = [content_selectors]
            
            # Try multiple content selectors
            for selector in content_selectors:
                content_elements = soup.select(selector)
                if content_elements:
                    content = ' '.join([elem.get_text().strip() for elem in content_elements])
                    break
            
            # Fallback to paragraphs if no specific content selector works
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs[:20]])
            
            # Extract description (first part of content)
            description = content[:300] + "..." if len(content) > 300 else content
            
            return {
                'title': title,
                'description': description,
                'content': content,
                'url': url,
                'source': source_config.get('name', 'Unknown'),
                'published_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    def store_articles(self, articles: List[Dict]) -> int:
        """Store articles in database"""
        if not articles:
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stored_count = 0
        
        for article in articles:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO news_articles 
                    (title, description, content, url, source, published_at, collection_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article.get('title', ''),
                    article.get('description', ''),
                    article.get('content', ''),
                    article.get('url', ''),
                    article.get('source', 'Unknown'),
                    article.get('published_at'),
                    article.get('collection_method', 'unknown')
                ))
                
                if cursor.rowcount > 0:
                    stored_count += 1
                    
            except Exception as e:
                logger.error(f"Error storing article from {article.get('source', 'Unknown')}: {e}")
        
        conn.commit()
        conn.close()
        
        return stored_count
    
    def collect_historical_data(self, from_date: datetime, to_date: datetime) -> Dict[str, int]:
        """Collect historical data by date range with detailed source tracking"""
        logger.info(f"Starting historical data collection: {from_date.date()} to {to_date.date()}")
        logger.info(f"Total days to process: {(to_date - from_date).days + 1}")
        
        source_stats = {source['name']: 0 for source in self.news_sources}
        total_articles = 0
        current_date = from_date
        
        # Collect data day by day for better organization
        day_count = 0
        total_days = (to_date - from_date).days + 1
        
        while current_date <= to_date:
            day_count += 1
            progress_percent = (day_count / total_days) * 100
            logger.info(f"Processing date: {current_date.strftime('%Y-%m-%d')} ({progress_percent:.1f}% complete)")
            
            daily_stats = {}
            
            # For each source, try archive scraping first, then current scraping
            for source in self.news_sources:
                source_name = source['name']
                try:
                    # Try archive scraping for historical dates
                    if current_date.date() < datetime.now().date():
                        articles = self.scrape_historical_archive(source, current_date)
                    else:
                        # For today, use current news scraping
                        articles = self.scrape_current_news(source)
                    
                    stored_count = self.store_articles(articles)
                    source_stats[source_name] += stored_count
                    daily_stats[source_name] = stored_count
                    total_articles += stored_count
                    
                    # Be extra respectful between sources and dates
                    time.sleep(3)
                    
                except Exception as e:
                    logger.error(f"Error collecting from {source_name}: {e}")
            
            # Log daily summary
            daily_total = sum(daily_stats.values())
            if daily_total > 0:
                logger.info(f"  Daily summary for {current_date.strftime('%Y-%m-%d')}: {daily_total} articles")
                for source_name, count in daily_stats.items():
                    if count > 0:
                        logger.info(f"    {source_name}: {count} articles")
            else:
                logger.info(f"  No articles found for {current_date.strftime('%Y-%m-%d')}")
            
            current_date += timedelta(days=1)
        
        logger.info("=" * 60)
        logger.info("HISTORICAL COLLECTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total articles collected: {total_articles}")
        logger.info("Articles by source:")
        for source_name, count in source_stats.items():
            logger.info(f"  {source_name}: {count} articles")
        logger.info("=" * 60)
        
        return source_stats
    
    def collect_data_since_last_collection(self, initial_collection_days: int = 365*10) -> Dict[str, int]:
        """Collect data from last collection time to current time with source tracking"""
        from_time, to_time = self.get_collection_window(initial_collection_days)
        
        # For large time ranges, collect in chunks
        if (to_time - from_time).days > 30:  # More than 30 days
            logger.info("Large time range detected, using chunked collection...")
            return self.collect_historical_data(from_time, to_time)
        else:
            # Standard collection for smaller ranges
            logger.info("Starting standard data collection...")
            
            source_stats = {source['name']: 0 for source in self.news_sources}
            total_articles = 0
            
            # Scrape all configured sources for current news
            for source in self.news_sources:
                source_name = source['name']
                try:
                    articles = self.scrape_current_news(source)
                    stored_count = self.store_articles(articles)
                    source_stats[source_name] = stored_count
                    total_articles += stored_count
                    logger.info(f"✓ {source_name}: {stored_count} articles")
                    time.sleep(2)  # Be extra respectful between sources
                except Exception as e:
                    logger.error(f"Error collecting from {source_name}: {e}")
            
            logger.info("=" * 50)
            logger.info("STANDARD COLLECTION SUMMARY")
            logger.info("=" * 50)
            logger.info(f"Total articles collected: {total_articles}")
            logger.info("Articles by source:")
            for source_name, count in source_stats.items():
                logger.info(f"  {source_name}: {count} articles")
            logger.info("=" * 50)
            
            return source_stats
    
    def get_articles_since_last_collection(self) -> List[Dict]:
        """Get articles collected since last collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if self.last_collection_time:
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at, collection_method
                FROM news_articles 
                WHERE collected_at >= ?
                ORDER BY collected_at DESC
            ''', (self.last_collection_time.isoformat(),))
        else:
            # If no last collection time, get last 10 years
            since_time = datetime.now() - timedelta(days=365*10)
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at, collection_method
                FROM news_articles 
                WHERE collected_at >= ?
                ORDER BY collected_at DESC
            ''', (since_time.isoformat(),))
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                'title': row[0],
                'description': row[1],
                'content': row[2],
                'url': row[3],
                'source': row[4],
                'published_at': row[5],
                'collected_at': row[6],
                'collection_method': row[7]
            })
        
        conn.close()
        return articles
    
    def get_all_articles(self, limit: int = 10000) -> List[Dict]:
        """Get all articles from database (with limit)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, description, content, url, source, published_at, collected_at, collection_method
            FROM news_articles 
            ORDER BY published_at DESC
            LIMIT ?
        ''', (limit,))
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                'title': row[0],
                'description': row[1],
                'content': row[2],
                'url': row[3],
                'source': row[4],
                'published_at': row[5],
                'collected_at': row[6],
                'collection_method': row[7]
            })
        
        conn.close()
        return articles
    
    def run_collection(self, initial_collection_days: int = 365*10):
        """Run data collection with enhanced historical support and detailed logging"""
        logger.info("=" * 70)
        logger.info("NEWS DATA COLLECTION STARTED")
        logger.info("=" * 70)
        
        # Show collection window
        from_time, to_time = self.get_collection_window(initial_collection_days)
        logger.info(f"Collection window: {from_time} to {to_time}")
        logger.info(f"Days to collect: {(to_time - from_time).days}")
        
        # Collect data
        source_stats = self.collect_data_since_last_collection(initial_collection_days)
        
        # Get articles from this session
        recent_articles = self.get_articles_since_last_collection()
        
        logger.info("=" * 70)
        logger.info("FINAL COLLECTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"New articles collected: {len(recent_articles)}")
        logger.info("Collection breakdown by source:")
        for source_name, count in source_stats.items():
            percentage = (count / len(recent_articles) * 100) if len(recent_articles) > 0 else 0
            logger.info(f"  {source_name}: {count} articles ({percentage:.1f}%)")
        logger.info("=" * 70)
        
        return {
            'new_articles': len(recent_articles),
            'total_available': len(recent_articles),
            'articles': recent_articles,
            'source_breakdown': source_stats,
            'collection_period': {
                'from': from_time.isoformat(),
                'to': to_time.isoformat(),
                'days': (to_time - from_time).days
            }
        }

# Utility functions
def urljoin(base: str, url: str) -> str:
    """Simple URL join function"""
    if url.startswith('http'):
        return url
    if base.endswith('/') and url.startswith('/'):
        return base[:-1] + url
    if not base.endswith('/') and not url.startswith('/'):
        return base + '/' + url
    return base + url

