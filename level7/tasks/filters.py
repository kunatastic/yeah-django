from django_filters.filters import ChoiceFilter, DateFilter
from tasks.models import STATUS_CHOICES, Task, History
from django_filters.rest_framework import FilterSet
from django.db.models import Q

STATUS_CHOICES_CUSTOM = (
  ("COMPLETED","COMPLETED"),
  ("NOT_COMPLETED","NOT_COMPLETED")
)
class HistoryFilter(FilterSet):
    created_date = DateFilter(method='custom_date_filter')
    class Meta:
        model = History
        fields = ['status_current', 'status_previous', 'created_date']
    def custom_date_filter(self, queryset, name, value):
        return queryset.filter(
            updated_date__year=value.year,
            updated_date__month=value.month,
            updated_date__day=value.day,
        )

class TaskFilter(FilterSet):
    status = ChoiceFilter(method='completed_custom_filter', choices=STATUS_CHOICES_CUSTOM)
    class Meta:
        model = Task
        fields = ['status']
    def completed_custom_filter(self, queryset, name, value):
        if value == "COMPLETED":
            return queryset.filter(status="COMPLETED")
        elif value == "NOT_COMPLETED":
            return queryset.filter(~Q(status="COMPLETED"))
