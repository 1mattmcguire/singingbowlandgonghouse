from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env", override=True)
# ---------------------------
# HELPERS
# ---------------------------
def _env_bool(name, default="0"):
    return os.getenv(name, default).strip().lower() in ["1", "true", "yes"]

def _env_csv(name, default=""):
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

# ---------------------------
# CORE SETTINGS
# ---------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "")

DEBUG = _env_bool("DEBUG", "1")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-key"
    else:
        raise ImproperlyConfigured("SECRET_KEY is required")

ALLOWED_HOSTS = _env_csv("ALLOWED_HOSTS", "127.0.0.1,localhost")

# ---------------------------
# INSTALLED APPS (FIXED)
# ---------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # ✅ REQUIRED (fixes your error)
    "django.contrib.sitemaps",  # required so the built-in sitemap.xml template is loadable
    "main",
]

# ✅ REQUIRED FOR SITES
SITE_ID = 1

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------
# URLS / WSGI (FIXED NAME)
# ---------------------------
ROOT_URLCONF = "SingingBallAndGongHouse.urls"
WSGI_APPLICATION = "SingingBallAndGongHouse.wsgi.application"

# ---------------------------
# TEMPLATES
# ---------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "main" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------
# DATABASE
# ---------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------
# PASSWORD VALIDATION
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------
# INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# ---------------------------
# STATIC / MEDIA
# ---------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------
# EMAIL (GMAIL SMTP)
# ---------------------------
# Gmail App Password setup:
# 1) Enable 2-Step Verification on your Google account.
# 2) Open Google Account -> Security -> App passwords.
# 3) Generate an app password for "Mail" and use that value as EMAIL_HOST_PASSWORD.
# 4) Do not use your normal Gmail password here.
# Securely set these in your .env or hosting environment:
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-16-char-app-password
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip()
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "").strip()

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER).strip()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", DEFAULT_FROM_EMAIL).strip()

if not DEBUG and (not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD):
    raise ImproperlyConfigured(
        "EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are required when DEBUG=False"
    )

# ---------------------------
# SECURITY (PRODUCTION)
# ---------------------------
if not DEBUG:
    # The app runs behind a TLS-terminating proxy in production. Trust the
    # forwarded scheme so HTTPS requests are not mistaken for plain HTTP,
    # otherwise SECURE_SSL_REDIRECT will bounce every request in a loop.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
