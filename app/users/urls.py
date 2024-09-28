from django.urls import path

from users.views import UsersListView, FriendsListView, UserDetailView

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users"),  # path from all users list
    path(
        "users/<uuid:user_id>", UserDetailView.as_view(), name="user_detail"
    ),  # path from one user
    path(
        "users/friends", FriendsListView.as_view(), name="friends"
    ),  # path from only my friends list
]
