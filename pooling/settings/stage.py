from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','tapestry-pooling.el.r.appspot.com']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pooling',
        'USER': 'tapestry-staging',
        'PASSWORD': 'pooling@123',
        'HOST': '/cloudsql/[tapestry-pooling:europe-west4:postgres]',
        'PORT': '5432',
    }
}