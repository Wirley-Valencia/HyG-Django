from django.db import models
from user.models import CustomUser
from carts.models import Cart
from enum import Enum
from django.db.models.signals import pre_save
import uuid
# Create your models here.


class OroderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = "PAYED"
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'


choices = [(tag, tag.value) for tag in OroderStatus]


class Order(models.Model):
    order_id = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, choices=choices, default=OroderStatus.CREATED)
    shipping_total = models.DecimalField(
        default=5, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return self.order_id

    def cancel(self):
        self.status = OroderStatus.CANCELED
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_total(self):
        return self.cart.total + self.shipping_total


class OrderPickup(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='pickup_info')
    pickup_datetime = models.DateTimeField()

    class Meta:
        verbose_name = "Información de Recogida"
        verbose_name_plural = "Información de Recogida"

    def __str__(self):
        return f"Recogida para la orden {self.order.order_id}"


def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
