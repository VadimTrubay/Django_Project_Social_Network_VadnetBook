from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),  # include admin rout
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # include schema swagger rout
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # include schema swagger rout
    path("api/v1/", include("users.urls")),  # include users rout
    path(
        "api/v1/api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # include rest framework rout
]
