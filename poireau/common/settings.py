"""
Django settings for poireau project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""



from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

COMMON_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(COMMON_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Dev secret key. DO NOT go to production with this.
DEFAULT_SECRET_KEY = 'r#)o^2osljpen358lu$iau5*ji14ip=^$1cj-2b1*mtt&s7is8'
SECRET_KEY = DEFAULT_SECRET_KEY

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


ADMINS = []
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
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collected")

STATICFILES_DIRS = (
    os.path.join(COMMON_DIR, "static"),
)

# Auth
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"

# Application settings
SONGS_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "songs", "test_songs"))
CHOIR_NAME = "Choir"


# Security
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

try:
    from .local_settings import *
except ImportError:
    print("poireau/common/local_settings.py not found or produced an ImportError. Default parameters used.")
