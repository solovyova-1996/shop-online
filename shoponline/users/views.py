from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect, redirect, \
    get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, UpdateView

from basket.models import Basket
from shoponline.mixin import BaseClassContextMixin, CustomAuthDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required

from users.models import User


class LoginLoginView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Войти'


class Logout(LogoutView):
    template_name = 'mainapp/index.html'


class Register(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect(self.success_url)

        return redirect(self.success_url)


class Profile(UpdateView, BaseClassContextMixin, CustomAuthDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Профиль'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, *args, **kwargs):
        context = super(Profile, self).get_context_data(*args, **kwargs)
        context['basket'] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object(),
                               files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             # получаем введеные пользователем данные
#             username = request.POST['username']
#             password = request.POST['password']
#             # проверяем есть ли в базе данный пользователь
#             user = auth.authenticate(username=username, password=password)
#             # если пользователь есть в базе и активен авторизуем его и перенаправляем на главную страницу
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'title': 'Войти', 'form': form, }
#     return render(request, 'users/login.html', context=context)

#
# def register(request):
#     # получаем данные введенные пользователем, проверяем на правильность заполнения формы, сохраняем данные
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Вы успешно зарегистрировались")
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'Регистрация', 'form': form, }
#     return render(request, 'users/register.html', context=context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        # экземпляр юзера уже существует и при пост запросе будет обновлен
        form = UserProfileForm(data=request.POST, instance=request.user,
                               files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль сохранен')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, 'Профиль не сохранен')
    context = {'title': 'Пофиль',
               # если есть одинаковые поля у юзера и формы, то они заполняться даннными
               'form': UserProfileForm(instance=request.user),
               'basket': Basket.objects.filter(user=request.user), }
    return render(request, 'users/profile.html', context=context)
