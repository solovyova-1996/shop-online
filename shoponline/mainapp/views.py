from django.shortcuts import render

from mainapp.models import Product, Category


def index(request):
    return render(request,'mainapp/index.html')
def products(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request,'mainapp/products.html',context=context)