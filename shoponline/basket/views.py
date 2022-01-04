from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import Product
from basket.models import Basket
from django.contrib.auth.decorators import login_required


@login_required
def basket_add(request, product_id):
    # получаем продукт по id
    product = Product.objects.get(id=product_id)
    #  находим есть ли у пользователя уже корзина с таким продуктом
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        # если с таким продуктом корзины нет, создаем новую корзину
        Basket.objects.create(user=request.user, product=product, quantity=1)
        # получаем адрес страницы на которой находились и возвращаемся на нее
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        # если корзина существует увеличиваем quantity
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
