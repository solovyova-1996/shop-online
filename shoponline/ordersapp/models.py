from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


from mainapp.models import Product


class Order(models.Model):
    FORMING = "FM"
    SEND_TO_PROCEED = "STP"
    PAID = "PD"
    PROCEEDED = "PRD"
    READY = 'RDY'
    CANCEL = 'CNC'
    CHOICE_ORDER_STATUS = (
        (FORMING, 'формируется'), (SEND_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачено'), (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'), (CANCEL, 'отмена заказа'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=CHOICE_ORDER_STATUS,
                              verbose_name='статус', max_length=3,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'Текущий заказа {self.pk}'  # def total_quantity(self):  #     items =

    def get_total_quantity(self):
        # select_related позволяет получить все связанные данные из модели OrderItem (все товары заказа)
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    # в модели хранятся товары и то к какому заказу они относятся
    # с помощью related_name можно обратиться(из Order) ко всем товарам заказа
    order = models.ForeignKey(Order, related_name='orderitems',
                              verbose_name='заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk).quantity
