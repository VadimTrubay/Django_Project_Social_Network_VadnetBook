from django.urls import path
from .views import SignupView, SigninView, LogoutView, UserDetailView

urlpatterns = [
    path(
        "auth/signup", SignupView.as_view(), name="signup"
    ),  # path registration from user
    path("auth/signin", SigninView.as_view(), name="signin"),  # path login from user
    path("auth/me", UserDetailView.as_view(), name="me"),  # path about me from user
    path("auth/logout", LogoutView.as_view(), name="logout"),  # path logout from user
]
