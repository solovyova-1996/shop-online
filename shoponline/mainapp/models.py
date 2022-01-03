from django.db import models


# создание модели для категории товара, имя категории должно быть уникальным
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)


# создание модели для товаров, при удалении категории все товары этой категории удаляются
class Product(models.Model):
    name = models.CharField(max_length=256)
    img = models.ImageField(upload_to='product_img', blank=True,
                            max_length=256)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
