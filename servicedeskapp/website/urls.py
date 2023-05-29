from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.create_incident, name="create-incident"),
    path('login', views.user_login, name="login"),
    path('account', views.account, name="account"),
    path('admin-panel', views.admin_panel, name="admin-panel"),
    path('logout', views.user_logout, name="logout"),
    path('INC<str:inc_number>', views.inc_details, name="inc"),
    path('new', views.create_note, name="create-note"),

]
