from django.contrib import admin
from django.urls import path

from django.shortcuts import render
from django.http import HttpResponseRedirect


pending = []
completed = []

# tag a task as completed
def view_completed_task(request,index):
    completed.append(pending[index-1])
    pending.pop(index-1)
    return HttpResponseRedirect("/tasks/")

# view all the completed tasks
def view_all_completed_task(request):
    return render(request, "AllCompletedTask.html", {"completed": completed})

# view both completed and pending tasks
def view_all_task(request):
    return render(request, "AllTask.html", {"pending": pending, "completed": completed})

# add a new task & view pending tasks
def view_task(request):
    return render(request, "AddTask.html", {"pending": pending})

# add a new task
def view_add_task(request):
    task_value = request.GET["task"]
    pending.append(task_value)
    return HttpResponseRedirect("/tasks/")

# delete a pending task
def view_delete_task(request,index):
    pending.pop(index-1)
    return HttpResponseRedirect("/tasks/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("complete_task/<int:index>/", view_completed_task),
    path("completed_tasks/", view_all_completed_task),
    path("all_tasks/", view_all_task),
    path("tasks/",view_task),
    path("add-task/",view_add_task),
    path("delete-task/<int:index>/",view_delete_task),
]
