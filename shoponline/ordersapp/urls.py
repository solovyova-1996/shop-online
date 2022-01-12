from django.urls import path

from .views import OrderList, OrderCreate, OrderDelete, OrderDetail, OrderUpdate, order_forming_complete

app_name = 'orders'
urlpatterns = [path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', OrderDetail.as_view(), name='detail'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),
               ]
