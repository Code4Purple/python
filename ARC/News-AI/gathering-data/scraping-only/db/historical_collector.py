# db/historical_collector.py
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import time
import random

logger = logging.getLogger(__name__)

class HistoricalDataCollector:
    def __init__(self, scraper_instance):
        self.scraper = scraper_instance
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        ]
    
    def get_random_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    
    def scrape_sitemap(self, base_url: str, target_date: datetime) -> List[str]:
        """Scrape sitemap for articles from specific date"""
        try:
            # Try common sitemap locations
            sitemap_urls = [
                f"{base_url}/sitemap.xml",
                f"{base_url}/sitemap_index.xml",
                f"{base_url}/news-sitemap.xml",
                f"{base_url}/sitemap-{target_date.strftime('%Y-%m-%d')}.xml"
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    headers = self.get_random_headers()
                    response = requests.get(sitemap_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'xml')
                        urls = []
                        
                        # Extract URLs from sitemap
                        for loc in soup.find_all('loc'):
                            url = loc.get_text()
                            # Filter by date if possible
                            urls.append(url)
                        
                        return urls[:50]  # Limit to 50 URLs
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping sitemap: {e}")
        
        return []
    
    def collect_monthly_data(self, source_config: Dict, year: int, month: int) -> List[Dict]:
        """Collect data for a specific month"""
        articles = []
        
        # Try different approaches
        try:
            # 1. Try archive URLs
            if source_config.get('archive_url_pattern'):
                # Try multiple days in the month
                days_to_try = [1, 7, 14, 21, 28]  # Sample days
                for day in days_to_try:
                    try:
                        target_date = datetime(year, month, day)
                        archive_articles = self.scraper.scrape_historical_archive(source_config, target_date)
                        articles.extend(archive_articles)
                        time.sleep(2)
                    except:
                        continue
            
            # 2. Try sitemap approach
            sitemap_urls = self.scrape_sitemap(source_config['base_url'], datetime(year, month, 1))
            for url in sitemap_urls[:10]:  # Limit to 10 URLs
                try:
                    article_data = self.scraper.scrape_article(url, source_config)
                    if article_data:
                        article_data['collection_method'] = 'sitemap'
                        articles.append(article_data)
                    time.sleep(1)
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error collecting monthly data for {source_config['name']}: {e}")
        
        return articles

# Enhanced collection in main.py
def collect_10_years_data():
    """Collect 10 years of data systematically"""
    from news_scraper import EnhancedNewsScraper
    
    scraper = EnhancedNewsScraper()
    collector = HistoricalDataCollector(scraper)
    
    print("Starting 10-year data collection...")
    
    # Collect data year by year
    current_year = datetime.now().year
    start_year = current_year - 10
    
    total_articles = 0
    
    for year in range(start_year, current_year + 1):
        print(f"Collecting data for year {year}...")
        
        for month in range(1, 13):
            if year == current_year and month > datetime.now().month:
                break
                
            print(f"  Month {year}-{month:02d}...")
            
            # For each source, collect monthly data
            for source in scraper.news_sources:
                try:
                    monthly_articles = collector.collect_monthly_data(source, year, month)
                    stored_count = scraper.store_articles(monthly_articles)
                    total_articles += stored_count
                    print(f"    {source['name']}: {stored_count} articles")
                    time.sleep(3)  # Be respectful
                except Exception as e:
                    logger.error(f"Error collecting {source['name']} data: {e}")
    
    print(f"10-year collection completed: {total_articles} articles")
    return total_articles
