import pytest
from datetime import date
from django.utils import timezone
from hyg.models import Gastos

@pytest.mark.django_db
def test_gastos_creation():
    
    Gastos.objects.create(description="Compra de libros", date=date.today(), price=50)
    assert Gastos.objects.count() == 1

@pytest.mark.django_db
def test_gastos_read():
   
    gasto = Gastos.objects.create(description="Compra de libros", date=date.today(), price=50)
    gasto_db = Gastos.objects.get(description="Compra de libros")
    assert gasto == gasto_db

@pytest.mark.django_db
def test_gastos_update():
    
    gasto = Gastos.objects.create(description="Compra de libros", date=date.today(), price=50)
    gasto.description = "Compra de material escolar"
    gasto.save()
    gasto_db = Gastos.objects.get(pk=gasto.pk)
    assert gasto_db.description == "Compra de material escolar"

@pytest.mark.django_db
def test_gastos_deletion():
   
    gasto = Gastos.objects.create(description="Compra de libros", date=date.today(), price=50)
    gasto.delete()
    assert Gastos.objects.count() == 0
