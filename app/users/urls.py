from django.urls import path
from .views import (
    SignupView,
    SigninView,
    LogoutView,
    UserDetailView,
    UserProfileView,
    UsersDetailView,
)

urlpatterns = [
    path(
        "auth/signup", SignupView.as_view(), name="signup"
    ),  # path registration from user
    path("auth/signin", SigninView.as_view(), name="signin"),  # path login from user
    path(
        "auth/profile", UserProfileView.as_view(), name="profile"
    ),  # path profile from user
    path("auth/me", UserDetailView.as_view(), name="me"),  # path about me from user
    path("auth/logout", LogoutView.as_view(), name="logout"),  # path logout from user
    path("auth/users", UsersDetailView.as_view(), name="users"),  # path from users list
]
