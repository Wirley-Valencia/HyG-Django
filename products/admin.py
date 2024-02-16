from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'amount', 'price',
              'image', 'cantidad_disponible', 'expiration_date')
    list_display = ('__str__', 'slug', 'amount', 'created_at',
                    'cantidad_disponible', 'expiration_date')


admin.site.register(Product, ProductAdmin)
