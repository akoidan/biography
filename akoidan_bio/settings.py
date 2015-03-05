"""
Django settings for akoidan_bio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.conf import global_settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sl!g$fcf89grtd_&)e)l2!0u84i!bm&4_r8x^ody68sfcz_q6_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    # TODO fix hardcoded dirname
    join(BASE_DIR + '/akoidan_bio/', 'templates'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'akoidan_bio',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'akoidan_bio.request_middware.RequestMiddleware'
)

ROOT_URLCONF = 'akoidan_bio.urls'

WSGI_APPLICATION = 'akoidan_bio.wsgi.application'

# AUTH_USER_MODEL = 'akoidan_bio.models.UserProfile'
AUTH_USER_MODEL = 'akoidan_bio.UserProfile'


TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'akoidan_bio.context_processors.create_login_out_page',
)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

REQUESTS_COUNT = 10

DEFAULT_PROFILE_ID = 1

USE_TZ = True

MEDIA_ROOT =  os.path.join(BASE_DIR, 'photos')

MEDIA_URL = "photo/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
