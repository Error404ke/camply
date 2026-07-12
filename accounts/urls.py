from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('profile/view/<str:username>/', views.profile_view, name='profile_view_user'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/add-account/', views.profile_add_account, name='profile_add_account'),
]
