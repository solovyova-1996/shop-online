from django.db import models


# создание модели для категории товара, имя категории должно быть уникаьным
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
