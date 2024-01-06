from django.db import models
from django.utils.html import format_html

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'Categoria'
        ordering = ['id']


class Products(models.Model):
    price = models.IntegerField()
    code = models.CharField(max_length=255, null=True)
    amount = models.FloatField(null=True)
    name = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Atributo de fecha de vencimiento
    expiration_date = models.DateField(null=True)
    status = models.CharField(max_length=50, null=True)
    # image = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.name  # Mantén el nombre del campo como "name"

    # def show_image(self):
    #     return format_html('<img src={} width="100" /> ', self.image.url)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'Producto'
        ordering = ['id']


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
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

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
