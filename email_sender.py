# email_sender.py
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.zoho.eu"
        self.port = 587
        self.sender_email = os.getenv('ZOHO_EMAIL')
        self.password = os.getenv('ZOHO_APP_PASSWORD')
        
    def send_single_test(self):
        """Send a test email to yourself"""
        try:
            self._send_email(
                to_email=self.sender_email,
                is_test=True
            )
            print(f"✉️ Test email sent successfully to {self.sender_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending test email: {str(e)}")
            return False
            
    def send_emails_from_file(self, email_file, delay=2):
        """Send emails to all addresses in the file"""
        try:
            # Read emails from file
            with open(email_file, 'r') as f:
                emails = [email.strip() for email in f.readlines() if email.strip()]
                
            print(f"📧 Found {len(emails)} emails to send")
            print("Starting email dispatch...")
            
            success_count = 0
            failed_emails = []
            
            for i, email in enumerate(emails, 1):
                try:
                    print(f"\nSending email {i}/{len(emails)} to {email}...")
                    self._send_email(to_email=email)
                    success_count += 1
                    print(f"✅ Sent successfully to {email}")
                    
                    if i < len(emails):  # Don't delay after the last email
                        print(f"⏳ Waiting {delay} seconds before next email...")
                        time.sleep(delay)
                        
                except Exception as e:
                    print(f"❌ Failed to send to {email}: {str(e)}")
                    failed_emails.append(email)
                    
            # Print summary
            print("\n📊 Email Sending Summary")
            print("=" * 50)
            print(f"Total emails: {len(emails)}")
            print(f"Successfully sent: {success_count}")
            print(f"Failed: {len(failed_emails)}")
            
            if failed_emails:
                print("\nFailed email addresses:")
                for email in failed_emails:
                    print(f"- {email}")
                    
            return success_count == len(emails)
            
        except Exception as e:
            print(f"❌ Error in email sending process: {str(e)}")
            return False
            
    def _send_email(self, to_email, is_test=False):
        """Send single email"""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = "Indigenous actor in Germany"
        
        body = """Hi,

Maybe I could be a good fit for your film.

My reel and bio can be found at: www.wilfredocasas.com/acting

Cheers,
Wilfredo"""

        if is_test:
            body = "TEST EMAIL\n\n" + body
            
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session and send
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.sender_email, self.password)
        server.send_message(msg)
        server.quit()

if __name__ == "__main__":
    import sys
    
    sender = EmailSender()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Test email:   python email_sender.py test")
        print("  Send emails:  python email_sender.py send path/to/emails.txt [delay_seconds]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "test":
        sender.send_single_test()
    elif command == "send":
        if len(sys.argv) < 3:
            print("❌ Please provide the path to the email file")
            sys.exit(1)
        delay = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        sender.send_emails_from_file(sys.argv[2], delay)
