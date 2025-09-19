# main.py - Phase 2: Job Detection and Display

from driver_manager import create_chrome_driver, close_driver
from navigator import CrewUnitedNavigator
from job_scraper import CrewUnitedJobScraper
from config import KEEP_BROWSER_OPEN, VERBOSE

def main():
    """Phase 2: Navigate to jobs page and detect job listings with details"""
    
    print("🎬 CREW UNITED SCRAPER - PHASE 2")
    print("Goal: Navigate to jobs page and detect job listings")
    print()
    
    driver = None
    
    try:
        # STEP 1: Create driver and navigate
        driver = create_chrome_driver()
        navigator = CrewUnitedNavigator(driver)
        scraper = CrewUnitedJobScraper(driver)
        
        print("🚀 STEP 1: Navigation")
        success = navigator.navigate_to_jobs_page()
        
        if not success:
            print("❌ Navigation failed!")
            close_driver(driver, 10)
            return False
        
        # STEP 2: Detect and extract jobs from all pages
        print("\n🕵️ STEP 2: Job Detection")
        all_jobs = scraper.paginate_and_scrape()
        
        if not all_jobs:
            print("❌ No job elements found")
            close_driver(driver, 30)
            return False
        
        print(f"\n🎭 FOUND {len(all_jobs)} 'NO BUDGET (ACTORS*ACTRESSES AND SPEAKERS)' JOBS")

        # Display the jobs
        has_jobs = scraper.display_target_jobs(all_jobs)

        if has_jobs:
            print(f"\n🎉 PHASE 2 COMPLETED SUCCESSFULLY!")
            print(f"   📊 Total elements found: {len(job_elements)}")
            print(f"   📋 Jobs with content: {len(all_jobs)}")
        else:
            print(f"\n❌ NO TARGET JOBS FOUND")
            print(f"   📊 Total elements: {len(job_elements)}")
            print(f"   📋 Jobs extracted: {len(all_jobs)}")

        close_driver(driver, KEEP_BROWSER_OPEN)
        return has_jobs

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if driver:
            close_driver(driver, 10)
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    
    success = main()
    
    if success:
        print("\n🎯 READY FOR PHASE 3!")
        print("Next step: Extract detailed data from each job")
    else:
        print("\n🔧 PHASE 2 NEEDS FIXING")
        print("Check the job details above to see what was found vs expected.")
