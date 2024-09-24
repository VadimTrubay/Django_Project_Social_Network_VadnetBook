from django.urls import path

from users.views import UsersListView, FriendsListView

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users"),  # path from all users list
    path(
        "users/friends", FriendsListView.as_view(), name="friends"
    ),  # path from only my friends list
]
