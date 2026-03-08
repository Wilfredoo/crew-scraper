# Initialize and activate virtual environment
init-env:
	python3 -m venv venv
	@echo "Now run: source venv/bin/activate"

# Install dependencies
install:
	./venv/bin/pip install -r requirements.txt

# Scrape new jobs from Crew-United only
scrape:
	./venv/bin/python main.py

# Scrape emails from Filmmakers.eu only  
scrape-filmmakers:
	./venv/bin/python filmmakers_scraper.py

# Scrape comprehensive agency data from Filmmakers.eu (CSV format)
scrape-filmmakers-csv:
	./venv/bin/python filmmakers_scraper.py comprehensive

# Scrape from BOTH sites and combine results (recommended)
scrape-all:
	./venv/bin/python unified_scraper.py both

# Scrape from specific site using unified scraper
scrape-crew:
	./venv/bin/python unified_scraper.py crew

scrape-filmmakers-unified:
	./venv/bin/python unified_scraper.py filmmakers

# Test the comprehensive data extraction functionality
test-scraper:
	./venv/bin/python test_comprehensive_scraper.py

# Send emails from most recent file (prioritizes combined files)
# Send emails from most recent file (prioritizes combined files)
send:
	@if ls combined_emails_*.txt 1> /dev/null 2>&1; then \
		./venv/bin/python email_sender.py send $$(ls -t combined_emails_*.txt | head -1); \
	elif ls emails_*.txt 1> /dev/null 2>&1 || ls filmmakers_emails_*.txt 1> /dev/null 2>&1; then \
		./venv/bin/python email_sender.py send $$(ls -t emails_*.txt filmmakers_emails_*.txt 2>/dev/null | head -1); \
	else \
		echo "❌ No email files found. Run 'make scrape-all' first."; \
	fi

# Send test email to yourself
test-email:
	./venv/bin/python email_sender.py test
