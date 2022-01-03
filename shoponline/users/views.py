from django.shortcuts import render

from users.forms import UserLoginForm


def login(request):
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
