
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.core.mail import send_mail
from task_manager.celery import app
from pytz import timezone
from tasks.models import Task, Report
from django.contrib.auth.models import User




# # Periodic Task
# @periodic_task(run_every=timedelta(seconds=5))
# def every_30_seconds():
#     print("Running Every 15 Seconds!")

@periodic_task(run_every=timedelta(minutes=60))
# @periodic_task(run_every=timedelta(seconds=5))
def send_email_reminder():
    print("Running Every 15 Seconds!")
    now_time = datetime.now(timezone("Asia/Kolkata"))
    reports = Report.objects.select_for_update().filter(enabled = True, notify_at__lte = now_time, sent = False)


    print(f"Sending all non recurring email reminder at [{now_time}]")
    print(f"I will send email to {reports.count()} users")
    print("========================================================================================")
    for report in reports:

        user = User.objects.get(id=report.user.id)
        tasks = Task.objects.filter(user=user, deleted=False)
        
        print(f"NOW TIME {now_time}")
        print(f"REP TIME {report.notify_at}")

        # Computation
        completed_tasks = tasks.filter(completed=True).count()
        total_tasks = tasks.count()
        try:
            completed_percentage = (completed_tasks / total_tasks) * 100
        except ZeroDivisionError:
            completed_percentage = 0

        content = f"Hi {user.username},\n\nHere is your task report for {now_time.day}\{now_time.month}\{now_time.year}.\n\n1. Completed Tasks: {completed_tasks} \n2. Pending Tasks: {total_tasks-completed_tasks} \n3. Completed Percentage: {completed_percentage}%\n\nTEAM Task Manager"

        subject = f"[{now_time.year}, {now_time.day} {now_time.month}] Task Report for {user.username}" 

        if not report.recurring:
            report.enabled = False
        report.sent = True
        report.save()

        send_mail(subject, content, "reminder@task-manager.com", [user.email])
        print(f"Sent to {user} at {now_time}")
        print(content)


# Implemented a naive Cronjob for setting sent flag to False on recurring reports
@periodic_task(run_every=timedelta(hours=24))
# @periodic_task(run_every=timedelta(seconds=5))
def reset_recurring_reports():
    now_time = datetime.now(timezone("Asia/Kolkata"))
    print("Resetting recurring reports at [{}]".format(now_time))
    reports = Report.objects.select_for_update().filter(recurring=True, sent=True, enabled = True).update(sent=False)