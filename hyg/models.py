from django.db import models
from django.utils.html import format_html
from products.models import Product
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
from email.mime.multipart import MIMEMultipart
# Create your models here.


class Suppliers(models.Model):
    company = models.CharField(max_length=255, null=True, blank=True, verbose_name='Empresa')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='Correo')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nombre Proveedor')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Numero de contacto')

    def __str__(self):
        return self.company

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

    @staticmethod
    def send_email_to_supplier(sender, instance, created, **kwargs):
        if created:
            subject = 'Nueva compra realizada'
            template = 'email/email_compra.html'
            context = {'purchase': instance}

            # Renderizar el contenido del correo electrónico desde una plantilla HTML
            html_message = render_to_string(template, context)
            plain_message = strip_tags(html_message)
            from_email = 'vanessavalencia1052@gmail.com' 
            to_email = instance.supplier.email

            # Enviar el correo electrónico
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

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
    description = models.CharField(max_length=255, null=True, verbose_name='Descripción')
    date = models.DateField(null=True, verbose_name='Fecha')
    price = models.IntegerField(verbose_name='Valor del gasto')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'gasto'
        verbose_name_plural = 'gastos'
        db_table = 'gastos'
        ordering = ['id']
post_save.connect(Compra.send_email_to_supplier, sender=Compra)