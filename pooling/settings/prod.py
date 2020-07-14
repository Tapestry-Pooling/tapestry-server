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
        'PASSWORD': 'password1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



