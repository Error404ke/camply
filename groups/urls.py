from django.urls import path, include
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('stories/', include('stories.urls')),
]
