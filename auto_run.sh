#!/bin/bash
# auto_run.sh - Automated scrape + email send for crew-united-scraper
# Runs every 10 days via launchd (com.wilfredo.crew-united-scraper)

PROJECT_DIR="/Users/wilfredo/Desktop/projects/crew-united-scraper"
LOG="$PROJECT_DIR/auto_run.log"

cd "$PROJECT_DIR" || { echo "[$(date)] ERROR: Could not cd to $PROJECT_DIR" >> "$LOG"; exit 1; }

echo "" >> "$LOG"
echo "========================================" >> "$LOG"
echo "Auto-run started: $(date)" >> "$LOG"
echo "========================================" >> "$LOG"

# Run in automated mode (headless Chrome, no browser kept open)
export AUTOMATED=1

# Step 1: Scrape both sites
echo "[$(date)] Starting scrape..." >> "$LOG"
./venv/bin/python unified_scraper.py both >> "$LOG" 2>&1

SCRAPE_EXIT=$?
echo "[$(date)] Scrape finished (exit code: $SCRAPE_EXIT)" >> "$LOG"

# Step 2: Send emails (mirrors the Makefile 'send' logic)
echo "[$(date)] Starting email send..." >> "$LOG"

if ls combined_emails_*.txt 1>/dev/null 2>&1; then
    LATEST=$(ls -t combined_emails_*.txt | head -1)
    echo "[$(date)] Sending from: $LATEST" >> "$LOG"
    ./venv/bin/python email_sender.py send "$LATEST" >> "$LOG" 2>&1
elif ls emails_*.txt 1>/dev/null 2>&1 || ls filmmakers_emails_*.txt 1>/dev/null 2>&1; then
    LATEST=$(ls -t emails_*.txt filmmakers_emails_*.txt 2>/dev/null | head -1)
    echo "[$(date)] Sending from: $LATEST" >> "$LOG"
    ./venv/bin/python email_sender.py send "$LATEST" >> "$LOG" 2>&1
else
    echo "[$(date)] No email files found — nothing to send." >> "$LOG"
fi

echo "[$(date)] Auto-run complete." >> "$LOG"
