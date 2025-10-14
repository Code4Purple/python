# main.py
from news_scraper import NewsScraper
from db.data_organizer import organize_scraped_data

def main():
    print("=== News Data Collection System ===")
    
    # Initialize and run scraper
    scraper = NewsScraper()
    result = scraper.run_collection()
    
    print(f"\nCollection Results:")
    print(f"New articles: {result['new_articles']}")
    print(f"Available for processing: {result['total_available']}")
    
    # Organize data into folders
    print("\nOrganizing data into source folders...")
    stats = organize_scraped_data()
    
    print(f"\nOrganization Results:")
    for source, count in stats.items():
        print(f"  {source}: {count} articles")

if __name__ == "__main__":
    main()
