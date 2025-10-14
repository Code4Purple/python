# enhanced_data_organizer.py
import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedNewsDataOrganizer:
    def __init__(self, db_path: str = "news_data.db", base_data_dir: str = "news_data"):
        self.db_path = db_path
        self.base_data_dir = base_data_dir
        self.metadata_file = os.path.join(base_data_dir, "organization_metadata.json")
        self.setup_directories()
    
    def setup_directories(self):
        """Create base directory and metadata file"""
        if not os.path.exists(self.base_data_dir):
            os.makedirs(self.base_data_dir)
            logger.info(f"Created base data directory: {self.base_data_dir}")
        
        # Initialize metadata file if it doesn't exist
        if not os.path.exists(self.metadata_file):
            self.save_metadata({
                "last_organization": None,
                "total_articles_organized": 0,
                "sources": {}
            })
    
    def load_metadata(self) -> Dict:
        """Load organization metadata"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
        return {}
    
    def save_metadata(self, metadata: Dict):
        """Save organization metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def create_source_directory(self, source_name: str) -> str:
        """Create directory structure for news source"""
        # Clean source name
        clean_source_name = "".join(c for c in source_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_source_name = clean_source_name.replace(' ', '_')
        
        # Create main source directory
        source_dir = os.path.join(self.base_data_dir, clean_source_name)
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
        
        # Create subdirectories for organization
        subdirs = ['articles', 'metadata', 'summaries']
        for subdir in subdirs:
            subdir_path = os.path.join(source_dir, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
        
        return source_dir
    
    def sanitize_filename(self, title: str, max_length: int = 100) -> str:
        """Create safe filename"""
        filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = filename.replace(' ', '_')
        if len(filename) > max_length:
            filename = filename[:max_length]
        if not filename:
            filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return filename
    
    def save_article_files(self, article: Dict, source_dir: str) -> Dict[str, str]:
        """Save article in multiple formats"""
        try:
            filename = self.sanitize_filename(article['title'])
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Main article file
            article_file = os.path.join(source_dir, 'articles', f"{filename}.txt")
            counter = 1
            original_article_file = article_file
            while os.path.exists(article_file):
                name_without_ext = os.path.splitext(original_article_file)[0]
                article_file = f"{name_without_ext}_{counter}.txt"
                counter += 1
            
            # Save main article content
            with open(article_file, 'w', encoding='utf-8') as f:
                f.write(self.format_article_content(article))
            
            # Save metadata as JSON
            metadata_file = os.path.join(source_dir, 'metadata', f"{filename}.json")
            counter = 1
            original_metadata_file = metadata_file
            while os.path.exists(metadata_file):
                name_without_ext = os.path.splitext(original_metadata_file)[0]
                metadata_file = f"{name_without_ext}_{counter}.json"
                counter += 1
            
            metadata = {
                'title': article['title'],
                'url': article['url'],
                'source': article['source'],
                'published_at': article.get('published_at'),
                'collected_at': article.get('collected_at'),
                'file_created': datetime.now().isoformat(),
                'word_count': len(article.get('content', '').split()),
                'article_file': os.path.basename(article_file)
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Save summary (first 500 characters)
            summary_file = os.path.join(source_dir, 'summaries', f"{filename}.txt")
            counter = 1
            original_summary_file = summary_file
            while os.path.exists(summary_file):
                name_without_ext = os.path.splitext(original_summary_file)[0]
                summary_file = f"{name_without_ext}_{counter}.txt"
                counter += 1
            
            summary = article.get('description', '')[:500]
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            return {
                'article': article_file,
                'metadata': metadata_file,
                'summary': summary_file
            }
            
        except Exception as e:
            logger.error(f"Error saving article files: {e}")
            return {}
    
    def format_article_content(self, article: Dict) -> str:
        """Format article with rich metadata"""
        content = []
        
        # Header
        content.append("=" * 100)
        content.append("NEWS ARTICLE")
        content.append("=" * 100)
        content.append("")
        
        # Metadata section
        content.append("METADATA:")
        content.append("-" * 20)
        content.append(f"Title: {article['title']}")
        content.append(f"Source: {article['source']}")
        content.append(f"URL: {article['url']}")
        content.append(f"Published: {article.get('published_at', 'Unknown')}")
        content.append(f"Collected: {article.get('collected_at', datetime.now().isoformat())}")
        content.append(f"Word Count: {len(article.get('content', '').split())}")
        content.append("")
        
        # Content sections
        content.append("=" * 100)
        content.append("ARTICLE CONTENT")
        content.append("=" * 100)
        content.append("")
        content.append(article.get('content', 'No content'))
        content.append("")
        content.append("=" * 100)
        content.append("END OF ARTICLE")
        content.append("=" * 100)
        
        return "\n".join(content)
    
    def organize_articles(self, articles: List[Dict], update_metadata: bool = True) -> Dict[str, int]:
        """Organize articles with full metadata support"""
        if not articles:
            return {}
        
        stats = {}
        metadata = self.load_metadata()
        
        # Group by source
        articles_by_source = {}
        for article in articles:
            source = article['source']
            if source not in articles_by_source:
                articles_by_source[source] = []
            articles_by_source[source].append(article)
        
        # Process each source
        for source, source_articles in articles_by_source.items():
            logger.info(f"Processing {len(source_articles)} articles from {source}")
            
            source_dir = self.create_source_directory(source)
            saved_count = 0
            
            for article in source_articles:
                files_created = self.save_article_files(article, source_dir)
                if files_created:
                    saved_count += 1
            
            stats[source] = saved_count
            
            # Update source metadata
            if source not in metadata['sources']:
                metadata['sources'][source] = {
                    'total_articles': 0,
                    'last_updated': None
                }
            metadata['sources'][source]['total_articles'] += saved_count
            metadata['sources'][source]['last_updated'] = datetime.now().isoformat()
        
        # Update global metadata
        metadata['last_organization'] = datetime.now().isoformat()
        metadata['total_articles_organized'] = metadata.get('total_articles_organized', 0) + sum(stats.values())
        
        if update_metadata:
            self.save_metadata(metadata)
        
        return stats

# Automatic integration with news scraper
def setup_automatic_organization(db_path: str = "news_data.db"):
    """Setup automatic organization that runs with the scraper"""
    
    def organize_callback(scraper_instance):
        """Callback function to run after scraping"""
        logger.info("Running automatic data organization after scraping...")
        organizer = EnhancedNewsDataOrganizer(db_path)
        
        # Get recently collected articles
        recent_articles = scraper_instance.get_recent_articles(hours=1)  # Last hour
        if recent_articles:
            stats = organizer.organize_articles(recent_articles)
            logger.info(f"Organized {sum(stats.values())} recent articles")
        else:
            logger.info("No recent articles to organize")
    
    return organize_callback

# Example integration
def integrated_example():
    """Example of integrated scraping and organization"""
    print("=== Integrated News Scraping and Organization ===\n")
    
    # This would be integrated with your main scraper
    # For demo purposes, showing the structure:
    
    print("1. News scraper collects articles...")
    print("2. Articles stored in database...")
    print("3. Data organizer automatically creates folder structure...")
    print("4. Each article saved as separate text file...")
    print("5. Metadata and summaries created...")
    print()
    
    # Show expected folder structure
    print("Expected folder structure:")
    print("news_data/")
    print("├── BBC_News/")
    print("│   ├── articles/")
    print("│   ├── metadata/")
    print("│   └── summaries/")
    print("├── CNN/")
    print("│   ├── articles/")
    print("│   ├── metadata/")
    print("│   └── summaries/")
    print("└── organization_metadata.json")

if __name__ == "__main__":
    integrated_example()
