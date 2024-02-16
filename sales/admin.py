from django.contrib import admin
from .models import Product,Venta, DetalleVenta,Cliente

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaInline]
    list_display = ('cliente', 'fecha', 'total')


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'subtotal')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')

