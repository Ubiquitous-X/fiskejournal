from .base import *

DEBUG = True

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

CORS_ALLOW_ALL_ORIGINS = True

SESSION_COOKIE_HTTPONLY = True

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'
