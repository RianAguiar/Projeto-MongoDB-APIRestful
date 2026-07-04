from rest_framework import generics
from .models import Project, User, Task, Comment
from .serializers import (
    ProjectSerializer,
    UserSerializer,
    TaskSerializer,
    CommentSerializer,
)

class TaskAPIView(APIView):
    def get(self, request):
        # buscar todas as tarefas no MongoDB
        pass

    def post(self, request):
        # criar uma tarefa
        pass


class TaskDetailAPIView(APIView):
    def get(self, request, taskId):
        # buscar tarefa por taskId
        pass

    def put(self, request, taskId):
        # atualizar tarefa
        pass

    def delete(self, request, taskId):
        # excluir tarefa
        pass