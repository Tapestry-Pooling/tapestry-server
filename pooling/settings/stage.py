from .base import *

DEBUG = os.environ['DEBUG']
# SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['127.0.0.1','localhost','tapestry-pooling-284109.ew.r.appspot.com']

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

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


CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://dev-tapestry-pooling-aea91.web.app"
]

