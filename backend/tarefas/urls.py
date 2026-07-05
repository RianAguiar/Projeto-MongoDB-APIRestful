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

'''
json endpoint users
{
    "userId": 1,
    "name": "João Silva",
    "username": "joaosilva",
    "email": "joao@email.com",
    "password": "123456",
    "role": "admin"
}


json endpoint projects
{
    "projectId": 1,
    "name": "Projeto MongoDB",
    "description": "Projeto de estudos",
    "owner": 1
}


json endpoint comments
{
    "commentId": 1,
    "task": 1,
    "body": "A tarefa foi concluída com sucesso.",
    "createdBy": 1,
    "createdAt": "2026-07-05T01:23:43.106454Z"
}

ENDPOINT TASKS QUEBRADA
'''
