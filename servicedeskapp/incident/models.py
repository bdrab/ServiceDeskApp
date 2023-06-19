from django.db import models
from django.contrib.auth.models import User
import time
import os
from servicedeskapp import settings
from notifier.models import Notification
time.time()
# Create your models here.


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    name = models.TextField(blank=True)
    scope = models.ManyToManyField(Category)
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name


class KnowledgeFiles(models.Model):
    name = models.CharField(max_length=12, blank=True)
    extension = models.CharField(max_length=12, blank=True)
    file = models.FileField(upload_to="files/knowledge_files/")

    def delete(self, *args, **kwargs):
        os.remove(str(settings.BASE_DIR) + "\\" + self.file.name.replace("/", "\\"))
        super(KnowledgeFiles, self).delete(*args, **kwargs)


class KnowledgeArticle(models.Model):
    name = models.CharField(max_length=25, blank=True)
    knowledge_files = models.ManyToManyField(KnowledgeFiles, default=None, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Incident(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="engineer", default=None)
    assignment_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="group", default=None)
    number = models.IntegerField(default=time.time_ns)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(null=True, blank=True)
    state = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, default=None, blank=True)
    knowledge = models.BooleanField(default=False, blank=False, null=False)
    knowledge_article = models.ManyToManyField(KnowledgeArticle, default=None, blank=True)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        inc_exist = Incident.objects.filter(pk=self.pk).exists()

        super().save(*args, **kwargs)

        if not inc_exist:
            new_notification = Notification(inc=self, has_been_sent=False)
            new_notification.save()


class Attachment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=12, blank=True)
    extension = models.CharField(max_length=12, blank=True)
    file = models.FileField(upload_to="files/inc_attachments/")

    def delete(self, *args, **kwargs):
        os.remove(str(settings.BASE_DIR) + "\\" + self.file.name.replace("/", "\\"))
        super(Attachment, self).delete(*args, **kwargs)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    incident = models.ForeignKey(Incident, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.JSONField(default=dict)
    phone_number = models.CharField(max_length=12, default=None, blank=True, null=True)
