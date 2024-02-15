from django.db import models
from django.utils.html import format_html
from products.models import Product

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
    description = models.CharField(max_length=255, null=True)
    #    amount = cantidad, suppliers = proveedores
    amountc = models.IntegerField()
    datec = models.DateField(null=True, blank=True)
    pricec = models.IntegerField()
    supplier = models.ForeignKey(
        Suppliers, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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
