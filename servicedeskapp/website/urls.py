from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.create_incident, name="create-incident"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('knowledge', views.knowledge, name="knowledge"),
    path('INC<str:inc_number>', views.inc_details, name="inc"),
    path('files/inc_attachments/<str:attachment_name>', views.view_attachment, name="view-attachment"),
    path('files/knowledge_files/<str:knowledge_file_name>', views.view_knowledge_file, name="view-knowledge-file"),
]
