# navigator.py - Phase 1: Navigation to Jobs Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from config import BASE_URL, JOBS_URL, WAIT_TIMEOUT, PAGE_LOAD_DELAY, VERBOSE

class CrewUnitedNavigator:
    
    def __init__(self, driver):
        self.driver = driver

    def dismiss_cookie_banner(self):
        """
        Best-effort cookie/consent dismissal.
        Crew United's markup changes; try a few common selectors and ignore failures.
        """
        candidates = [
            (By.ID, "onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "button[aria-label*='Accept' i]"),
            (By.CSS_SELECTOR, "button[title*='Accept' i]"),
            (By.XPATH, "//button[contains(translate(normalize-space(.),'ACEPT','acept'),'accept')]"),
            (By.XPATH, "//button[contains(translate(normalize-space(.),'ALLEZUSTIMMEN','allezustimmen'),'zustimmen')]"),
        ]

        for by, sel in candidates:
            try:
                btn = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((by, sel)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                try:
                    btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", btn)
                if VERBOSE:
                    print("🍪 Dismissed cookie/consent banner")
                return True
            except Exception:
                continue

        return False

    def go_to_jobs_page_direct(self):
        """Navigate directly to the jobs URL (more robust than clicking header links)."""
        if VERBOSE:
            print(f"🌍 Navigating directly to: {JOBS_URL}")

        try:
            self.driver.get(JOBS_URL)
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            self.dismiss_cookie_banner()
            if VERBOSE:
                print("   ✅ Jobs page loaded (direct navigation)")
            return True
        except Exception as e:
            print(f"   ❌ Failed to load jobs page directly: {e}")
            return False
    
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

            self.dismiss_cookie_banner()
            
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
            self.dismiss_cookie_banner()

            # Try multiple selectors since site markup changes over time.
            selectors = [
                (By.CSS_SELECTOR, "a.jobs"),
                (By.CSS_SELECTOR, "a[href='/en/jobs/']"),
                (By.CSS_SELECTOR, "a[href^='/en/jobs']"),
                (By.CSS_SELECTOR, "a[href*='/en/jobs']"),
                (By.XPATH, "//a[contains(@href,'/en/jobs')]"),
                (By.XPATH, "//a[normalize-space()='Jobs' or contains(translate(normalize-space(.),'JOBS','jobs'),'jobs')]"),
            ]

            jobs_link = None
            last_err = None
            for by, sel in selectors:
                try:
                    jobs_link = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((by, sel))
                    )
                    break
                except Exception as e:
                    last_err = e
                    continue

            if jobs_link is None:
                raise TimeoutException(str(last_err) if last_err else "Jobs link not found")
            
            if VERBOSE:
                print("   ✅ Found Jobs link")
                print("🖱️  Clicking Jobs link...")
            
            # Click the link (with JS fallback in case an overlay intercepts it)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", jobs_link)
            try:
                jobs_link.click()
            except Exception:
                self.dismiss_cookie_banner()
                self.driver.execute_script("arguments[0].click();", jobs_link)
            
            if VERBOSE:
                print("   ✅ Jobs link clicked")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to find/click Jobs link: {e}")
            if VERBOSE:
                try:
                    print(f"   🔎 Debug URL: {self.driver.current_url}")
                    print(f"   🔎 Debug Title: {self.driver.title}")
                    anchors = self.driver.find_elements(By.TAG_NAME, "a")
                    jobish = []
                    for a in anchors:
                        try:
                            href = (a.get_attribute("href") or "").strip()
                            txt = (a.text or "").strip()
                            if "/jobs" in href or "jobs" in txt.lower():
                                jobish.append((txt, href))
                        except Exception:
                            continue
                    if jobish:
                        print("   🔎 Links that look job-related (up to 8):")
                        for txt, href in jobish[:8]:
                            print(f"      - {txt[:60]} -> {href[:120]}")
                    else:
                        print("   🔎 No job-like links found on page")
                except Exception:
                    pass
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

        # Prefer direct navigation: avoids brittle header selectors and click interception.
        if self.go_to_jobs_page_direct():
            if self.wait_for_jobs_to_load():
                return True
        
        # Step 1: Go to main page
        if not self.go_to_main_page():
            return False
        
        # Small delay to let page settle
        time.sleep(2)
        
        # Step 2: Click Jobs link
        if not self.click_jobs_link():
            # As a final fallback, try direct navigation one more time.
            if not self.go_to_jobs_page_direct():
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
