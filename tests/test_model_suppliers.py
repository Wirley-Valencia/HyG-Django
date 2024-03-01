import pytest
from hyg.models import Suppliers


@pytest.mark.django_db
def test_suppliers_creation():
   
    supplier = Suppliers.objects.create(
        name='Test Supplier',
        email='test@example.com',
        phone='123456789'
    )

   
    assert supplier.name == 'Test Supplier'
    assert supplier.email == 'test@example.com'
    assert supplier.phone == '123456789'


@pytest.mark.django_db
def test_suppliers_update():
    
    supplier = Suppliers.objects.create(
        name='Test Supplier',
        email='test@example.com',
        phone='123456789'
    )

   
    updated_name = 'Updated Supplier'
    updated_email = 'updated@example.com'
    updated_phone = '987654321'

    supplier.name = updated_name
    supplier.email = updated_email
    supplier.phone = updated_phone
    supplier.save()

    
    updated_supplier = Suppliers.objects.get(id=supplier.id)

   
    assert updated_supplier.name == updated_name
    assert updated_supplier.email == updated_email
    assert updated_supplier.phone == updated_phone


