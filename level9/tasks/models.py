
from cgitb import enable
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    priority = models.IntegerField(default=-1)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return self.title+" "+str(self.priority)+" "+str(self.completed)

class History(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status_previous = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    status_current = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    created_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.task.title + " " + self.status_previous + " " + self.status_current

# https://medium.com/@singhgautam7/django-signals-master-pre-save-and-post-save-422889b2839
@receiver(pre_save, sender=Task)
def addHistory(sender, instance, **kwargs):
    if instance.id is None:
        return
    previous = Task.objects.get(id=instance.pk)
    if previous is not None and previous.status != instance.status:
        History(task=instance, status_previous=previous.status, status_current=instance.status).save()


# REPORT MODEL
class Report(models.Model):
    notify_at = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)

    sent = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False) # Whether the report is enabled or not. Also can be used as delete flag


    def __str__(self):
        return f"{self.user} {self.notify_at} {self.recurring} {self.enabled}"
        

# CREATE SILENT REPORT ON USER CREATION
@receiver(post_save, sender=User)
def create_silent_report(sender, instance, created, **kwargs):
    if created:
        Report(user=instance).save()
