from .base import *

DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['127.0.0.1','localhost','tapestry-pooling.el.r.appspot.com']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
<<<<<<< HEAD
        'NAME': 'pooling',
        'USER': 'tapestry-staging',
        'PASSWORD': 'pooling@123',
        'HOST': '/cloudsql/[tapestry-pooling:europe-west4:postgres]',
        'PORT': '5432',
=======
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
>>>>>>> 8d50428e3c80c10743dc2a1f10ad34e5d3c38eca
    }
}