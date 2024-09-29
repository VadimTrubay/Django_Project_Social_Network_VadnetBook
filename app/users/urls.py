from django.urls import path

from users.views import (
    UsersListView,
    UserDetailView,
    FollowUserView,
    UnfollowUserView,
    FollowersListView,
    FollowingListView,
    # UsersSearchResultsView,
)

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users"),  # path from all users list
    path(
        "users/<uuid:user_id>", UserDetailView.as_view(), name="user_detail"
    ),  # path from one user
    # Подписаться на пользователя
    path("users/follow/<uuid:user_id>", FollowUserView.as_view(), name="follow_user"),
    # Отписаться от пользователя
    path(
        "users/unfollow/<uuid:user_id>",
        UnfollowUserView.as_view(),
        name="unfollow_user",
    ),
    # Список подписчиков
    path("users/followers", FollowersListView.as_view(), name="followers_list"),
    # Список тех, на кого подписан пользователь
    path("users/following", FollowingListView.as_view(), name="following_list"),
    # # Поиск пользователей по имени
    # path("users/search", UsersSearchResultsView.as_view(), name="search"),
]
