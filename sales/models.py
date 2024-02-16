from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver



class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        detalles = DetalleVenta.objects.filter(venta=self)
        total = sum(detalle.subtotal for detalle in detalles)
        self.total = total
        self.save()

    def __str__(self):
        return f"Venta {self.id} - Cliente: {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField() 
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        
        self.subtotal = self.producto.price * self.cantidad
        super().save(*args, **kwargs)
        self.venta.calcular_total()

    def __str__(self):
        return f"Detalle Venta {self.id} - Producto: {self.producto.title}, Cantidad: {self.cantidad}, Subtotal: {self.subtotal}"

