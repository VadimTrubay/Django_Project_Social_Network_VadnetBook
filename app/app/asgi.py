import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from dialogs.consumers import MessageConsumer
from dialogs.middleware import TokenAuthMiddleware
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(  # Ваш middleware для WebSocket
            URLRouter(
                [
                    re_path(
                        "^ws/dialogs/(?P<dialog_id>[0-9a-f-]+)/messages/$",
                        MessageConsumer.as_asgi(),
                    ),  # Пример маршрута
                ]
            )
        ),
    }
)
