from django.shortcuts import render

from django.urls import path
from . import views

urlpatterns = [
    # Projects
    path("projects/", views.ProjectListCreateAPIView.as_view(), name="project-list-create"),
    path("projects/<int:pk>/", views.ProjectRetrieveUpdateDestroyAPIView.as_view(), name="project-detail"),

    # Users
    path("users/", views.UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user-detail"),

    # Tasks
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", views.TaskRetrieveUpdateDestroyAPIView.as_view(), name="task-detail"),

    # Comments
    path("comments/", views.CommentListCreateAPIView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", views.CommentRetrieveUpdateDestroyAPIView.as_view(), name="comment-detail"),
]