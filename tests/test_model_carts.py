import pytest
import decimal
from user.models import CustomUser  
from carts.models import Cart, CartProducts
from products.models import Product

@pytest.mark.django_db
def test_add_product_to_cart():

    user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='test_password')
    product = Product.objects.create(title='Test Product', price=decimal.Decimal('10.0')) 
    cart = Cart.objects.create(cart_id='123', user=user)

    cart_product = CartProducts.objects.create(cart=cart, product=product, quantity=1)

    expected_total = decimal.Decimal(product.price) + (decimal.Decimal(product.price) * decimal.Decimal(Cart.FEE))

    assert cart.products.count() == 1
    assert cart.subtotal == product.price
    assert cart.total == expected_total


@pytest.mark.django_db
def test_remove_product_from_cart():
    
    user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='test_password') 
    product = Product.objects.create(title='Test Product', price=10.0)
    cart = Cart.objects.create(cart_id='123', user=user)

    cart_product = CartProducts.objects.create(cart=cart, product=product, quantity=1)
    assert cart.products.count() == 1

    cart.products.remove(product)

    assert cart.products.count() == 0
    assert cart.subtotal == 0
    assert cart.total == 0

@pytest.mark.django_db
def test_edit_cart_products():
    
    user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='test_password')
    product1 = Product.objects.create(title='Product 1', price=decimal.Decimal('10.0'))
    product2 = Product.objects.create(title='Product 2', price=decimal.Decimal('15.0'))
    product3 = Product.objects.create(title='Product 3', price=decimal.Decimal('20.0'))
    cart = Cart.objects.create(cart_id='123', user=user)

    cart_product1 = CartProducts.objects.create(cart=cart, product=product1, quantity=1)
    cart_product2 = CartProducts.objects.create(cart=cart, product=product2, quantity=1)
    assert cart.products.count() == 2
    assert cart.subtotal == product1.price + product2.price
    cart.products.remove(product1)
    assert cart.products.count() == 1
    assert cart.subtotal == product2.price
    cart_product3 = CartProducts.objects.create(cart=cart, product=product3, quantity=1)

    assert cart.products.count() == 2
    assert cart.subtotal == product2.price + product3.price

