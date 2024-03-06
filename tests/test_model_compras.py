import pytest
from datetime import date
from django.test import TestCase
from hyg.models import Compra, Suppliers, Product

@pytest.mark.django_db
def test_create_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')
    product = Product.objects.create(
        title='Producto de prueba',
        description='Descripción de prueba',
        price=10.99,
        slug='producto-de-prueba',
        expiration_date=date(2024, 12, 31),
        image='products/imgs/image.jpg',
        cantidad_disponible=10
    )

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
        product=product
    )

    assert Compra.objects.count() == 1


@pytest.mark.django_db
def test_update_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')
    product = Product.objects.create(
        title='Producto de prueba',
        description='Descripción de prueba',
        price=10.99,
        slug='producto-de-prueba',
        expiration_date=date(2024, 12, 31),
        image='products/imgs/image.jpg',
        cantidad_disponible=10
    )

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
        product=product
    )

    compra.description = 'Compra actualizada'
    compra.save()
    compra_actualizada = Compra.objects.get(id=compra.id)
    assert compra_actualizada.description == 'Compra actualizada'

@pytest.mark.django_db
def test_delete_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')
    product = Product.objects.create(
        title='Producto de prueba',
        description='Descripción de prueba',
        price=10.99,
        slug='producto-de-prueba',
        expiration_date=date(2024, 12, 31),
        image='products/imgs/image.jpg',
        cantidad_disponible=10
    )

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
        product=product
    )

    compra.delete()
    assert Compra.objects.count() == 0

