from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from ordersapp.models import OrderItem
from users.models import User
from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):
#     def delete(self,*args,**kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(BasketQuerySet, self).delete()

class Basket(models.Model):
    # objects= BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    # @staticmethod
    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    # @staticmethod
    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    # при удалении корзины возвращаются остатки на склад
    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete()
    # # при сохранении корзины отнимаем от количества продуктов на складе
    # def safe(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # если корзина есть
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.get_item(int(self.pk))
    #     else:
    #         # от количества товара на складе отнимаем количество переданное в заказе
    #         self.product.quantity -= self.quantity
    #         self.product.save()
    #     super(Basket, self).safe()


    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk).quantity
# сигнал перед удалением корзины(или заказа) возвращаем товары на склад
@receiver(pre_delete,sender=Basket)
@receiver(pre_delete,sender=OrderItem)
def product_quantity_update_delete(sender,instance,**kwargs):
    instance.product.quantity += instance.quantity
    instance.save()
# сигнал перед сохранением корзины или заказа удалить товар со склада
@receiver(pre_save,sender=Basket)
@receiver(pre_save,sender=OrderItem)
def product_quantity(sender,instance,**kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(int(instance.pk))
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()