from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from django.core.mail import send_mail

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env (local dev)
load_dotenv(dotenv_path=BASE_DIR / ".env")

# ---------------------------
# Helpers
# ---------------------------
def _env_bool(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _env_csv(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [part.strip() for part in raw.split(",") if part.strip()]


# ---------------------------
# Core settings
# ---------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
DEBUG = _env_bool("DEBUG", "0")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-development-only-change-me"
    else:
        raise ImproperlyConfigured("SECRET_KEY environment variable is required when DEBUG=False.")

ALLOWED_HOSTS = _env_csv("ALLOWED_HOSTS")

render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
if render_hostname:
    ALLOWED_HOSTS = list(dict.fromkeys([*ALLOWED_HOSTS, render_hostname]))

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# ---------------------------
# Application definition
# ---------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

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

ROOT_URLCONF = "SingingBallAndGongHouse.urls"

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

WSGI_APPLICATION = "SingingBallAndGongHouse.wsgi.application"


# ---------------------------
# Database
# ---------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=int(os.getenv("CONN_MAX_AGE", "600")),
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ---------------------------
# Password validation
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------
# Internationalization
# ---------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kathmandu").strip()
USE_I18N = True
USE_TZ = True


# ---------------------------
# Static / Media
# ---------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===========================
# Email Configuration (SMTP)
# ===========================
# IMPORTANT: Uses these env vars:
# EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL,
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL, ADMIN_EMAIL, EMAIL_TIMEOUT

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'singingbowlandgonghouse@gmail.com'
EMAIL_HOST_PASSWORD ='hlsajhwhdgfqosgo'

# Use authenticated SMTP user by default (best for Gmail)
DEFAULT_FROM_EMAIL = 'singingbowlandgonghouse@gmail.com'
ADMIN_EMAIL = 'singingbowlandgonghouse@gmail.com'

EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "10"))

# Validate SMTP settings
if not EMAIL_HOST or not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    if DEBUG:
        # Dev fallback: print emails to console
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
        print("⚠️ Email running in CONSOLE mode (missing SMTP settings).")
        print("EMAIL_HOST:", EMAIL_HOST)
        print("EMAIL_HOST_USER:", EMAIL_HOST_USER)
        print("EMAIL_HOST_PASSWORD set?:", bool(EMAIL_HOST_PASSWORD))
    else:
        raise ImproperlyConfigured(
            "EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD are required when DEBUG=False."
        )


# WhatsApp Configuration
ADMIN_WHATSAPP_NUMBER = os.getenv("ADMIN_WHATSAPP_NUMBER", "+9779843213802").strip()


# ---------------------------
# Security (recommended when DEBUG=False)
# ---------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", "1")
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", "1")
    CSRF_COOKIE_SECURE = _env_bool("CSRF_COOKIE_SECURE", "1")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Example:
    # CSRF_TRUSTED_ORIGINS=https://your-service.onrender.com,https://www.yourdomain.com
    CSRF_TRUSTED_ORIGINS = _env_csv("CSRF_TRUSTED_ORIGINS")


# ---------------------------
# Optional: Email logging (helps debug delivery problems)
# ---------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.core.mail": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}