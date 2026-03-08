import os
import glob
from datetime import datetime
import shutil

def archive_email_files():
    """Move existing email files to dated archive folders"""
    # Create archive directory if it doesn't exist
    archive_dir = "archived_scrapes"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    # Find all email files (crew-united, filmmakers, and combined)
    email_files = glob.glob('emails_*.txt') + glob.glob('filmmakers_emails_*.txt') + glob.glob('combined_emails_*.txt')
    
    for file in email_files:
        try:
            # Use file modified date so archiving works with any filename format
            modified_timestamp = os.path.getmtime(file)
            date_obj = datetime.fromtimestamp(modified_timestamp)
            readable_date = date_obj.strftime('%B %d, %Y')  # e.g., "September 23, 2025"
            
            # Create dated folder if it doesn't exist
            date_folder = os.path.join(archive_dir, readable_date)
            if not os.path.exists(date_folder):
                os.makedirs(date_folder)
            
            # Move file to dated folder
            shutil.move(file, os.path.join(date_folder, file))
            print(f"Archived {file} to {readable_date}/")
            
        except Exception as e:
            print(f"Error archiving {file}: {str(e)}")


def get_most_recent_email_file():
    """Find the most recent email file from current directory or archives"""
    # First, check if there are any current email files (shouldn't be any after archiving)
    current_files = glob.glob('emails_*.txt') + glob.glob('filmmakers_emails_*.txt') + glob.glob('combined_emails_*.txt')
    
    # Get all archived email files
    archived_files = []
    archive_dir = "archived_scrapes"
    
    if os.path.exists(archive_dir):
        for root, dirs, files in os.walk(archive_dir):
            for file in files:
                if (file.startswith('emails_') or 
                    file.startswith('filmmakers_emails_') or 
                    file.startswith('combined_emails_')) and file.endswith('.txt'):
                    archived_files.append(os.path.join(root, file))
    
    # Combine all files
    all_files = current_files + archived_files
    
    if not all_files:
        return None
    
    # Sort by modification time, most recent first
    all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return all_files[0]


def load_previous_emails():
    """Load emails from the most recent email file"""
    recent_file = get_most_recent_email_file()
    
    if not recent_file:
        print("📧 No previous email files found - all emails will be considered new")
        return set()
    
    try:
        with open(recent_file, 'r', encoding='utf-8') as f:
            previous_emails = set(line.strip() for line in f if line.strip())
        
        print(f"📧 Loaded {len(previous_emails)} emails from previous scrape: {os.path.basename(recent_file)}")
        return previous_emails
        
    except Exception as e:
        print(f"❌ Error loading previous emails from {recent_file}: {str(e)}")
        return set()


def filter_new_emails(current_emails, previous_emails=None):
    """Filter out emails that were in the previous scrape"""
    if previous_emails is None:
        previous_emails = load_previous_emails()
    
    if not previous_emails:
        print(f"✨ All {len(current_emails)} emails are new (no previous scrape to compare)")
        return current_emails
    
    # Convert current emails to set for efficient comparison
    current_email_set = set(current_emails)
    
    # Find new emails (not in previous scrape)
    new_emails = current_email_set - previous_emails
    
    # Find repeated emails (for reporting)
    repeated_emails = current_email_set & previous_emails
    
    print(f"📊 Email comparison results:")
    print(f"   🆕 New emails: {len(new_emails)}")
    print(f"   🔄 Repeated emails: {len(repeated_emails)}")
    print(f"   📧 Total current emails: {len(current_emails)}")
    
    if repeated_emails and len(repeated_emails) <= 5:
        print(f"   🔄 Repeated: {', '.join(sorted(repeated_emails))}")
    elif repeated_emails:
        print(f"   🔄 Repeated: {', '.join(sorted(list(repeated_emails)[:3]))} and {len(repeated_emails)-3} more...")
    
    return list(new_emails)
