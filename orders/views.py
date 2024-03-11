from django.shortcuts import render
from carts.utils import get_or_create_cart
from .models import Order
from .utils import get_or_create_order
from .utils import breadcrumb
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.decorators import login_required


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
