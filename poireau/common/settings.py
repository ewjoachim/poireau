"""
Django settings for poireau project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _

import os

import dj_database_url

COMMON_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(COMMON_DIR)


def from_env(name, default=None, coerce=str):
    """
    Gets the environment variable with that name.
    - returns default if not present (not casted).
    - coerce is a callable that will be called on
        the string value of the env var if provided.
        Ususal coerce callables are int, bool, str, float etc.
        (bool casting will consider as Truthy
        "true", "1" and "yes" (case insensitive),
        everything else will be false.)
    """
    value = os.environ.get(name, None)

    if value is None:
        return default

    if coerce:
        if coerce is bool:
            coerce = lambda v: v.lower() in ("true", "1", "yes")
        return coerce(value)

    return value

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Dev secret key. DO NOT go to production with this.
SECRET_KEY = from_env("SECRET_KEY", default='r#)o^2osljpen358lu$iau5*ji14ip=^$1cj-2b1*mtt&s7is8')

DEBUG = from_env("DEBUG", default=False, coerce=bool)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = from_env("ALLOWED_HOSTS", default="").split(",")


ADMINS = [admin.split(":")[:2] for admin in from_env("ADMINS", default="").split(",")]
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'bootstrap3',
    'poireau.songs',
    'poireau.singers',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'poireau.common.urls'

WSGI_APPLICATION = 'poireau.common.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)

LOCALE_PATHS = (
    os.path.join(COMMON_DIR, "locale"),
)

TEMPLATE_DIRS = (
    os.path.join(COMMON_DIR, "templates"),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collected")

STATICFILES_DIRS = (
    os.path.join(COMMON_DIR, "static"),
)

# Auth
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"

# Application settings
DEFAULT_SONG_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "songs", "test_songs"))
SONGS_FOLDER = from_env("SONGS_FOLDER", default=DEFAULT_SONG_FOLDER)
CHOIR_NAME = from_env("CHOIR_NAME", default="Choir")


# Security
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG


EMAIL_HOST = from_env("EMAIL_HOST", default=from_env("POSTMARK_SMTP_SERVER", default="localhost"))
EMAIL_HOST_USER = from_env("EMAIL_HOST_USER", default=from_env("POSTMARK_API_TOKEN", default=""))
EMAIL_HOST_PASSWORD = from_env("EMAIL_HOST_PASSWORD", default=from_env("POSTMARK_API_TOKEN", default=""))
EMAIL_USE_TLS = from_env("EMAIL_USE_TLS", default=False, coerce=bool)
EMAIL_PORT = from_env("EMAIL_PORT", default=25 if not EMAIL_USE_TLS else 587, coerce=int)
