from django.urls import path

from admins.views import index, UserCreateView, UserDeleteView, UserUpdateView, \
    UserListView

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users', UserListView.as_view(), name='admins-users'),
    path('users-create/', UserCreateView.as_view(), name='users-create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='users-update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='users-delete'),
]
