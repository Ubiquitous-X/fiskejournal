from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '192.168.1.5', 'ubuntuvm', '104.248.252.143', 'olundsfiske.se']

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://ubuntuvm", "https://olundsfiske.se"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://ubuntuvm", "https://olundsfiske.se"]

STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'

# Loggning för produktion
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

# Ensure that the CSRF cookie is only sent over HTTPS
CSRF_COOKIE_SECURE = True

# Ensure that the CSRF cookie is only sent in same-site requests
CSRF_COOKIE_SAMESITE = 'Strict'

# Ensure that the session cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True

# Enable the browser's XSS filter
SECURE_BROWSER_XSS_FILTER = True
#
# # Ensure that the browser only recognizes certain content types
SECURE_CONTENT_TYPE_NOSNIFF = True
#
# # Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True
#
# # Prevent the application from being displayed within a frame or iframe
# X_FRAME_OPTIONS = 'DENY'
#
# # Enable HSTS (HTTP Strict Transport Security) with a max age of one year
# SECURE_HSTS_SECONDS = 31536000
#
# # Include all subdomains in the HSTS policy
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#
# # Enable HSTS preload
SECURE_HSTS_PRELOAD = True
#
# # Set the referrer policy to 'strict-origin-when-cross-origin'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
#
# # Specify the header that the proxy uses to indicate HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#
# # Specify a list of commands that should be refused on the server
# SECURE_REFUSE_COMMANDS = ['rm', 'wget', 'curl']
#
# # Ensure that the session cookie is only accessible via HTTP
# SESSION_COOKIE_HTTPONLY = True
#
# # Ensure that the session cookie is only sent in same-site requests
# SESSION_COOKIE_SAMESITE = 'Lax'
#
# # # Ensure that the session expires when the user closes their browser
# # SESSION_EXPIRE_AT_BROWSER_CLOSE = True
