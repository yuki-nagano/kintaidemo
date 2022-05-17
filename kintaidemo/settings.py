"""
Django settings for kintaidemo project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/

settings.py for Heroku
https://github.com/heroku/python-getting-started/blob/main/gettingstarted/settings.py
"""

import sentry_sdk
<<<<<<< HEAD
import yaml
=======
<<<<<<< HEAD
import yaml
=======
>>>>>>> 1a85541ecba6d0b117e6f4c426b337c1bee8e85a
>>>>>>> fe530d68e5d1f03596fb6cbb864f23cef13bb9e3
from sentry_sdk.integrations.django import DjangoIntegration


from pathlib import Path
import os
from dotenv import load_dotenv
import django_heroku

load_dotenv()

# 一番上のプロジェクトディレクトリをベースとして指定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS_DIR = os.path.join(BASE_DIR, 'kintaidemo')
default_yaml_path = os.path.join(SETTINGS_DIR, 'default.yaml')

with open(default_yaml_path) as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)

# LOGGING = {
#     'root': {
#         'level': 'DEBUG'
#     },
#     'version': 1,
#     'formatters': 'verbose',
#     'handlers': {
#         'default': {
#             'class': 'logging.StreamHandler'
#         }
#     },
#     'loggers': {
#         'django.server': {
#             'handlers': ['default'],
#             'level': 'DEBUG'
#         }
#     }
# }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

# for local, will set it up by host later
# DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Memo: this is also set on Heroku Config
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['kintaidemo.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # add app
    'kintaiapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'kintaidemo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "kintaiapp/templates")],
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

WSGI_APPLICATION = 'kintaidemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

database_url = os.getenv('DATABASE_URL')

DATABASES = {
    'default': {
        'DATABASE_URL': database_url
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Tokyo" # タイムゾーンを日本時間に設定

USE_I18N = True

USE_TZ = False # TrueにするとDBのタイムゾーンはUTCとなるためFalseに設定


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'kintaiapp/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'kintaiapp/static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())

# 日付表示をYYYY-MM-DDに変更
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
USE_L10N = False

sentry_sdk.init(
    dsn="https://132a721953d14391ab8fe0c5f5079648@o1245804.ingest.sentry.io/6403168",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
<<<<<<< HEAD

globals().update(settings)
=======
<<<<<<< HEAD

globals().update(settings)
=======
>>>>>>> 1a85541ecba6d0b117e6f4c426b337c1bee8e85a
>>>>>>> fe530d68e5d1f03596fb6cbb864f23cef13bb9e3
