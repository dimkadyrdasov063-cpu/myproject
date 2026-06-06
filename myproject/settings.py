"""
Django settings for myproject project.
"""
import os
import sys
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ── SECURITY ───────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-zzx3)g01)vm_c-&o@v9-ad3(2^&mqe+xh%$cctim-=ua6v(5k+')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://*.onrender.com',
]

LOGIN_REDIRECT_URL = '/myapp/'
LOGOUT_REDIRECT_URL = '/myapp/'
LOGIN_URL = 'articles:login'
PASSWORD_RESET_TIMEOUT = 86400

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'dimka_app',
    'blog',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # для статики на render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# ── DATABASE ───────────────────────────────────────────
# локально берёт sqlite, на render берёт PostgreSQL из DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3'
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── STATIC ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'