
from tkinter import N
from django.db import models

from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    priority = models.IntegerField(default=-1)

    def __str__(self):
        return self.title+" "+str(self.priority)+" "+str(self.completed)