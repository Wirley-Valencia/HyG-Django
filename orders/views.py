# from .models import Order, PickupDateTimeForm
from datetime import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render
from carts.utils import get_or_create_cart
from .models import Order, OrderPickup
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


@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })


@login_required(login_url='login')
# @validate_cart_and_order
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb(confirmation=True)
    })


@login_required(login_url='login')
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_order(request)
    destroy_cart(request)

    messages.error(request, 'Orden cancelada')
    return redirect('inicio')


# @login_required(login_url='login')
# def order_detail(request, order_id):
#     order = Order.objects.get(order_id=order_id)
#     if request.method == 'POST':
#         form = OrderPickupForm(request.POST)
#         if form.is_valid():
#             pickup_datetime = form.cleaned_data['pickup_datetime']
#             order_pickup = OrderPickup(
#                 order=order, pickup_datetime=pickup_datetime)
#             order_pickup.save()  # Guardar el objeto OrderPickup en la base de datos
#             return redirect('order_detail', order_id=order_id)
#     else:
#         form = OrderPickupForm()

#     return render(request, 'order_detail.html', {'order': order, 'form': form})

# @login_required(login_url='login')
# def confirm_order(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         pickup_datetime = request.POST.get('pickup_datetime')
#         order = Order.objects.get(order_id=order_id)
#         order.pickup_datetime = pickup_datetime
#         order.save()
#         return render(request, 'orders/confirm.html', {'order': order})
#     else:
#         return redirect('inicio')

# @login_required(login_url='login')
# def confirm_order(request):
#     if request.method == 'POST':
#         form = OrderPickupForm(request.POST)
#         if form.is_valid():
#             order_id = request.POST.get('order_id')
#             print(order_id)
#             pickup_datetime = form.cleaned_data['pickup_datetime']
#             order = Order.objects.get(order_id=order_id)
#             order.pickup_datetime = pickup_datetime
#             order.save()
#             return render(request, 'orders/confirm.html', {'order': order})
#     else:
#         return redirect('inicio')


# @login_required(login_url='login')
# def confirm_order(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         print("El id es al;sdkfjl;akdsfj;lkajsdfl;kajsdfklja;dflskja;lsdkfj;laksdfj;lkasdjfl;kjasdfl;kjas;dlfkj;alksdfj;lkadsfj;lkajs")
#         print(order_id)
#         order = get_object_or_404(Order, id=order_id)

#         # Obtener la fecha y hora de recogida del formulario
#         pickup_datetime = request.POST.get('pickup_datetime')
#         print("El pickup_datetime es al;sdkfjl;akdsfj;lkajsdfl;kajsdfklja;dflskja;lsdkfj;laksdfj;lkasdjfl;kjasdfl;kjas;dlfkj;alksdfj;lkadsfj;lkajs")
#         print(pickup_datetime)
#         # Verificar si ya existe una instancia de OrderPickup para este pedido
#         order_pickup, created = OrderPickup.objects.get_or_create(order=order)

#         # Si ya existe, actualizar la fecha y hora de recogida
#         order_pickup.pickup_datetime = pickup_datetime
#         order_pickup.save()

#         # Redirigir a la vista 'confirm'
#         return redirect('orders:confirm')

#     return render(request, 'tu_template.html')


# @login_required(login_url='login')
# def confirm_order(request):
#     if request.method == 'POST':
#         cart = get_or_create_cart(request)
#         order = get_or_create_order(cart, request)
#         pickup_datetime_str = request.POST.get('pickup_datetime')

#         return redirect('orders:confirm')

#     return render(request, 'tu_template.html')


@login_required(login_url='login')
def confirm_order(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        order = get_or_create_order(cart, request)
        pickup_datetime_str = request.POST.get('pickup_datetime')
        pickup_datetime = datetime.strptime(
            pickup_datetime_str, '%Y-%m-%dT%H:%M')

        # Crear instancia de OrderPickup
        order_pickup = OrderPickup(
            order=order, pickup_datetime=pickup_datetime)
        order_pickup.save()

        return redirect('orders:confirm')

    return render(request, 'tu_template.html')
