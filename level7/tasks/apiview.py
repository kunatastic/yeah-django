from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from django_filters.rest_framework import DjangoFilterBackend


from tasks.models import History, Task
from tasks.serializers import HistorySerializer, TaskSerializer
# from tasks.filters import HistoryFilter, TaskFilter


# 

from django.db.models import Q
from django.forms import CharField
from django_filters.rest_framework import ChoiceFilter, FilterSet

from tasks.models import History, Task

STATUS_CHOICES = (
    ("COMPLETED", "COMPLETED"),
    ("NOT_COMPLETED", "NOT_COMPLETED"),
)

class HistoryFilter(FilterSet):
    status_current = ChoiceFilter(choices=STATUS_CHOICES)
    print("iouerow")

# https://django-filter.readthedocs.io/en/stable/guide/usage.html#customize-filtering-with-filter-method
# https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering
class TaskFilter(FilterSet):
    status = ChoiceFilter(method='completed_custom_filter', choices=STATUS_CHOICES)
    class Meta:
        model = Task
        fields = ['status']
    def completed_custom_filter(self, queryset, name, value):
        if value == "COMPLETED":
            return queryset.filter(status="COMPLETED")
        elif value == "NOT_COMPLETED":
            return queryset.filter(~Q(status="COMPLETED"))

# 

class HistoryListApi(APIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        histories = History.objects.filter(task__user=request.user, task__deleted=False)
        serializer = HistorySerializer(histories, many=True).data
        return Response({"histories": serializer})
    def get_queryset(self):
        return History.objects.filter(tasks__user=self.request.user,task__deleted=False)
    def perform_create(self, serializer):
        serializer.save(tasks__user=self.request.user)


class TaskListApi(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get(self, request):
        task = Task.objects.filter(deleted=False)
        data = TaskSerializer(task, many=True).data
        return Response({'tasks':data})


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter


class HistoryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)
    filters_backends = (DjangoFilterBackend,)
    filterset_class = HistoryFilter 

    filterset_fields = ("status_current",)

    def get_queryset(self):
        return History.objects.filter(
            task__pk=self.kwargs["task_pk"],
            task__user=self.request.user,
        )

