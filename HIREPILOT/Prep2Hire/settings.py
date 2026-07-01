import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file (for local development only; Render injects env vars directly)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# Security
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-+&0#=zd20x+xffu#$7jduvmsb)lihg%w2+$f8hhy4=zc!ms19v')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = ["hire-pilot-s2z7.onrender.com", "localhost", "127.0.0.1"]

# Required in Django 4.0+ when DEBUG=False — allows forms to POST on Render
CSRF_TRUSTED_ORIGINS = [
    "https://hire-pilot-s2z7.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ─────────────────────────────────────────────────────────────────────────────
# Application definition
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Home',
    'jobs',
    'skill_development',
    'resume_analyzer',
    'resume_builder',
    'judge',
    'referrals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be directly after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Prep2Hire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Home.context_processors.supabase_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'Prep2Hire.wsgi.application'

# ─────────────────────────────────────────────────────────────────────────────
# Database
# Uses PostgreSQL on Render (via DATABASE_URL), SQLite locally.
# dj_database_url.config() reads DATABASE_URL and applies SSL for Render.
# ─────────────────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# Auth / redirects
# ─────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_REDIRECT_URL = '/dashboard/'   # go to dashboard after login
LOGOUT_REDIRECT_URL = '/'            # go to home after logout
LOGIN_URL = '/login/'                # where @login_required redirects to

AUTHENTICATION_BACKENDS = [
    'Home.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ─────────────────────────────────────────────────────────────────────────────
# Internationalisation
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────────────────────────
# Static files — WhiteNoise serves them in production
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────────────────────────────────────
# Media files
# ─────────────────────────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────────────────────────────────────
# Email (Brevo HTTP API / SMTP fallback)
# ─────────────────────────────────────────────────────────────────────────────
# Brevo HTTP API (replaces SMTP to avoid Render timeout)
BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
BREVO_SENDER_EMAIL = os.environ.get('BREVO_SENDER_EMAIL', '')

# Keep these for Django's built-in password reset views
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('BREVO_SMTP_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('BREVO_SMTP_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')

# ─────────────────────────────────────────────────────────────────────────────
# Site URL — used in email links; set to your Render domain in production
# ─────────────────────────────────────────────────────────────────────────────
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# ─────────────────────────────────────────────────────────────────────────────
# Supabase Auth
# JS SDK (loaded via CDN in templates) handles OAuth; Django verifies the token.
# ─────────────────────────────────────────────────────────────────────────────
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://mbugyhaebsauetyywgse.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

# ─────────────────────────────────────────────────────────────────────────────
# Google OAuth 2.0
# ─────────────────────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

# ─────────────────────────────────────────────────────────────────────────────
# Razorpay Payment Gateway
# ─────────────────────────────────────────────────────────────────────────────
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '')

# ─────────────────────────────────────────────────────────────────────────────
# Logging Configuration
# ─────────────────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Startup sanity check — warn loudly in logs if critical env vars are missing
# ─────────────────────────────────────────────────────────────────────────────
import logging as _logging
_startup_logger = _logging.getLogger('django')
if not SUPABASE_KEY:
    _startup_logger.warning(
        '[HirePilot] SUPABASE_KEY is not set. '
        'Google OAuth via Supabase will fail. '
        'Set this in your .env file or Render environment variables.'
    )
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    _startup_logger.warning(
        '[HirePilot] GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set. '
        'Configure these in your .env file or Render environment variables.'
    )
