from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_redirect, name='login_redirect'),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('groups/', include('groups.urls')),
    path('events/', include('events.urls')),
    path('housing/', include('housing.urls')),
    path('resources/', include('resources.urls')),
    path('announcements/', include('announcements.urls')),
    path('profiles/', include('profiles.urls')),
    path('notifications/', include('notify.urls')),
    path('slides/', include('slides.urls')),
    path('posts/', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'camly_project.views.custom_404'
