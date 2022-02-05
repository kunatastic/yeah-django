from django.db import transaction

from tasks.models import Task


def cascade_logic(user, priority):
    store = []
    # Array of continuous tasks with increasing priority by 1
    while Task.objects.filter(user=user, priority=priority, completed=False, deleted=False).exists():
        temp_task = Task.objects.filter(user=user, priority=priority, completed=False, deleted=False)[0]
        print("FOUND THIS",temp_task)
        store.append(temp_task)
        priority = priority + 1

    # Update the priority of the continuous tasks by 1
    for task in store:
        print(task)
        Task.objects.filter(id=task.id).update(priority=task.priority + 1)

    """https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-update"""
    # Task.objects.update(store, ['priority'])  