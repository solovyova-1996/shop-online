from django.shortcuts import render

from mainapp.models import Product, Category


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None):
    # фильтрация продуктов по категориям
    products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
    context = {'title': 'Каталог', 'categories': Category.objects.all(),
        'products': products, }
    return render(request, 'mainapp/products.html', context=context)
