# Crew United Job Scraper

Automatically scrapes "No budget (actors*actresses and speakers)" jobs from Crew United. Perfect for actors looking for casting opportunities!

## 🚀 Quick Start

1. **First time setup:**
```bash
# Create virtual environment
make init-env

# Activate it
source venv/bin/activate

# Install dependencies
make install
```

2. **Regular usage:**
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the scraper
make run
```

## 🔧 What It Does

- Opens Chrome browser (visual mode)
- Goes to Crew United jobs page
- Finds all "No budget (actors*actresses and speakers)" roles
- Shows job details including:
  - Role title
  - Email contact
  - Project details
  - Job description preview

## 📝 Requirements

- Python 3.x
- Chrome browser installed
- Zoho email account (for sending applications)

## ⚠️ Common Issues & Solutions

1. **"ModuleNotFoundError: No module named 'selenium'"**
   ```bash
   source venv/bin/activate  # Make sure virtual env is active
   make install             # Reinstall dependencies
   ```

2. **Chrome doesn't open**
   - Check Chrome is installed
   - Try: `make install` to reinstall dependencies

3. **Package installation fails**
   ```bash
   # Complete reset:
   rm -rf venv
   make init-env
   source venv/bin/activate
   make install
   ```

## 🔄 Regular Maintenance

If you haven't used the script in a while:
```bash
source venv/bin/activate
make install
make run
```

## 📨 Email Setup (Optional)

To enable automatic email sending:

1. Create `.env` file:
```bash
ZOHO_EMAIL=your.email@zoho.com
ZOHO_APP_PASSWORD=your_app_specific_password
```

2. Get App Password from:
   - Zoho Mail → Settings → Security → App Passwords