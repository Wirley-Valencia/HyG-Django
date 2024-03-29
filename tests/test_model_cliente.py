import pytest
from django.core.exceptions import ValidationError
from sales.models import Cliente
@pytest.mark.django_db
def test_cliente_model_validations():
    cliente1 = Cliente(nombre='Cliente 1', email='cliente1@gmail.com', telefono='1234567890')
    cliente1.full_clean()  

    with pytest.raises(ValidationError) as e:
        cliente2 = Cliente(nombre='Cliente 2', email='cliente2@gmail.com', telefono='abc')
        cliente2.full_clean() 
    assert 'El teléfono debe contener solo números.' in str(e.value)

    with pytest.raises(ValidationError) as e:
        cliente3 = Cliente(nombre='Cliente 3', email='cliente3@example.com', telefono='1234567890')
        cliente3.full_clean()
    assert 'El email debe ser de Gmail.' in str(e.value)
    
    with pytest.raises(ValidationError) as e:
        cliente4 = Cliente(nombre='Cliente 4', email='cliente4@gmail.com', telefono='12345')
        cliente4.full_clean()  
    assert 'El teléfono debe tener menos de 10 dígitos.' in str(e.value)
@pytest.mark.django_db
def test_create_cliente():
    
    cliente = Cliente.objects.create(nombre='Cliente de prueba', email='cliente@example.com', telefono='1234567890')
    assert cliente.nombre == 'Cliente de prueba'
    assert cliente.email == 'cliente@example.com'
    assert cliente.telefono == '1234567890'
@pytest.mark.django_db
def test_update_cliente():
    cliente = Cliente.objects.create(nombre='Cliente de prueba', email='cliente@example.com', telefono='1234567890')

    cliente.nombre = 'Nuevo nombre de cliente'
    cliente.email = 'nuevo_email@example.com'
    cliente.telefono = '0987654321'
    cliente.save()
    cliente_modificado = Cliente.objects.get(id=cliente.id)
    assert cliente_modificado.nombre == 'Nuevo nombre de cliente'
    assert cliente_modificado.email == 'nuevo_email@example.com'
    assert cliente_modificado.telefono == '0987654321'
@pytest.mark.django_db
def test_delete_cliente():
    cliente = Cliente.objects.create(nombre='Cliente de prueba', email='cliente@example.com', telefono='1234567890')
    cliente.delete()
    with pytest.raises(Cliente.DoesNotExist):
        Cliente.objects.get(id=cliente.id)