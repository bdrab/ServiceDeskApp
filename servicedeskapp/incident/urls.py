from django.urls import path
from . import views

urlpatterns = [
    path('tags/<str:tag>', views.tags, name="tags"),
    path('categories/<str:category>', views.categories, name="categories"),
    path('create-tag', views.create_tag, name="create-tag"),
]
