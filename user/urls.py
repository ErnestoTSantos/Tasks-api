from django.urls import path

from user.views import DetailUser, ListUser, create_user, status_check

urlpatterns = [
    path("", status_check),
    path("list_users/", ListUser.as_view()),
    path("create_user/", create_user),
    path("user_details/<int:id>/", DetailUser.as_view()),
]
