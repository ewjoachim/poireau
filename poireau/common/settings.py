"""
Django settings for poireau project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from __future__ import unicode_literals

import json

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

CONFIGURATION = {}

if "POIREAU_CONFIGURATION_FILE" in os.environ:
    try:
        with open(os.environ["POIREAU_CONFIGURATION_FILE"], "r") as file_handler:
            CONFIGURATION = json.load(file_handler)
    except IOError:
        raise ValueError(
            "Env var POIREAU_CONFIGURATION_FILE is found but the file is not found at location {}".format(
                os.environ["POIREAU_CONFIGURATION_FILE"]
            )
        )


def from_environ(param_name, default=None):
    """
    Will search the environment variables for one named "<SETTING_NAME>"
    and use it or use provided default.
    """
    return CONFIGURATION.get(param_name, default)


COMMON_DIR = os.path.dirname(unicode(__file__))
BASE_DIR = os.path.dirname(COMMON_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Dev secret key. DO NOT go to production with this.
DEFAULT_SECRET_KEY = 'r#)o^2osljpen358lu$iau5*ji14ip=^$1cj-2b1*mtt&s7is8'
SECRET_KEY = from_environ("SECRET_KEY", DEFAULT_SECRET_KEY)

DEBUG = from_environ("DEBUG", "1") == "1"

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = from_environ("ALLOWED_HOSTS", "").split(",")


ADMINS = [admin.split(":") for admin in from_environ("ADMINS", "").split(",")]
MANAGERS = ADMINS

EMAIL_SETTINGS = {
    "host": "localhost",
    "user": "",
    "password": "",
    "tls": True,
    "port": 587
}
EMAIL_SETTINGS.update(json.loads(from_environ("MAIL_SETTINGS", "{}")))

EMAIL_HOST = EMAIL_SETTINGS["host"]
EMAIL_HOST_USER = EMAIL_SETTINGS["user"]
EMAIL_HOST_PASSWORD = EMAIL_SETTINGS["password"]
EMAIL_USE_TLS = EMAIL_SETTINGS["tls"]
EMAIL_PORT = EMAIL_SETTINGS["port"]

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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "collected")

STATICFILES_DIRS = (
    os.path.join(COMMON_DIR, "static"),
)

# Auth
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"

# Application settings
SONGS_FOLDER = from_environ("SONGS_FOLDER", os.path.normpath(os.path.join(BASE_DIR, "songs", "test_songs")))
CHOIR_NAME = from_environ("CHOIR_NAME", "Choir")


# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

