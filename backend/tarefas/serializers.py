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
    description = serializers.CharField(required=False,allow_blank=True)
    createdBy = serializers.IntegerField()
    members = serializers.ListField(child=serializers.IntegerField(),required=False)
    createdAt = serializers.DateTimeField(required=False)
    updatedAt = serializers.DateTimeField(required=False)

class UserSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,max_length=128)
    createdAt = serializers.DateTimeField(required=False)
    updatedAt = serializers.DateTimeField(required=False)

class CommentSerializer(serializers.Serializer):
    commentId = serializers.IntegerField()
    task = serializers.IntegerField()
    user = serializers.IntegerField()
    content = serializers.CharField()
    createdAt = serializers.DateTimeField(required=False)
    updatedAt = serializers.DateTimeField(required=False)
