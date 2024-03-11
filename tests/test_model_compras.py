import pytest
from datetime import date
from django.test import TestCase
from hyg.models import Compra, Suppliers, Product
from django.utils import timezone


@pytest.mark.django_db
def test_create_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
    )

    assert Compra.objects.count() == 1


@pytest.mark.django_db
def test_update_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
    )

    compra.description = 'Compra actualizada'
    compra.save()
    compra_actualizada = Compra.objects.get(id=compra.id)
    assert compra_actualizada.description == 'Compra actualizada'

@pytest.mark.django_db
def test_delete_compra():
    supplier = Suppliers.objects.create(name='Proveedor de prueba')

    compra = Compra.objects.create(
        description='Compra de prueba',
        amountc=5,
        datec=date(2024, 2, 21),
        pricec=100,
        supplier=supplier,
    )

    compra.delete()
    assert Compra.objects.count() == 0
