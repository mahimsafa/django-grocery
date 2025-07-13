from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('unit_price', 'total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'sub_total', 'shipping_fee', 'tax', 'grand_total', 'created_at')
    search_fields = ('id', 'customer__first_name', 'customer__last_name', 'customer__email')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('sub_total', 'shipping_fee', 'tax', 'grand_total',)
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'variant', 'quantity', 'unit_price', 'total_price')
    search_fields = ('order__id', 'variant__name', 'variant__product__name')
    list_filter = ('variant__product',)
