from django.db import models
from django.utils.html import format_html
from products.models import Product
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


class Suppliers(models.Model):
    email = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        db_table = 'proveedor'
        ordering = ['id']


class Compra(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descripción', null=True)
    amountc = models.IntegerField(verbose_name='Cantidad')
    datec = models.DateField(verbose_name='Fecha', null=True, blank=True)
    pricec = models.IntegerField(verbose_name='Precio')
    supplier = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, null=True, verbose_name='Proveedor')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')

    def clean(self):
        # Validación para asegurarse de que 'amountc' no sea negativo
        if self.amountc < 0:
            raise ValidationError({'amountc': 'La cantidad no puede ser negativa.'})

        # Validación para asegurarse de que 'pricec' no sea negativo
        if self.pricec < 0:
            raise ValidationError({'pricec': 'El precio no puede ser negativo.'})

        # Validación para asegurarse de que 'datec' sea hasta un mes anterior a la fecha actual
        if self.datec:
            one_month_ago = timezone.now().date() - timezone.timedelta(days=30)
            if self.datec > timezone.now().date() or self.datec < one_month_ago:
                raise ValidationError({'datec': 'La fecha debe ser hasta un mes anterior a la fecha actual.'})


    class Meta:
        verbose_name = 'compra'
        verbose_name_plural = 'compras'
        db_table = 'compras'
        ordering = ['id']

    def __str__(self):
        return self.description
    
    


class Gastos(models.Model):
    description = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'gasto'
        verbose_name_plural = 'gastos'
        db_table = 'gastos'
        ordering = ['id']
