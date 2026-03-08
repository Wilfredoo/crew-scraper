# Comprehensive Agency Data Extraction

## Overview

The filmmakers scraper has been enhanced to extract comprehensive agency information, not just emails. This allows you to build a complete database of talent agencies for your outreach efforts.

## What Data is Extracted

The comprehensive mode extracts the following information for each agency:

- **Name**: Agency name
- **Email**: Contact email address
- **Phone**: Phone number (if available)
- **Address**: Physical address
- **Country**: Country where the agency is located
- **Website**: Agency website URL
- **Regions**: Regions served (e.g., D/A/CH, UK & Ireland)
- **Specialties**: Type of services (Acting agency, Model agency, etc.)

## Usage

### 1. Comprehensive Data Extraction (CSV Format)
```bash
# Extract all agency data to CSV file (ready for Google Sheets)
python3 filmmakers_scraper.py comprehensive

# Or using Make
make scrape-filmmakers-csv
```

### 2. Email-Only Extraction (Original Mode)
```bash
# Extract only emails (backward compatibility)
python3 filmmakers_scraper.py email

# Or using the original command
python3 filmmakers_scraper.py
```

### 3. Starting from a Specific Page
```bash
# Start from page 10 with comprehensive data
python3 filmmakers_scraper.py comprehensive 10

# Start from page 5 with email-only
python3 filmmakers_scraper.py email 5
```

## Output Files

### Comprehensive Mode
- **CSV File**: `filmmakers_agencies_YYYYMMDD_HHMMSS.csv`
  - Contains all agency data in structured format
  - Ready for import into Google Sheets or Excel
  - Headers: name, email, phone, address, country, website, regions, specialties

### Email-Only Mode
- **Text File**: `filmmakers_emails_YYYYMMDD_HHMMSS.txt`
  - Contains only email addresses (one per line)
  - Compatible with existing email sender

## Progressive Saving

Both modes include progressive saving to prevent data loss:
- **Comprehensive**: Progress saved every 10 pages as separate CSV files
- **Email-Only**: Progress saved after each page to a single text file

## Google Sheets Import

To import the CSV file into Google Sheets:

1. Open Google Sheets
2. Go to File → Import
3. Upload the `filmmakers_agencies_*.csv` file
4. Choose "Create new spreadsheet" or "Insert new sheet(s)"
5. Set separator type to "Comma"
6. Click "Import data"

## Data Quality Notes

- **Email Validation**: All emails are validated using regex patterns
- **Phone Number Extraction**: Supports various international formats
- **Address Parsing**: Attempts to separate country from full address
- **Deduplication**: Agencies with the same email are deduplicated
- **Error Handling**: Individual agency extraction errors don't stop the entire process

## Testing

Test the functionality without running the full scraper:
```bash
python3 test_comprehensive_scraper.py
```

This creates sample CSV files and tests the data extraction logic.

## Examples

### Sample CSV Output
```csv
name,email,phone,address,country,website,regions,specialties
"London Talent Agency",info@londontalent.co.uk,"+44 20 7160 6333","123 Piccadilly, London, UK",United Kingdom,https://londontalent.co.uk,"UK & Ireland","Acting agency, Voice Agency"
"Berlin Casting",contact@berlincast.de,"+49 30 403 01850","Unter den Linden 1, Berlin, Germany",Germany,https://berlincast.de,"D/A/CH","Model agency, Young talent"
```

### Command Examples
```bash
# Full comprehensive extraction
python3 filmmakers_scraper.py comprehensive

# Email-only from page 20
python3 filmmakers_scraper.py email 20

# Test the system
python3 test_comprehensive_scraper.py
```

## Legal Considerations

The scraper respects rate limits and follows ethical web scraping practices:
- 2-3 second delays between page requests
- Progressive saving to handle interruptions gracefully  
- No aggressive crawling patterns
- Public data only (agency contact information)

## Troubleshooting

### Common Issues

1. **No data extracted**: Check internet connection and site availability
2. **CSV import errors**: Ensure file is saved with UTF-8 encoding
3. **Missing phone/address data**: Some agencies may not provide complete information
4. **Duplicate agencies**: Agencies are deduplicated by email address

### Getting Help

If you encounter issues:
1. Check the terminal output for specific error messages
2. Try running the test script first
3. Start with a smaller page range to isolate issues
4. Ensure Chrome browser is installed and up to date

## Legacy Compatibility

The original email-only functionality is preserved:
- All existing commands continue to work
- Email files are still generated in comprehensive mode
- Unified scraper integration remains unchanged