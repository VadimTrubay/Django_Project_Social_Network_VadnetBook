from django.urls import path

from userprofile.views import (
    UserProfileView,
    ProfileUpdateView,
    ProfileDeleteView,
    ProfileUpdatePhotoView,
    ProfileUpdateStatusView,
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/edit", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/delete", ProfileDeleteView.as_view(), name="profile_delete"),
    path(
        "profile/edit/photo",
        ProfileUpdatePhotoView.as_view(),
        name="profile_edit_photo",
    ),
    path(
        "profile/edit/status",
        ProfileUpdateStatusView.as_view(),
        name="profile_edit_status",
    ),
]
