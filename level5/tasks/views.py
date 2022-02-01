# Add your Views Here


from re import search
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task


# tag a task as completed
def view_completed_task(request,index):
    Task.objects.filter(id=index).filter(deleted=False).update(completed=True)
    return HttpResponseRedirect("/tasks/")

# view all the completed tasks
def view_all_completed_task(request):
    completed = Task.objects.filter(completed=True).filter(deleted=False)
    return render(request, "AllCompletedTask.html", {"completed": completed, "showCompleted": len(completed)!=0 })

# view both completed and pending tasks
def view_all_task(request):
    pending = Task.objects.filter(completed=False).filter(deleted=False)
    completed = Task.objects.filter(completed=True).filter(deleted=False)
    return render(request, "AllTask.html", {"pending": pending, "showPending": len(pending)!=0, "completed": completed, "showCompleted": len(completed)!=0})

# add a new task & view pending tasks
def view_task(request):
    search_value = request.GET.get("search") 
    pending = Task.objects.filter(deleted=False).filter(completed=False)
    if search_value:
        pending = pending.filter(title__icontains=search_value)
    return render(request, "AddTask.html", {"pending": pending, "showPending": len(pending)!=0})

# add a new task
def view_add_task(request):
    task_value = request.GET["task"]
    Task(title=task_value).save()
    return HttpResponseRedirect("/tasks/")

# delete a pending task
def view_delete_task(request,index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks/")
