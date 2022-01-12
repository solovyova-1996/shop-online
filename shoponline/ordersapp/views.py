from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from ordersapp.models import Order


class OrderList(ListView):
    model = Order


    #     каждый пользователь видит только свои заказы
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DeleteView):
    pass


class OrderDetail(DetailView):
    pass


def order_forming_complete(request, pk):
    pass
