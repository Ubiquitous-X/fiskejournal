import os
from ..celery import app as celery_app

environment = os.getenv('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.


__all__ = ('celery_app',)
