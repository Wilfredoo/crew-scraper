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
	python3 email_sender.py send $$(ls -t emails_*.txt | head -1)

# Send test email to yourself
test-email:
	python3 email_sender.py test
