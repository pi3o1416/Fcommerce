
from .base import *

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DEV_DB_NAME'),
        'USER': env('DEV_DB_USER'),
        'PASSWORD': env('DEV_DB_PASS'),
        'HOST': env('DEV_DB_HOST'),
        'PORT': env('DEV_DB_PORT')
    }
}

CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TIME_LIMIT = 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://localhost:6379/'

# PG Settings

PG_PAYMENT_INITIATE_URL = 'https://sandbox.aamarpay.com/jsonpost.php'
TRXN_DETAIL_URL = 'https://sandbox.aamarpay.com/api/v1/trxcheck/request.php'
