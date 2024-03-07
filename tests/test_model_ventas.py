import pytest
from datetime import date
from products.models import Product
from django.utils import timezone
from sales.models import Venta, DetalleVenta, Cliente
from django.test import TestCase


class TestVentas(TestCase):

    def test_create_venta(self):
        cliente = Cliente.objects.create(nombre="Cliente de prueba")
        product = Product.objects.create(
            title='Producto de prueba',
            description='Descripción de prueba',
            price=10.99,
            slug='producto-de-prueba',
            expiration_date=date(2024, 12, 31),
            image='products/imgs/image.jpg',
            cantidad_disponible=10
        )
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now().date(), total=100)
        detalle_venta = DetalleVenta.objects.create(venta=venta, producto=product, cantidad=2)

        assert Venta.objects.count() == 1
        assert DetalleVenta.objects.count() == 1

    def test_update_venta(self):
        cliente = Cliente.objects.create(nombre="Cliente de prueba")
        product = Product.objects.create(
            title='Producto de prueba',
            description='Descripción de prueba',
            price=10.99,
            slug='producto-de-prueba',
            expiration_date=date(2024, 12, 31),
            image='products/imgs/image.jpg',
            cantidad_disponible=10
        )
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now().date(), total=100)
        detalle_venta = DetalleVenta.objects.create(venta=venta, producto=product, cantidad=2)
        venta.total = 200
        venta.save()
        updated_venta = Venta.objects.get(pk=venta.pk)
        assert updated_venta.total == 200

    def test_delete_venta(self):
        cliente = Cliente.objects.create(nombre="Cliente de prueba")
        product = Product.objects.create(
            title='Producto de prueba',
            description='Descripción de prueba',
            price=10.99,
            slug='producto-de-prueba',
            expiration_date=date(2024, 12, 31),
            image='products/imgs/image.jpg',
            cantidad_disponible=10
        )
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now().date(), total=100)
        detalle_venta = DetalleVenta.objects.create(venta=venta, producto=product, cantidad=2)
        venta.delete()
        Venta.objects.count(), 0
        DetalleVenta.objects.count(), 0
