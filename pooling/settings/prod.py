from .base import *

DEBUG = False

ALLOWED_HOSTS = ['', ]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pooling',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '/cloudsql/[tapestry-pooling:europe-west4:postgres]',
        'PORT': '5432',
    }
}



