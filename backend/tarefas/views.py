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

        # regra: owner precisa existir
        if not repository.user_exists(data["owner"]):
            return Response(
                {"detail": "Usuário 'owner' informado não existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # regra: todos os membros informados precisam existir
        member_ids = data.get("users", [])
        for member_id in member_ids:
            if not repository.user_exists(member_id):
                return Response(
                    {"detail": f"Usuário {member_id} informado em 'users' não existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # regra: o owner sempre é membro do próprio projeto
        if data["owner"] not in member_ids:
            member_ids.append(data["owner"])
        data["users"] = member_ids

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

        if not repository.user_exists(data["owner"]):
            return Response(
                {"detail": "Usuário 'owner' informado não existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member_ids = data.get("users", [])
        for member_id in member_ids:
            if not repository.user_exists(member_id):
                return Response(
                    {"detail": f"Usuário {member_id} informado em 'users' não existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # regra: o owner não pode deixar de ser membro do projeto
        if data["owner"] not in member_ids:
            member_ids.append(data["owner"])
        data["users"] = member_ids

        data["updatedAt"] = timezone.now()
        updated = repository.update_project(projectId, data)
        return Response(ProjectSerializer(updated).data)

    def delete(self, request, projectId):
        project = repository.get_project(projectId)
        if not project:
            return Response({"detail": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # regra: apagar um projeto remove em cascata suas tarefas e os comentários delas
        repository.delete_project_cascade(projectId)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- USERS ----------------

class UserAPIView(APIView):
    def get(self, request):
        users_list = repository.list_users()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # regra: username e email precisam ser únicos
        if repository.username_or_email_taken(data["username"], data["email"]):
            return Response(
                {"detail": "Nome de usuário ou e-mail já cadastrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        # regra: username e email precisam continuar únicos (ignorando o próprio usuário)
        if repository.username_or_email_taken(data["username"], data["email"], exclude_user_id=userId):
            return Response(
                {"detail": "Nome de usuário ou e-mail já cadastrado para outro usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "password" in data:
            data["password"] = make_password(data["password"])
        data["updatedAt"] = timezone.now()
        updated = repository.update_user(userId, data)
        return Response(UserSerializer(updated).data)

    def delete(self, request, userId):
        user = repository.get_user(userId)
        if not user:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # regra: não dá pra excluir um usuário dono de projeto(s)
        if repository.user_owns_any_project(userId):
            return Response(
                {"detail": "Usuário não pode ser excluído pois é dono de um ou mais projetos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        repository.delete_user(userId)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- TASKS ----------------

class TaskAPIView(APIView):
    def get(self, request):
        tasks_list = repository.list_tasks()
        serializer = TaskSerializer(tasks_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        project = repository.get_project(data["project"])
        if not project:
            return Response({"detail": "Projeto informado não existe."}, status=status.HTTP_400_BAD_REQUEST)

        # regra: quem cria a tarefa precisa ser membro do projeto
        if not repository.is_project_member(project, data["createdBy"]):
            return Response(
                {"detail": "Usuário 'createdBy' não é membro do projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        completed_by = data.get("completedBy")

        if data.get("done"):
            # regra: tarefa criada já concluída precisa informar quem concluiu,
            # e essa pessoa precisa ser membro do projeto
            if not completed_by:
                return Response(
                    {"detail": "'completedBy' é obrigatório quando a tarefa é criada como concluída."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not repository.is_project_member(project, completed_by):
                return Response(
                    {"detail": "Usuário 'completedBy' não é membro do projeto."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data["completedAt"] = timezone.now()
        else:
            # regra: tarefa não concluída não pode ter dados de conclusão
            data["completedAt"] = None
            data["completedBy"] = None
            completed_by = None

        data["createdAt"] = timezone.now()
        data["updatedAt"] = timezone.now()
        created = repository.create_task(data)

        if completed_by:
            repository.adjust_completed_tasks_count(completed_by, +1)

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

        project = repository.get_project(data["project"])
        if not project:
            return Response({"detail": "Projeto informado não existe."}, status=status.HTTP_400_BAD_REQUEST)

        # regra: quem "possui" a tarefa precisa ser membro do projeto
        if not repository.is_project_member(project, data["createdBy"]):
            return Response(
                {"detail": "Usuário 'createdBy' não é membro do projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_done = task.get("done", False)
        old_completed_by = task.get("completedBy")
        new_done = data.get("done", False)
        new_completed_by = data.get("completedBy")

        if new_done:
            # regra: toda tarefa concluída precisa ter um responsável válido pela conclusão
            if not new_completed_by:
                return Response(
                    {"detail": "'completedBy' é obrigatório quando done=true."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not repository.is_project_member(project, new_completed_by):
                return Response(
                    {"detail": "Usuário 'completedBy' não é membro do projeto."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not old_done:
                # está sendo concluída agora
                data["completedAt"] = timezone.now()
                repository.adjust_completed_tasks_count(new_completed_by, +1)
            elif new_completed_by != old_completed_by:
                # já estava concluída, mas o responsável mudou
                if old_completed_by:
                    repository.adjust_completed_tasks_count(old_completed_by, -1)
                repository.adjust_completed_tasks_count(new_completed_by, +1)
                data["completedAt"] = timezone.now()
            else:
                # segue concluída, com o mesmo responsável: mantém a data original
                data["completedAt"] = task.get("completedAt") or timezone.now()
        else:
            # regra: reabrir a tarefa limpa os dados de conclusão
            data["completedAt"] = None
            data["completedBy"] = None
            if old_done and old_completed_by:
                repository.adjust_completed_tasks_count(old_completed_by, -1)

        data["updatedAt"] = timezone.now()
        updated = repository.update_task(taskId, data)
        return Response(TaskSerializer(updated).data)

    def delete(self, request, taskId):
        task = repository.get_task(taskId)
        if not task:
            return Response({"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # regra: apagar uma tarefa remove os comentários dela também
        repository.delete_task_cascade(taskId)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- COMMENTS ----------------

class CommentAPIView(APIView):
    def get(self, request):
        comments_list = repository.list_comments()
        serializer = CommentSerializer(comments_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = repository.get_task(data["task"])
        if not task:
            return Response({"detail": "Tarefa informada não existe."},status=status.HTTP_400_BAD_REQUEST)

        project = repository.get_project(task["project"])

        if not project or not repository.is_project_member(project, data["createdBy"]):
            return Response({"detail": "Usuário 'createdBy' não é membro do projeto da tarefa."},status=status.HTTP_400_BAD_REQUEST,)
        now = timezone.now()
        data["createdAt"] = now
        data["updatedAt"] = now

        created = repository.create_comment(data)

        serializer = CommentSerializer(created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        task = repository.get_task(data["task"])
        if not task:
            return Response({"detail": "Tarefa informada não existe."}, status=status.HTTP_400_BAD_REQUEST)

        project = repository.get_project(task["project"])
        if not project or not repository.is_project_member(project, data["createdBy"]):
            return Response(
                {"detail": "Usuário 'createdBy' não é membro do projeto da tarefa."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["updatedAt"] = timezone.now()
        updated = repository.update_comment(commentId, data)
        return Response(CommentSerializer(updated).data)

    def delete(self, request, commentId):
        deleted = repository.delete_comment(commentId)
        if not deleted:
            return Response({"detail": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)