"""
Django settings for challenge project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "local")

if ENVIRONMENT == "local":
    DEBUG = True
    SECRET_KEY = "django-insecure-69#4zj@w1*i*p=abwm_ll)*6-5aozqs(co2fl6)!xfqla*7u4a"
    ALLOWED_HOSTS = ["localhost"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    STRAVA_VERIFY_TOKEN = "supersecretkey"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    ADMINS = [("Site Admin", "webmaster@localhost")]
else:
    DEBUG = os.getenv("DJANGO_DEBUG", False)
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    ALLOWED_HOSTS = ["results.romseyroadrunners.co.uk"]
    CSRF_TRUSTED_ORIGINS = ["https://results.romseyroadrunners.co.uk"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "postgresql",
            "USER": os.getenv("DB_USERNAME"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "NAME": os.getenv("DB_NAME"),
            "CONN_MAX_AGE": 300,
        }
    }
    STATIC_ROOT = "/static/"
    STRAVA_VERIFY_TOKEN = os.getenv("STRAVA_VERIFY_TOKEN")
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ADMINS = [("Site Admin", EMAIL_HOST_USER)]

# Email subject prefix used for emails to admins or managers
EMAIL_SUBJECT_PREFIX = "[RRR Club Results] "

# Application definition

INSTALLED_APPS = [
    "main.apps.MainConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # social providers
    "allauth.socialaccount.providers.strava",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "challenge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "challenge.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
LOGIN_REDIRECT_URL = "index"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_ADAPTER = "challenge.auth_adapter.DeactivateSocialAccountAdapter"
ACCOUNT_ADAPTER = "challenge.auth_adapter.DeactivateAccountAdapter"
ACCOUNT_FORMS = {"signup": "challenge.auth_adapter.AccountSignupForm"}

SOCIALACCOUNT_FORMS = {"signup": "challenge.auth_adapter.SocialAccountSignupForm"}

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_STORE_TOKENS = True

LOGLEVEL = os.getenv("LOGLEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGLEVEL,
    },
    "loggers": {
        "stravalib": {"handlers": ["console"], "propagate": True, "level": "WARNING"}
    },
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = "rrr-club-challenge"
AWS_S3_REGION_NAME = "eu-west-1"
