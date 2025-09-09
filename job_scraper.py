# job_scraper.py - Fixed: Only "No budget (actors*actresses and speakers)" jobs

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import WAIT_TIMEOUT, VERBOSE
import re

class CrewUnitedJobScraper:
    
    def __init__(self, driver):
        self.driver = driver
        
        # Target category - the exact one we want
        self.target_category = "no budget (actors*actresses and speakers)"
    
    def find_target_job_elements(self):
        """Find ONLY job elements that have our target category"""
        
        if VERBOSE:
            print("🔍 FINDING TARGET CATEGORY JOBS")
            print("=" * 30)
        
        try:
            # Look specifically for breadcrumb elements containing our target text
            breadcrumb_selector = "span.cu-ui-common-breadcrumb-part"
            breadcrumb_elements = self.driver.find_elements(By.CSS_SELECTOR, breadcrumb_selector)
            
            target_job_elements = []
            
            if VERBOSE:
                print(f"   📋 Found {len(breadcrumb_elements)} breadcrumb elements")
            
            for breadcrumb in breadcrumb_elements:
                try:
                    breadcrumb_text = breadcrumb.text.strip().lower()
                    
                    if VERBOSE and breadcrumb_text:
                        print(f"   🔍 Checking breadcrumb: {breadcrumb_text[:50]}...")
                    
                    if self.target_category in breadcrumb_text:
                        # Find the parent job element (li element containing this breadcrumb)
                        job_element = breadcrumb.find_element(By.XPATH, "./ancestor::li[contains(@class, '') or not(@class)]")
                        target_job_elements.append(job_element)
                        
                        if VERBOSE:
                            print(f"   ✅ MATCH FOUND! Added job element")
                            
                except Exception as e:
                    if VERBOSE:
                        print(f"   ⚠️  Error checking breadcrumb: {e}")
                    continue
            
            if VERBOSE:
                print(f"   🎯 Total target jobs found: {len(target_job_elements)}")
            
            return target_job_elements
                
        except Exception as e:
            if VERBOSE:
                print(f"   ❌ Error finding target job elements: {e}")
            return []
    
    def extract_job_data(self, job_element):
        """Extract data from a confirmed target job element"""
        
        job_data = {
            'title': None,
            'email': None,
            'raw_text': None,
            'is_target_category': True  # We know it's target since we pre-filtered
        }
        
        try:
            # Get all text
            job_data['raw_text'] = job_element.text.strip()
            
            if not job_data['raw_text']:
                return job_data
            
            # Extract title from first meaningful line
            lines = job_data['raw_text'].split('\n')
            for line in lines[:5]:
                line = line.strip()
                if line and len(line) > 3 and len(line) < 100:
                    if not any(skip in line.lower() for skip in ['new', 'budget', 'hours', 'eur', 'days old']):
                        job_data['title'] = line
                        break
            
            # Extract email
            job_data['email'] = self._extract_email(job_element, job_data['raw_text'])
                        
        except Exception as e:
            if VERBOSE:
                print(f"   ⚠️  Error extracting data: {e}")
        
        return job_data
    
    def _extract_email(self, element, text):
        """Extract email from element"""
        
        # Try obfuscated email first
        try:
            email_links = element.find_elements(By.CSS_SELECTOR, "a[onclick*='putTogether']")
            for link in email_links:
                onclick_attr = link.get_attribute('onclick')
                if onclick_attr and 'putTogether' in onclick_attr:
                    start = onclick_attr.find("'") + 1
                    end = onclick_attr.find("'", start)
                    if start > 0 and end > start:
                        obfuscated = onclick_attr[start:end]
                        actual_email = obfuscated.replace('$_isdot_$', '.').replace('$_isat_$', '@')
                        return actual_email
        except:
            pass
        
        # Try direct mailto
        try:
            email_links = element.find_elements(By.CSS_SELECTOR, "a[href*='mailto:']")
            for link in email_links:
                href = link.get_attribute('href')
                if href and 'mailto:' in href:
                    return href.replace('mailto:', '')
        except:
            pass
        
        # Try regex on text
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def display_target_jobs(self, target_jobs):
        """Display the found target category jobs"""
        
        if not target_jobs:
            print("❌ NO 'NO BUDGET (ACTORS*ACTRESSES AND SPEAKERS)' JOBS FOUND")
            return False
        
        print(f"🎭 FOUND {len(target_jobs)} 'NO BUDGET (ACTORS*ACTRESSES AND SPEAKERS)' JOBS")
        print("=" * 80)
        
        for i, job_data in enumerate(target_jobs, 1):
            print(f"\n🎬 JOB {i}:")
            print(f"   📝 Title: {job_data['title'] or 'NO TITLE'}")
            print(f"   📧 Email: {job_data['email'] or 'NO EMAIL'}")
            
            if job_data['raw_text']:
                preview = job_data['raw_text'][:200] + "..." if len(job_data['raw_text']) > 200 else job_data['raw_text']
                preview = ' '.join(preview.split())
                print(f"   📄 Preview: {preview}")
            
            print("-" * 80)
        
        return True
    
    def detect_target_jobs_on_page(self):
        """Main function - only get 'No budget (actors*actresses and speakers)' jobs"""
        
        if VERBOSE:
            print("\n" + "=" * 80)
            print("🎭 FINDING 'NO BUDGET (ACTORS*ACTRESSES AND SPEAKERS)' JOBS ONLY")
            print("=" * 80)
        
        try:
            # Find only target job elements (pre-filtered)
            target_job_elements = self.find_target_job_elements()
            
            if not target_job_elements:
                print("❌ No target category jobs found on page")
                return False, 0
            
            # Extract data from confirmed target jobs
            target_jobs = []
            for job_element in target_job_elements:
                job_data = self.extract_job_data(job_element)
                target_jobs.append(job_data)
            
            if VERBOSE:
                print(f"📊 Found and processed {len(target_jobs)} target jobs")
            
            # Display results
            success = self.display_target_jobs(target_jobs)
            
            if success:
                print(f"\n✅ SUCCESS: Found {len(target_jobs)} target category jobs")
                return True, len(target_jobs)
            else:
                print(f"\n❌ NO TARGET JOBS FOUND")
                return False, 0
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, 0