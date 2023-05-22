import re
import os
import logging.config
from django.core.management import utils
from webui.PCWConfig import ConfigFile, CONFIG_FILE

"""
Django settings for webui project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# See https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = utils.get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('PCW_DEBUG', False)

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('DOMAINNAME', os.uname().nodename)]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Application definition

INSTALLED_APPS = [
    'ocw.apps.OcwConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'dbbackup',
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

ROOT_URLCONF = 'webui.urls'

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

WSGI_APPLICATION = 'webui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 30,  # Mitigate https://docs.djangoproject.com/en/dev/ref/databases/#database-is-locked-errors
        }
    }
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'db.backups')}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                + 'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                + 'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                + 'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATIC_URL = '/static/'

loglevel = 'INFO'

if os.path.exists(CONFIG_FILE):
    loglevel = ConfigFile().get('default/loglevel', loglevel)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'ocw': {
            'level': loglevel,
            'handlers': ['console'],
            'propagate': False,
        }
    },
})


def build_absolute_uri(path=''):
    ''' Create a absolute url from given path. You could use reverse() to create a path which points to a specific
    view.
    Parameters:
    -----------
    path : (optional) give the path which will appended to the base URL

    Example:
    --------
         url = build_absolute_uri(reverse(views.delete, args=[i.id]))
    '''
    base_url = ConfigFile().get('default/base-url', "publiccloud.qa.suse.de")

    if not re.match('^http', base_url):
        base_url = 'https://{}'.format(base_url)

    base_url = re.sub('/+$', '', base_url)

    if len(path) == 0:
        return base_url

    if not re.match('^/', path):
        path = '/{}'.format(path)

    return base_url + path
