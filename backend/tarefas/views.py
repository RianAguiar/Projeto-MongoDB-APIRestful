from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import repository
from .serializers import (
    ProjectSerializer,
    UserSerializer,
    TaskSerializer,
    CommentSerializer,
)


# ---------------- PROJECTS ----------------

class ProjectAPIView(APIView):
    def get(self, request):
        projects = repository.list_projects()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["createdAt"] = timezone.now()
        data["updatedAt"] = timezone.now()
        created = repository.create_project(data)
        return Response(ProjectSerializer(created).data, status=status.HTTP_201_CREATED)


class ProjectDetailAPIView(APIView):
    def get(self, request, projectId):
        project = repository.get_project(projectId)
        if not project:
            return Response({"detail": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProjectSerializer(project).data)

    def put(self, request, projectId):
        project = repository.get_project(projectId)
        if not project:
            return Response({"detail": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["updatedAt"] = timezone.now()
        updated = repository.update_project(projectId, data)
        return Response(ProjectSerializer(updated).data)

    def delete(self, request, projectId):
        deleted = repository.delete_project(projectId)
        if not deleted:
            return Response({"detail": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- USERS ----------------

class UserAPIView(APIView):
    def get(self, request):
        users = repository.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["password"] = make_password(data["password"])
        data["createdAt"] = timezone.now()
        data["updatedAt"] = timezone.now()
        created = repository.create_user(data)
        return Response(UserSerializer(created).data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(APIView):
    def get(self, request, userId):
        user = repository.get_user(userId)
        if not user:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    def put(self, request, userId):
        user = repository.get_user(userId)
        if not user:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if "password" in data:
            data["password"] = make_password(data["password"])
        data["updatedAt"] = timezone.now()
        updated = repository.update_user(userId, data)
        return Response(UserSerializer(updated).data)

    def delete(self, request, userId):
        deleted = repository.delete_user(userId)
        if not deleted:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- TASKS ----------------

class TaskAPIView(APIView):
    def get(self, request):
        tasks = repository.list_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["createdAt"] = timezone.now()
        data["updatedAt"] = timezone.now()
        created = repository.create_task(data)
        return Response(TaskSerializer(created).data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    def get(self, request, taskId):
        task = repository.get_task(taskId)
        if not task:
            return Response({"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        return Response(TaskSerializer(task).data)

    def put(self, request, taskId):
        task = repository.get_task(taskId)
        if not task:
            return Response({"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["updatedAt"] = timezone.now()

        # se a tarefa está sendo marcada como concluída agora
        if data.get("done") and not task.get("done"):
            data["completedAt"] = timezone.now()

        updated = repository.update_task(taskId, data)
        return Response(TaskSerializer(updated).data)

    def delete(self, request, taskId):
        deleted = repository.delete_task(taskId)
        if not deleted:
            return Response({"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- COMMENTS ----------------

class CommentAPIView(APIView):
    def get(self, request):
        comments = repository.list_comments()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["createdAt"] = timezone.now()
        data["updatedAt"] = timezone.now()
        created = repository.create_comment(data)
        return Response(CommentSerializer(created).data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    def get(self, request, commentId):
        comment = repository.get_comment(commentId)
        if not comment:
            return Response({"detail": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(CommentSerializer(comment).data)

    def put(self, request, commentId):
        comment = repository.get_comment(commentId)
        if not comment:
            return Response({"detail": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["updatedAt"] = timezone.now()
        updated = repository.update_comment(commentId, data)
        return Response(CommentSerializer(updated).data)

    def delete(self, request, commentId):
        deleted = repository.delete_comment(commentId)
        if not deleted:
            return Response({"detail": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)