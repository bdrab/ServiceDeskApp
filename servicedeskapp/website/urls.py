from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.new_inc, name="create"),
    path('account', views.account, name="account"),
    path('logout', views.user_logout, name="logout"),
    path('INC<str:inc_number>', views.inc_details, name="inc"),
    path('new', views.create_new_message, name="create-message"),

]
