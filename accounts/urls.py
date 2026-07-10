from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    
    # Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/landlord/', views.landlord_dashboard, name='landlord_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    
    # Admin Management
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/landlords/', views.manage_landlords, name='manage_landlords'),
    path('admin/approve-landlord/<int:profile_id>/', views.approve_landlord, name='approve_landlord'),
]
