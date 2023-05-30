from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.create_incident, name="create-incident"),
    path('login', views.user_login, name="login"),
    path('account', views.account, name="account"),
    path('logout', views.user_logout, name="logout"),
    path('INC<str:inc_number>', views.inc_details, name="inc"),
    path('create-note', views.create_note, name="create-note"),
    path('start-work/<str:inc_number>', views.start_work, name="start-work"),
    path('resolve-inc/<str:inc_number>', views.resolve_inc, name="resolve-inc"),

]
