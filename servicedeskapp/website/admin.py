from django.contrib import admin
from incident.models import Incident, Message, Category
# Register your models here.

admin.site.register(Incident)
admin.site.register(Message)
admin.site.register(Category)
