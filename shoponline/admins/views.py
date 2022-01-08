from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mainapp.models import Category, Product
from shoponline.mixin import CustomDispatchMixin
from users.models import User
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, \
    CategoryAdminCreate, ProductAdmin


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins-users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание пользователя'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins-users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Редактирование пользователя'
        return context


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admins-users')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, CustomDispatchMixin):
    model = Category
    template_name = 'admins/admin-categories-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = Category
    template_name = 'admins/admin-categories-create.html'
    form_class = CategoryAdminCreate
    success_url = reverse_lazy('admins:admins-categories')
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = Category
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = CategoryAdminCreate
    success_url = reverse_lazy('admins:admins-categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Редактирование категории'
        return context


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = Category
    template_name = 'admins/admin-categories-update-delete.html'
    success_url = reverse_lazy('admins:admins-categories')
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:products')
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Товары'
        return context


class ProductCreateView(CreateView, CustomDispatchMixin):
    model = Product
    form_class = ProductAdmin
    template_name = 'admins/admin-product-create.html'
    success_url = reverse_lazy('admins:products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание товара'
        return context


class ProductUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    form_class = ProductAdmin
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Редактирование товара'
        return context


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:products')
