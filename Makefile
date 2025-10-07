# Initialize and activate virtual environment
init-env:
	python3 -m venv venv
	@echo "Now run: source venv/bin/activate"

# Install dependencies
install:
	python3 -m pip install -r requirements.txt

# Scrape new jobs (deletes old email files first)
scrape:
	python3 main.py

# Send emails from most recent file
send:
	@if ls emails_*.txt 1> /dev/null 2>&1; then \
		python3 email_sender.py send $$(ls -t emails_*.txt | head -1); \
	else \
		echo "❌ No email files found. Run 'make scrape' first or check if new emails were found."; \
	fi

# Send test email to yourself
test-email:
	python3 email_sender.py test
