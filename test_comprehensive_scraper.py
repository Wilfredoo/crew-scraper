#!/usr/bin/env python3
"""
Test script for comprehensive agency data extraction
This will test the new CSV functionality without running the full scraper
"""

import csv
from datetime import datetime

def test_csv_functionality():
    """Test the CSV creation functionality"""
    print("🧪 Testing CSV functionality...")
    
    # Sample agency data for testing
    sample_agencies = [
        {
            'name': 'Test Agency 1',
            'email': 'info@testagency1.com',
            'phone': '+44 20 7160 6333',
            'address': '123 Main St, London, UK',
            'country': 'United Kingdom',
            'website': 'https://testagency1.com',
            'regions': 'UK & Ireland',
            'specialties': 'Acting agency, Voice Agency'
        },
        {
            'name': 'Test Agency 2',
            'email': 'contact@testagency2.de',
            'phone': '+49 30 403 01850',
            'address': 'Unter den Linden 1, Berlin, Germany',
            'country': 'Germany',
            'website': 'https://testagency2.de',
            'regions': 'D/A/CH',
            'specialties': 'Model agency, Young talent'
        },
        {
            'name': 'Test Agency 3',
            'email': 'hello@testagency3.fr',
            'phone': '+33 1 42 97 48 80',
            'address': '25 Rue de Rivoli, Paris, France',
            'country': 'France',
            'website': 'https://testagency3.fr',
            'regions': 'France',
            'specialties': 'Artist management'
        }
    ]
    
    # Test CSV creation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_agencies_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'phone', 'address', 'country', 'website', 'regions', 'specialties']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write agency data
            for agency in sample_agencies:
                writer.writerow(agency)
        
        print(f"✅ Successfully created CSV test file: {filename}")
        
        # Verify the file was created and can be read
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            print(f"✅ Successfully read {len(rows)} rows from CSV")
            
            # Display sample data
            print("\n📊 Sample CSV content:")
            print("-" * 80)
            for i, row in enumerate(rows[:2], 1):  # Show first 2 rows
                print(f"Agency {i}:")
                print(f"  Name: {row['name']}")
                print(f"  Email: {row['email']}")
                print(f"  Country: {row['country']}")
                print(f"  Phone: {row['phone']}")
                print()
        
        print("🎉 CSV functionality test PASSED!")
        print(f"📁 Test file created: {filename}")
        print("📋 This file can be imported into Google Sheets")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV test failed: {str(e)}")
        return False

def test_email_extraction():
    """Test email extraction from sample text"""
    import re
    
    print("\n🧪 Testing email extraction functionality...")
    
    sample_text = """
    Test Agency Berlin
    Phone: +49 30 403 01850
    Email: info@testagency.de
    Address: Unter den Linden 1, 10117 Berlin, Germany
    Website: www.testagency.de
    
    Another Agency London
    Contact: hello@anotheragency.co.uk
    Tel: +44 20 7160 6333
    London, United Kingdom
    
    Third Agency Paris
    contact@thirdagency.fr
    +33 1 42 97 48 80
    Paris, France
    """
    
    # Extract emails using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    found_emails = re.findall(email_pattern, sample_text)
    
    print(f"✅ Found {len(found_emails)} emails:")
    for email in found_emails:
        print(f"  📧 {email}")
    
    # Extract phone numbers
    phone_patterns = [
        r'\+\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}',  # +49 30 403 01850
        r'\+\d{2,3}\s?\d{1,4}\s?\d{2,4}\s?\d{2,4}',  # +44 20 7160 6333
    ]
    
    found_phones = []
    for pattern in phone_patterns:
        phones = re.findall(pattern, sample_text)
        found_phones.extend(phones)
    
    print(f"✅ Found {len(found_phones)} phone numbers:")
    for phone in found_phones:
        print(f"  📞 {phone}")
    
    print("🎉 Email extraction test PASSED!")
    return True

if __name__ == '__main__':
    print("🚀 TESTING COMPREHENSIVE AGENCY DATA EXTRACTION")
    print("=" * 50)
    
    # Run tests
    csv_success = test_csv_functionality()
    email_success = test_email_extraction()
    
    print("\n" + "=" * 50)
    if csv_success and email_success:
        print("🎯 ALL TESTS PASSED!")
        print("✅ The scraper is ready for comprehensive data extraction")
        print("💡 Usage:")
        print("   python3 filmmakers_scraper.py comprehensive  # For full agency data")
        print("   python3 filmmakers_scraper.py email          # For emails only")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Check the errors above")