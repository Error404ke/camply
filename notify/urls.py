from django.urls import path
from . import views

app_name = 'notify'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
]
