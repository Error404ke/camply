from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import home
from redirects.views import inbox_redirect, notifications_redirect, profile_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('stories/', include('stories.urls')),
    path('chat/', include('chat.urls')),
    path('groups/', include('groups.urls')),
    path('events/', include('events.urls')),
    path('housing/', include('housing.urls')),
    path('resources/', include('resources.urls')),
    path('notify/', include('notify.urls')),
    # Redirects for tab bar
    path('inbox/', inbox_redirect, name='inbox_redirect'),
    path('notifications/', notifications_redirect, name='notifications_redirect'),
    path('profile/', profile_redirect, name='profile_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
