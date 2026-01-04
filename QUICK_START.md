# Quick Start Guide - SendGrid Email Setup

## 🚀 Quick Setup (3 Steps)

### Step 1: Get SendGrid API Key
1. Go to https://app.sendgrid.com
2. Settings → API Keys → Create API Key
3. Copy your API key

### Step 2: Create .env File

**Option A: Use the setup script (Recommended)**
```bash
python setup_env.py
```

**Option B: Create manually**
1. Create a file named `.env` in your project root
2. Add this content (replace YOUR_API_KEY):
```env
SENDGRID_API_KEY=YOUR_API_KEY_HERE
ADMIN_EMAIL=singingbowlandgonghouse@gmail.com
DEFAULT_FROM_EMAIL=singingbowlandgonghouse@gmail.com
```

### Step 3: Test Email
```bash
python manage.py test_email
```

## ✅ Done!

Now when customers make bookings:
- ✅ Client receives confirmation email
- ✅ You receive notification at singingbowlandgonghouse@gmail.com

## 📚 Need More Help?

See `SENDGRID_SETUP.md` for detailed instructions.





