from django.urls import path
from . import views

app_name = 'redirects'

urlpatterns = [
    path('', views.inbox_redirect, name='inbox_redirect'),
]
