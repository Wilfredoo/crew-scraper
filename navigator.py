# navigator.py - Phase 1: Navigation to Jobs Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import BASE_URL, WAIT_TIMEOUT, PAGE_LOAD_DELAY, VERBOSE

class CrewUnitedNavigator:
    
    def __init__(self, driver):
        self.driver = driver
    
    def go_to_main_page(self):
        """Navigate to the main Crew United page"""
        
        if VERBOSE:
            print(f"🌍 Navigating to: {BASE_URL}")
        
        try:
            self.driver.get(BASE_URL)
            
            # Wait for page to load
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            if VERBOSE:
                print("   ✅ Main page loaded successfully")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to load main page: {e}")
            return False
    
    def click_jobs_link(self):
        """Find and click the Jobs link"""
        
        if VERBOSE:
            print("🔍 Looking for Jobs link...")
        
        try:
            # Wait for the Jobs link to be clickable
            # Based on your HTML: <a class="jobs" href="/en/jobs/">
            jobs_link = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.jobs"))
            )
            
            if VERBOSE:
                print("   ✅ Found Jobs link")
                print("🖱️  Clicking Jobs link...")
            
            # Click the link
            jobs_link.click()
            
            if VERBOSE:
                print("   ✅ Jobs link clicked")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to find/click Jobs link: {e}")
            return False
    
    def wait_for_jobs_to_load(self):
        """Wait for the jobs page to fully load with JavaScript content"""
        
        if VERBOSE:
            print(f"⏳ Waiting {PAGE_LOAD_DELAY} seconds for jobs to load...")
            print("   (JavaScript needs time to fetch and display jobs)")
        
        time.sleep(PAGE_LOAD_DELAY)
        
        # Check current URL
        current_url = self.driver.current_url
        if VERBOSE:
            print(f"   📍 Current URL: {current_url}")
        
        # Check if we're on a jobs-related page
        if "/jobs/" in current_url or "job" in current_url.lower():
            if VERBOSE:
                print("   ✅ Successfully on jobs page!")
            return True
        else:
            if VERBOSE:
                print("   ⚠️  URL doesn't look like jobs page, but continuing...")
            return True  # Continue anyway, might still work
    
    def navigate_to_jobs_page(self):
        """Complete navigation flow to jobs page"""
        
        if VERBOSE:
            print("=" * 50)
            print("🚀 STARTING NAVIGATION TO JOBS PAGE")
            print("=" * 50)
        
        # Step 1: Go to main page
        if not self.go_to_main_page():
            return False
        
        # Small delay to let page settle
        time.sleep(2)
        
        # Step 2: Click Jobs link
        if not self.click_jobs_link():
            return False
        
        # Step 3: Wait for jobs to load
        if not self.wait_for_jobs_to_load():
            return False
        
        if VERBOSE:
            print("=" * 50)
            print("🎉 NAVIGATION SUCCESSFUL!")
            print("=" * 50)
            print("The browser should now show the jobs page with loaded content.")
        
        return True