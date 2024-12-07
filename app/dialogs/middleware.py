import os
from urllib.parse import parse_qs

import django
from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import User
from django.db import close_old_connections
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        print("payload", payload)
    except Exception as e:
        print(f"no payload {e}")
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload["exp"])
    if token_exp < datetime.utcnow():
        print("no date-time")
        return AnonymousUser()

    try:
        user = get_user_model().objects.get(id=payload["user_id"])
        print("user", user)
    except User.DoesNotExist:
        print("no user")
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token = dict(scope["headers"])[b"authorization"].decode("utf-8")
            if token.startswith("Bearer "):
                token = token[7:]

            # Извлекаем токен из параметров URL
            # print(scope)
            # Декодируем query_string и парсим параметры
            # query_string = scope['query_string'].decode('utf-8')
            # print(f"Query string received: {query_string}")  # Debug log
            # query_params = parse_qs(query_string)
            #
            # # Извлекаем токен
            # token = query_params.get('token', [None])[0]
            # print(f"Token received: {token}")  # Debug log
            if token is None:
                await send({"type": "websocket.close", "code": 4000})
                return

            print(f"Token received: {token}")  # Debug log
        except ValueError:
            token = None

        scope["user"] = await get_user(token)
        # print("Token scope", scope["user"])
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
