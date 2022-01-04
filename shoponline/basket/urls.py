from django.urls import path

from .views import basket_add, basket_remove

app_name = 'basket'
urlpatterns = [
    path('add/<int:product_id>/', basket_add, name='basket'),
    path('basket_remove/<int:product_id>/', basket_remove, name='basket_remove'),
]
