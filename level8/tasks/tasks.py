
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.core.mail import send_mail
from task_manager.celery import app
from tasks.models import Task, Report
from django.contrib.auth.models import User




# Periodic Task
@periodic_task(run_every=timedelta(seconds=5))
def every_30_seconds():
    print("Running Every 15 Seconds!")

# @periodic_task(run_every=timedelta(minutes=15))
@periodic_task(run_every=timedelta(seconds=5))
def send_email_reminder():
    print("Sending Email Reminder!")
    now_time = datetime.now()
    reports = Report.objects.filter(enabled=True)
    for report in reports:
        if not report.enabled:
            continue

        user = User.objects.get(id=report.user.id)
        tasks = Task.objects.filter(user=user, deleted=False)

        # Computation
        completed_tasks = tasks.filter(completed=True)
        total_tasks = tasks.count()
        completed_percentage = (completed_tasks.count() / total_tasks) * 100

        content = f"Hi {user.username},\n\n Here is your task report for {now_time.day} {now_time.month} {now_time.year}.\n\n1. Completed Tasks: {completed_tasks} \n2. Pending Tasks: {total_tasks-completed_tasks} \n3. Completed Percentage: {completed_percentage}%"

        if report.recurring:
            subject = f"[{now_time.year}, {now_time.day} {now_time.month}] Daily Task Report for {user.username}"
        else:
            subject = f"[{now_time.year}, {now_time.day} {now_time.month}] Task Report for {user.username}" 
            report.update(enabled=False)

        send_mail(subject, content, "reminder@task-manager.com", [user.email])
        print(f"Sent to {user.email} at {now_time}")