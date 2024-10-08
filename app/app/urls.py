from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
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
    path("api/v1/", include("authenticate.urls")),  # include auth rout
    path("api/v1/", include("userprofile.urls")),  # include userprofile rout
    path("api/v1/", include("users.urls")),  # include users rout
    path("api/v1/", include("dialogs.urls")),  # include users rout
    path(
        "api/v1/api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # include rest framework rout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
