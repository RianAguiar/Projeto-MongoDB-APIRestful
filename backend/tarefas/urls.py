from django.urls import path
from .views import (
    ProjectAPIView,
    ProjectDetailAPIView,
    UserAPIView,
    UserDetailAPIView,
    TaskAPIView,
    TaskDetailAPIView,
    CommentAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    # Projects
    path("projects/", ProjectAPIView.as_view()),
    path("projects/<int:projectId>/", ProjectDetailAPIView.as_view()),

    # Users
    path("users/", UserAPIView.as_view()),
    path("users/<int:userId>/", UserDetailAPIView.as_view()),

    # Tasks
    path("tasks/", TaskAPIView.as_view()),
    path("tasks/<int:taskId>/", TaskDetailAPIView.as_view()),

    # Comments
    path("comments/", CommentAPIView.as_view()),
    path("comments/<int:commentId>/", CommentDetailAPIView.as_view()),
]