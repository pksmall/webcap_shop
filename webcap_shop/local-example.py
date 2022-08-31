import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost')
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('POSTGRES_PORT', '6379')
REDIS_USERNAME = os.environ.get('REDIS_USER', '')
REDIS_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

if REDIS_USERNAME and REDIS_PASSWORD:
    REDIS_DATA = 'redis://' + REDIS_USERNAME + ':' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + REDIS_PORT
else:
    REDIS_DATA = 'redis://' + REDIS_HOST + ':' + REDIS_PORT

CACHES = {
     'default': {
         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
         'LOCATION': REDIS_DATA,
         'TIMEOUT': None,
     }
}
