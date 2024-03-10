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
