from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd**-4=dxmsvyrkj97ejt=x=3zcbq#^57-&omzb(5g%)@fw0wn@'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    'django_extensions'
]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1', '172.17.0.1')

# Uncomment this line to enable template caching
# Dont forget to change the LOCATION path
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/home/marco.cofano/Documents/wagtail-website/train_climb/cache"
    }
}

STATIC_URL = '/static/'

try:
    from .local import *
except ImportError:
    pass
