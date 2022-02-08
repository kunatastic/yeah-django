from django.db import transaction

from tasks.models import Task

# https://docs.djangoproject.com/en/4.0/topics/db/transactions/#controlling-transactions-explicitly
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-update
@transaction.atomic
def cascade_logic(user, priority):
    store = []
    filtered_tasks = Task.objects.select_for_update().filter(user=user, completed=False, deleted=False)

    # Array of continuous tasks with increasing priority by 1
    while True:
        task_w_priority = filtered_tasks.filter(priority=priority)
        if len(task_w_priority) == 0:
            break
        task_w_priority[0].priority += 1
        store.append(task_w_priority[0])
        priority = priority + 1
    Task.objects.bulk_update(store, ['priority'])  