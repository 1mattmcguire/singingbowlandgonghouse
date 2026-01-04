# Deployment Guide for Singing Bowl & Gong House

## 🚀 Quick Start - Deploy Your Website

### Step 1: Buy a Domain
**Recommended Domain Registrars:**
- **Namecheap** (https://www.namecheap.com) - $10-15/year, easy to use
- **Google Domains** (https://domains.google) - $12/year
- **GoDaddy** (https://www.godaddy.com) - Popular but slightly more expensive

**Domain Suggestions:**
- `singingbowlandgonghouse.com`
- `singingbowlgonghouse.com`
- `soundhealingnepal.com`

### Step 2: Choose a Hosting Platform

#### **Option A: Railway (Recommended for Beginners)**
- **Website:** https://railway.app
- **Cost:** ~$5-20/month (has free trial)
- **Pros:** Very easy, automatic deployments, free SSL
- **Steps:**
  1. Sign up at Railway
  2. Connect your GitHub repository
  3. Railway auto-detects Django
  4. Add environment variables
  5. Deploy!

#### **Option B: Render (Free Tier Available)**
- **Website:** https://render.com
- **Cost:** Free tier available, $7/month for production
- **Pros:** Free tier, easy setup, good documentation
- **Steps:**
  1. Sign up at Render
  2. Create new Web Service
  3. Connect GitHub repo
  4. Use build command: `pip install -r requirements.txt`
  5. Start command: `gunicorn SingingBallAndGongHouse.wsgi:application`

#### **Option C: PythonAnywhere (Easiest)**
- **Website:** https://www.pythonanywhere.com
- **Cost:** $5/month (Beginner plan)
- **Pros:** Very beginner-friendly, good for Django
- **Steps:**
  1. Sign up at PythonAnywhere
  2. Upload your files
  3. Configure web app
  4. Point domain to your account

#### **Option D: DigitalOcean App Platform**
- **Website:** https://www.digitalocean.com/products/app-platform
- **Cost:** $5/month
- **Pros:** Reliable, good performance
- **Steps:**
  1. Sign up at DigitalOcean
  2. Create App from GitHub
  3. Configure environment
  4. Deploy

### Step 3: Prepare Your Code for Production

#### 3.1 Update Settings for Production

I've created a `settings_production.py` file. You'll need to:
1. Set `DEBUG = False`
2. Add your domain to `ALLOWED_HOSTS`
3. Use environment variables for secrets

#### 3.2 Update Requirements

Add production dependencies to `requirements.txt`:
- `gunicorn` (WSGI server)
- `whitenoise` (static files)
- `psycopg2-binary` (if using PostgreSQL)
- `python-decouple` (for environment variables)

#### 3.3 Create Environment Variables

Never commit secrets to code! Use environment variables:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `EMAIL_HOST_PASSWORD`

### Step 4: Deploy Checklist

Before deploying, make sure:

- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Secret key is in environment variables (not in code)
- [ ] Database is configured (PostgreSQL recommended)
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] Migrations are run (`python manage.py migrate`)
- [ ] Email settings are configured
- [ ] SSL/HTTPS is enabled (most platforms do this automatically)

### Step 5: Connect Domain to Hosting

1. Get your hosting platform's nameservers or IP address
2. Go to your domain registrar
3. Update DNS settings:
   - **Option A:** Update nameservers (easiest)
   - **Option B:** Add A record pointing to hosting IP
   - **Option C:** Add CNAME record

### Step 6: Post-Deployment

1. Test all pages work
2. Test booking form submission
3. Test contact form submission
4. Verify emails are being sent
5. Check admin panel works
6. Test on mobile devices

## 📋 Detailed Platform-Specific Guides

### Railway Deployment

1. **Create Account:** https://railway.app
2. **New Project** → Deploy from GitHub
3. **Add Environment Variables:**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```
4. **Add PostgreSQL** (optional but recommended)
5. **Deploy!**

### Render Deployment

1. **Create Account:** https://render.com
2. **New Web Service** → Connect GitHub
3. **Settings:**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn SingingBallAndGongHouse.wsgi:application`
4. **Add Environment Variables**
5. **Add PostgreSQL Database** (free tier available)
6. **Deploy!**

### PythonAnywhere Deployment

1. **Create Account:** https://www.pythonanywhere.com
2. **Upload Files** via Files tab
3. **Create Web App:**
   - Manual configuration
   - Python 3.10
   - Django
4. **Configure WSGI file**
5. **Set up static files**
6. **Reload Web App**

## 🔒 Security Checklist

- [ ] `DEBUG = False` in production
- [ ] Secret key is secure and in environment variables
- [ ] `ALLOWED_HOSTS` is set correctly
- [ ] HTTPS/SSL is enabled
- [ ] Database credentials are secure
- [ ] Email password is in environment variables
- [ ] Admin panel has strong password
- [ ] CSRF protection is enabled (default in Django)

## 📧 Email Configuration

Your email is already configured! Just make sure:
- Gmail App Password is in environment variables
- `EMAIL_HOST_PASSWORD` is set correctly
- Test email sending after deployment

## 🆘 Need Help?

Common issues:
1. **Static files not loading:** Run `collectstatic` command
2. **500 errors:** Check `DEBUG = False` and `ALLOWED_HOSTS`
3. **Database errors:** Make sure migrations are run
4. **Email not working:** Verify App Password is correct

## 💰 Estimated Costs

- **Domain:** $10-15/year
- **Hosting:** $5-20/month
- **Total:** ~$70-255/year

## 🎉 You're Ready!

Your Django site is ready to deploy. Choose a platform, follow the steps, and your website will be live!








