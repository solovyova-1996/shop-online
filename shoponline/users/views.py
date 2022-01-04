from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from users.forms import UserLoginForm, UserRegisterForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # получаем введеные пользователем данные
            username = request.POST['username']
            password = request.POST['password']
            # проверяем есть ли в базе данный пользователь
            user = auth.authenticate(username=username, password=password)
            # если пользователь есть в базе и активен авторизуем его и перенаправляем на главную страницу
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Войти',
        'form': form,
    }
    return render(request, 'users/login.html', context=context)


def register(request):
    # получаем данные введенные пользователем, проверяем на правильность заполнения формы, сохраняем данные
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/register.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request):
    context = {
        'title': 'Пофиль',
    }
    return render(request, 'users/profile.html', context=context)
