from django.shortcuts import render


def login(request):
    context = {
        'title': 'Войти',
    }
    return render(request, 'users/login.html', context=context)


def register(request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'users/register.html', context=context)
