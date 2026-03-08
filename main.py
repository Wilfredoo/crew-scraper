# main.py - Phase 2: Job Detection and Display

import os
from driver_manager import create_chrome_driver, close_driver
from navigator import CrewUnitedNavigator
from job_scraper import CrewUnitedJobScraper
from config import KEEP_BROWSER_OPEN, VERBOSE

def main():
    """Phase 2: Navigate to jobs page and detect job listings with details"""
    
    print("🎬 CREW UNITED SCRAPER - PHASE 2")
    print("Goal: Navigate to jobs page and detect job listings")
    print()
    
    # Archive existing email files before starting new scrape
    from utils import archive_email_files
    archive_email_files()
    
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
        
        # Display the jobs
        has_jobs = scraper.display_target_jobs(all_jobs)

        if has_jobs:
            print(f"\n🎉 PHASE 2 COMPLETED SUCCESSFULLY!")
            print(f"   📊 Total jobs found: {len(all_jobs)}")
            print(f"   📋 Jobs with content: {len(all_jobs)}")
            
            # Check if any new email file was created
            import glob
            current_email_files = glob.glob('emails_*.txt')
            if current_email_files:
                # Sort by modification time to get the newest
                current_email_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                newest_file = current_email_files[0]
                print(f"   📄 New emails saved to: {newest_file}")
                print(f"\n🚀 Ready to send emails! Run: make send")
            else:
                print(f"   📄 No new email file created (no new unique emails found)")
                print(f"\n😎 All emails were duplicates from previous scrape - nothing to send!")
        else:
            print(f"\n❌ NO TARGET JOBS FOUND")
            print(f"   📊 Total jobs found: {len(all_jobs)}")
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
