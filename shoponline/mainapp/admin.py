from django.contrib import admin

from mainapp.models import Category, Product

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # добавление нужных полей в админке
    list_display = ('name', 'price', 'quantity', 'category')
    # отображение полей при просмотре одного продукта
    fields = ('name','img','description', 'price', 'quantity', 'category',)
    # поля только для чтения
    readonly_fields = ('description',)
# поля, по которомы сортировать
    ordering = ('name','price')
    search_fields = ('name',)
