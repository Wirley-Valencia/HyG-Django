from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ('title', 'description','amount', 'price', 'image', 'expiration_date')
    list_display = ('__str__', 'slug', 'created_at','expiration_date','amount',)


admin.site.register(Product, ProductAdmin)
