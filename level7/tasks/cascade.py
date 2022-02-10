from django.db import transaction

from tasks.models import Task

# https://docs.djangoproject.com/en/4.0/topics/db/transactions/#controlling-transactions-explicitly
@transaction.atomic
def cascade_logic(user, priority):
    store = []
    # Array of continuous tasks with increasing priority by 1
    while Task.objects.filter(user=user, priority=priority, completed=False, deleted=False).exists():
        temp_task = Task.objects.filter(user=user, priority=priority, completed=False, deleted=False)[0]
        temp_task.priority += 1
        store.append(temp_task)
        priority = priority + 1

    """https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-update"""
    Task.objects.bulk_update(store, ['priority'])  