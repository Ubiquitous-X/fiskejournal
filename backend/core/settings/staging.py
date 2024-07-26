from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '192.168.1.5', 'ubuntuvm', 'olundsfiske.se']

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://ubuntuvm", "https://olundsfiske.se"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://ubuntuvm", "https://olundsfiske.se"]

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Loggning för produktion
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
