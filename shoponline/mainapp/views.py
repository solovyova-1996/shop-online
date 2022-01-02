from django.shortcuts import render


def index(request):
    return render(request,'mainapp/index.html')
def products(request):
    context = {
        'title': 'Каталог',
        'products': [{'name':''},{'name':''},{'name':''},{'name':''},{'name':''},{'name':''}],
    }
    return render(request,'mainapp/products.html',context=context)