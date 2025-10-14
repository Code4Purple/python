# news_scraper.py
import requests
import sqlite3
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import logging
import random

# Create db directory if it doesn't exist
DB_DIR = "db"
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Set up logging to db folder
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
        Initialize the news scraper with clean folder structure
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
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def get_default_sources(self) -> List[Dict]:
        """Default news sources if config file is missing"""
        return [
            {
                'name': 'BBC News',
                'base_url': 'https://www.bbc.com',
                'url': 'https://www.bbc.com/news',
                'selectors': {
                    'article_links': 'a[href*="/news/"]',
                    'title': 'h1',
                    'content': 'article'
                }
            },
            {
                'name': 'Reuters',
                'base_url': 'https://www.reuters.com',
                'url': 'https://www.reuters.com/world/',
                'selectors': {
                    'article_links': 'a[href*="/world/"]',
                    'title': 'h1',
                    'content': 'div[data-testid="ArticleBody"]'
                }
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
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_collected_at ON news_articles(collected_at)
        ''')
        
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
    
    def get_collection_window(self) -> tuple:
        """Get the time window for data collection"""
        now = datetime.now()
        
        # If this is first run or no previous data, collect last 24 hours
        if not self.last_collection_time:
            from_time = now - timedelta(hours=24)
            logger.info("First collection - will collect last 24 hours of data")
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
        }
    
    def scrape_page(self, url: str) -> Optional[BeautifulSoup]:
        """Scrape a webpage and return BeautifulSoup object"""
        try:
            headers = self.get_random_headers()
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_source_articles(self, source_config: Dict) -> List[Dict]:
        """Scrape articles from a specific news source"""
        articles = []
        source_name = source_config.get('name', 'Unknown')
        logger.info(f"Scraping {source_name}...")
        
        soup = self.scrape_page(source_config['url'])
        if not soup:
            return articles
        
        try:
            # Find article links based on selectors
            link_selector = source_config['selectors'].get('article_links', 'a')
            article_links = soup.select(link_selector)
            
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
                            articles.append(article_data)
                            processed_urls.append(full_url)
                    
                    # Be respectful - add delay
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error processing link from {source_name}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping source {source_name}: {e}")
        
        logger.info(f"Scraped {len(articles)} articles from {source_name}")
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
                content = ' '.join([p.get_text().strip() for p in paragraphs[:15]])
            
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
                    (title, description, content, url, source, published_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    article.get('title', ''),
                    article.get('description', ''),
                    article.get('content', ''),
                    article.get('url', ''),
                    article.get('source', 'Unknown'),
                    article.get('published_at')
                ))
                
                if cursor.rowcount > 0:
                    stored_count += 1
                    
            except Exception as e:
                logger.error(f"Error storing article from {article.get('source', 'Unknown')}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Stored {stored_count} new articles in database")
        return stored_count
    
    def collect_data_since_last_collection(self) -> int:
        """Collect data from last collection time to current time"""
        logger.info("Starting data collection...")
        
        from_time, to_time = self.get_collection_window()
        
        total_articles = 0
        
        # Scrape all configured sources
        for source in self.news_sources:
            try:
                articles = self.scrape_source_articles(source)
                stored_count = self.store_articles(articles)
                total_articles += stored_count
                time.sleep(2)  # Be extra respectful between sources
            except Exception as e:
                logger.error(f"Error collecting from {source.get('name', 'Unknown')}: {e}")
        
        logger.info(f"Data collection completed. Total new articles: {total_articles}")
        return total_articles
    
    def get_articles_since_last_collection(self) -> List[Dict]:
        """Get articles collected since last collection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if self.last_collection_time:
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at
                FROM news_articles 
                WHERE collected_at >= ?
                ORDER BY collected_at DESC
            ''', (self.last_collection_time.isoformat(),))
        else:
            # If no last collection time, get last 24 hours
            since_time = datetime.now() - timedelta(hours=24)
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at
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
                'collected_at': row[6]
            })
        
        conn.close()
        return articles
    
    def get_all_articles(self, limit: int = 1000) -> List[Dict]:
        """Get all articles from database (with limit)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, description, content, url, source, published_at, collected_at
            FROM news_articles 
            ORDER BY collected_at DESC
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
                'collected_at': row[6]
            })
        
        conn.close()
        return articles
    
    def run_collection(self):
        """Run data collection (this is the main function to call)"""
        logger.info("=" * 60)
        logger.info("NEWS DATA COLLECTION STARTED")
        logger.info("=" * 60)
        
        # Show collection window
        from_time, to_time = self.get_collection_window()
        logger.info(f"Collection window: {from_time} to {to_time}")
        
        # Collect data
        collected_count = self.collect_data_since_last_collection()
        
        # Get articles from this session
        recent_articles = self.get_articles_since_last_collection()
        
        logger.info("=" * 60)
        logger.info("COLLECTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"New articles collected: {collected_count}")
        logger.info(f"Articles available for processing: {len(recent_articles)}")
        logger.info("=" * 60)
        
        return {
            'new_articles': collected_count,
            'total_available': len(recent_articles),
            'articles': recent_articles
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


