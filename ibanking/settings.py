import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING
SECRET_KEY = 'django-insecure-rs#^u5)5kmtcnq9x(x0*#m#u$_+#qx($5t!o@%c!yed1a*68di'

DEBUG = True

# ✅ FIXED
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# ---------------- INSTALLED APPS ---------------- #

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'corebank',
    'employee',
]


# ---------------- MIDDLEWARE ---------------- #

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'ibanking.urls'


# ---------------- TEMPLATES ---------------- #

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'ibanking.wsgi.application'


# ---------------- DATABASE ---------------- #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------- EMAIL CONFIG ---------------- #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'khushietiwari28112005@gmail.com'
EMAIL_HOST_PASSWORD = 'fhipaeaynnuyjoqy'


# ---------------- PASSWORD VALIDATION ---------------- #

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


# ---------------- INTERNATIONALIZATION ---------------- #

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------- STATIC FILES ---------------- #

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------- SESSION CONFIG ---------------- #

SESSION_COOKIE_AGE = 300   # 5 minutes
SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# ---------------- LOGIN / LOGOUT ---------------- #

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/customer-dashboard/'
LOGOUT_REDIRECT_URL = '/login/'


# ---------------- CSRF FIX ---------------- #

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


# ---------------- RECAPTCHA ---------------- #

RECAPTCHA_PUBLIC_KEY = '6Lfk3GgsAAAAAM7XPSxS3MJukw3AJrLQTZfCSrMn'
RECAPTCHA_PRIVATE_KEY = '6Lfk3GgsAAAAAP5cMt4_p9Rqjv5W2brWynGkp4Ci'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
