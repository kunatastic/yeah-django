from tasks.models import Task, History
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from tasks.filters import TaskFilter, HistoryFilter
from tasks.serializers import TaskSerializer, HistorySerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HistoryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HistoryFilter 

    def get_queryset(self):
        return History.objects.filter(
            task__pk=self.kwargs["task_pk"],
            task__user=self.request.user,
        )
