from django.urls import reverse
from user.models import CustomUser
import pytest

def superadmin_user():
    return CustomUser.objects.create_superuser(username='superadmin', email='superadmin@example.com', password='password')

@pytest.mark.django_db
def test_superuser_login(client):

    superadmin_user_instance = superadmin_user()
    login_url = reverse('inicio')
    client.login(username='superadmin', password='password')
    response = client.get(login_url)
    assert response.status_code == 200  
