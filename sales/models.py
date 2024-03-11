from django.utils import timezone
from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import re


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validar el email
        if not re.match(r'^[^@]+@gmail\.com$', self.email):
            raise ValidationError('El email debe ser de Gmail.')

        # Validar el teléfono
        if self.telefono is not None:
            if not self.telefono.isdigit():
                raise ValidationError(
                    'El teléfono debe contener solo números.')
            elif len(self.telefono) < 10:
                raise ValidationError(
                    'El teléfono debe tener menos de 10 dígitos.') 
 

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True )

    def calcular_total(self):
        detalles = DetalleVenta.objects.filter(venta=self)
        total = sum(detalle.subtotal for detalle in detalles)
        self.total = total
        self.save()

    def __str__(self):
        return f"Venta {self.id} - Cliente: {self.cliente.nombre}"

    def clean(self):
        if any(char.isalpha() for char in str(self.fecha)):
            raise ValidationError(
                'Introduzca un formato correcto para la fecha.')
        if self.fecha > timezone.now().date():
            raise ValidationError(
                'La fecha de la venta no puede ser en el futuro.')

        # if self.total <= 0:
        #     raise ValidationError(
        #         'El total de la venta debe ser mayor que cero.')


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        
        producto = self.producto
        cantidad_anterior = 0

       
        if self.pk:
            detalle_anterior = DetalleVenta.objects.get(pk=self.pk)
            cantidad_anterior = detalle_anterior.cantidad

        super().save(*args, **kwargs)

        producto.total_cantidad_disponible -= self.cantidad - cantidad_anterior
        producto.save()
        self.subtotal = self.producto.price * self.cantidad
        super().save(*args, **kwargs)
        self.venta.calcular_total()

    def delete(self, *args, **kwargs):
        
        producto = self.producto
        cantidad_anterior = self.cantidad
        
        super().delete(*args, **kwargs)

        producto.total_cantidad_disponible += cantidad_anterior
        producto.save()

        
        self.venta.calcular_total()

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor que cero.')

        if self.subtotal < 0:
            raise ValidationError('El subtotal no puede ser negativo.')

    def __str__(self):
        return f"Detalle Venta {self.id} - Producto: {self.producto.title}, Cantidad: {self.cantidad}, Subtotal: {self.subtotal}"
