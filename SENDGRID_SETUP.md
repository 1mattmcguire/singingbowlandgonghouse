# SendGrid Email Setup Guide

This guide will help you set up SendGrid for sending booking confirmation emails.

## 📋 Prerequisites

1. A SendGrid account (sign up at https://sendgrid.com - free tier available)
2. A verified sender email address (singingbowlandgonghouse@gmail.com)

## 🔑 Step 1: Get Your SendGrid API Key

1. Log in to your SendGrid account: https://app.sendgrid.com
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Give it a name (e.g., "Django Booking System")
5. Select **Full Access** or **Restricted Access** with Mail Send permissions
6. Click **Create & View**
7. **Copy the API key immediately** (you won't be able to see it again!)

## 📧 Step 2: Verify Your Sender Email

1. In SendGrid, go to **Settings** → **Sender Authentication**
2. Click **Verify a Single Sender**
3. Fill in the form:
   - **From Email Address**: singingbowlandgonghouse@gmail.com
   - **From Name**: Singing Bowl & Gong House
   - **Reply To**: singingbowlandgonghouse@gmail.com
   - Complete the rest of the form
4. Check your email and click the verification link

## ⚙️ Step 3: Configure Environment Variables

### Option A: Local Development (Using .env file)

1. Create a `.env` file in your project root (same folder as `manage.py`)
2. Add the following content:

```env
# SendGrid Configuration
SENDGRID_API_KEY=your-actual-sendgrid-api-key-here
DEFAULT_FROM_EMAIL=singingbowlandgonghouse@gmail.com
ADMIN_EMAIL=singingbowlandgonghouse@gmail.com
```

3. Replace `your-actual-sendgrid-api-key-here` with your actual API key from Step 1

### Option B: Production (Render.com or other hosting)

1. Go to your hosting dashboard
2. Navigate to your service → **Environment** or **Environment Variables**
3. Add the following environment variables:

| Key | Value |
|-----|-------|
| `SENDGRID_API_KEY` | Your SendGrid API key |
| `ADMIN_EMAIL` | singingbowlandgonghouse@gmail.com |
| `DEFAULT_FROM_EMAIL` | singingbowlandgonghouse@gmail.com |

## 🧪 Step 4: Test Your Email Configuration

After setting up your API key, test the email configuration:

```bash
python manage.py test_email
```

Or test with specific email addresses:

```bash
python manage.py test_email --client-email=your-email@example.com --admin-email=singingbowlandgonghouse@gmail.com
```

## ✅ Step 5: Verify It's Working

1. Make a test booking through your website
2. Check that:
   - ✅ Client receives a confirmation email
   - ✅ Admin (singingbowlandgonghouse@gmail.com) receives a notification email

## 🔍 Troubleshooting

### Issue: "SendGrid API key not found"
- **Solution**: Make sure you've set `SENDGRID_API_KEY` in your `.env` file or environment variables
- **Check**: Run `python manage.py test_email` to see current configuration

### Issue: "Email not sending"
- **Solution**: Verify your sender email is verified in SendGrid
- **Check**: Go to SendGrid → Settings → Sender Authentication

### Issue: "Authentication failed"
- **Solution**: Verify your API key is correct and has Mail Send permissions
- **Check**: Create a new API key if needed

### Issue: Emails going to spam
- **Solution**: 
  - Verify your sender email in SendGrid
  - Set up domain authentication (recommended for production)
  - Check SendGrid activity logs

## 📊 Monitoring

- Check SendGrid dashboard for email delivery statistics
- View email activity: https://app.sendgrid.com/activity
- Check bounce/spam reports if emails aren't being delivered

## 🔒 Security Notes

- ✅ Never commit your `.env` file to git (it's already in `.gitignore`)
- ✅ Never share your API key publicly
- ✅ Use environment variables in production
- ✅ Rotate API keys periodically

## 📞 Support

If you encounter issues:
1. Check SendGrid activity logs
2. Run `python manage.py test_email` to diagnose
3. Check Django logs for error messages
4. Verify API key permissions in SendGrid dashboard

---

**Note**: The system will automatically fall back to Gmail SMTP if SendGrid API key is not set, but SendGrid is recommended for production use.





