from django.db import models
from user.models import CustomUser
from carts.models import Cart
import uuid
from .common import OroderStatus, choices
from enum import Enum
from django.db.models.signals import pre_save, post_save
import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from email.mime.multipart import MIMEMultipart
from django.contrib.auth import get_user_model
# Create your models here.


CustomUser = get_user_model()


def obtener_email_usuario(user_id):
    try:
        usuario = CustomUser.objects.get(id=user_id)
        correo = usuario.email
        return correo
    except CustomUser.DoesNotExist:
        return None


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

    def complete(self):
        self.status = OroderStatus.COMPLETED
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_total(self):
        return self.cart.total


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


@receiver(post_save, sender=Order)
def send_email_user(sender, instance, created, **kwargs):
    if created:
        subject = 'Nuevo pedido realizado'
        template = 'email/email_order_user.html'

        nombre_cliente = instance.user.username
        codigo_orden = instance.order_id

        context = {'nombre_cliente': nombre_cliente,
                   'codigo_orden': codigo_orden}

        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        from_email = 'vanessavalencia1052@gmail.com'
        to_email = instance.user.email
        send_mail(subject, plain_message, from_email, [
                  to_email], html_message=html_message)
