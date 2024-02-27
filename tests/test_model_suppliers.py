import pytest
from hyg.models import Suppliers, Compra, Gastos


@pytest.mark.django_db
def test_suppliers_creation():

    supplier = Suppliers.objects.create(
        name='Test Supplier',
        email='test@gmail.com',
        phone='1234567899'
    )

    assert supplier.name == 'Test Supplier'
    assert supplier.email == 'test@gmail.com'
    assert supplier.phone == '1234567899'


@pytest.mark.django_db
def test_suppliers_update():

    supplier = Suppliers.objects.create(
        name='Test Supplier',
        email='test@gmail.com',
        phone='1234567899'
    )

    updated_name = 'Updated Supplier'
    updated_email = 'updated@gmail.com'
    updated_phone = '9876543219'

    supplier.name = updated_name
    supplier.email = updated_email
    supplier.phone = updated_phone
    supplier.save()

    updated_supplier = Suppliers.objects.get(id=supplier.id)

    assert updated_supplier.name == updated_name
    assert updated_supplier.email == updated_email
    assert updated_supplier.phone == updated_phone
