# driver_manager.py - Phase 1: Chrome Driver Management

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import HEADLESS, VERBOSE

def create_chrome_driver():
    """Create and configure Chrome driver for scraping"""
    
    if VERBOSE:
        print("🔧 Setting up Chrome driver...")
    
    # Chrome options
    chrome_options = Options()
    
    # Browser behavior
    if HEADLESS:
        chrome_options.add_argument("--headless")
        if VERBOSE:
            print("   → Running in headless mode (no visible browser)")
    else:
        if VERBOSE:
            print("   → Running with visible browser (you'll see Chrome open)")
    
    # Standard options for better compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent to look more like a real browser
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Create driver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove webdriver property to avoid detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        if VERBOSE:
            print("   ✅ Chrome driver created successfully")
        
        return driver
        
    except Exception as e:
        print(f"   ❌ Failed to create Chrome driver: {e}")
        raise

def close_driver(driver, delay_seconds=0):
    """Close the Chrome driver with optional delay"""
    
    if delay_seconds > 0:
        if VERBOSE:
            print(f"⏰ Keeping browser open for {delay_seconds} seconds...")
            print("   (You can inspect the page during this time)")
        
        import time
        time.sleep(delay_seconds)
    
    if driver:
        if VERBOSE:
            print("🚪 Closing Chrome browser...")
        driver.quit()
        if VERBOSE:
            print("   ✅ Browser closed")