from django.contrib import auth
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse

from users.forms import UserLoginForm


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
            print(form.errors)
    else:
        form = UserLoginForm()
    context = {
        'title': 'Войти',
        'form': form,
    }
    return render(request, 'users/login.html', context=context)


def register(request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'users/register.html', context=context)
