from django.db import models
from products.models import Product
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Titulo')
    description = models.TextField(verbose_name='Descripción')
    products = models.ManyToManyField(Product, blank=True, verbose_name='Productos')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.title
