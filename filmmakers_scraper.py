# filmmakers_scraper.py - Scraper for filmmakers.eu talent agencies

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from config import WAIT_TIMEOUT, VERBOSE
import re
import time
import csv
from datetime import datetime

class FilmmakersScraper:
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.filmmakers.eu/talent_agency_search/new"
        self.start_page = 1  # Can be overridden
        
    def navigate_and_setup_filters(self):
        """Navigate to filmmakers.eu talent agency search"""
        if VERBOSE:
            print("🌐 Navigating to filmmakers.eu talent agency search...")
            
        try:
            # Navigate to the search page
            self.driver.get(self.base_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            if VERBOSE:
                print("✅ Page loaded successfully")
                print("🌍 Will scrape ALL regions for maximum email coverage")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during navigation: {str(e)}")
            return False
    
    def scrape_all_pages(self, extract_full_data=False):
        """Scrape all pages of talent agencies and extract emails or full agency data"""
        all_emails = []
        all_agencies = []
        page = getattr(self, 'start_page', 1)  # Start from specified page or page 1
        max_pages = 100  # Safety limit
        
        # Create progressive save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        progressive_filename = f'filmmakers_emails_progress_{timestamp}.txt'
        progressive_csv_filename = f'filmmakers_agencies_progress_{timestamp}.csv'
        
        try:
            while page <= max_pages:
                if VERBOSE:
                    print(f"\n📖 Processing Page {page}")
                    print("=" * 30)
                
                # Check if we're actually on a valid page with content
                try:
                    # Look for the pagination container to verify page loaded
                    pagination = self.driver.find_element(By.XPATH, "/html/body/main/div/div[3]/nav/ul")
                    
                    # Check if page has agency content
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    
                    # If page shows no results or error, we've reached the end
                    if ("no results" in page_text.lower() or 
                        "not found" in page_text.lower() or
                        len(page_text.strip()) < 500):  # Very short page likely means no content
                        
                        if VERBOSE:
                            print("🏁 Reached end - no more content or invalid page")
                        break
                        
                except Exception as e:
                    if VERBOSE:
                        print(f"🏁 Cannot find pagination or page content: {str(e)}")
                    break
                
                # Extract data from current page
                if extract_full_data:
                    page_agencies = self.extract_agencies_from_page()
                    
                    if page_agencies:
                        # Extract just emails for compatibility
                        page_emails = [agency['email'] for agency in page_agencies if agency.get('email')]
                        
                        # Filter out duplicates
                        new_emails = [email for email in page_emails if email not in all_emails]
                        new_agencies = []
                        
                        # Filter out duplicate agencies based on email
                        existing_emails = {agency['email'] for agency in all_agencies if agency.get('email')}
                        for agency in page_agencies:
                            if agency.get('email') and agency['email'] not in existing_emails:
                                new_agencies.append(agency)
                        
                        all_emails.extend(new_emails)
                        all_agencies.extend(new_agencies)
                        
                        # Progressive save every 10 pages only (not every page)
                        if page % 10 == 0:
                            try:
                                if all_agencies:
                                    self.save_agencies_to_csv(all_agencies, f"{timestamp}_backup_page_{page}")
                                if VERBOSE:
                                    print(f"💾 Backup saved after page {page}")
                            except Exception as e:
                                if VERBOSE:
                                    print(f"⚠️  Could not save backup: {str(e)}")
                        elif VERBOSE:
                            print(f"💾 Progress tracking (will save final file at end)")
                        
                        if VERBOSE:
                            print(f"🏢 Found {len(page_agencies)} agencies on page {page}")
                            print(f"📧 New unique emails: {len(new_emails)}")
                            print(f"📊 Total agencies so far: {len(all_agencies)}")
                            print(f"📊 Total emails so far: {len(all_emails)}")
                    
                else:
                    # Original email-only extraction
                    page_emails = self.extract_emails_from_page()
                    
                    if page_emails:
                        # Filter out duplicates while adding
                        new_emails = [email for email in page_emails if email not in all_emails]
                        all_emails.extend(new_emails)
                        
                        # PROGRESSIVE SAVE: Save after each page
                        try:
                            with open(progressive_filename, 'w', encoding='utf-8') as f:
                                for email in all_emails:
                                    f.write(f"{email}\n")
                            if VERBOSE:
                                print(f"💾 Progress saved to {progressive_filename}")
                        except Exception as e:
                            if VERBOSE:
                                print(f"⚠️  Could not save progress: {str(e)}")
                        
                        if VERBOSE:
                            print(f"📧 Found {len(page_emails)} emails on page {page}")
                            print(f"📧 New unique emails: {len(new_emails)}")
                            print(f"📊 Total emails so far: {len(all_emails)}")
                
                # Check if we found any data on this page
                if not (page_agencies if extract_full_data else page_emails):
                    if VERBOSE:
                        print(f"⚠️  No data found on page {page}")
                    # If several consecutive pages have no data, probably reached the end
                    if page > 3:
                        if VERBOSE:
                            print("🏁 Multiple pages with no data - probably reached the end")
                        break
                
                # Try to navigate to next page using the next button (ORIGINAL WORKING METHOD)
                try:
                    # Look for the next button using the correct XPath
                    next_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[3]/nav/ul/li[9]/a"))
                    )
                    
                    # Check if the button is disabled or if we're at the end
                    if "disabled" in next_button.get_attribute("class"):
                        if VERBOSE:
                            print("🏁 Next button is disabled - reached last page")
                        break
                    
                    if VERBOSE:
                        print(f"👆 Clicking next page button...")
                    
                    # Use JavaScript click to bypass element interception
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)  # Wait for page load
                    
                except (TimeoutException, NoSuchElementException):
                    if VERBOSE:
                        print("🏁 Next button not found - reached last page")
                    break
                except Exception as e:
                    if VERBOSE:
                        print(f"⚠️  Error clicking next button: {str(e)}")
                    break
                
                page += 1
            
            # Final save
            if extract_full_data and all_agencies:
                csv_filename = self.save_agencies_to_csv(all_agencies, timestamp)
                print(f"\n🎉 Comprehensive scraping completed!")
                print(f"📊 Total pages scraped: {page - 1}")
                print(f"🏢 Total agencies found: {len(all_agencies)}")
                print(f"📧 Total emails found: {len(all_emails)}")
                if csv_filename:
                    print(f"📊 CSV file: {csv_filename}")
                return all_agencies, all_emails
            
            else:
                # Original email-only save
                final_filename = self.save_emails_to_file(all_emails, f"filmmakers_emails_{timestamp}.txt")
                
                print(f"\n🎉 Email scraping completed!")
                print(f"📊 Total pages scraped: {page - 1}")
                print(f"📧 Total emails found: {len(all_emails)}")
                if final_filename:
                    print(f"📧 Final file: filmmakers_emails_{timestamp}.txt")
                
                return all_emails
                
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try to save what we have
            if extract_full_data:
                if all_agencies:
                    self.save_agencies_to_csv(all_agencies, f"{timestamp}_emergency_save")
                return all_agencies, all_emails
            else:
                if all_emails:
                    self.save_emails_to_file(all_emails, f"filmmakers_emails_{timestamp}_emergency.txt")
                    print(f"💾 Emergency save: filmmakers_emails_{timestamp}_emergency.txt")
                return all_emails
            
            return ([], []) if extract_full_data else []

    def extract_emails_from_page(self):
        """Extract ALL emails from the current page (backward compatibility)"""
        emails = []
        
        try:
            # Wait for page to be loaded
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get all text on the page
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract emails using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, page_text)
            
            # Also look for mailto links
            try:
                email_links = self.driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
                for link in email_links:
                    email = link.get_attribute('href').replace('mailto:', '').strip()
                    if email:
                        found_emails.append(email)
            except:
                pass
            
            # Clean and validate emails
            for email in found_emails:
                email = email.strip().lower()
                if self.is_valid_email(email) and email not in emails:
                    emails.append(email)
                    if VERBOSE:
                        print(f"   ✅ Found: {email}")
            
            return emails
            
        except Exception as e:
            if VERBOSE:
                print(f"⚠️  Error extracting emails from page: {str(e)}")
            return emails

    def extract_agencies_from_page(self):
        """Extract ALL agency information from the current page"""
        agencies = []
        
        try:
            # Wait for page to be loaded
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find all agency sections - look for h3 elements with agency names (links)
            agency_elements = self.driver.find_elements(By.XPATH, "//h3/a[contains(@href, '/agents/')]")
            
            if VERBOSE:
                print(f"   🏢 Found {len(agency_elements)} agency elements")
            
            for agency_element in agency_elements:
                try:
                    agency_data = self.extract_single_agency_data(agency_element)
                    if agency_data and agency_data.get('email'):  # Only include if we have an email
                        agencies.append(agency_data)
                        if VERBOSE:
                            print(f"   ✅ {agency_data['name']}: {agency_data['email']}")
                    
                except Exception as e:
                    if VERBOSE:
                        print(f"   ⚠️  Error processing agency element: {str(e)}")
                    continue
            
            return agencies
            
        except Exception as e:
            if VERBOSE:
                print(f"⚠️  Error extracting agencies from page: {str(e)}")
            return agencies
    
    def extract_single_agency_data(self, agency_element):
        """Extract data from a single agency element"""
        agency_data = {
            'name': '',
            'email': '',
            'phone': '',
            'address': '',
            'country': '',
            'website': '',
            'regions': '',
            'specialties': ''
        }
        
        try:
            # Get agency name from the link text
            agency_data['name'] = agency_element.text.strip()
            
            # Get the website URL from the href
            agency_data['website'] = agency_element.get_attribute('href') or ''
            
            # Find the parent container that holds all the agency info
            # Go up to find the main agency container
            parent = agency_element.find_element(By.XPATH, "../..")
            agency_text = parent.text
            
            # Extract email using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, agency_text)
            if emails:
                agency_data['email'] = emails[0].lower()
            
            # Extract phone using regex (various international formats)
            phone_patterns = [
                r'\+\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}',  # +49 30 403 01850
                r'\+\d{2,3}\s?\d{1,4}\s?\d{2,4}\s?\d{2,4}',  # +44 20 7160 6333
                r'\+\d{10,15}',  # +447789935248
                r'\d{2,4}\s?\d{2,4}\s?\d{2,4}\s?\d{2,4}',  # 020 7160 6333
            ]
            
            for pattern in phone_patterns:
                phones = re.findall(pattern, agency_text)
                if phones:
                    agency_data['phone'] = phones[0].strip()
                    break
            
            # Extract address and country
            # Look for common country/city patterns
            lines = agency_text.split('\n')
            for i, line in enumerate(lines):
                line_clean = line.strip()
                
                # Check if line contains country indicators
                countries = ['Germany', 'Austria', 'Switzerland', 'France', 'Italy', 'Spain', 'United Kingdom', 
                           'Netherlands', 'Belgium', 'Denmark', 'Sweden', 'Norway', 'Poland', 'Czech', 
                           'Portugal', 'Greece', 'Ireland', 'Finland', 'Hungary', 'Slovakia', 'Slovenia',
                           'Croatia', 'Bulgaria', 'Romania', 'Latvia', 'Lithuania', 'Estonia']
                
                for country in countries:
                    if country in line_clean:
                        agency_data['country'] = country
                        # The line with country often contains address
                        agency_data['address'] = line_clean
                        break
                
                # Look for regions like D/A/CH, UK & Ireland, etc.
                if any(region in line_clean for region in ['D/A/CH', 'UK & Ireland', 'Benelux', 'Nordic', 'Iberia']):
                    agency_data['regions'] = line_clean
                
                # Look for specialties (Acting agency, Artist management, etc.)
                specialties_keywords = ['Acting agency', 'Artist management', 'Model agency', 'Voice Agency', 
                                      'Young talent', 'Casting', 'Management', 'Talent agency']
                for keyword in specialties_keywords:
                    if keyword.lower() in line_clean.lower():
                        if agency_data['specialties']:
                            agency_data['specialties'] += f", {keyword}"
                        else:
                            agency_data['specialties'] = keyword
            
            # Clean up address - remove email and phone if they got mixed in
            if agency_data['address']:
                # Remove email and phone from address
                address_clean = agency_data['address']
                if agency_data['email']:
                    address_clean = address_clean.replace(agency_data['email'], '').strip()
                if agency_data['phone']:
                    address_clean = address_clean.replace(agency_data['phone'], '').strip()
                agency_data['address'] = address_clean
            
            return agency_data
            
        except Exception as e:
            if VERBOSE:
                print(f"   ⚠️  Error extracting data for {agency_data.get('name', 'unknown')}: {str(e)}")
            return agency_data
    
    def is_valid_email(self, email):
        """Basic email validation"""
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(pattern, email) is not None
    
    def save_agencies_to_csv(self, agencies, timestamp=None):
        """Save agencies data to a CSV file"""
        if not agencies:
            print("📝 No agencies to save")
            return None
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"filmmakers_agencies_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'email', 'phone', 'address', 'country', 'website', 'regions', 'specialties']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write agency data
                for agency in agencies:
                    writer.writerow(agency)
            
            print(f"📊 Saved {len(agencies)} agencies to {filename}")
            return filename
            
        except Exception as e:
            print(f"⚠️  Error saving agencies to CSV: {str(e)}")
            return None

    def save_emails_to_file(self, emails, filename=None):
        """Save emails to a text file"""
        if not emails:
            print("⚠️  No emails to save")
            return False
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'filmmakers_emails_{timestamp}.txt'
        
        try:
            # Remove duplicates
            unique_emails = list(dict.fromkeys(emails))
            
            with open(filename, 'w', encoding='utf-8') as f:
                for email in unique_emails:
                    f.write(f"{email}\n")
            
            print(f"💾 Saved {len(unique_emails)} unique emails to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving emails: {str(e)}")
            return False

