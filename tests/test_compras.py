import pytest
from hyg.models import Suppliers, Compra
from products.models import Product

@pytest.mark.django_db
def test_compra_creation():
    compra = Compra.objects.create(
        description='Test Purchase',
        amountc=5,
        datec='2024-02-16',
        pricec=100
    )

    # Verificación de la creación
    assert compra.description == 'Test Purchase'
    assert compra.amountc == 5
    assert compra.datec.strftime('%Y-%m-%d') == '2024-02-16'
    assert compra.pricec == 100

@pytest.mark.django_db
def test_compra_update():
    compra = Compra.objects.create(
        description='Test Purchase',
        amountc=5,
        datec='2024-02-16',
        pricec=100
    )

    updated_description = 'Updated Purchase'
    updated_amountc = 10
    updated_datec = '2024-02-17'
    updated_pricec = 200

    compra.description = updated_description
    compra.amountc = updated_amountc
    compra.datec = updated_datec
    compra.pricec = updated_pricec
    compra.save()

    updated_compra = Compra.objects.get(id=compra.id)

    assert updated_compra.description == updated_description
    assert updated_compra.amountc == updated_amountc
    assert updated_compra.datec.strftime('%Y-%m-%d') == updated_datec
    assert updated_compra.pricec == updated_pricec