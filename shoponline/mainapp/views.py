from django.shortcuts import render

from mainapp.models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None, page_id=1):
    # фильтрация продуктов по категориям
    products = Product.objects.filter(
        category_id=category_id) if category_id != None else Product.objects.all()
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
        'products': products_paginator,
    }
    return render(request, 'mainapp/products.html', context=context)
