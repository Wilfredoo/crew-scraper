# unified_scraper.py - Run multiple scrapers and combine results

import sys
from datetime import datetime
from utils import filter_new_emails, archive_email_files
import os

def run_crew_united_scraper():
    """Run the crew-united scraper"""
    print("🎬 STARTING CREW-UNITED SCRAPER")
    print("="*50)
    
    from main import main as crew_main
    return crew_main()

def run_filmmakers_scraper():
    """Run the filmmakers.eu scraper"""
    print("\n🌐 STARTING FILMMAKERS.EU SCRAPER")
    print("="*50)
    
    from filmmakers_scraper import main as filmmakers_main
    return filmmakers_main()

def combine_email_files():
    """Combine emails from both scrapers into one deduplicated file"""
    import glob
    
    # Find the most recent email files
    crew_files = glob.glob('emails_*.txt')
    filmmakers_files = glob.glob('filmmakers_emails_*.txt')
    
    all_emails = []
    sources = []
    
    # Get emails from crew-united files
    if crew_files:
        crew_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        latest_crew = crew_files[0]
        try:
            with open(latest_crew, 'r', encoding='utf-8') as f:
                crew_emails = [line.strip() for line in f if line.strip()]
            all_emails.extend(crew_emails)
            sources.append(f"Crew-United: {len(crew_emails)} emails from {latest_crew}")
        except Exception as e:
            print(f"⚠️  Error reading {latest_crew}: {str(e)}")
    
    # Get emails from filmmakers files
    if filmmakers_files:
        filmmakers_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        latest_filmmakers = filmmakers_files[0]
        try:
            with open(latest_filmmakers, 'r', encoding='utf-8') as f:
                filmmakers_emails = [line.strip() for line in f if line.strip()]
            all_emails.extend(filmmakers_emails)
            sources.append(f"Filmmakers.eu: {len(filmmakers_emails)} emails from {latest_filmmakers}")
        except Exception as e:
            print(f"⚠️  Error reading {latest_filmmakers}: {str(e)}")
    
    if not all_emails:
        print("⚠️  No email files found to combine")
        return False
    
    # Apply deduplication against previous combined scrapes
    new_emails = filter_new_emails(all_emails)
    
    if not new_emails:
        print("✅ No new emails found after deduplication")
        return True
    
    # Save combined deduplicated emails
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    combined_filename = f'combined_emails_{timestamp}.txt'
    
    try:
        # Remove duplicates within current batch while preserving order
        unique_emails = list(dict.fromkeys(new_emails))
        
        with open(combined_filename, 'w', encoding='utf-8') as f:
            for email in unique_emails:
                f.write(f"{email}\n")
        
        print(f"\n📊 COMBINATION RESULTS:")
        print("="*50)
        for source in sources:
            print(f"   {source}")
        print(f"   📧 Total unique new emails: {len(unique_emails)}")
        print(f"   📄 Saved to: {combined_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving combined emails: {str(e)}")
        return False

def main():
    """Main function to run unified scraping"""
    print("🚀 UNIFIED EMAIL SCRAPER")
    print("Scraping emails from Crew-United AND Filmmakers.eu")
    print("="*60)
    
    # Archive existing email files first
    archive_email_files()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        scraper_choice = sys.argv[1].lower()
    else:
        scraper_choice = "both"
    
    crew_success = False
    filmmakers_success = False
    
    if scraper_choice in ["both", "crew", "crew-united"]:
        crew_success = run_crew_united_scraper()
    
    if scraper_choice in ["both", "filmmakers", "filmmakers.eu"]:
        filmmakers_success = run_filmmakers_scraper()
    
    if scraper_choice == "both" and (crew_success or filmmakers_success):
        print(f"\n🔗 COMBINING RESULTS")
        print("="*50)
        combine_success = combine_email_files()
    else:
        combine_success = True  # Don't fail if only running one scraper
    
    # Summary
    print(f"\n📊 FINAL SUMMARY")
    print("="*50)
    
    if scraper_choice in ["both", "crew", "crew-united"]:
        status = "✅ Success" if crew_success else "❌ Failed"
        print(f"   Crew-United: {status}")
    
    if scraper_choice in ["both", "filmmakers", "filmmakers.eu"]:
        status = "✅ Success" if filmmakers_success else "❌ Failed"
        print(f"   Filmmakers.eu: {status}")
    
    if scraper_choice == "both":
        status = "✅ Success" if combine_success else "❌ Failed"
        print(f"   Combination: {status}")
    
    overall_success = (
        (scraper_choice in ["both", "crew", "crew-united"] and crew_success) or
        (scraper_choice in ["both", "filmmakers", "filmmakers.eu"] and filmmakers_success)
    ) and combine_success
    
    if overall_success:
        print(f"\n🎉 ALL SCRAPING COMPLETED SUCCESSFULLY!")
        print(f"🚀 Ready to send emails! Run: make send")
    else:
        print(f"\n⚠️  SOME ISSUES OCCURRED")
        print(f"Check the output above for details")
    
    return overall_success

if __name__ == '__main__':
    main()