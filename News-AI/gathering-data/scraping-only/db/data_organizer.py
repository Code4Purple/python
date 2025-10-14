# db/data_organizer.py
import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsDataOrganizer:
    def __init__(self, db_path: str = os.path.join("db", "news_data.db"), base_data_dir: str = "news_data"):
        """
        Initialize the data organizer
        """
        self.db_path = db_path
        self.base_data_dir = base_data_dir
        self.setup_directories()
    
    def setup_directories(self):
        """Create base directory for organized data"""
        if not os.path.exists(self.base_data_dir):
            os.makedirs(self.base_data_dir)
            logger.info(f"Created base data directory: {self.base_data_dir}")
    
    def create_source_directory(self, source_name: str) -> str:
        """Create directory for specific news source"""
        # Clean source name for directory use
        clean_source_name = "".join(c for c in source_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_source_name = clean_source_name.replace(' ', '_')
        
        source_dir = os.path.join(self.base_data_dir, clean_source_name)
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
            logger.info(f"Created directory for {source_name}: {source_dir}")
        
        return source_dir
    
    def sanitize_filename(self, title: str, max_length: int = 100) -> str:
        """Create a safe filename from article title"""
        # Remove invalid characters
        filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Limit length
        if len(filename) > max_length:
            filename = filename[:max_length]
        # Ensure it's not empty
        if not filename:
            filename = "untitled_article"
        return filename
    
    def save_article_to_file(self, article: Dict, source_dir: str) -> bool:
        """Save individual article to text file"""
        try:
            # Create filename from title
            filename = self.sanitize_filename(article['title'])
            filepath = os.path.join(source_dir, f"{filename}.txt")
            
            # If file exists, add timestamp to make it unique
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name_without_ext = os.path.splitext(original_filepath)[0]
                filepath = f"{name_without_ext}_{counter}.txt"
                counter += 1
            
            # Create article content
            content = self.format_article_content(article)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.debug(f"Saved article: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving article to file: {e}")
            return False
    
    def format_article_content(self, article: Dict) -> str:
        """Format article content for text file"""
        content = []
        
        # Article metadata
        content.append("=" * 80)
        content.append("NEWS ARTICLE")
        content.append("=" * 80)
        content.append(f"")
        content.append(f"Title: {article['title']}")
        content.append(f"Source: {article['source']}")
        content.append(f"URL: {article['url']}")
        content.append(f"Published: {article.get('published_at', 'Unknown')}")
        content.append(f"Collected: {article.get('collected_at', datetime.now().isoformat())}")
        content.append(f"")
        content.append("=" * 80)
        content.append("DESCRIPTION")
        content.append("=" * 80)
        content.append(f"")
        content.append(article.get('description', 'No description'))
        content.append(f"")
        content.append("=" * 80)
        content.append("FULL CONTENT")
        content.append("=" * 80)
        content.append(f"")
        content.append(article.get('content', 'No content'))
        content.append(f"")
        content.append("=" * 80)
        content.append("END OF ARTICLE")
        content.append("=" * 80)
        
        return "\n".join(content)
    
    def get_all_articles(self) -> List[Dict]:
        """Get all articles from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at
                FROM news_articles 
                ORDER BY collected_at DESC
            ''')
            
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
            logger.info(f"Retrieved {len(articles)} articles from database")
            return articles
            
        except Exception as e:
            logger.error(f"Error retrieving articles: {e}")
            return []
    
    def organize_all_data(self) -> Dict[str, int]:
        """Organize all data into source-specific folders"""
        logger.info("Starting data organization...")
        
        articles = self.get_all_articles()
        return self.organize_articles(articles)
    
    def organize_articles(self, articles: List[Dict]) -> Dict[str, int]:
        """Organize articles by source"""
        if not articles:
            logger.warning("No articles to organize")
            return {}
        
        # Statistics tracking
        stats = {}
        total_saved = 0
        
        # Group articles by source
        articles_by_source = {}
        for article in articles:
            source = article['source']
            if source not in articles_by_source:
                articles_by_source[source] = []
            articles_by_source[source].append(article)
        
        # Process each source
        for source, source_articles in articles_by_source.items():
            logger.info(f"Processing {len(source_articles)} articles from {source}")
            
            # Create source directory
            source_dir = self.create_source_directory(source)
            
            # Save articles
            saved_count = 0
            for article in source_articles:
                if self.save_article_to_file(article, source_dir):
                    saved_count += 1
                    total_saved += 1
            
            stats[source] = saved_count
            logger.info(f"Saved {saved_count} articles to {source_dir}")
        
        logger.info(f"Data organization completed. Total articles saved: {total_saved}")
        return stats

# Integration function
def organize_scraped_data():
    """Organize scraped data into source-specific folders"""
    logger.info("Starting data organization...")
    
    organizer = NewsDataOrganizer()
    stats = organizer.organize_all_data()
    
    logger.info("Data organization completed!")
    for source, count in stats.items():
        logger.info(f"  {source}: {count} articles")
    
    return stats
