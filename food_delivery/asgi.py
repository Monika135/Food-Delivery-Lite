# import os
# import django
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
# django.setup()
# # Safe to import routing here
# import bookings.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": None,  # placeholder, will set below
# })


# from bookings.middleware import JWTAuthMiddleware

# application["websocket"] = JWTAuthMiddleware(
#     URLRouter(
#         bookings.routing.websocket_urlpatterns
#     )
# )

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_delivery.settings")

django.setup()


from bookings.routing import websocket_urlpatterns
from bookings.middleware import JWTAuthMiddleware  # if you have a custom middleware


application = ProtocolTypeRouter({
    "http": django.core.asgi.get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})



# """
# ASGI config for mysite project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = get_asgi_application()
