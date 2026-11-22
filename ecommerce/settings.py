
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Safaricom Daraja configuration. Keep secrets in environment variables.
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox').lower()
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', '')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', '')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE', '')
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', '')
MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL', '')
# MPESA_CALLBACK_TOKEN = os.environ.get('MPESA_CALLBACK_TOKEN', '')
MPESA_TRANSACTION_TYPE = os.environ.get('MPESA_TRANSACTION_TYPE', 'CustomerPayBillOnline')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')
if not SECRET_KEY and DEBUG:
    import secrets
    SECRET_KEY = secrets.token_urlsafe(50)
elif not SECRET_KEY and not DEBUG:
    raise ImproperlyConfigured("SECRET_KEY environment variable is required in production")

ALLOWED_HOSTS = [h.strip() for h in os.environ.get(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1'
).split(',') if h.strip()]
for _host in ('.onrender.com', '.vercel.app'):
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get(
    'CSRF_TRUSTED_ORIGINS', ''
).split(',') if o.strip()]
for _origin in ('https://*.onrender.com', 'https://*.vercel.app'):
    if _origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_origin)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'ecommerce.admin.apps.AdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
      'ecommerce.ui.apps.UiConfig',
      'ecommerce.payments.apps.PaymentsConfig',
      'ecommerce.accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'account_profile'
LOGOUT_REDIRECT_URL = 'home'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases
# Uses DATABASE_URL (PostgreSQL, e.g. Render Postgres) when set,
# otherwise falls back to local SQLite for development.
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
    )
}

# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

# STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
MEDIA_URL = '/media/'
# MEDIA_ROOT can be overridden by env var so it points at a mounted
# persistent disk on Render (must equal the disk mountPath).
MEDIA_ROOT = os.environ.get('MEDIA_ROOT') or (BASE_DIR / 'media')

# Vercel Blob Storage for media on Vercel (read-only filesystem)
USE_VERCEL_BLOB = bool(
    os.environ.get('BLOB_READ_WRITE_TOKEN')
    and os.environ.get('BLOB_STORE_ID')
)
if USE_VERCEL_BLOB:
    VERCEL_BLOB_READ_WRITE_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN', '')
    VERCEL_BLOB_STORE_ID = os.environ.get('BLOB_STORE_ID', '')
    DEFAULT_FILE_STORAGE = 'ecommerce.core.storage.VercelBlobStorage'
    MEDIA_URL = f'https://{VERCEL_BLOB_STORE_ID}.blob.vercel-storage.com/'

# WhiteNoise additional settings
WHITENOISE_MAX_AGE = 31536000  # 1 year
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
