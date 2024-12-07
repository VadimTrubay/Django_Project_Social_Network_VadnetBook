# routing.py
from django.urls import re_path
from .consumers import MessageConsumer

websocket_urlpatterns = [
    re_path(r'^ws/dialogs/(?P<dialog_id>[0-9a-f-]+)/messages/$', MessageConsumer.as_asgi()),
]
