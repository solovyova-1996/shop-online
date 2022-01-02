from django.contrib import admin
from django.urls import path, include

from mainapp.views import index, products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/',include('mainapp.urls',namespace='products')),
]
