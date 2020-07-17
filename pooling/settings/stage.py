from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pooling',
        'USER': 'tapestry-staging',
        'PASSWORD': 'pooling@123',
        'HOST': '35.204.186.25',
        'PORT': '5432',
    }
}



