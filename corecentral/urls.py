from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('squad/', include('team.urls', namespace='team')),
    path('fixtures/', include('matches.urls', namespace='matches')),
    path('news/', include('news.urls', namespace='news')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
