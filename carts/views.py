from django.shortcuts import render
from .utils import get_or_create_cart
# Create your views here.
from .models import Cart, CartProducts, CartProductsManager
from products.models import Product, Stock
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages


def cart(request):

    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        'cart': cart
    })


# def add(request):
#     cart = get_or_create_cart(request)
#     product = get_object_or_404(Product, pk=request.POST.get('product_id'))
#     quantity = int(request.POST.get('quantity', 1))

#     cart_product = CartProducts.objects.create_or_update_quantity(
#         cart=cart, product=product, quantity=quantity)

#     product.total_cantidad_disponible -= quantity
#     product.save()

#     print("antes")
#     return render(request, 'carts/add.html', {

#         'quantity': quantity,
#         'product': product
#     })

def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= product.total_cantidad_disponible:
        stock_disponible = Stock.objects.filter(
            product=product,
            cantidad_disponible__gt=0,
            status=Stock.AVAILABLE
        ).order_by('expiration_date')

        cantidad_restante = quantity
        for stock in stock_disponible:
            if cantidad_restante <= 0:
                break
            if stock.cantidad_disponible >= cantidad_restante:
                stock.cantidad_disponible -= cantidad_restante
                stock.save()
                cantidad_restante = 0
            else:
                cantidad_restante -= stock.cantidad_disponible
                stock.cantidad_disponible = 0
                stock.save()

        if cantidad_restante > 0:
            # No hay suficiente stock disponible
            messages.error(
                request, 'No hay suficiente stock disponible para este producto.')
        else:
            # Se agrega el producto al carrito
            cart_product = CartProducts.objects.create_or_update_quantity(
                cart=cart, product=product, quantity=quantity)
            product.total_cantidad_disponible -= quantity
            product.save()
            messages.success(request, 'Producto agregado al carrito.')
    else:
        messages.error(
            request, 'Stock insuficiente. No puedes agregar mas productos')

    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'product': product
    })


def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)
    return redirect('carts:cart')
