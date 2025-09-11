# Initialize and activate virtual environment
init-env:
	python3 -m venv venv
	@echo "Now run: source venv/bin/activate"

# Install dependencies
install:
	python3 -m pip install -r requirements.txt

# Run the scraper
run:
	python3 main.py
