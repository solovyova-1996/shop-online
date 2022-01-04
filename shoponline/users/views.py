from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from basket.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    if request.method == 'POST':
        # экземпляр юзера уже существует и при пост запросе будет обновлен
        form = UserProfileForm(data=request.POST, instance=request.user,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    context = {
        'title': 'Пофиль',
        # если есть одинаковые поля у юзера и формы, то они заполняться даннными
        'form': UserProfileForm(instance=request.user),
        'basket': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context=context)
