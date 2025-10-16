import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from bookings.middleware import JWTAuthMiddleware
import bookings.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            bookings.routing.websocket_urlpatterns
        )
    ),
})
