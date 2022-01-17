from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from basket.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem
from shoponline.mixin import BaseClassContextMixin


class OrderList(ListView):
    model = Order

    #     каждый пользователь видит только свои заказы
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'Создать заказ'
        # главная модель - Order, подчиненная модель - Orderitem, какую форму использовать для работы с моделями OrderItemsForm, extra - сколько пустых строк
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemsForm, extra=1)
        if self.request.POST:
            # При пост запросе заполняем форму
            formset = OrderFormSet(self.request.POST)
        else:
            # если у юзера есть корзины то заполняем продуктами из корзины заказ
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemsForm,
                                                     extra=basket_items.count())
                formset = OrderFormSet()  # formset-это форма
                print(formset.forms)
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                #     заказ будет удаляться при переходе на заказ
                # basket_items.delete()
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        # забираем контекст
        context = self.get_context_data()
        # забираем строки с товарами из заказа
        orderitems = context['orderitems']
        # выполняется либо весь запрос коректно либо вовсе не выполняется - объявляем атомарную транзакцию
        with transaction.atomic():
            # назначаем для формы юзера
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # если заказ пустой удаляем его
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Обновление заказ'
        # главная модель - Order, подчиненная модель - Orderitem, какую форму использовать для работы с моделями OrderItemsForm, extra - сколько пустых строк
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemsForm, extra=1)
        if self.request.POST:
            # При пост запросе заполняем форму
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        # забираем контекст
        context = self.get_context_data()
        # забираем строки с товарами из заказа
        orderitems = context['orderitems']
        # выполняется либо весь запрос коректно либо вовсе не выполняется - объявляем атомарную транзакцию
        with transaction.atomic():
            # назначаем для формы юзера
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # если заказ пустой удаляем его
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    # использование BaseClassContextMixin позволяет отправлять в контекст title
    title = 'Просмотр заказа'


def order_forming_complete(request, pk):
    # получаем заказа и изменяем его статус
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))
# контроллер для оплаты
def payment_result(request):
    status = request.GET.get('ik_inv_st')
    if status == 'success':
        order_pk = request.GET.get('ik_pm_no')
        order_item = Order.objects.get(pk=order_pk)
        order_item.status = Order.PAID
        order_item.save()
    return HttpResponseRedirect(reverse('orders:list'))