def main():
    """Main function to run filmmakers.eu scraper"""
    from driver_manager import create_chrome_driver, close_driver
    from config import KEEP_BROWSER_OPEN
    import sys
    
    print("🎬 FILMMAKERS.EU SCRAPER")
    print("Choose extraction mode:")
    print("1. Email-only extraction (legacy mode)")
    print("2. Comprehensive agency data extraction (CSV format)")
    print()
    
    # Check command line arguments for mode selection
    extract_full_data = False
    start_page = 1
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['full', 'comprehensive', 'csv']:
            extract_full_data = True
            print("🏢 Selected: Comprehensive agency data extraction")
        elif sys.argv[1].lower() in ['email', 'emails', 'simple']:
            extract_full_data = False
            print("📧 Selected: Email-only extraction")
        else:
            # Try to parse as page number
            try:
                start_page = int(sys.argv[1])
                print(f"🔄 Starting from page {start_page} (email-only mode)")
            except:
                print("⚠️  Invalid argument, using default settings")
    
    # Check for second argument (start page in comprehensive mode)
    if len(sys.argv) > 2 and extract_full_data:
        try:
            start_page = int(sys.argv[2])
            print(f"🔄 Starting from page {start_page}")
        except:
            print("⚠️  Invalid page number, starting from page 1")
    
    if not extract_full_data and len(sys.argv) == 1:
        # Interactive mode selection
        while True:
            choice = input("Enter choice (1 for emails, 2 for comprehensive): ").strip()
            if choice == '1':
                extract_full_data = False
                print("📧 Selected: Email-only extraction")
                break
            elif choice == '2':
                extract_full_data = True
                print("🏢 Selected: Comprehensive agency data extraction")
                break
            else:
                print("Please enter 1 or 2")
    
    driver = None
    
    try:
        # Create driver
        driver = create_chrome_driver()
        scraper = FilmmakersScraper(driver)
        
        # Navigate to page
        print("🚀 STEP 1: Navigation")
        success = scraper.navigate_and_setup_filters()
        
        if not success:
            print("❌ Navigation failed!")
            close_driver(driver, 10)
            return False
        
        # Note: Starting page > 1 not supported since site doesn't allow direct page URLs
        # Must navigate sequentially using next button
        if start_page > 1:
            print(f"⚠️  Note: Starting page {start_page} not supported - must start from page 1")
            print("   Site requires sequential navigation using next button")
            start_page = 1
        
        # Scrape all pages
        if extract_full_data:
            print(f"\n🏢 STEP 2: Comprehensive Agency Data Extraction from Page {start_page} onwards")
            scraper.start_page = start_page  # Set starting page
            agencies, emails = scraper.scrape_all_pages(extract_full_data=True)
            
            if not agencies:
                print("❌ No agencies found")
                close_driver(driver, 30)
                return False
            
            print("\n💾 STEP 3: Final Results")
            print(f"   🏢 Total agencies: {len(agencies)}")
            print(f"   📧 Total emails: {len(emails)}")
            print(f"   📊 Results saved to CSV file")
        
        else:
            print(f"\n🕵️ STEP 2: Email Extraction from Page {start_page} onwards")
            scraper.start_page = start_page  # Set starting page
            all_emails = scraper.scrape_all_pages(extract_full_data=False)
            
            if not all_emails:
                print("❌ No emails found")
                close_driver(driver, 30)
                return False
            
            print("\n💾 STEP 3: Final Results")
            print(f"   📧 Total unique emails: {len(set(all_emails))}")
            print(f"   📄 Results saved to text file with progressive backup")
        
        close_driver(driver, KEEP_BROWSER_OPEN)
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        if driver:
            close_driver(driver, 10)
        return False

if __name__ == '__main__':
    success = main()
    
    if success:
        print("\n🎯 FILMMAKERS.EU SCRAPING COMPLETE!")
        print("📊 CSV files are ready for Google Sheets import")
        print("📧 Email files can be used with your email sender")
    else:
        print("\n🔧 SCRAPING NEEDS FIXING")
        print("Check the output above for errors")