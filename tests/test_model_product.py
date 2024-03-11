from products.models import Product
import pytest
import os
import django
from django.conf import settings
from django.test import TestCase
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

<<<<<<< HEAD

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectohyg.settings')
=======
""" os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectohyg.settings')  
>>>>>>> fac592d0643d61a148092b5d3a86d429f687e647

django.setup() """


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99,
            slug='test-product',
            image='products/test.jpg'
        )
 
    def test_product_creation(self):
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'This is a test product')
        self.assertEqual(float(product.price), 10.99)

    def test_slug_generation(self):

        product = Product.objects.get(id=self.product.id)
        expected_slug = 'test-product'
        self.assertEqual(product.slug, expected_slug)

    @pytest.mark.django_db
    def test_product_update(self):
        product = Product.objects.create(title='Test Product',
                                         description='Esto es una prueba de Test',
                                         price=12.99,
                                         image='products/test.jpg')

        update_title = 'Actualizar el producto'
        update_description = 'Esto es la actualizacion de prueba'
        update_price = 97.00
        product.title = update_title
        product.description = update_description
        product.price = update_price
        product.save()

        update_product = Product.objects.get(id=product.id)

        assert update_product.title == update_title
        assert update_product.description == update_description
        assert update_product.price == update_price


@pytest.mark.django_db
def test_product_deletion():
    product = Product.objects.create(
        title='Test Product',
        description='This is a test product',
        price=10.99,
        slug='test-product',
        image='products/test.jpg'
    )

    product_id = product.id
    product.delete()

    with pytest.raises(ObjectDoesNotExist):
        deleted_product = Product.objects.get(id=product_id)
