# main.py
from news_scraper import NewsScraper
from db.data_organizer import NewsDataOrganizer
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to run the complete news data collection and organization system
    """
    print("=" * 70)
    print("NEWS DATA COLLECTION AND ORGANIZATION SYSTEM")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Initialize and run news scraper
        print("Step 1: Collecting news data...")
        print("-" * 40)
        
        # Initialize news scraper
        scraper = NewsScraper()
        
        # Run collection (collects data from last run to now)
        # For first run, this will attempt to collect last 10 years of data
        collection_result = scraper.run_collection(initial_collection_days=365*10)
        
        print(f"\nCollection Results:")
        print(f"  New articles collected: {collection_result['new_articles']}")
        print(f"  Total articles available: {collection_result['total_available']}")
        print(f"  Collection period: {collection_result['collection_period']['days']} days")
        print()
        
        # Step 2: Organize data into hierarchical folder structure
        print("Step 2: Organizing data into folders...")
        print("-" * 40)
        
        # Initialize data organizer
        organizer = NewsDataOrganizer()
        
        # Organize all collected data
        organization_stats = organizer.organize_all_data()
        
        print(f"\nOrganization Results:")
        total_organized = sum(organization_stats.values())
        print(f"  Total articles organized: {total_organized}")
        print(f"  Sources processed: {len(organization_stats)}")
        
        for source, count in organization_stats.items():
            print(f"    {source}: {count} articles")
        print()
        
        # Step 3: Show final organization statistics
        print("Step 3: Final system status...")
        print("-" * 40)
        
        # Get detailed statistics
        final_stats = organizer.get_organization_statistics()
        
        print(f"Final System Status:")
        print(f"  Total sources: {final_stats['total_sources']}")
        print(f"  Total articles organized: {final_stats['total_articles']}")
        
        # Show database info
        db_size = os.path.getsize(scraper.db_path) if os.path.exists(scraper.db_path) else 0
        db_size_mb = db_size / (1024 * 1024)
        print(f"  Database size: {db_size_mb:.2f} MB")
        print(f"  Database location: {scraper.db_path}")
        
        # Show data directory info
        data_dir = organizer.base_data_dir
        print(f"  Data directory: {os.path.abspath(data_dir)}")
        
        print()
        print("=" * 70)
        print("PROCESSING COMPLETE!")
        print("Data is now available in hierarchical folder structure:")
        print("news_data/Source_Name/YYYY/MM/DD/article_files.txt")
        print("=" * 70)
        
        return {
            'collection': collection_result,
            'organization': organization_stats,
            'final_stats': final_stats
        }
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
        print(f"\n❌ Error occurred: {e}")
        return None

def quick_collection(days: int = 30):
    """
    Quick collection function for recent data only
    
    Args:
        days (int): Number of days to collect (default: 30)
    """
    print(f"Quick Collection: Last {days} days")
    print("=" * 50)
    
    try:
        # Quick collection and organization
        scraper = NewsScraper()
        collection_result = scraper.run_collection(initial_collection_days=days)
        
        organizer = NewsDataOrganizer()
        organization_stats = organizer.organize_recent_data(days=days)
        
        print(f"\nQuick Collection Results:")
        print(f"  New articles: {collection_result['new_articles']}")
        print(f"  Organized: {sum(organization_stats.values())} articles")
        
        return collection_result, organization_stats
        
    except Exception as e:
        logger.error(f"Error in quick collection: {e}")
        return None, None

def collect_10_years_data():
    """
    Special function to attempt collection of 10 years of data
    """
    print("10-Year Data Collection")
    print("=" * 30)
    
    try:
        scraper = NewsScraper()
        print("Attempting to collect 10 years of historical data...")
        print("This may take a while and depends on website availability...")
        
        collection_result = scraper.run_collection(initial_collection_days=365*10)
        
        print(f"\n10-Year Collection Results:")
        print(f"  New articles collected: {collection_result['new_articles']}")
        print(f"  Collection period: {collection_result['collection_period']['days']} days")
        
        # Organize the data
        print("\nOrganizing collected data...")
        organizer = NewsDataOrganizer()
        organization_stats = organizer.organize_all_data()
        
        print(f"  Articles organized: {sum(organization_stats.values())}")
        
        return collection_result, organization_stats
        
    except Exception as e:
        logger.error(f"Error in 10-year collection: {e}")
        return None, None

def show_current_status():
    """Show current system status without collecting new data"""
    print("Current System Status")
    print("=" * 30)
    
    try:
        # Show database info
        scraper = NewsScraper()
        if os.path.exists(scraper.db_path):
            db_size = os.path.getsize(scraper.db_path)
            db_size_mb = db_size / (1024 * 1024)
            print(f"Database: {scraper.db_path}")
            print(f"Size: {db_size_mb:.2f} MB")
        else:
            print("Database: Not found")
        
        # Show organized data info
        organizer = NewsDataOrganizer()
        stats = organizer.get_organization_statistics()
        print(f"Organized articles: {stats['total_articles']}")
        print(f"Sources: {stats['total_sources']}")
        
        # Show folder structure
        if os.path.exists(organizer.base_data_dir):
            print(f"Data directory: {os.path.abspath(organizer.base_data_dir)}")
        else:
            print("Data directory: Not created yet")
            
    except Exception as e:
        logger.error(f"Error showing status: {e}")

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            # Quick collection with optional days parameter
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            quick_collection(days)
        elif sys.argv[1] == "10years":
            # Attempt 10-year collection
            collect_10_years_data()
        elif sys.argv[1] == "status":
            # Show current status
            show_current_status()
        else:
            print("Usage:")
            print("  python main.py           # Full collection and organization")
            print("  python main.py quick [days]  # Quick collection (default 30 days)")
            print("  python main.py 10years       # Attempt 10-year collection")
            print("  python main.py status        # Show current status")
    else:
        # Run full process
        main()
