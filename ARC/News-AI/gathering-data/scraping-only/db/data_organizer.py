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
        Initialize the data organizer with hierarchical folder structure
        """
        self.db_path = db_path
        self.base_data_dir = base_data_dir
        self.setup_directories()
    
    def setup_directories(self):
        """Create base directory for organized data"""
        if not os.path.exists(self.base_data_dir):
            os.makedirs(self.base_data_dir)
            logger.info(f"Created base data directory: {self.base_data_dir}")
    
    def create_hierarchical_directory(self, source_name: str, article_date: datetime) -> str:
        """Create hierarchical directory structure: source/year/month/day"""
        # Clean source name for directory use
        clean_source_name = "".join(c for c in source_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_source_name = clean_source_name.replace(' ', '_')
        
        # Extract date components
        year = article_date.strftime('%Y')
        month = article_date.strftime('%m')
        day = article_date.strftime('%d')
        
        # Create full path: news_data/Source_Name/YYYY/MM/DD/
        source_dir = os.path.join(self.base_data_dir, clean_source_name)
        year_dir = os.path.join(source_dir, year)
        month_dir = os.path.join(year_dir, month)
        day_dir = os.path.join(month_dir, day)
        
        # Create directory structure if it doesn't exist
        for directory in [source_dir, year_dir, month_dir, day_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.debug(f"Created directory: {directory}")
        
        return day_dir
    
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
            filename = f"untitled_article_{datetime.now().strftime('%H%M%S')}"
        return filename
    
    def parse_article_date(self, article: Dict) -> datetime:
        """Parse the date from article, fallback to collection date"""
        try:
            # Try published date first
            if article.get('published_at'):
                if isinstance(article['published_at'], str):
                    # Handle different date formats
                    date_str = article['published_at']
                    if 'T' in date_str:
                        # ISO format
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        # Try common formats
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y/%m/%d']:
                            try:
                                return datetime.strptime(date_str, fmt)
                            except:
                                continue
                elif isinstance(article['published_at'], datetime):
                    return article['published_at']
            
            # Fallback to collected date
            if article.get('collected_at'):
                if isinstance(article['collected_at'], str):
                    return datetime.fromisoformat(article['collected_at'].replace('Z', '+00:00'))
                elif isinstance(article['collected_at'], datetime):
                    return article['collected_at']
            
        except Exception as e:
            logger.debug(f"Error parsing date for article '{article.get('title', 'Unknown')}': {e}")
        
        # Ultimate fallback - current time
        return datetime.now()
    
    def save_article_to_file(self, article: Dict) -> bool:
        """Save individual article to hierarchical folder structure"""
        try:
            # Parse article date
            article_date = self.parse_article_date(article)
            
            # Create hierarchical directory
            day_dir = self.create_hierarchical_directory(article['source'], article_date)
            
            # Create filename from title with timestamp to ensure uniqueness
            timestamp = article_date.strftime('%H%M%S')
            filename = self.sanitize_filename(article['title'])
            filepath = os.path.join(day_dir, f"{filename}_{timestamp}.txt")
            
            # If file exists, add counter to make it unique
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name_parts = os.path.splitext(original_filepath)
                filepath = f"{name_parts[0]}_{counter}{name_parts[1]}"
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
        content.append("")
        content.append(f"Title: {article['title']}")
        content.append(f"Source: {article['source']}")
        content.append(f"URL: {article['url']}")
        content.append(f"Published: {article.get('published_at', 'Unknown')}")
        content.append(f"Collected: {article.get('collected_at', datetime.now().isoformat())}")
        content.append("")
        content.append("=" * 80)
        content.append("DESCRIPTION")
        content.append("=" * 80)
        content.append("")
        content.append(article.get('description', 'No description'))
        content.append("")
        content.append("=" * 80)
        content.append("FULL CONTENT")
        content.append("=" * 80)
        content.append("")
        content.append(article.get('content', 'No content'))
        content.append("")
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
    
    def get_articles_since_date(self, since_date: datetime) -> List[Dict]:
        """Get articles collected since specific date"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, description, content, url, source, published_at, collected_at
                FROM news_articles 
                WHERE collected_at >= ?
                ORDER BY collected_at DESC
            ''', (since_date.isoformat(),))
            
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
            logger.info(f"Retrieved {len(articles)} articles since {since_date}")
            return articles
            
        except Exception as e:
            logger.error(f"Error retrieving articles: {e}")
            return []
    
    def organize_all_data(self) -> Dict[str, int]:
        """Organize all data into hierarchical folder structure"""
        logger.info("Starting hierarchical data organization...")
        
        articles = self.get_all_articles()
        return self.organize_articles(articles)
    
    def organize_recent_data(self, days: int = 30) -> Dict[str, int]:
        """Organize recent data (last N days)"""
        since_time = datetime.now() - timedelta(days=days)
        logger.info(f"Organizing data from last {days} days...")
        
        articles = self.get_articles_since_date(since_time)
        return self.organize_articles(articles)
    
    def organize_articles(self, articles: List[Dict]) -> Dict[str, int]:
        """Organize articles with hierarchical folder structure"""
        if not articles:
            logger.warning("No articles to organize")
            return {}
        
        # Statistics tracking
        stats = {}
        total_saved = 0
        
        # Process each article
        for article in articles:
            source = article['source']
            
            # Save article
            if self.save_article_to_file(article):
                total_saved += 1
                stats[source] = stats.get(source, 0) + 1
            else:
                logger.warning(f"Failed to save article: {article.get('title', 'Unknown')}")
        
        logger.info(f"Data organization completed. Total articles saved: {total_saved}")
        
        # Log statistics by source
        for source, count in stats.items():
            logger.info(f"  {source}: {count} articles organized")
        
        return stats
    
    def get_organization_statistics(self) -> Dict:
        """Get detailed statistics about organized data"""
        stats = {
            'total_sources': 0,
            'total_articles': 0,
            'sources': {}
        }
        
        if not os.path.exists(self.base_data_dir):
            return stats
        
        # Walk through directory structure
        for source_folder in os.listdir(self.base_data_dir):
            source_path = os.path.join(self.base_data_dir, source_folder)
            if os.path.isdir(source_path):
                source_stats = {'total': 0, 'years': {}}
                
                # Count articles in each year/month/day
                for year_folder in os.listdir(source_path):
                    year_path = os.path.join(source_path, year_folder)
                    if os.path.isdir(year_path):
                        year_stats = {'total': 0, 'months': {}}
                        
                        for month_folder in os.listdir(year_path):
                            month_path = os.path.join(year_path, month_folder)
                            if os.path.isdir(month_path):
                                month_stats = {'total': 0, 'days': {}}
                                
                                for day_folder in os.listdir(month_path):
                                    day_path = os.path.join(month_path, day_folder)
                                    if os.path.isdir(day_path):
                                        file_count = len([f for f in os.listdir(day_path) if f.endswith('.txt')])
                                        month_stats['days'][day_folder] = file_count
                                        month_stats['total'] += file_count
                                
                                year_stats['months'][month_folder] = month_stats
                                year_stats['total'] += month_stats['total']
                        
                        source_stats['years'][year_folder] = year_stats
                        source_stats['total'] += year_stats['total']
                
                stats['sources'][source_folder] = source_stats
                stats['total_articles'] += source_stats['total']
        
        stats['total_sources'] = len(stats['sources'])
        return stats

# Integration functions
def organize_all_scraped_data():
    """Organize all scraped data into hierarchical folder structure"""
    logger.info("Starting full data organization...")
    
    organizer = NewsDataOrganizer()
    stats = organizer.organize_all_data()
    
    logger.info("Full data organization completed!")
    return stats

def organize_recent_scraped_data(days: int = 30):
    """Organize recent scraped data"""
    logger.info(f"Starting recent data organization (last {days} days)...")
    
    organizer = NewsDataOrganizer()
    stats = organizer.organize_recent_data(days)
    
    logger.info("Recent data organization completed!")
    return stats

