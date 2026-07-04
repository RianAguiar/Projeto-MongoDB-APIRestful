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
