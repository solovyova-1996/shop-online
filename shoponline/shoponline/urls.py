from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mainapp.views import index

urlpatterns = [path('admin/', admin.site.urls), path('', index, name='index'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('admins/', include('admins.urls', namespace='admins')),
    path('', include('social_django.urls', namespace='social')), ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
