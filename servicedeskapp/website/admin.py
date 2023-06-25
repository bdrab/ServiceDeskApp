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

# TODO: SMS notification should be added, based on contact info.
# TODO: Field when task was closed.
# TODO: Tags/categories should be alphabetically sorted or user should have possibility to input tag/category name
# TODO: In KB should be included only closed tasks
# TODO: HOMEPAGE!!!
# TODO: Change work notes style.

