# enhanced_news_scraper.py
import requests
import sqlite3
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import logging
import random
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedNewsScraper:
    def __init__(self, db_path: str = "news_data.db", state_file: str = "scraper_state.json"):
        """
        Initialize the enhanced news scraper with state tracking
        """
        self.db_path = db_path
        self.state_file = state_file
        self.setup_database()
        self.last_launch_time = self.get_last_launch_time()
        self.last_run_state = self.load_state()
        
        # Load news sources
        try:
            from news_sources import NEWS_SOURCES
            self.news_sources = NEWS_SOURCES
            logger.info(f"Loaded {len(self.news_sources)} news sources")
        except ImportError:
            logger.warning("news_sources.py not found, using default sources")
            self.news_sources = self.get_default_sources()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
                sentiment_score REAL,
                category TEXT
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_published_at ON news_articles(published_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_collected_at ON news_articles(collected_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON news_articles(source)')
        
        conn.commit()
        conn.close()
        logger.info("Database setup completed")
    
    def load_state(self) -> Dict:
        """Load scraper state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading state: {e}")
        return {}
    
    def save_state(self, state: Dict):
        """Save scraper state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def get_last_launch_time(self) -> Optional[datetime]:
        """Get the timestamp of the last launch from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT MAX(collected_at) FROM news_articles')
        result = cursor.fetchone()[0]
        
        conn.close()
        
        if result:
            try:
                # Handle different datetime formats
                if 'T' in result:
                    return datetime.fromisoformat(result.replace('Z', '+00:00'))
                else:
                    return datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.now() - timedelta(hours=1)  # Default to 1 hour ago
        return None
    
    def get_time_window(self) -> tuple:
        """Get the time window for data collection"""
        now = datetime.now()
        
        # If this is first run or no previous data, collect last 24 hours
        if not self.last_launch_time:
            from_time = now - timedelta(hours=24)
            logger.info("First run detected - will collect last 24 hours of data")
        else:
            from_time = self.last_launch_time
            logger.info(f"Collecting data from {from_time} to {now}")
        
        return from_time, now
    
    def should_process_article(self, article_data: Dict) -> bool:
        """Determine if article should be processed based on time and duplicates"""
        # Check if article already exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM news_articles WHERE url = ?', (article_data['url'],))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        
        if exists:
            logger.debug(f"Skipping duplicate article: {article_data['title'][:50]}...")
            return False
        
        # For scraping, we can't easily filter by exact publish time
        # But we can use the collection time as a proxy
        return True
    
    def collect_historical_data(self) -> int:
        """Collect historical data since last launch"""
        logger.info("Starting historical data collection...")
        
        from_time, to_time = self.get_time_window()
        
        # Update state
        current_state = {
            'last_collection_start': from_time.isoformat(),
            'last_collection_end': to_time.isoformat(),
            'collection_type': 'historical'
        }
        self.save_state(current_state)
        
        total_articles = 0
        
        # Scrape all configured sources
        for source in self.news_sources:
            try:
                logger.info(f"Processing {source['name']}...")
                articles = self.scrape_source_articles(source)
                
                # Filter articles by time (best effort)
                filtered_articles = []
                for article in articles:
                    # We'll store all articles but note the collection time
                    article['collection_window_start'] = from_time.isoformat()
                    article['collection_window_end'] = to_time.isoformat()
                    filtered_articles.append(article)
                
                stored_count = self.store_articles(filtered_articles)
                total_articles += stored_count
                time.sleep(2)  # Be extra respectful between sources
                
            except Exception as e:
                logger.error(f"Error collecting from {source.get('name', 'Unknown')}: {e}")
        
        logger.info(f"Historical data collection completed. Total new articles: {total_articles}")
        return total_articles
    
    def get_articles_since_last_launch(self) -> List[Dict]:
        """Get articles collected since last launch"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if self.last_launch_time:
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at
                FROM news_articles 
                WHERE collected_at >= ?
                ORDER BY collected_at DESC
            ''', (self.last_launch_time.isoformat(),))
        else:
            # If no last launch time, get last 24 hours
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
    
    def run_initial_collection(self):
        """Run initial data collection when AI launches"""
        logger.info("=" * 50)
        logger.info("AI LAUNCH DETECTED - Starting news data collection")
        logger.info("=" * 50)
        
        # Show time window
        from_time, to_time = self.get_time_window()
        logger.info(f"Collection window: {from_time} to {to_time}")
        
        # Collect historical data
        historical_count = self.collect_historical_data()
        
        # Start live collection
        self.start_live_collection()
        
        # Get articles from this session
        recent_articles = self.get_articles_since_last_launch()
        
        logger.info(f"Initial collection complete!")
        logger.info(f"  - Collected {historical_count} new articles")
        logger.info(f"  - Available articles for processing: {len(recent_articles)}")
        logger.info("=" * 50)
        
        return {
            'new_articles': historical_count,
            'total_available': len(recent_articles),
            'articles': recent_articles
        }

# Example usage showing the time-based collection
def demo_time_based_collection():
    """Demo showing how time-based collection works"""
    print("=== News Scraper Time-Based Collection Demo ===\n")
    
    # Initialize scraper
    scraper = EnhancedNewsScraper()
    
    print(f"Last launch time: {scraper.last_launch_time}")
    
    if scraper.last_launch_time:
        time_diff = datetime.now() - scraper.last_launch_time
        print(f"Time since last launch: {time_diff}")
    else:
        print("First run detected - will collect last 24 hours of data")
    
    # Run collection (commented out for demo)
    # result = scraper.run_initial_collection()
    
    print("\n=== Collection Process ===")
    print("1. System checks last launch time")
    print("2. Calculates time window (last launch to now)")
    print("3. Scrapes news sources for fresh content")
    print("4. Stores articles with collection timestamps")
    print("5. Starts live collection for ongoing updates")

if __name__ == "__main__":
    demo_time_based_collection()
