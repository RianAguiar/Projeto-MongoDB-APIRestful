from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    taskId = serializers.IntegerField()
    project = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    createdBy = serializers.IntegerField()
    priority = serializers.ChoiceField(choices=["low", "medium", "high"])
    done = serializers.BooleanField(default=False)
    startDate = serializers.DateField()
    completedAt = serializers.DateTimeField(required=False, allow_null=True)
    completedBy = serializers.IntegerField(required=False, allow_null=True)
    createdAt = serializers.DateTimeField(required=False)
    updatedAt = serializers.DateTimeField(required=False)

class ProjectSerializer(serializers.Serializer):
    projectId = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    owner = serializers.IntegerField()
    users = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

class UserSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=["admin", "member"])
    lastLogin = serializers.DateTimeField(required=False, allow_null=True)
    completedTasksCount = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True, max_length=128)


class CommentSerializer(serializers.Serializer):
    commentId = serializers.IntegerField()
    task = serializers.IntegerField()
    body = serializers.CharField()
    createdBy = serializers.IntegerField()
    createdAt = serializers.DateTimeField(required=False)