from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from tasks.models import Task, History

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["title", "description", "completed", "status", "user"]

class HistorySerializer(ModelSerializer):
    task = TaskSerializer(read_only=True)
    class Meta:
        model = History
        fields = ["id", "status_previous", "status_current", "created_date", "task"]