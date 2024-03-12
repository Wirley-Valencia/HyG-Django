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

    # if not cart.has_products() or order.billing_profile is None:
    #     return redirect('carts:cart')

    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    # shipping_address = order.shipping_address
    # if shipping_address is None:
    #     return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        # 'shipping_address': shipping_address,
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


@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(order_id=order_id)
    if request.method == 'POST':
        form = OrderPickupForm(request.POST)
        if form.is_valid():
            pickup_datetime = form.cleaned_data['pickup_datetime']
            order_pickup = OrderPickup.objects.create(
                order=order, pickup_datetime=pickup_datetime)
            return redirect('order_detail', order_id=order_id)
    else:
        form = OrderPickupForm()

    return render(request, 'order_detail.html', {'order': order, 'form': form})
