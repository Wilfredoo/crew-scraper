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
        
    # Find all email files
    email_files = glob.glob('emails_*.txt')
    
    for file in email_files:
        try:
            # Extract date from filename (format: emails_YYYYMMDD_HHMMSS.txt)
            date_str = file.split('_')[1]  # Get YYYYMMDD part
            date_obj = datetime.strptime(date_str, '%Y%m%d')
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
