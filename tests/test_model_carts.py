import pytest
import decimal
from user.models import CustomUser  
from carts.models import Cart, CartProducts
from products.models import Product

@pytest.mark.django_db
def test_add_product_to_cart():

    user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='test_password')
    product = Product.objects.create(title='Test Product', price=decimal.Decimal('10.0'))  # Convertir el precio a Decimal
    cart = Cart.objects.create(cart_id='123', user=user)

    cart_product = CartProducts.objects.create(cart=cart, product=product, quantity=1)

    expected_total = decimal.Decimal(product.price) + (decimal.Decimal(product.price) * decimal.Decimal(Cart.FEE))

    assert cart.products.count() == 1
    assert cart.subtotal == product.price
    assert cart.total == expected_total


@pytest.mark.django_db
def test_remove_product_from_cart():
    
    user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='test_password')  # Usa CustomUser en lugar de User
    product = Product.objects.create(title='Test Product', price=10.0)
    cart = Cart.objects.create(cart_id='123', user=user)

    cart_product = CartProducts.objects.create(cart=cart, product=product, quantity=1)

    assert cart.products.count() == 1

    cart.products.remove(product)

    assert cart.products.count() == 0
    assert cart.subtotal == 0
    assert cart.total == 0
