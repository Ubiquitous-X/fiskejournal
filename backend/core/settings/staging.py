from .base import *

DEBUG = True

ALLOWED_HOSTS = ['ubuntuvm']

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://ubuntuvm"]

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'

SESSION_COOKIE_HTTPONLY = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://ubuntuvm",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS"
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
