from django.contrib import admin
from incident.models import Incident, Message, Category, Group, Profile, Attachment, Tag, KnowledgeFiles, KnowledgeArticle
from notifier.models import Notification
# Register your models here.

admin.site.register(Incident)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Attachment)
admin.site.register(Tag)
admin.site.register(KnowledgeFiles)
admin.site.register(KnowledgeArticle)
admin.site.register(Notification)
