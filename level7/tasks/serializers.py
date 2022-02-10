from tasks.models import History
from rest_framework.serializers import ModelSerializer
from tasks.models import Task, User


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'completed', 'status')

class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = ('id','task', 'status_previous', 'status_current', 'created_date')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
    