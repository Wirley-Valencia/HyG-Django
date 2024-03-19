# from .models import Order, PickupDateTimeForm
from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.shortcuts import render
from carts.utils import get_or_create_cart
from .models import Order, OrderPickup
from sales.models import Venta
from .utils import get_or_create_order
from .utils import breadcrumb
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import destroy_order
from carts.utils import destroy_cart
from .forms import OrderPickupForm
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models.query import EmptyQuerySet
from django.views.generic.list import ListView
from .decorators import validate_cart_and_order


class OrderListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "orders/orders.html"

    def get_queryset(self):
        return self.request.user.orders_completed()


@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })


@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_order(request)
    destroy_cart(request)

    messages.error(request, 'Orden cancelada')
    return redirect('inicio')


@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb(confirmation=True)
    })


# @login_required(login_url='login')
# # @validate_cart_and_order
# def complete(request):
#     cart = get_or_create_cart(request)
#     order = get_or_create_order(cart, request)

#     if request.user.id != order.user_id:
#         return redirect('carts:cart')

#     order.complete()

#     destroy_order(request)
#     destroy_cart(request)

#     messages.success(request, 'Compra realizada con éxito')

#     return redirect('inicio')


@login_required(login_url='login')
@validate_cart_and_order
def confirm_order(request, cart, order):
    if request.method == 'POST':
        pickup_datetime_str = request.POST.get('pickup_datetime')
        pickup_datetime = datetime.strptime(
            pickup_datetime_str, '%Y-%m-%dT%H:%M')

        # Crear una instancia de OrderPickup
        order_pickup, created = OrderPickup.objects.get_or_create(
            order=order, defaults={'pickup_datetime': pickup_datetime})

        if not created:
            order_pickup.pickup_datetime = pickup_datetime
            order_pickup.save()

        # cliente, created = Cliente.objects.get_or_create(
        #     email=order.user.email,
        #     defaults={'telefono': order.user.customuser.cell_phone}
        # )

        # if created:
        #     cliente.nombre = order.user.username
        #     cliente.save()

        # venta = Venta.objects.create(
        #     cliente=cliente,
        #     fecha=pickup_datetime.date(),
        #     total=order.total,
        # )

        order.complete()
        # order.delete()  # Eliminar el pedido una vez completada la venta

        messages.success(request, 'Compra realizada con éxito')

        return redirect('orders:confirm')

    return render(request, 'tu_template.html')
