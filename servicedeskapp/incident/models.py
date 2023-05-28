from django.db import models
import uuid
from django.contrib.auth.models import User
import time

time.time()
# Create your models here.


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Incident(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="engineer", default=None)
    number = models.IntegerField(default=time.time_ns())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    incident = models.ForeignKey(Incident, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
