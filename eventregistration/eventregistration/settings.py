"Django settings for eventregistration project."

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# FLAW 1: A01:2021 - Broken Access Control
# Issue: DEBUG mode is enabled in production, exposing sensitive information
SECRET_KEY = 'django-insecure-hardcoded-secret-key-do-not-use-in-production-12345'
DEBUG = True # Exposes error pages with sensitive information
ALLOWED_HOSTS = ['*']  # Allows any host

# FIX 1: Disable DEBUG in production and use environment variables
# import os
# SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-development')
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Source: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # FLAW 2: A01:2021 - Broken Access Control (CSRF Protection Disabled)
    # 'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection is DISABLED
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = 'login'

# FIX 2: Enable CSRF protection by uncommenting the middleware
# Uncomment the line above: 'django.middleware.csrf.CsrfViewMiddleware',
# Source: https://docs.djangoproject.com/en/4.2/ref/csrf/

ROOT_URLCONF = 'eventregistration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventregistration.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []  # FLAW 3 - Weak password validation

# FIX 3: A07:2021 - Identification and Authentication Failures
# Enable strong password validators to prevent weak passwords
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 12,
#         }
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
# Source: https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#module-django.contrib.auth.password_validation

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FLAW 4: A05:2021 - Security Misconfiguration
# Missing security headers
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'ALLOW'

# FIX 4: Enable security headers
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True  # Only in production with HTTPS
# SESSION_COOKIE_SECURE = True  # Only in production with HTTPS
# CSRF_COOKIE_SECURE = True  # Only in production with HTTPS
# Source: https://docs.djangoproject.com/en/4.2/ref/middleware/#module-django.middleware.security