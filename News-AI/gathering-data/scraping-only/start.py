# example_integration.py
from enchanced_news_scrapper import NewsScraper
from enhanced_data_organizer import NewsDataOrganizer

def main():
    # Initialize scraper
    scraper = NewsScraper()
    
    # Run initial collection
    print("Collecting news data...")
    result = scraper.run_initial_collection()
    
    # Automatically organize data
    print("Organizing data into source folders...")
    organizer = NewsDataOrganizer()
    stats = organizer.organize_recent_data(hours=24)
    
    print(f"Organization complete: {stats}")
    
    # Show where data is stored
    print("\nData is now organized in:")
    stats = organizer.get_data_statistics()
    for source, count in stats.items():
        print(f"  news_data/{source}/ - {count} articles")

if __name__ == "__main__":
    main()
