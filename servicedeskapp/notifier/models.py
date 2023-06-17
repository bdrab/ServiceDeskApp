from django.db import models


class Notification(models.Model):
    inc = models.ForeignKey("incident.Incident", on_delete=models.CASCADE, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    has_been_sent = models.BooleanField(default=False)
