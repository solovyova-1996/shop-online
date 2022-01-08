from django.urls import path

from admins.views import index, UserCreateView, UserDeleteView, UserUpdateView, \
    UserListView, CategoryListView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

app_name = 'admins'
urlpatterns = [path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins-users'),
    path('users-create/', UserCreateView.as_view(), name='users-create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(),
         name='users-update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(),
         name='users-delete'),
    path('categories/', CategoryListView.as_view(), name='admins-categories'),
    path('categories-create/', CategoryCreateView.as_view(),
         name='categories-create'),
    path('categories-update/<int:pk>/', CategoryUpdateView.as_view(),
         name='categories-update'),
    path('categories-delete/<int:pk>/', CategoryDeleteView.as_view(),
         name='categories-delete'), ]
