import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

django.setup()

# Grundläggande loggning för fel och viktiga händelser
logger = logging.getLogger(__name__)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})

logger.info("ASGI application configured with WebSocket support.")
