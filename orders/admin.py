from django.contrib import admin


from .models import Order, OrderPickup
# Register your models here.

admin.site.register(Order)


@admin.register(OrderPickup)
class OrderPickupAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'pickup_datetime']
    list_filter = ['pickup_datetime']
    search_fields = ['order__order_id']
