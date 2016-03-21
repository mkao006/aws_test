"""
Django settings for random_walker project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
import dj_database_url
import json
from django.core.exceptions import ImproperlyConfigured
from unipath import Path

BASE_DIR = Path(__file__).ancestor(2)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, "random_walker/settings.json")) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """ Get the secret variable or return explicit exception."""

    try:
        return secrets[setting]
    except:
        error_msg = "Set the {0} environment variable".format(settting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = get_secret("BUCKET_NAME")
AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# if socket.gethostname() == 'mk-IdeaPad-U330p':
#     DEBUG = True
# else:
#     DEBUG = False
DEBUG = True

# ALLOWED_HOSTS = ['emperorkao.com']
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'random_walker',
    'user_action',
    'django_mobile',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
)

ROOT_URLCONF = 'random_walker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'random_walker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'random_walker_aws_test',
            'USER': 'mk',
            'PASSWORD': 'kbmk1986',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

##
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# # Tell django-storages that when coming up with the URL for an item in
# # S3 storage, keep it simple - just use this domain plus the path. (If
# # this isn't set, things get complicated). This controls how the
# # `static` template tag from `staticfiles` gets expanded, if you're
# # using it.

# # We also use it in the next setting.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# # This is used by the `static` template tag from `static`, if you're
# # using that. Or if anything else refers directly to STATIC_URL. So
# # it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# # Tell the staticfiles app to use S3Boto storage when writing the
# # collected static files (when you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# LOGIN_URL = os.path.join(BASE_DIR, 'registration/login_view/')
