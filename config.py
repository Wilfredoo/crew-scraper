# config.py - Phase 1: Basic Configuration

# URLs
BASE_URL = 'https://www.crew-united.com/en/'
JOBS_URL = 'https://www.crew-united.com/en/jobs/'

# Navigation settings
WAIT_TIMEOUT = 15  # Seconds to wait for elements
PAGE_LOAD_DELAY = 10  # Seconds to wait for JavaScript to load jobs
KEEP_BROWSER_OPEN = 60  # Seconds to keep browser open for inspection

# Debug settings
import os as _os
HEADLESS = _os.environ.get('AUTOMATED', '0') == '1'  # True when run by scheduler
KEEP_BROWSER_OPEN = 0 if _os.environ.get('AUTOMATED', '0') == '1' else 60
VERBOSE = True    # Print detailed logs