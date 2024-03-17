from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


CustomUser = get_user_model()


class Product(models.Model):

    title = models.CharField(max_length=50, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0, verbose_name='Precio')
    slug = models.SlugField(null=False, blank=False,
                            unique=True, verbose_name='Slug')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado en')
    image = models.ImageField(
        upload_to='media', null=False, blank=False, verbose_name='Imagen')
    total_cantidad_disponible = models.IntegerField(
        default=0, null=True, verbose_name='Cantidad disponible')

    AVAILABLE = 'DIS'
    INACTIVE = 'INA'
    OUT_OF_STOCK = 'OOS'

    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (INACTIVE, 'Inactivo'),
        (OUT_OF_STOCK, 'Agotado'),
    ]
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return self.title

    def clean(self):
        # if self.expiration_date and self.expiration_date < timezone.now().date():
        #     raise ValidationError(
        #         'La fecha de expiración no puede ser anterior a la fecha actual.')

        if self.price < 100:
            raise ValidationError(
                'El precio debe tener por lo menos 3 digitos.')

        # if self.cantidad_disponible is not None and self.cantidad_disponible < 0:
        #     raise ValidationError('La cantidad no puede ser negativa.')
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    @staticmethod
    def check_product_stock(sender, instance, created, **kwargs):
        CustomUser = get_user_model()
        usuarios = CustomUser.objects.filter(is_staff=1)

        for usuario in usuarios:
            if not created and instance.total_cantidad_disponible == 5:
                subject = 'Producto a punto de agotarse'
                template = 'email/email_quantity_warning.html'
                context = {'product': instance}

                html_message = render_to_string(template, context)
                plain_message = strip_tags(html_message)
                from_email = 'vanessavalencia1052@gmail.com'
                to_email = usuario.email  # Obtener el correo electrónico del usuario

                # Enviar el correo electrónico al usuario
                send_mail(subject, plain_message, from_email, [
                          to_email], html_message=html_message)


post_save.connect(Product.check_product_stock, sender=Product)

# def restar_stock(self, cantidad):
#     """
#     Resta la cantidad especificada del stock del producto.
#     """
#     self.stock -= cantidad
#     self.save()


def set_slug(sender, instance, *args, **kwargs):  # callback
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug


pre_save.connect(set_slug, sender=Product)


class Stock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Producto')
    expiration_date = models.DateField(
        null=True, verbose_name='Fecha de Vencimiento')
    cantidad_disponible = models.IntegerField(
        default=0, verbose_name='Cantidad Disponible')
    codigo = models.CharField(
        max_length=50, unique=True, verbose_name='Codigo')
    AVAILABLE = 'DIS'
    INACTIVE = 'INA'

    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (INACTIVE, 'Inactivo'),
    ]
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default=AVAILABLE, verbose_name='Estado')

    def __str__(self):
        return f"{self.product.title} - {self.expiration_date}"


@receiver(post_save, sender=Stock)
@receiver(post_delete, sender=Stock)
def update_product_total_cantidad_disponible(sender, instance, **kwargs):
    product = instance.product
    total_cantidad_disponible = Stock.objects.filter(product=product).aggregate(
        total=Sum('cantidad_disponible'))['total'] or 0
    product.total_cantidad_disponible = total_cantidad_disponible

    if total_cantidad_disponible == 0:
        product.status = Product.OUT_OF_STOCK
    else:
        product.status = Product.AVAILABLE

    product.save()
