from django.urls import path

from authenticate.views import SignUpView, SignInView, UserDetailView

urlpatterns = [
    path("auth/signup", SignUpView.as_view(), name="signup"),
    path("auth/signin", SignInView.as_view(), name="signin"),
    path("auth/me", UserDetailView.as_view(), name="me"),
]
