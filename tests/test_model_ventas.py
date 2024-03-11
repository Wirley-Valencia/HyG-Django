import pytest
from datetime import date
from products.models import Product
from django.utils import timezone
from sales.models import Venta, DetalleVenta, Cliente
from django.test import TestCase




def crear_cliente():
    return Cliente.objects.create(
        nombre="Roberto",
        email="Roberto@gmail.com",
        telefono="123456789"
    )

def crear_producto():
    return Product.objects.create(
        title="Producto Ejemplo",
        description="Descripción de prueba",
        price=10.99,
        expiration_date=date(2024, 12, 31),
        image="productos/imgs/imagen.jpg",
        cantidad_disponible=10
    )

def crear_venta(cliente):
    return Venta.objects.create(
        cliente=cliente,
        fecha=date(2024, 2, 21),
        total=100.00
    )

def crear_detalle_venta(venta, producto):
    return DetalleVenta.objects.create(
        venta=venta,
        producto=producto,
        cantidad=3,
        subtotal=30.00
    )

@pytest.mark.django_db
def test_crear_venta():
    cantidad_inicial = Venta.objects.count()
    cliente = crear_cliente()
    crear_venta(cliente)
    assert Venta.objects.count() == cantidad_inicial + 1

@pytest.mark.django_db
def test_leer_venta():
    cliente = crear_cliente()
    venta = crear_venta(cliente)
    assert venta in Venta.objects.all()

@pytest.mark.django_db
def test_actualizar_venta():
    cliente = crear_cliente()
    venta = crear_venta(cliente)
    venta.fecha = date(2024, 3, 1)
    venta.save()
    venta_actualizada = Venta.objects.get(id=venta.id)
    assert venta_actualizada.fecha == date(2024, 3, 1)

@pytest.mark.django_db
def test_eliminar_venta():
    cantidad_inicial = Venta.objects.count()
    cliente = crear_cliente()
    venta = crear_venta(cliente)
    venta.delete()
    assert Venta.objects.count() == 0
