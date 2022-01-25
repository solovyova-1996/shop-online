from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string

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
        print(basket)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        basket = Basket.objects.filter(user=request.user)
        context = {'basket': basket}
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
