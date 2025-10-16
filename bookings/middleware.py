from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()  # This is safe because get_user_model() doesn't hit DB yet

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        # Lazy import here
        self.scope["user"] = await self.get_user(token)
        inner = self.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def get_user(self, token):
        # Lazy import of model here
        from django.contrib.auth.models import AnonymousUser

        if not token:
            return AnonymousUser()
        try:
            validated_token = UntypedToken(token)
            user = JWTAuthentication().get_user(validated_token)
            return user
        except Exception:
            return AnonymousUser()
