
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

# @periodic_task(run_every=timedelta(minutes=60))
@periodic_task(run_every=timedelta(seconds=5))
def send_email_reminder():

    
    now_time = datetime.now(timezone("Asia/Kolkata"))
    reports = Report.objects.filter(enabled = True)


    print(f"Sending Email Reminder at [{now_time}]")
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

        # Destrustion of the report and current task time 
        nt_day = now_time.day
        nt_month = now_time.month
        nt_year = now_time.year
        nt_hour = now_time.hour

        rt_day = report.notify_at.day
        rt_month = report.notify_at.month
        rt_year = report.notify_at.year
        rt_hour = report.notify_at.hour

        if report.recurring:
            if nt_hour == rt_hour: 
                subject = f"[{now_time.year}, {now_time.day} {now_time.month}] Daily Task Report for {user.username}"
            else:
                continue
        else:
            if nt_day == rt_day and nt_month == rt_month and nt_year == rt_year and nt_hour == rt_hour:
                subject = f"[{now_time.year}, {now_time.day} {now_time.month}] Task Report for {user.username}" 
            else:
                continue
            report.update(enabled=False)
        send_mail(subject, content, "reminder@task-manager.com", [user.email])
        print(f"Sent to {user} at {now_time}")
        print(content)