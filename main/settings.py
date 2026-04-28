from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep secret key in production safe
SECRET_KEY = 'django-insecure-&l-%nj^cy*%^x0jjd8az6^4z$!y)9+55==j42^9flw9+s$h+6^'

# ❗ IMPORTANT: set False in production
DEBUG = False


# ✅ FIXED: required for Render deployment
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'self-management-system-2.onrender.com'
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'self_management_system',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # ✅ FIXED (important)
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

WSGI_APPLICATION = 'main.wsgi.application'


# DATABASE (SQLite - OK for small projects)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # ✅ FIXED for India
USE_I18N = True
USE_TZ = True


# STATIC FILES (IMPORTANT for Render)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# (optional but useful)
STATICFILES_DIRS = [
    BASE_DIR / "static"
]