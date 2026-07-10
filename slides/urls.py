from django.urls import path
from . import views

app_name = 'slides'

urlpatterns = [
    path('', views.slide_list, name='slide_list'),
]
