from django.contrib import admin
from django.urls import path
from tasks.views import (view_add_task, view_all_completed_task, view_all_task,
                         view_completed_task, view_delete_task, view_task)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("complete_task/<int:index>/", view_completed_task),
    path("completed_tasks/", view_all_completed_task),
    path("all_tasks/", view_all_task),
    path("tasks/",view_task),
    path("add-task/",view_add_task),
    path("delete-task/<int:index>/",view_delete_task),
]
