# config.py - Phase 1: Basic Configuration

# URLs
BASE_URL = 'https://www.crew-united.com/en/'
JOBS_URL = 'https://www.crew-united.com/en/jobs/'

# Navigation settings
WAIT_TIMEOUT = 15  # Seconds to wait for elements
PAGE_LOAD_DELAY = 10  # Seconds to wait for JavaScript to load jobs
KEEP_BROWSER_OPEN = 60  # Seconds to keep browser open for inspection

# Debug settings
HEADLESS = False  # Set to True to run without seeing browser
VERBOSE = True    # Print detailed logs