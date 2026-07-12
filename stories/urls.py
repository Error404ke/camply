from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.create_story, name='create_story'),
    path('<int:story_id>/', views.story_view, name='story_view'),
]
