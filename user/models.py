from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    # image = models.ImageField(default='users/usuario_defecto.jpg',
    #                           upload_to='users/', verbose_name='Imagen de perfil')
    address = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Dirección')
    location = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Localidad')
    telephone = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Teléfono')
    cell_phone = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Celular')

    class Meta:
        verbose_name = 'Usuario personalizado'
        verbose_name_plural = 'Usuarios personalizados'
        ordering = ['-id']

    def __str__(self):
        return self.username
