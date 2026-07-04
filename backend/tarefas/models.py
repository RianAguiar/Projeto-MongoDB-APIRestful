from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        MEMBER = "member", "Membro"

    userId = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.MEMBER)
    lastLogin = models.DateTimeField(null=True, blank=True)
    completedTasksCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
    
class Project(models.Model):

    projectId = models.PositiveIntegerField(unique=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    users = models.ManyToManyField(
        User,
        related_name="projects"
    )

    def __str__(self):
        return self.name
    
    
class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"

    taskId = models.PositiveIntegerField(unique=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    createdBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    done = models.BooleanField(default=False)
    startDate = models.DateField()

    completedAt = models.DateTimeField(
        null=True,
        blank=True
    )

    completedBy = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_tasks"
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):

    commentId = models.PositiveIntegerField(unique=True)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    body = models.TextField()

    createdBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.createdBy.username}"