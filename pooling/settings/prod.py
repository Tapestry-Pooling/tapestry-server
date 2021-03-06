from .base import *

DEBUG = True
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'tapestry-pooling-f9f8e.ew.r.appspot.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}

SITE_ID = 3

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tapestry-pooling-f9f8e.web.app",
    "https://app.tapestry-pooling.com"
]
