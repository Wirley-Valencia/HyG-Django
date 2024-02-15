from django.contrib import admin
from .models import  Product, Compra,  Suppliers, Gastos
from import_export import resources
from import_export.admin import ImportExportModelAdmin










@admin.register(Compra)
class CompraAdmin(ImportExportModelAdmin):
    list_display = ('id', 'supplier', 'product', 'datec',
                    'amountc', 'pricec', 'description',)
    list_editable = ('supplier', 'product',)
    search_fields = ('supplier', 'product',)
    list_per_page = 5


class CompraResource(resources.ModelResource):
    class Meta:
        model = Compra
        fields = ('id', 'supplier', 'product', 'datec',
                  'amountc', 'pricec', 'description',)


@admin.register(Suppliers)
class SuppliersAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'email', 'phone',)
    list_editable = ('email', 'phone',)
    search_fields = ('name',)


class SuppliersResource(resources.ModelResource):
    class Meta:
        model = Suppliers
        fields = ('id', 'name', 'email', 'phone',)
