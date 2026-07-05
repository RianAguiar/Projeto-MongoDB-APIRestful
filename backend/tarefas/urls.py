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
    path("projects/", ProjectAPIView.as_view()),  # GET (listar) POST (criar)
    path("projects/<int:projectId>/", ProjectDetailAPIView.as_view()),  # GET (buscar), PUT/PATCH (atualizar), DELETE (remover)

    # Users
    path("users/", UserAPIView.as_view()),  # GET (listar) POST (criar)
    path("users/<int:userId>/", UserDetailAPIView.as_view()),  # GET, PUT/PATCH, DELETE

    # Tasks
    path("tasks/", TaskAPIView.as_view()),  # GET (listar) POST (criar)
    path("tasks/<int:taskId>/", TaskDetailAPIView.as_view()),  # GET, PUT/PATCH, DELETE

    # Comments
    path("comments/", CommentAPIView.as_view()),  # GET (listar) POST (criar)
    path("comments/<int:commentId>/", CommentDetailAPIView.as_view()),  # GET, PUT/PATCH, DELETE
]