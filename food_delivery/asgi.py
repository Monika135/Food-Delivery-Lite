import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

# Safe to import routing here
import bookings.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": None,  # placeholder, will set below
})


from bookings.middleware import JWTAuthMiddleware

application["websocket"] = JWTAuthMiddleware(
    URLRouter(
        bookings.routing.websocket_urlpatterns
    )
)
