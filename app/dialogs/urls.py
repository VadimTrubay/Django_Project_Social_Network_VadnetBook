from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DialogViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"dialogs", DialogViewSet, basename="dialog")
router.register(r"messages", MessageViewSet, basename="message")


urlpatterns = [
    path("", include(router.urls)),
]
