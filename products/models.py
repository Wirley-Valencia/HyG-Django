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

class Product(models.Model):
    
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media', null=False, blank=False)
    total_cantidad_disponible = models.IntegerField(default=0, null=True)
    

    AVAILABLE = 'DIS'
    INACTIVE = 'INA'
    OUT_OF_STOCK = 'OOS'

    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (INACTIVE, 'Inactivo'),
        (OUT_OF_STOCK, 'Agotado'),
    ]
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=AVAILABLE)
    
    def __str__(self):
        return self.title
    

    def clean(self):
        # if self.expiration_date and self.expiration_date < timezone.now().date():
        #     raise ValidationError(
        #         'La fecha de expiración no puede ser anterior a la fecha actual.')

        if self.price < 100:
            raise ValidationError('El precio debe tener por lo menos 3 digitos.')

        # if self.cantidad_disponible is not None and self.cantidad_disponible < 0:
        #     raise ValidationError('La cantidad no puede ser negativa.')
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"



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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiration_date = models.DateField(null=True)
    cantidad_disponible = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.expiration_date}"
    
@receiver(post_save, sender=Stock)
@receiver(post_delete, sender=Stock)
def update_product_total_cantidad_disponible(sender, instance, **kwargs):
    product = instance.product
    total_cantidad_disponible = Stock.objects.filter(product=product).aggregate(total=Sum('cantidad_disponible'))['total'] or 0
    product.total_cantidad_disponible = total_cantidad_disponible
    
    if total_cantidad_disponible == 0: 
        product.status = Product.OUT_OF_STOCK
    else:  
        product.status = Product.AVAILABLE
        
    product.save()