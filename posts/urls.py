from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('create-reel/', views.create_reel, name='create_reel'),
    path('create-story/', views.create_story, name='create_story'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('like-reel/<int:reel_id>/', views.like_reel, name='like_reel'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('story/view/<int:story_id>/', views.view_story, name='view_story'),
    path('story/delete/<int:story_id>/', views.delete_story, name='delete_story'),
]
