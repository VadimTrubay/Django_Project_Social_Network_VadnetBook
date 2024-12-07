from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from rest_framework_nested.routers import NestedSimpleRouter
from .views import DialogViewSet

# from .views import MessageViewSet

# Основной роутер для диалогов
router = DefaultRouter()
router.register(r"dialogs", DialogViewSet, basename="dialog")

# # Вложенный роутер для сообщений
# dialogs_router = NestedSimpleRouter(router, r"dialogs", lookup="dialog")
# dialogs_router.register(r"messages", MessageViewSet, basename="dialog-messages")

urlpatterns = [
    path("", include(router.urls)),
    # path("", include(dialogs_router.urls)),
]
