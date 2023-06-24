from django.urls import path
from . import views

urlpatterns = [
    path('tags/<str:tag>', views.tags, name="tags"),
    path('categories/<str:category>', views.categories, name="categories"),
    path('knowledge_article/<int:article>', views.knowledge_article, name="article"),
    path('create-tag', views.create_tag, name="create-tag"),
    path('create-knowledge-article', views.create_knowledge_article, name="create-knowledge-article"),
    path('add-attachment', views.add_attachment, name="add-attachment"),
    path('create-note', views.create_note, name="create-note"),
    path('start-work/<str:inc_number>', views.start_work, name="start-work"),
    path('resolve-inc/<str:inc_number>', views.resolve_inc, name="resolve-inc"),
    path('create', views.create_incident, name="create-incident"),
    path('add-knowledge-article', views.add_knowledge_article, name="add-knowledge-article"),
]
