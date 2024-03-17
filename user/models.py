from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from orders.common import OroderStatus
# Create your models here.


class CustomUser(AbstractUser):
    # image = models.ImageField(default='users/usuario_defecto.jpg',
    #                           upload_to='users/', verbose_name='Imagen de perfil')
    address = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Dirección')

    cell_phone = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Celular')

    accepted_terms = models.BooleanField(default=False)

    def clean(self):

        if self.cell_phone and len(self.cell_phone) != 10:
            raise ValidationError('El celular debe tener 10 dígitos.')

    class Meta:
        verbose_name = 'Usuario personalizado'
        verbose_name_plural = 'Usuarios personalizados'
        ordering = ['-id']

    def __str__(self):
        return self.username

    def orders_completed(self):
        return self.order_set.filter(status=OroderStatus.COMPLETED).order_by('-id')
